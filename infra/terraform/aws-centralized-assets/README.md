# AWS Centralized Assets Terraform

This Terraform root module provisions a realistic baseline for the
architecture recorded in ADR 0001:

- one centralized S3 bucket for source assets
- separate logical prefixes for RAW masters, XMP sidecars, and optional
  rendered JPEG companions
- a derived serving-export prefix for Stage 5 outputs used by downstream
  cloud loaders
- a DynamoDB table for idempotent Stage 5 loader status tracking
- an attachable IAM policy for a future Stage 5 loader runtime
- local scripts and analytic outputs remain outside the bucket

## What It Creates

- one S3 bucket
- bucket versioning
- bucket-wide server-side encryption
- bucket public-access blocking
- one DynamoDB status table with on-demand billing, encryption, and
  point-in-time recovery
- one IAM policy granting read-only access to Stage 5 serving exports
  and read/write access to loader status records
- lifecycle rules for:
  - RAW masters
  - XMP sidecars
  - JPEG companions
  - Stage 5 serving exports

## Prefix Convention

The design uses one bucket with separate prefixes rather than separate
buckets by default:

- `raw/`
- `xmp/`
- `jpeg/`
- `outputs/stage5/`

These prefixes are conventions for source-asset separation. S3 does not
enforce folder semantics itself, but the outputs from this module make
those canonical URIs explicit.

## Usage

```bash
cd infra/terraform/aws-centralized-assets
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Notes

- This module does not upload any assets.
- It provisions the storage and loader-control boundary only.
- The Stage 1 verifier/extractor can later target the bucket and these
  prefixes directly.
- Stage 5 exports can be synced to `outputs/stage5/` as derived serving
  inputs for a future cloud loader.
- The module does not provision a compute runtime. A later Lambda,
  ECS/Fargate, Glue, or Batch loader can attach the emitted IAM policy
  and use the status table for idempotency.
