# Stage 5 Cloud Loader Contract

## Purpose

This contract defines how a future cloud loader should ingest Stage 5
serving exports after they are uploaded to object storage.

Stage 5 exports are file-based serving artifacts. The cloud loader is a
later operational component that validates those artifacts, records load
state, and eventually loads them into queryable storage.

This document intentionally defines the contract before choosing a
compute runtime such as Lambda, Step Functions, Glue, ECS/Fargate, or
Batch.

## Current Boundary

Producer:

```text
local pipeline scripts
```

Canonical local input:

```text
outputs/stage5/stage5_manifest.json
outputs/stage5/exports/stage5_asset_summary.json
outputs/stage5/exports/stage5_feature_family_summary.json
outputs/stage5/exports/stage5_artifact_catalog.json
```

Canonical object-storage prefix:

```text
s3://<source-assets-bucket>/outputs/stage5/
```

Terraform currently provisions:

```text
S3 source-assets bucket
outputs/stage5/ serving-export prefix convention
DynamoDB loader status table
IAM policy for a future loader runtime
```

Terraform does not currently provision loader compute.

## Loader Reading Order

The Stage 5 manifest uses a human-facing export sequence:

```text
asset summary -> feature family summary -> artifact catalog
```

The cloud loader should use a machine-validation order:

```text
stage5_manifest.json
artifact catalog
feature family summary
asset summary
```

Rationale:

- the manifest is the entrypoint and compact contract
- the artifact catalog is the broadest provenance and hash surface
- feature-family summary defines derived evidence categories
- asset summary contains the row-level serving data

## Required Loader Inputs

The loader must read:

```text
outputs/stage5/stage5_manifest.json
```

The manifest must declare:

```text
stage = stage5_operational_serving_layer
status = complete
export_sequence[]
summary.asset_count
summary.feature_family_count
summary.artifact_count
```

Each `export_sequence[]` item must include:

```text
order
role
produced_by
artifact.path
artifact.sha256
artifact.size_bytes
```

## Required Exports

The loader currently expects exactly these Stage 5 export roles:

```text
asset_summary_export
feature_family_summary_export
artifact_catalog_export
```

Expected local paths:

```text
outputs/stage5/exports/stage5_asset_summary.json
outputs/stage5/exports/stage5_feature_family_summary.json
outputs/stage5/exports/stage5_artifact_catalog.json
```

Expected object keys are the same paths under the Stage 5 S3 prefix.

## Validation Rules

The loader must fail fast if:

- `stage5_manifest.json` is missing
- the manifest is not valid JSON
- manifest `stage` is not `stage5_operational_serving_layer`
- manifest `status` is not `complete`
- an expected export role is missing
- an artifact path points outside `outputs/stage5/`
- an artifact is missing from object storage
- an artifact size does not match the manifest
- an artifact SHA-256 digest does not match the manifest
- required top-level fields are missing from an export

The loader should treat unknown extra files under `outputs/stage5/` as
non-blocking unless they are referenced by the manifest.

## Idempotency

The loader must be idempotent. Running the same load more than once
should not create duplicate downstream rows or duplicate success records.

Recommended load identity:

```text
load_id = sha256(stage5_manifest.json bytes)
```

This ties the load identity to the exact manifest content. If the
manifest changes, the loader sees a new load attempt. If the manifest is
unchanged, the loader can safely skip or re-validate the existing load.

The DynamoDB status table should use:

```text
partition key: load_id
```

Recommended status fields:

```text
load_id
status
stage
source_bucket
source_prefix
manifest_key
manifest_sha256
artifact_count
asset_count
feature_family_count
started_at
updated_at
completed_at
error_code
error_message
```

## Loader Status States

Recommended state machine:

```text
registered
validating
validated
loading
loaded
failed
skipped
```

State meanings:

```text
registered
  load_id has been observed, but validation has not started

validating
  manifest and referenced exports are being checked

validated
  manifest, sizes, hashes, roles, and required schemas passed

loading
  validated exports are being written to downstream storage

loaded
  downstream load completed successfully

failed
  validation or load failed

skipped
  the same load_id was already loaded or intentionally ignored
```

## Initial Definition Of Loaded

For the first cloud-loader iteration, `loaded` may mean only:

```text
all Stage 5 artifacts were found, parsed, size-checked, hash-checked,
and recorded in the loader status table
```

It does not need to mean that data has already been inserted into a
warehouse, database, or analytics table.

Later iterations may extend `loaded` to mean:

```text
asset summary rows loaded
feature family summary rows loaded
artifact catalog rows loaded
load audit record written
```

## Failure Behavior

Validation failures should:

- write `failed` status when possible
- preserve the failing `load_id`
- record an explicit `error_code`
- record a concise `error_message`
- avoid partial downstream writes when validation has not completed

Load failures after validation should:

- preserve validated artifact metadata
- write `failed` status
- allow retry with the same `load_id`
- avoid duplicate downstream rows on retry

## Runtime Selection Guidance

Initial local validator:

```text
Python script reading local Stage 5 files
```

Likely first cloud runtime:

```text
Lambda
```

Best when the loader only validates small JSON files and writes status.

Step Functions becomes useful when:

```text
validation, loading, retry, and notification become separate steps
```

Glue becomes useful when:

```text
exports are converted into data lake tables or queried through Athena
```

ECS/Fargate becomes useful when:

```text
loader code needs a containerized Python runtime with heavier dependencies
```

Batch becomes useful when:

```text
the workload shifts from small Stage 5 metadata exports to large
compute-heavy reprocessing jobs
```

## Non-Goals

This contract does not define:

- production database schemas
- dashboard views
- model-training datasets
- RAW image processing in the cloud
- rendered-image generation in the cloud
- final choice of cloud compute runtime

Those are later contracts.

