# Kili to Hugging Face Space

This document shows the steps to train a model on the challenge date and publish it to Hugging Face spaces.

## YoloV5 training
* Run this [notebook](https://colab.research.google.com/drive/1KnueteFtzQsWBjqMLsFfCDPhjePCAAju#scrollTo=maPYRHhBTb5I) that checks out the [YoloV5 fork](https://github.com/PierreLeveau/yolov5). The fork has the following modifications w.r.t the Kili fork:
  * It contains the "Plastic in litter" dataset definition.
  * It can download the Kili data and split it into train/validation/test sets.
* The training is logged into [Weights and Biases](https://wandb.ai/pierreleveau/YOLOv5?workspace=user-pierreleveau). The model can be downloaded from the UI when the training is over.

## Model upload
* Model is then uploaded manually to the following location through:
```
     gsutil cp ~/Downloads/best.pt gs://kili-datasets-public/plastic-in-river/model/
```
It will be immediately made available to this [Hugging face space](https://huggingface.co/spaces/Kili/plastic_in_river).

## Potential improvements
* Automate everything.
