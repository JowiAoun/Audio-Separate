import json
from dotenv import load_dotenv

from src import helpers as h
from src import constants as c

import boto3
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

load_dotenv('.env')
h.make_dirs()

with open('../terraform-vars.json', 'r') as file:
  terraform_vars = json.load(file)
AWS_SQS_QUEUE_URL = terraform_vars['sqs_queue_url']['value'] # TODO: Verify before program start that all env vars are not None
AWS_S3_BUCKET_NAME = terraform_vars['s3_bucket_name']['value']
AWS_LAMBDA_FUNCTION_NAME = terraform_vars['lambda_function_name']['value']

templates = Jinja2Templates(directory="templates")
app = FastAPI()
aws_s3 = boto3.client('s3')
aws_sqs = boto3.client('sqs')
aws_lambda = boto3.client('lambda')

@app.get("/upload/", response_class=HTMLResponse)
async def handle_upload_form(request: Request):
  try:
    return templates.TemplateResponse("upload.html", {"request": request})
  except Exception as err:
    return {"success": False, "error": "Internal server error"}


@app.post("/upload/")
async def handle_upload_file(_: Request, file: UploadFile = File(...), stems: str = Form(...)):
  try:
    file.filename, file.ext = h.split_path(file.filename)

    res = h.verify_file(file.ext, file.size)
    if res is not None:
      return res

    new_hash = h.create_hash()

    meta_data = h.create_meta(file.filename, file.ext, file.size, int(stems), new_hash.timestamp().timestamp)
    if meta_data is None:
      raise Exception()

    res = await h.write_file(file, new_hash.str + file.ext)
    if res is False:
      raise Exception()

    aws_s3.upload_file(
      Filename = c.INPUT_DIR + '/' + new_hash.str + file.ext,
      Bucket = AWS_S3_BUCKET_NAME,
      Key = new_hash.str + file.ext,
      ExtraArgs = {'Metadata': meta_data}
    )

    aws_sqs.send_message(
      QueueUrl = AWS_SQS_QUEUE_URL,
      MessageBody = new_hash.str,
      DelaySeconds = 0,
    )

    await h.delete_input_file(new_hash.str + file.ext)

    return {"success": True, "hashname": new_hash.str}

  except Exception as err:
    # TODO: Add logging
    print(err)
    return {"success": False, "error": "Internal server error"}
