# Creative Workflow Batch Transformation Pipeline

Systems engineering project showing how creative-production workflows can be structured as deterministic, scalable pipelines rather than ad hoc editing sequences.

## Executive Summary

This repository models creative-production work as a reproducible,
multi-stage pipeline with explicit boundaries, non-destructive state
transitions, and validation checkpoints. Even when executed inside
GUI-based tools, the workflow is treated as a production system rather
than an ad hoc editing sequence.

Across the documented stages, the project demonstrates how metadata
ingestion, image normalization, and semantic batch editing can be
composed into a deterministic workflow that scales more reliably than
repeated manual editing.

## Problem

Creative-production workflows often accumulate as informal editing
habits inside GUI tools, making them hard to reproduce, audit, and
scale across large datasets. Without explicit stage boundaries and
validation checkpoints, small inconsistencies compound into rework,
operator drift, and weak rollback safety.

The core systems problem is therefore not only how to optimally perform isolated
editing operations, but how to organize them into a stable pipeline
that remains batch-safe under real tooling limitations.

## Solution Overview

The repository addresses that problem by breaking the workflow into
three documented stages:

1. Metadata ingestion, enrichment, and query design
2. Baseline conditioning and rollback
3. Bulk AI mask definition propagation

Each stage isolates a specific class of transformations, defines clear
inputs and outputs, and introduces validation boundaries before later
operations are applied. The result is a workflow that is more
deterministic, easier to reason about, and safer to evolve over time.

In Stages 2 and 3, batch execution does not imply a single static
transformation applied uniformly across every file. Both stages operate
at dataset scale while still producing image-specific results at
runtime: normalization responds to the conditions of each image, and AI
mask propagation generates semantic selections whose effective impact
varies by image content.

## Key Constraints

Across the documented stages, the shared engineering constraints and
design themes are:

- deterministic, stage-bounded workflow design
- batch-safe operations under tooling constraints
- reproducibility through clear validation checkpoints
- structured automation with human review at defined boundaries


## Pipeline Stages

This repository is organized as a single multi-stage pipeline with supporting documentation for each major stage.

Stage 1 establishes the metadata and query foundation for the workflow.

- **Identity initialization:** Single-preset ingest establishes the protected authorship baseline
- **Semantic enrichment:** Post-import presets and keywords add non-overlapping descriptive metadata
- **Query layer:** Filter-based retrieval and Smart Collections derive reusable views over image records

Stages 2 and 3 form the image-processing portion of the pipeline, which currently follows this progression:

- **Preprocessing:** Local corrective cleaning
- **Normalization:** Dataset-wide luminance standardization with scene-level color normalization
- **Semantic operations:** Batch AI masking
- **Human review:** Manual refinement pass

### 1. Metadata Ingestion, Enrichment, and Query Pipeline
Location: [Stage 1](pipeline_stages/001_metadata-ingestion-enrichment-query-pipeline/README.md)

Focus areas:
- deterministic ingest behavior under single-preset constraints
- non-destructive metadata enrichment through non-overlapping field assignments
- metadata-driven indexing and retrieval patterns enabling both rapid ad-hoc queries and declarative views over image records

### 2. Baseline Conditioning and Rollback Pipeline
Location: [Stage 2](pipeline_stages/002_baseline-conditioning-and-rollback/README.md)

- local corrective cleanup and dataset-wide luminance normalization across heterogeneous images
- scene-level color normalization that preserves natural hue differences across scenes
- virtual copies for rollbackable experimentation while reducing operator cognitive load

### 3. Bulk AI Mask Definition Propagation 
Location: [Stage 3](pipeline_stages/003_bulk-ai-mask-definition-propagation/README.md)

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of AI-generated semantic masks to batch edit operations
- qualitative evaluation of mask quality and workflow reliability against manual editing results


## Repository Structure

```text
creative-workflow-batch-transformation-pipeline/
├── .github/
│   └── agent_instructions/
│       ├── global/
│       └── repo/
├── .gitignore
├── Commit-Message-Pre-Agent-Prompt-Refinement.png
├── README.md
├── docs/
│   ├── README.md
│   ├── architecure
│   ├── diagrams
│   └── stage 2 batch normalization concerns/
│       ├── Attachments/
│       └── stage 2 batch normalization.md
├── engineering_learning_workspace/
├── pipeline_stages/
│   ├── 001_metadata-ingestion-enrichment-query-pipeline/
│   │   ├── README.md
│   │   └── assets/
│   │       ├── diagrams/
│   │       └── images/
│   ├── 002_baseline-conditioning-and-rollback/
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
│   ├── agent_prompt
│   └── python/
│       └── README.md
└── tests/
    └── README.md
```
