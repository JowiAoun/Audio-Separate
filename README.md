## Audio-Separate-AI

Audio Separate AI is an application allowing to separate vocals from audio files.

This works using [demucs](https://github.com/facebookresearch/demucs) from the Facebook research team, made based on the paper [Hybrid Spectrogram and Waveform Source Separation](https://arxiv.org/pdf/2111.03600).

In terms of architecture, this application uses services on [AWS](https://aws.amazon.com/) which are spun up with [Terraform](https://www.terraform.io/) to do the following in order:

1. Push the unprocessed file on an S3 bucket and push its hash in an SQS queue
2. Pull the unprocessed file and process it on a lambda, with layer caching for the AI model
3. Push the processed file to the S3 bucket and notify the API service
4. Allow for downloading the processed vocals & sounds on the client

### Requirements
- Python 3.8.x to 3.10.x
- Terraform with set crendentials for publishing the app on AWS

### Installation
- Create a virtual environment with `python -m venv .venv`
- Activate the virtual environment with `source .venv/bin/activate`
- Install required packages `pip install -r api-service/requirements.txt && pip install -r splitter-service/requirements.txt`
- Initialize terraform backend `terraform init`
- Apply any additional features `terraform apply`

### Test
- Run the `api-service` with `python3 api-service/main.py`
- Publish an audio to the page
- Download separated audios