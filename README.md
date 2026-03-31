# Creative Workflow Batch Transformation Pipeline

A systems engineering portfolio project documenting how creative-production workflows can be structured as deterministic, scalable batch pipelines rather than ad hoc, non-repeatable editing sequences.

This repository is organized as a single umbrella project with three related case studies:

1. Metadata Ingestion, Enrichment, and Query Pipeline
2. Baseline Image Normalization Pipeline
3. Bulk AI Mask Definition Propagation

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
│   ├── metadata-ingestion-enrichment-query-pipeline/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   ├── baseline-image-normalization/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   └── bulk-ai-mask-definition-propagation/
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

### 1. Metadata Ingestion, Enrichment, and Query Pipeline
Location: [case-studies/metadata-ingestion-and-enrichment/README.md](/Users/julianbuccat/Repos/system-design-case-studies/case-studies/metadata-ingestion-enrichment-query-pipeline/README.md)

Focus areas:
- deterministic ingest behavior under single-preset constraints
- schema-level protection of identity metadata via non-overlapping field assignments
- post-ingest enrichment without destructive metadata overwrites
- metadata-driven indexing and retrieval patterns enabling rapid ad-hoc queries and declarative views over image records

### 2. Baseline Image Normalization Pipeline
Location: [case-studies/baseline-image-normalization/README.md](/Users/julianbuccat/Repos/system-design-case-studies/case-studies/baseline-image-normalization/README.md)

- luminance and color normalization across heterogeneous images with varying capture conditions
- staged preprocessing establishing a normalized baseline before downstream pixel-level and further semantic operations
- exemplar-based calibration to propagate consistent transformations across heterogeneous data
- increased workflow throughput while reducing operator cognitive load

### 3. Bulk AI Mask Definition Propagation 
Location: [case-studies/bulk-ai-masking-batch-rebinding-experiment/README.md](/Users/julianbuccat/Repos/system-design-case-studies/case-studies/bulk-ai-mask-definition-propagation/README.md)

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of semantic segmentation outputs to batch edit operations
- qualitative evaluation of mask boundary accuracy and subject-detection completeness against manual editing results
- analysis of when AI-assisted segmentation remains reliable enough for deterministic pipeline workflows




