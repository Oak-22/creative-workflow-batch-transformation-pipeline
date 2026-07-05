output "bucket_name" {
  description = "Centralized source-assets bucket name."
  value       = aws_s3_bucket.source_assets.bucket
}

# Outputs publish useful post-provision values for humans or for
# downstream Terraform/config consumers.
output "bucket_arn" {
  description = "ARN of the centralized source-assets bucket."
  value       = aws_s3_bucket.source_assets.arn
}

output "bucket_uri" {
  description = "S3 URI of the centralized source-assets bucket."
  value       = "s3://${aws_s3_bucket.source_assets.bucket}"
}

output "raw_prefix_uri" {
  description = "Canonical S3 URI for RAW masters."
  value       = "s3://${aws_s3_bucket.source_assets.bucket}/${var.raw_prefix}"
}

output "xmp_prefix_uri" {
  description = "Canonical S3 URI for XMP sidecars or metadata snapshots."
  value       = "s3://${aws_s3_bucket.source_assets.bucket}/${var.xmp_prefix}"
}

output "acr_prefix_uri" {
  description = "Canonical S3 URI for ACR sidecars containing Lightroom mask/local adjustment state."
  value       = "s3://${aws_s3_bucket.source_assets.bucket}/${var.acr_prefix}"
}

output "jpeg_prefix_uri" {
  description = "Canonical S3 URI for optional JPEG companions."
  value       = "s3://${aws_s3_bucket.source_assets.bucket}/${var.jpeg_prefix}"
}

output "serving_exports_prefix_uri" {
  description = "Canonical S3 URI for derived Stage 5 serving exports."
  value       = "s3://${aws_s3_bucket.source_assets.bucket}/${var.serving_exports_prefix}"
}

output "loader_status_table_name" {
  description = "DynamoDB table name for Stage 5 loader status records."
  value       = aws_dynamodb_table.stage5_loader_status.name
}

output "loader_status_table_arn" {
  description = "DynamoDB table ARN for Stage 5 loader status records."
  value       = aws_dynamodb_table.stage5_loader_status.arn
}

output "stage5_loader_policy_arn" {
  description = "IAM policy ARN to attach to a future Stage 5 cloud loader role."
  value       = aws_iam_policy.stage5_loader.arn
}
