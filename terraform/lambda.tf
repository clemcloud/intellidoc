resource "aws_lambda_function" "processor" {
  function_name = "${var.project_name}-processor"
  filename      = "${path.module}/../lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda.zip")

  handler = "lambda_function.lambda_handler"
  runtime = "python3.11"
  role    = aws_iam_role.lambda_exec.arn

  timeout     = 60
  memory_size = 512

  # needs to sit inside the vpc to reach rds privately
  vpc_config {
    subnet_ids         = [aws_subnet.private_a.id, aws_subnet.private_b.id]
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      DB_HOST        = aws_db_instance.main.address
      DB_NAME        = "intellidoc"
      DB_USER        = "intellidoc_user"
      DB_PASSWORD    = var.db_password
      GEMINI_API_KEY = var.gemini_api_key
    }
  }
}

# security group for lambda itself, allows outbound to reach rds and s3/internet
resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-lambda-sg"
  description = "allows lambda to reach rds and the internet"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# lets s3 actually invoke this lambda
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.uploads.arn
}

# the actual trigger - fires the lambda whenever a file is uploaded
resource "aws_s3_bucket_notification" "upload_trigger" {
  bucket = aws_s3_bucket.uploads.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.processor.arn
    events               = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}