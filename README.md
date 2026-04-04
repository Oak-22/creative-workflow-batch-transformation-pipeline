# Creative Workflow Batch Transformation Pipeline

A systems engineering portfolio project demonstrating how creative-production workflows can be structured as deterministic, scalable batch pipelines rather than ad hoc, non-repeatable editing sequences.

This repository is organized as a single multi-stage pipeline with supporting documentation for each major stage:

1. Metadata Ingestion, Enrichment, and Query Pipeline
2. Baseline Image Normalization Pipeline
3. Bulk AI Mask Definition Propagation

Within the image-processing portion of the pipeline, transformations currently follow this progression:

- **Preprocessing:** Dust removal batch pass
- **Normalization:** Luminance + color normalization
- **Semantic operations:** Batch AI masking
- **Human review:** Manual refinement pass

## Project Framing

The portfolio treats image workflow operations as pipeline systems with clear boundaries, failure modes, validation points, and downstream dependencies.

Even when transformation steps are executed inside GUI-based creative tools, the pipeline is framed as a real production workflow with explicit stage boundaries, operator checkpoints, validation gates, and reproducible state transitions.

Across the documented stages, the shared engineering themes are:

- deterministic initialization of asset state
- separation of identity, semantic, and transformation layers
- batch-safe operations under tooling constraints
- reproducibility through explicit validation and operator-visible checkpoints
- reduction of manual editing time through structured automation

## Repository Structure

```text
creative-workflow-batch-transformation-pipeline/
├── README.md
├── pipeline_stages/
│   ├── 001_metadata-ingestion-enrichment-query-pipeline/
│   │   ├── README.md
│   │   └── assets/
│   │       └── images/
│   ├── 002_baseline-image-normalization/
│   │   ├── README.md
│   │   └── assets/
│   └── 003_bulk-ai-mask-definition-propagation/
│       ├── README.md
│       └── assets/
├── docs/
│   ├── README.md
│   ├── architecure
│   └── diagrams
├── notes/
│   ├── git_learn.md
│   └── ssh_learn.md
├── scripts/
│   └── python/
│       └── README.md
├── analysis/
│   └── metrics/
└── tests/
    └── README.md
```

## Pipeline Stages

### 1. Metadata Ingestion, Enrichment, and Query Pipeline
Location: [pipeline_stages/001_metadata-ingestion-enrichment-query-pipeline/README.md](/Users/julianbuccat/Projects/dev/creative_workflow_batch_transformation_pipeline/pipeline_stages/001_metadata-ingestion-enrichment-query-pipeline/README.md)

Focus areas:
- deterministic ingest behavior under single-preset constraints
- schema-level protection of identity metadata via non-overlapping field assignments
- post-ingest enrichment without destructive metadata overwrites
- metadata-driven indexing and retrieval patterns enabling rapid ad-hoc queries and declarative views over image records

### 2. Baseline Image Normalization Pipeline
Location: [pipeline_stages/002_baseline-image-normalization/README.md](/Users/julianbuccat/Projects/dev/creative_workflow_batch_transformation_pipeline/pipeline_stages/002_baseline-image-normalization/README.md)

- luminance and color normalization across heterogeneous images with varying capture conditions
- staged preprocessing establishing a normalized baseline before downstream pixel-level and further semantic operations
- exemplar-based calibration to propagate consistent transformations across heterogeneous data
- increased workflow throughput while reducing operator cognitive load

### 3. Bulk AI Mask Definition Propagation 
Location: [pipeline_stages/003_bulk-ai-mask-definition-propagation/README.md](/Users/julianbuccat/Projects/dev/creative_workflow_batch_transformation_pipeline/pipeline_stages/003_bulk-ai-mask-definition-propagation/README.md)

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of semantic segmentation outputs to batch edit operations
- qualitative evaluation of mask boundary accuracy and subject-detection completeness against manual editing results
- analysis of when AI-assisted segmentation remains reliable enough for deterministic pipeline workflows



