variable "aws_region" {
  description = "AWS region for the centralized source-assets bucket."
  type        = string
}

variable "bucket_name" {
  description = "Globally unique S3 bucket name for centralized source assets."
  type        = string
}

variable "environment" {
  description = "Environment tag value, e.g. dev, prod, research."
  type        = string
  default     = "research"
}

variable "raw_prefix" {
  # Prefix variables model logical separation inside one bucket.
  description = "Prefix for RAW masters."
  type        = string
  default     = "raw/"
}

variable "xmp_prefix" {
  description = "Prefix for XMP sidecars or metadata snapshots."
  type        = string
  default     = "xmp/"
}

variable "acr_prefix" {
  description = "Prefix for ACR sidecars containing Lightroom mask/local adjustment state."
  type        = string
  default     = "acr/"
}

variable "jpeg_prefix" {
  description = "Prefix for optional JPEG companions or rendered review assets."
  type        = string
  default     = "jpeg/"
}

variable "serving_exports_prefix" {
  description = "Prefix for derived Stage 5 serving exports used by downstream loaders."
  type        = string
  default     = "outputs/stage5/"
}

variable "loader_status_table_name" {
  description = "DynamoDB table name for idempotent Stage 5 loader status records."
  type        = string
  default     = "digital-asset-stage5-loader-status"
}

variable "force_destroy" {
  description = "Allow bucket destroy even when objects remain. Keep false for safety."
  type        = bool
  default     = false
}

variable "tags" {
  description = "Additional tags to apply to provisioned resources."
  type        = map(string)
  default     = {}
}
