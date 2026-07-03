## Output Artifacts

This directory contains derived JSON evidence produced by the pipeline.
The JSON files are intentionally verbose because they preserve source
paths, hashes, stage labels, summaries, and per-asset records.

Read outputs by stage, then by production order:

```text
stage1/
  source metadata extraction, validation, and manifest

stage2/
  stage2_manifest.json as the compact review index
  frozen Develop-state checkpoints
  -> Develop-setting extracts
  -> pre/post Develop comparison

stage3/
  stage3_manifest.json as the compact review index
  frozen semantic/local sidecar checkpoints
  -> mask-state extracts
  -> adjacent checkpoint comparisons
  -> exploratory Lightroom write-behavior probes

stage4/
  RAW pixel-signal metrics

lightroom_sdk/
  exploratory Lightroom SDK export artifacts
```

Stage-specific ordering notes live in:

- `stage2/README.md`
- `stage3/README.md`

Treat these outputs as derived evidence. When a source checkpoint,
extractor schema, or comparison script changes, regenerate the affected
artifact and every downstream artifact that depends on it.
