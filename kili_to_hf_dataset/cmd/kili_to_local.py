from kili2hfds.downloader import Downloader #, Uploader

if __name__ == "__main__":
    
    dl = Downloader()
    
    kili_project_id = "ckzdzhh260ec00mub7gqjfetz"
    hf_local_clone_path = "/Users/pierreleveau/data/litter-challenge-test"

    # TODO: label names should be fetched from Kili's JSON interface
    dl.download_and_save_by_split(kili_project_id, hf_local_clone_path, ["PLASTIC_BAG", "PLASTIC_BOTTLE", "OTHER_PLASTIC_WASTE", "NOT_PLASTIC_WASTE"]) 

