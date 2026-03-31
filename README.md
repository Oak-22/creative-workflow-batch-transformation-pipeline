# Creative Workflow Batch Transformation Pipeline

A systems engineering portfolio project documenting how creative-production workflows can be structured as deterministic, scalable batch pipelines rather than ad hoc editing sequences.

This repository is organized as a single umbrella project with three related case studies:

1. Metadata Ingestion and Enrichment Pipeline
2. Baseline Image Normalization Pipeline
3. Bulk AI Masking Batch Rebinding Experiment

## Project Framing

The portfolio treats image workflow operations as pipeline systems with clear boundaries, failure modes, validation points, and downstream dependencies.

Across the three case studies, the shared engineering themes are:

- deterministic initialization of asset state
- separation of identity, semantic, and transformation layers
- batch-safe operations under tooling constraints
- reproducibility through explicit validation and operator-visible checkpoints
- reduction of manual editing time through structured automation

## Repository Structure

```text
creative-workflow-batch-transformation-pipeline/
├── README.md
├── case-studies/
│   ├── metadata-ingestion-and-enrichment/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   ├── baseline-image-normalization/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   └── bulk-ai-masking-batch-rebinding-experiment/
│       ├── README.md
│       └── assets/
│           ├── diagrams/
│           └── images/
├── docs/
│   ├── architecture/
│   └── portfolio-notes/
├── scripts/
│   └── python/
├── analysis/
│   └── metrics/
├── simulation/
└── tests/
```

## Case Studies

### 1. Metadata Ingestion and Enrichment Pipeline
Location: [case-studies/metadata-ingestion-and-enrichment/README.md](/Users/julianbuccat/Repos/system-design-case-studies/case-studies/metadata-ingestion-and-enrichment/README.md)

Focus areas:
- deterministic ingest behavior under single-preset constraints
- immutable identity metadata vs mutable semantic metadata
- post-ingest enrichment without field collisions
- metadata-driven indexing and retrieval patterns

### 2. Baseline Image Normalization Pipeline
Location: [case-studies/baseline-image-normalization/README.md](/Users/julianbuccat/Repos/system-design-case-studies/case-studies/baseline-image-normalization/README.md)

Focus areas:
- luminance normalization across heterogeneous capture conditions
- staged preprocessing before downstream semantic or color operations
- exemplar-based calibration for cross-scene consistency
- throughput and cognitive-load reduction in manual workflows

### 3. Bulk AI Masking Batch Rebinding Experiment
Location: [case-studies/bulk-ai-masking-batch-rebinding-experiment/README.md](/Users/julianbuccat/Repos/system-design-case-studies/case-studies/bulk-ai-masking-batch-rebinding-experiment/README.md)

Focus areas:
- precomputed semantic masks as reusable transformation bindings
- bulk relinking of mask outputs to batch edit operations
- failure analysis for model drift, mask instability, and domain mismatch
- evaluation of when AI assistance remains deterministic enough for pipeline use

## Naming Conventions

Recommended file and folder naming conventions:

- Use kebab-case for directories and portfolio-facing markdown files.
- Remove dates from primary artifact names unless the date is analytically important.
- Reserve dates for version history, changelogs, or appendix material.
- Prefer `README.md` inside each case-study folder so each study opens cleanly in GitHub and local editors.

Examples:

- `Image_Metadata_Pipeline_2026-02-26.md` -> `case-studies/metadata-ingestion-and-enrichment/README.md`
- `Baseline_Image_Noramlization_Pipeline_2026-03-03_.md` -> `case-studies/baseline-image-normalization/README.md`
- Future diagrams: `system-context.png`, `stage-1-luminance-normalization.png`, `mask-rebinding-flow.png`
- Future appendices: `appendix-validation-checklist.md`, `appendix-failure-modes.md`

## Asset Placement Guidance

Use assets close to the case study they support.

- Put case-study-specific screenshots in `case-studies/<study>/assets/images/`.
- Put architecture diagrams, sequence diagrams, and stage flow visuals in `case-studies/<study>/assets/diagrams/`.
- Use `docs/architecture/` only for diagrams or references shared across multiple case studies.
- Keep filenames descriptive and stable so markdown links do not need frequent rewrites.

Suggested pattern:

- `assets/images/` for screenshots, UI captures, before/after samples
- `assets/diagrams/` for pipeline diagrams, sequence flows, state-transition visuals, validation checklists

## Optional Future Code and Analysis Folders

These folders are included so the repository can grow from design artifact to executable engineering portfolio:

- [scripts/python](/Users/julianbuccat/Repos/system-design-case-studies/scripts/python): utilities for metadata parsing, batch file audits, preset validation, or experiment helpers
- [analysis/metrics](/Users/julianbuccat/Repos/system-design-case-studies/analysis/metrics): throughput measurements, error-rate summaries, calibration comparisons, and experiment outputs
- [simulation](/Users/julianbuccat/Repos/system-design-case-studies/simulation): lightweight pipeline simulations, synthetic datasets, or workflow modeling notebooks/scripts
- [tests](/Users/julianbuccat/Repos/system-design-case-studies/tests): validation fixtures and regression checks for future code artifacts

## Suggested Portfolio Conventions

To keep the repository reading like a systems engineering artifact instead of a note dump:

- Start each case study with problem, constraints, architecture, validation, failure modes, and tradeoffs.
- Treat visuals as system evidence, not decoration.
- Keep implementation notes and exploratory drafts in `docs/portfolio-notes/` instead of mixing them into the top-level narrative.
- Add appendices when needed, but keep each case study's main `README.md` focused on the engineering story.

## Next Expansion Opportunities

1. Add a shared system-context diagram in `docs/architecture/` showing how the three pipelines connect.
2. Add appendix files per case study for validation checklists and failure-mode analysis.
3. Add small Python utilities once you want the portfolio to include executable workflow tooling.
