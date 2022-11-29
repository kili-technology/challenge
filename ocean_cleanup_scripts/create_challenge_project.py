from kili.client import Kili
import os
import click
from tqdm import tqdm
import time

json_interface = {
  "jobs": {
    "CLASSIFICATION_JOB": {
      "content": {
        "categories": {
          "MARINE_DEBRIS": {
            "children": [],
            "name": "Marine debris",
            "shortcut": "D",
            "id": "category1"
          },
          "MARINE_LIFE_OR_VEGETATION": {
            "children": [],
            "name": "Marine life or vegetation",
            "shortcut": "L",
            "id": "category2"
          },
          "OTHER": {
            "children": [],
            "name": "Other",
            "shortcut": "O",
            "id": "category3"
          },
          "UNKNOWN": {
            "children": [],
            "name": "Unknown",
            "shortcut": "U",
            "id": "category4"
          }
        },
        "input": "radio"
      },
      "instruction": "Categories",
      "isChild": False,
      "mlTask": "CLASSIFICATION",
      "models": {},
      "isVisible": False,
      "required": 1,
      "isNew": False
    }
  }
}
instructions_url = 'https://docs.google.com/presentation/d/1mrNPpuJtQmdJC9rwxetF4OTbAS6jsFx4E9KYEkwJosg/edit#slide=id.g18da292e706_0_35'
admin_members = ['theo.dullin+challenge@kili-technology.com'] #, 'edouard.darchaimbaud+challenge@kili-technology.com', 'benjamin.fourio+challenge@kili-technology.com']

asset_external_ids = [str(i) for i in range(1, 184884)]
bucket_address = 'https://storage.googleapis.com/label-public-staging/cropstender08/'

def get_priorities(local_dataset_dir):
    priorities={}
    for external_id in asset_external_ids:
        local_file_path = os.path.join(local_dataset_dir, str(external_id)+'.jpg')
        size = os.stat(local_file_path).st_size
        priorities[external_id]=size
    return priorities


@click.command()
@click.option('--n', help='number of project to create', default=1)
@click.option('--title', help='title of the project to create', default='Ocean Cleanup Challenge - Team project')
@click.option('--local-dataset-dir', help='to calculate the asset priorities', default='/Users/theodullin/cropstender08')
@click.option('--api-key', help='Your Kili API Key')
def main(n,title,local_dataset_dir, api_key=None):
    api_key = api_key or os.getenv('KILI_API_KEY')
    if api_key is None:
        raise ValueError('No API KEY, give it with  --api-key option')
    kili = Kili(api_key=api_key)
    project_ids=[]
    priorities_dict = get_priorities(local_dataset_dir)

    for i in range(n):
        #create project
        project_id=kili.create_project(
            title=title,
            input_type='IMAGE',
            description='',
            json_interface=json_interface)['id']
        time.sleep(3)

        # add instructions and forbid asset skip
        kili.update_properties_in_project(
            project_id=project_id,
            can_skip_asset=False,
            instructions=instructions_url)

        # add admin users
        for user_email in admin_members:
            kili.append_to_roles(project_id=project_id, user_email=user_email, role='ADMIN')


        # add assets
        kili.append_many_to_dataset(
            project_id=project_id,
            external_id_array=asset_external_ids,
            content_array=[bucket_address+str(external_id)+'.jpg' for external_id in asset_external_ids]
        )

        # prioritize assets
        # assets = kili.assets(project_id=project_id)
        # kili.update_properties_in_assets(
        #     asset_ids=[asset['id'] for asset in assets],
        #     priorities=[priorities_dict[asset['externalId']] for asset in assets]
        # )

        project_ids.append(project_id)

    print(project_ids)
    return project_ids



if __name__ == '__main__':
    main()