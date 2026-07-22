resource "random_id" "suffix" {
  byte_length = 4
}

# bucket names are global across all of aws, so we tack on
# a random suffix to avoid clashing with someone else's bucket
resource "aws_s3_bucket" "uploads" {
  bucket = "${var.project_name}-uploads-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_public_access_block" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}