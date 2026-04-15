# Creative Workflow Batch Transformation Pipeline

Systems engineering project showing how creative-production workflows can be structured as deterministic, scalable pipelines rather than ad hoc editing sequences.

## Project Framing

This repository models creative-production work as a reproducible
workflow with explicit stages, non-destructive state transitions, and
validation checkpoints

Even when executed inside GUI-based tools, the process is treated as a
production system rather than an ad hoc editing sequence.

Across the documented stages, the shared engineering themes are:

- deterministic, stage-bounded workflow design
- batch-safe operations under tooling constraints
- reproducibility through clear validation checkpoints
- structured automation with human review at defined boundaries

## Project Structure

This repository is organized as a single multi-stage pipeline with supporting documentation for each major stage:

1. Metadata Ingestion, Enrichment, and Query Pipeline
2. Baseline Image Normalization Pipeline
3. Bulk AI Mask Definition Propagation

Stage 1 establishes the metadata and query foundation for the workflow.

Stages 2 and 3 form the image-processing portion of the pipeline, which currently follows this progression:

- **Preprocessing:** Local corrective cleanup (for example dust removal and chromatic aberration correction)
- **Normalization:** Dataset-wide luminance and color standardization
- **Semantic operations:** Batch AI masking
- **Human review:** Manual refinement pass



## Repository Structure

```text
creative-workflow-batch-transformation-pipeline/
├── .gitignore
├── README.md
├── package-lock.json
├── docs/
│   ├── README.md
│   ├── architecure/
│   └── diagrams/
├── pipeline_stages/
│   ├── 001_metadata-ingestion-enrichment-query-pipeline/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   ├── 002_baseline-image-normalization/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   └── 003_bulk-ai-mask-definition-propagation/
│       ├── README.md
│       └── assets/
│           ├── diagrams/
│           └── images/
├── scripts/
│   └── python/
│       └── README.md
└── tests/
    └── README.md
```

## Pipeline Stages

### 1. Metadata Ingestion, Enrichment, and Query Pipeline
Location: `pipeline_stages/001_metadata-ingestion-enrichment-query-pipeline/` ([README](pipeline_stages/001_metadata-ingestion-enrichment-query-pipeline/README.md))

Focus areas:
- deterministic ingest behavior under single-preset constraints
- non-destructive metadata enrichment through non-overlapping field assignments
- metadata-driven indexing and retrieval patterns enabling both rapid ad-hoc queries and declarative views over image records

### 2. Baseline Image Normalization Pipeline
Location: `pipeline_stages/002_baseline-image-normalization/` ([README](pipeline_stages/002_baseline-image-normalization/README.md))

- local corrective cleanup and luminance/color normalization across heterogeneous images with varying capture conditions
- exemplar-based calibration to propagate consistent transformations across heterogeneous data
- virtual copies for rollbackable experimentation while reducing operator cognitive load

### 3. Bulk AI Mask Definition Propagation 
Location: `pipeline_stages/003_bulk-ai-mask-definition-propagation/` ([README](pipeline_stages/003_bulk-ai-mask-definition-propagation/README.md))

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of AI-generated semantic masks to batch edit operations
- qualitative evaluation of mask quality and workflow reliability against manual editing results
