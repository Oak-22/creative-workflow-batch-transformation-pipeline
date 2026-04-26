# Python Utilities

This directory contains stage-scoped Python helpers for extracting,
auditing, validating, and materializing workflow artifacts across the
three documented pipeline stages.

## Layout

```text
scripts/python/
├── README.md
├── common/
│   ├── __init__.py
│   └── io_utils.py
├── stage1/
│   ├── __init__.py
│   ├── extract_xmp_metadata.py
│   ├── validate_stage1_metadata.py
│   └── build_stage1_manifest.py
├── stage2/
│   ├── __init__.py
│   ├── extract_develop_settings.py
│   ├── audit_stage2_parameters.py
│   └── build_stage2_manifest.py
└── stage3/
    ├── __init__.py
    ├── create_stage3_review_sheet.py
    ├── ingest_stage3_review_results.py
    └── build_stage3_manifest.py
```

# Python Workflow Tooling

This directory contains stubbed Python tooling for external observability,
validation, and reporting around the Lightroom-based creative workflow.

The goal is not to replace Lightroom. The goal is to make stage state,
validation logic, and human review more inspectable and reproducible using
metadata exports such as XMP sidecar files and derived CSV manifests.


## Intent

- `common/`: shared filesystem and JSON helpers
- `stage1/`: metadata extraction, validation, and manifest generation
- `stage2/`: develop-setting extraction, parameter auditing, and
  manifest generation
- `stage3/`: review-sheet creation, review-result ingestion, and
  manifest generation

These files are currently lightweight entrypoint stubs so the package
structure exists before implementation details are filled in.

## Intended Outputs

Future outputs may include:

- normalized metadata extracts
- stage validation reports
- stage manifests
- exception logs
- review sheets
- summary reports

Example future output locations:

- `outputs/stage1/`
- `outputs/stage2/`
- `outputs/stage3/`

## CLI Philosophy

These scripts are currently stubs. Each script is structured as a future CLI
entrypoint with:
- argument parsing
- clear responsibility
- TODO scaffolding
- conservative placeholder output

## Notes

The initial version is intentionally lightweight. The first implementation
priority should likely be Stage 1, since XMP metadata extraction and manifest
validation are the clearest bridge between Lightroom state and external
analysis.


## Data Flow

Phase 1

• parse XMP files

• normalize into dataframe / CSV

• document schema

Phase 2

• implement Stage 1 validation rules

• generate pass/fail report

• generate completeness stats

Phase 3

• create workflow manifest across stages

• add exception flags

• summarize counts

Phase 4

• add Stage 2 parameter auditing if XMP supports it

• add Stage 3 review manifest/evaluation tables

Phase 5

• tests

• sample files

• CLI usage

• polished README section showing outputs