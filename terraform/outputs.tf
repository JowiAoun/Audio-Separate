output "sqs_queue_url" {
  value = aws_sqs_queue.audio-separate-queue-fifo.url
  sensitive = true
}

output "s3_bucket_name" {
  value = aws_s3_bucket.audio-separate-bucket.bucket
  sensitive = true
}

output "lambda_function_name" {
  value = aws_lambda_function.audio-separate-lambda.function_name
  sensitive = true
}
