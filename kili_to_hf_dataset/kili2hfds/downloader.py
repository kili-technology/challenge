import os
import math
from os.path import basename

from kili.client import Kili
import requests
from tqdm.auto import tqdm


class Downloader(object):
    def __init__(self, kili_api_key=None) -> None:
        self.kili_api_key = kili_api_key or os.environ["KILI_USER_API_KEY"]
        print(self.kili_api_key)

    def download_and_save_by_split(
        self, project_id, dest_path, label_names, train_val_proportions=None
    ):

        train_val_proportions = train_val_proportions or [0.8, 0.1]
        assert (
            sum(train_val_proportions) < 1.0
        ), "the train and validation split proportions should be <1.0"

        kili = Kili(api_key=self.kili_api_key)
        total = kili.count_assets(project_id=project_id)
        if total == 0:
            raise Exception("No asset in dataset!")
        first = 50
        assets = []
        for skip in tqdm(range(0, total, first)):
            assets += kili.assets(
                project_id=project_id,
                first=first,
                skip=skip,
                disable_tqdm=True,
                fields=[
                    "id",
                    "content",
                    "labels.createdAt",
                    "labels.jsonResponse",
                    "labels.labelType",
                ],
            )

        assets = [
            {
                **a,
                "labels": [
                    l
                    for l in sorted(a["labels"], key=lambda l: l["createdAt"])
                    if l["labelType"] in ["DEFAULT", "REVIEW"]
                ][-1:],
            }
            for a in assets
        ]
        assets = [a for a in assets if len(a["labels"]) > 0]

        n_train_assets = math.floor(len(assets) * train_val_proportions[0])
        n_val_assets = math.floor(len(assets) * train_val_proportions[1])

        asset_lists = {
            "train": assets[:n_train_assets],
            "validation": assets[n_train_assets : n_train_assets + n_val_assets],
            "test": assets[n_train_assets + n_val_assets :],
        }

        for name_list, asset_list in asset_lists.items():

            split_dest_path = os.path.join(dest_path, name_list)
            os.makedirs(split_dest_path, exist_ok=True)

            for asset in asset_list:
                img_data = requests.get(
                    asset["content"],
                    headers={"Authorization": f"X-API-Key: {self.kili_api_key}",},
                ).content
                image_filename = os.path.join(split_dest_path, asset["id"] + ".jpg")
                with open(image_filename, "wb") as handler:
                    handler.write(img_data)

            for asset in asset_list:
                annotation_filename = os.path.join(
                    split_dest_path, asset["id"] + ".txt"
                )
                with open(annotation_filename, "w") as handler:
                    json_response = asset["labels"][0]["jsonResponse"]
                    for job in json_response.values():
                        for annotation in job.get("annotations", []):
                            name = annotation["categories"][0]["name"]
                            category = label_names.index(name)
                            bounding_poly = annotation.get("boundingPoly", [])
                            if len(bounding_poly) < 1:
                                continue
                            if "normalizedVertices" not in bounding_poly[0]:
                                continue
                            normalized_vertices = bounding_poly[0]["normalizedVertices"]
                            x_s = [vertice["x"] for vertice in normalized_vertices]
                            y_s = [vertice["y"] for vertice in normalized_vertices]
                            x_min, y_min = min(x_s), min(y_s)
                            x_max, y_max = max(x_s), max(y_s)
                            _x_, _y_ = (x_max + x_min) / 2, (y_max + y_min) / 2
                            _w_, _h_ = x_max - x_min, y_max - y_min
                            handler.write(f"{category} {_x_} {_y_} {_w_} {_h_}\n")
