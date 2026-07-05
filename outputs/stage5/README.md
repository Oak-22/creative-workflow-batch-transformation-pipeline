## Stage 5 Output Order

Stage 5 turns the Stage 1-4 evidence chain into compact serving exports
for operational consumers.

The front-door artifact is:

```text
stage5_manifest.json
```

Read or regenerate the JSON artifacts in this order:

```text
1. exports/stage5_asset_summary.json
   one row per asset with feature-family presence, rendered target
   presence, and compact supporting evidence

2. exports/stage5_feature_family_summary.json
   one row per feature family with source-stage and artifact pointers

3. exports/stage5_artifact_catalog.json
   catalog of stage manifests and generated artifacts with hashes

4. stage5_manifest.json
   compact index over the Stage 5 serving exports
```


## Consumers

Stage 5 models these consumers:

```text
ml_data_science_team
business_operations_stakeholder
audit_compliance_governance_stakeholder
```

The data engineering/platform role is the producer of these exports, not
the consumer.


## Terminology

Stage 5 outputs are file-based exports. They are not database views.

Use this distinction:

```text
Stage 5 JSON exports
  local serving artifacts

Database tables
  later loaded structures

Database views
  later SQL-defined consumer surfaces
```


## Regeneration

Regenerate Stage 5 after Stage 1-4 manifests or Stage 4 handoff
artifacts change:

```bash
python3 scripts/python/stage5/01_build_serving_exports.py
python3 scripts/python/stage5/02_build_stage5_manifest.py
```
