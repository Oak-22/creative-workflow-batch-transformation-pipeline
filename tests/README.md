# Tests

This directory is reserved for executable validation support around the
workflow-observability scripts and any later quantitative analysis
tooling.

The tests in this repository are not meant to replace the workflow’s
primary visual or operational evidence. Their role is narrower and more
concrete:

- verify extraction logic over XMP sidecars, manifests, and review data
- protect schema assumptions and parsing behavior
- validate script-level transformations and reports
- support later quantitative checks over RAW-linked metadata, edit
  parameters, or rendered-output measurements when those analyses are
  implemented

In the project’s broader evidence model, tests sit below the workflow
artifacts and stage writeups. The visual and operational materials
usually establish the qualitative claim first; tests help ensure the
structured proof layer remains reproducible once scripts and analysis
pipelines are added.

Likely future contents include:

- fixture XMP sidecars
- sample manifests and review sheets
- parser and schema regression tests
- Stage 1 metadata validation tests
- Stage 2 parameter-audit tests
- Stage 3 review-ingestion tests
