# Kili2HFDS

Uploads a Kili dataset to Hugging Face datasets

## Install

### Prerequisite
In a virtual environment (Python >= 3.7)
```bash
    pip install -r requirements.txt
```

Also make sure that the environment variable $KILI_USER_API_KEY has been set with your Kili API token.

If this has not been done yet, create the hugging face dataset from the Hugging Face web UI.


### Commands
Run the following to export the Kili "plastic in river" dataset into the Hugging Face "Kili/plastic_in_river" dataset.
```bash
    bash entrypoints.sh kili2hfds
```

# References
inspired from:
  * [https://huggingface.co/datasets/svhn]
