# DTLN Speech Enhancement sample

The open source model DTLN was taken from the github repository in the [link](https://github.com/breizhn/DTLN).

## Setup

### Download the model file

Clone the model-interfaces repository and navigate to the speech-enhancement reference example:

```
git clone git@github.com:aixplain/aixplain-models-internal.git
cd aixplain-models-internal/docs/user/samples/speech-enhancement
```

Download the model file using the commands
```
wget https://aixplain-kserve-models-dev.s3.amazonaws.com/serving-models/sample-models/speech-enhancement/dtln/dtln/saved_model.pb
wget https://aixplain-kserve-models-dev.s3.amazonaws.com/serving-models/sample-models/speech-enhancement/dtln/dtln/variables/variables.data-00000-of-00001
wget https://aixplain-kserve-models-dev.s3.amazonaws.com/serving-models/sample-models/speech-enhancement/dtln/dtln/variables/variables.index
```

Place it in a folder called `dtln` in the current directory. The files should be placed in the following tree's structure:
```
dtln
| - saved_model.pb
| - variables
    | - variables.data-00000-of-00001
    | - variables.index
```

### Install requirements

```
sudo apt-get install ffmpeg

# Install model-interfaces from GitHub, preferably by using a virtualenv
pip install -e 'git+https://$GH_ACCESS_TOKEN@github.com/aixplain/aixplain-models-internal.git@master#egg=model_interfaces'

pip install -r src/requirements.txt
```

- GH_ACCESS_TOKEN: Generate a GitHub access token from your account that can clone the model_interfaces repository

Documentation to generate the GitHub personal access token can be found [here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

## Run the model locally

### Test using the given test and samples

```
ASSET_DIR=. ASSET_URI=dtln pytest
```

### Serve the model using a webserver

```
ASSET_DIR=. ASSET_URI=dtln python src/model.py
```

### Test the model server

```
python src/sample_request.py
```

## Build and Run the model with docker

Navigate to the speech-enhancement reference example:

```
cd docs/user/samples/speech-enhancement
```

### Build the model's container

```
docker build --build-arg GH_ACCESS_TOKEN=<TOKEN_FROM_GITHUB_ACCOUNT> --build-arg ASSET_URI=<ASSET_URI> . -t 535945872701.dkr.ecr.us-east-1.amazonaws.com/aixmodel-dtln
```

- GH_ACCESS_TOKEN: Generate a GitHub access token from your account that can clone the model_interfaces repository
- ASSET_URI: Your model's name; 'dtln' in this reference example.

### Run the container

```
docker run -e ASSET_DIR=/ -e ASSET_URI=dtln -p 8080:8080 535945872701.dkr.ecr.us-east-1.amazonaws.com/aixmodel-dtln
```
