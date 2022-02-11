import click

from kili2hfds.downloader import Downloader #, Uploader

@click.command()
@click.option('--local-path', help='Path of unzipped folder from https://bit.ly/3J8wGkU')
def main(local_path):
    
    dl = Downloader()
    
    kili_project_id = "ckzdzhh260ec00mub7gqjfetz"

    # TODO: label names should be fetched from Kili's JSON interface
    dl.download_and_save_by_split(kili_project_id, local_path, ["PLASTIC_BAG", "PLASTIC_BOTTLE", "OTHER_PLASTIC_WASTE"]) 

if __name__ == '__main__':
    main()