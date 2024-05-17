terraform {
  backend "s3" {
    bucket = "jowiaoun-tfstate"
    key    = "audio-separate.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "audio-separate-cloud" {
  cidr_block = "10.0.0.0/16"

  tags = {
    App = "audio-separate"
  }
}

resource "aws_subnet" "audio-separate-public-1a" {
  vpc_id            = aws_vpc.audio-separate-cloud.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    App = "audio-separate"
  }
}

resource "aws_subnet" "audio-separate-private-1a" {
  vpc_id            = aws_vpc.audio-separate-cloud.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    App = "audio-separate"
  }
}

resource "aws_s3_bucket" "audio-separate-bucket" {
  bucket = "audio-separate-bucket"

  tags = {
    App = "audio-separate"
  }
}

resource "aws_instance" "audio-separate-instance-api" {
  instance_type = "t2.micro"
  ami           = "ami-0bb84b8ffd87024d8"
  subnet_id     = aws_subnet.audio-separate-public-1a.id
  user_data = file("../api-service/setup.sh")

  tags = {
    App = "audio-separate"
  }
}

resource "aws_instance" "audio-separate-instance-splitter" {
  instance_type = "t2.micro"
  ami           = "ami-0bb84b8ffd87024d8"
  subnet_id     = aws_subnet.audio-separate-private-1a.id
  user_data = file("../splitter-service/setup.sh")

  tags = {
    App = "audio-separate"
  }
}

data "aws_iam_policy_document" "audio-separate-policy-lambda" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "audio-separate-role-lambda" {
  name               = "audio-separate-role-lambda"
  assume_role_policy = data.aws_iam_policy_document.audio-separate-policy-lambda.json

  tags = {
    App = "audio-separate"
  }
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../lambda-function/main.py"
  output_path = "../lambda-function/lambda-function-payload.zip"
}

resource "aws_sqs_queue" "audio-separate-queue-fifo" {
  name = "audio-separate-queue"
  message_retention_seconds = 86400

  tags = {
    App = "audio-separate"
  }
}

resource "aws_lambda_function" "audio-separate-lambda" {
  function_name = "audio-separate-lambda"
  filename      = "../lambda-function/lambda-function-payload.zip"
  role          = aws_iam_role.audio-separate-role-lambda.arn
  handler       = "main.handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.8"

  tags = {
    App = "audio-separate"
  }
}

resource "aws_lambda_event_source_mapping" "audio_separate_queue_trigger" {
  event_source_arn  = aws_sqs_queue.audio-separate-queue-fifo.arn
  function_name     = aws_lambda_function.audio-separate-lambda.arn
  batch_size        = 1

  enabled           = true
}

resource "aws_iam_role_policy" "lambda_sqs_policy" {
  role   = aws_iam_role.audio-separate-role-lambda.id
  policy = data.aws_iam_policy_document.sqs_policy.json
}

data "aws_iam_policy_document" "sqs_policy" {
  statement {
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [aws_sqs_queue.audio-separate-queue-fifo.arn]
  }
}
