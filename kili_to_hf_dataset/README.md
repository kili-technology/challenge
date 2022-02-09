# Kili2HFDS

Uploads a Kili dataset to Hugging Face datasets

## Install

### Prerequisite
In a virtual environment (Python >= 3.7)
```bash
    pip install -r requirements.txt
```
then 
```bash
    huggingface-cli login
```

Also make sure that the environment variable $KILI_USER_API_KEY has been set with your Kili API token.

If this has not been done yet, create the hugging face dataset from the command line.
Once done, create the repo:
```bash
    huggingface-cli repo create litter-challenge-test --type dataset
```
### Prod version
For the final version, do the following:
```
    huggingface-cli repo create litter-challenge --type dataset --organization kili
```
Note that the submodule `kili2hfds/litter-challenge-test` git submodule will have to be removed, and the one corresponding to the prod version will have to be added.

### Commands
Run the following to export the Kili "plastic in river" dataset into the Hugging Face "PierreLeveau/litter-challenge-test" dataset (dataset name subject to change)
```bash
    bash entrypoints.sh kili2hfds
```

# References
inspired from:
  * [https://huggingface.co/datasets/svhn]
