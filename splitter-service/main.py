import json
from starlette.responses import JSONResponse

from src import helpers as h
from src import constants as c

import boto3
import demucs.separate
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv('.env')
h.make_dirs()

with open('../terraform-vars.json', 'r') as file:
    terraform_vars = json.load(file)
AWS_SQS_QUEUE_URL = terraform_vars['sqs_queue_url']['value'] # TODO: Verify before program start that all env vars are not None
AWS_S3_BUCKET_NAME = terraform_vars['s3_bucket_name']['value']

app = FastAPI()
aws_sqs = boto3.client('sqs')
aws_s3 = boto3.client('s3')

@app.post("/process/", response_class=JSONResponse)
async def handle_process(request: Request):
  print("Handling process...")
  try:
    res = aws_sqs.receive_message(
      QueueUrl=AWS_SQS_QUEUE_URL,
      MaxNumberOfMessages=1,
      WaitTimeSeconds=10,
    )
    print(res)

    if 'Messages' not in res:
      return {"success": False}

    message = res['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    key = message['Body']

    print(message, receipt_handle, key)

    aws_s3.download_file(
      Bucket = AWS_S3_BUCKET_NAME,
      Key = key,
      Filename = c.INPUT_DIR + '/' + key
    )

    aws_sqs.delete_message(
      QueueUrl=AWS_SQS_QUEUE_URL,
      ReceiptHandle=receipt_handle
    )

    # process_song(key)

    # await h.delete_input_file()

    # aws_s3.upload_file(
    #   Filename=c.OUTPUT_DIR + '/' + new_hash.str + file.ext,
    #   Bucket=AWS_S3_BUCKET_NAME,
    #   Key=new_hash.str + file.ext + '-completed',
    #   ExtraArgs={'Metadata': meta_data}
    # )

    return {"success": True}

  except Exception as err:
    return {"success": False, "error": "Internal server error"}

def process_song(key):
  """Process the song to separate vocals and accompaniment."""
  demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", c.INPUT_DIR + key])
  print("Processing complete.")
