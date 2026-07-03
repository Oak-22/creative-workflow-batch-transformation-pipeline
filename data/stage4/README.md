## Stage 4 Data Layout

Stage 4 data folders hold optional evidence inputs for ML-readiness
handoff work. These files are separate from the generated JSON outputs
under `outputs/stage4/`.


## Rendered Targets

Use `rendered_targets/lightroom_jpeg_exports/` for Lightroom-rendered
JPEG exports that represent the current human-approved edit state.

Recommended export convention:

```text
data/stage4/rendered_targets/lightroom_jpeg_exports/
  JB107456.jpg
  JB107468.jpg
  JB107504.jpg
```

Use the same `asset_key` stem as the RAW/XMP sidecars. This keeps the
rendered target joinable to Stage 1-4 artifacts without embedding
additional mapping files.

Interpretation:

```text
RAW file
  source capture signal

XMP/ACR sidecars
  Lightroom parameter and mask state

Lightroom JPEG export
  rendered visual target for future model or QA evaluation
```

This rendered target layer can support a future before/after visual
comparison axis:

```text
RAW source
  -> Lightroom parameter state
  -> Lightroom-rendered JPEG target
```

That axis is intentionally future-facing. It gives a downstream
computer-vision, OCR, or multimodal evaluation workflow a concrete
rendered output to compare against the RAW source and XMP/ACR parameter
state.
