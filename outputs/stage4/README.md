## Stage 4 Output Order

Stage 4 packages the earlier stage evidence into an ML-readiness
handoff. It shows what feature families exist, which assets have
complete cross-stage coverage, and which additional evidence is required
before model development.

The front-door artifact is:

```text
stage4_manifest.json
```

That manifest is intentionally compact. It references the verbose JSON
artifacts by path, size, SHA-256 hash, role, and producing script.

Read or regenerate the JSON artifacts in this order:

```text
1. features/stage4_raw_pixel_signal_metrics.json
   extracts RAW pixel-signal summaries and decoded-read provenance

2. features/stage4_feature_inventory.json
   joins Stage 1-4 evidence by asset_key and reports feature coverage

3. handoff/stage4_dataset_readiness_report.json
   states handoff readiness and the next evidence requirements

4. handoff/stage4_ml_handoff_contract.json
   defines producer/consumer responsibilities and scope boundaries

5. stage4_manifest.json
   collates the Stage 4 evidence chain for review
```


## Raw Metrics Field Guide

`features/stage4_raw_pixel_signal_metrics.json` is organized for
human review as well as machine parsing.

The top-level object starts with:

```json
{
  "stage": "stage4_pixel_signal_metrics",
  "status": "complete",
  "summary": {
    "asset_count": 12,
    "complete_coverage_asset_count": 12,
    "histogram_bins": 16,
    "incomplete_coverage_asset_count": 0
  }
}
```

Each `records[]` item follows this reading order:

```text
asset_key
raw_path
file_provenance
decoder_provenance
read_coverage
raw_mosaic_metrics
rendered_preview_metrics
```

Interpret those objects as:

- `file_provenance`: exact RAW file identity through hash and size
- `decoder_provenance`: decoder, library versions, camera white
  balance, black/white levels, and sensor layout metadata
- `read_coverage`: decoded raster shapes, pixel counts, hashes, and
  histogram coverage checks
- `raw_mosaic_metrics`: sensor-domain RAW value summaries and CFA
  channel summaries
- `rendered_preview_metrics`: derived half-size RGB preview summaries
  such as luminance, saturation proxy, and red/green/blue channel-cast
  proxies


## Folder Grouping

Stage 4 intentionally separates feature evidence from handoff evidence:

```text
outputs/stage4/
  stage4_manifest.json

  features/
    stage4_raw_pixel_signal_metrics.json
    stage4_feature_inventory.json

  handoff/
    stage4_dataset_readiness_report.json
    stage4_ml_handoff_contract.json
```

The `features/` folder contains machine-readable feature surfaces. The
`handoff/` folder contains governance and readiness artifacts that
explain how those features may be used by a future ML team.


## Production Boundary

Stage 4 consumes already-generated artifacts from Stages 1-3 plus RAW
pixel-signal metrics:

```text
outputs/stage1/stage1_manifest.json
outputs/stage2/stage2_manifest.json
outputs/stage3/stage3_manifest.json
outputs/stage4/features/stage4_raw_pixel_signal_metrics.json
```

The RAW metric extractor requires the local Python environment with
`rawpy` and `numpy` installed:

```bash
.venv/bin/python scripts/python/stage4/01_extract_pixel_signal_metrics.py
```

After RAW metrics are current, regenerate the handoff artifacts in
order:

```bash
python3 scripts/python/stage4/02_build_feature_inventory.py
python3 scripts/python/stage4/03_build_dataset_readiness_report.py
python3 scripts/python/stage4/04_build_ml_handoff_contract.py
python3 scripts/python/stage4/05_build_stage4_manifest.py
```
