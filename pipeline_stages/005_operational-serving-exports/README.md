# Stage 5 - Operational Serving Exports

Stage 5 converts the Stage 1-4 evidence chain into compact serving
exports for downstream operational consumers.


## Purpose

Stages 1-4 preserve detailed evidence:

- asset context, source availability, and metadata state
- Develop-parameter deltas
- mask definition and mask-edit state
- RAW pixel signal metrics
- rendered JPEG target evidence
- ML-readiness handoff state

Stage 5 does not replace those artifacts. It builds smaller export
surfaces that point back to them.


## Producer And Consumers

The data engineering/platform role is the producer of Stage 5 exports.

The modeled consumers are:

```text
ML / data science team
  evaluates feature sufficiency, target definitions, and modeling feasibility

Business / operations stakeholder
  evaluates readiness, workflow leverage, and operational impact

Audit / compliance / governance stakeholder
  verifies provenance, claims, non-claims, and reproducibility
```


## Export Scope

Stage 5 currently produces file-based exports:

```text
outputs/stage5/exports/stage5_asset_summary.json
outputs/stage5/exports/stage5_feature_family_summary.json
outputs/stage5/exports/stage5_artifact_catalog.json
outputs/stage5/stage5_manifest.json
```

These are not database views. They are local serving exports that can be
loaded into database tables or object storage later.


## Later Infrastructure Boundary

A later infrastructure layer may create:

```text
database tables
warehouse tables
SQL views
dashboards
scheduled loader jobs
```

Terraform should provision infrastructure. Python should transform the
stage artifacts into loadable exports. SQL migrations should define
database tables and views.

The cloud-loader contract for the planned Stage 5 serving-export prefix,
DynamoDB status table, and future status views is documented in
`../../docs/cloud/stage5-loader-contract.md`.
