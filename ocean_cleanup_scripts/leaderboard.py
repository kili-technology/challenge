from kili.client import Kili
import pandas as pd
import os
import click
from tabulate import tabulate


def get_project_users(kili, project_id):
  return kili.project_users(project_id=project_id, fields=['user.email','user.firstname', 'user.lastname','numberOfLabeledAssets', 'honeypotMark'])

def get_max_annotated_assets(project_users):
  return max(project_user['numberOfLabeledAssets'] for project_user in project_users)

def compute_project_user_score(project_user_row, max_annotated_assets):
  number_of_labeled_assets = project_user_row['numberOfLabeledAssets']
  honeypot_mark = project_user_row['honeypotMark']
  score = 0
  if honeypot_mark is None:
    score = 100* number_of_labeled_assets/max_annotated_assets
  else:
    score = 70* number_of_labeled_assets/max_annotated_assets + 30 * honeypot_mark
  return score

@click.command()
@click.option('--api-key', help='Your Kili API Key')
@click.option('--project-id', help='The challenge project id')
def get_leaderboard(project_id, api_key=None):
    api_key = api_key or os.getenv('KILI_API_KEY')
    if api_key is None:
        raise ValueError('No API KEY, give it with  --api-key option')
    kili = Kili(api_key=api_key)
    project_users = get_project_users(kili, project_id)
    max_annotated_assets = get_max_annotated_assets(project_users)
    df_pu = pd.DataFrame(project_users)
    df_pu = pd.concat([df_pu.drop(["user"], axis=1), df_pu["user"].apply(pd.Series)], axis=1)
    df_pu['score'] = df_pu.apply(lambda row: compute_project_user_score(row, max_annotated_assets), axis=1)
    df_pu.sort_values(by=['score'], inplace=True, ascending=False, ignore_index=True)
    print(tabulate(df_pu.head(10), headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    get_leaderboard()
