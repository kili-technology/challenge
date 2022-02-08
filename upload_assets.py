import os

import click
from kili.client import Kili
from tqdm import tqdm

@click.command()
@click.option('--source', help='Path of unzipped folder from https://bit.ly/3J8wGkU')
@click.option('--project_id', default='ckzdzhh260ec00mub7gqjfetz')
def main(source, project_id):
    kili = Kili(api_key=os.getenv('KILI_API_KEY'))
    content_array = [os.path.join(source, f) for f in os.listdir(source) if f.endswith('.jpg')]
    first = 10
    for skip in tqdm(range(0, len(content_array), first)):
        kili.append_many_to_dataset(
                project_id=project_id,
                content_array=content_array[skip:(skip+first)])

if __name__ == '__main__':
    main()