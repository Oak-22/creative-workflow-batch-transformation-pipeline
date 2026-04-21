# Creative Workflow Batch Transformation Pipeline

Systems engineering project showing how creative-production workflows can be structured as deterministic, scalable pipelines rather than ad hoc editing sequences.

## Executive Summary

Creative-production work is modeled as a reproducible, multi-stage
pipeline with explicit boundaries, non-destructive state
transitions, and validation checkpoints. Even when executed inside
GUI-based tools, the workflow is designed with production system qualities rather
than an ad hoc editing sequence.

The core engineering pattern is deterministic orchestration around
uncertain inputs: creative image variance from heterogeneous capture
conditions, and probabilistic semantic segmentation behavior from AI
masking tools.

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
that remains batch-safe under real tooling limitations, heterogeneous
creative input data, and AI-assisted operations with partial,
non-binary failure modes.

## Solution Overview

The workflow addresses that problem through three documented stages:

1. Metadata ingestion, enrichment, and query design
2. Baseline conditioning and rollback
3. Bulk AI mask definition propagation

Each stage isolates a specific class of transformations, defines clear
inputs and outputs, and introduces validation boundaries before later
operations are applied. The result is a workflow that is more
deterministic, easier to reason about, and safer to evolve over time.

The stages build a reliability layer around increasingly uncertain
workflow surfaces: Stage 1 establishes deterministic metadata state,
Stage 2 controls visual variance introduced by capture conditions, and
Stage 3 constrains probabilistic AI mask outputs through qualification,
bounded propagation, and human review.

In Stages 2 and 3, batch execution does not imply a single static
transformation applied uniformly across every file. Both stages operate
at dataset scale while still producing image-specific results at
runtime: normalization responds to the conditions of each image, and AI
mask propagation generates semantic selections whose effective impact
varies by image content.

## Unit Economics of Batchability

A single deliverable image can require many mandatory corrections before
it is ready for final review. Some corrections are mandatory only when a
specific condition is present, such as dust, tilted framing, weak
luminance, foliage hue drift, or a semantic region that needs local
editing. The pipeline value comes from identifying which subset of those
mandatory corrections can be safely batch-enabled, which require
qualification first, and which must remain manual.

Representative correction categories include:

- **Local defects:** dust/distraction removal
- **Geometry:** straightening and crop decisions
- **Recovery:** AI-assisted recovery for borderline focus/noise cases when the image is otherwise worth keeping
- **Global visual baseline:** luminance and tonal adjustment
- **Scene-level visual baseline:** hue and color normalization within comparable scenes
- **Semantic local edits:** people, foliage, sky, background, foreground, or ground masks
- **Final artistic review:** manual refinement, crop finalization, and subjective delivery choices

The workflow treats each correction as a candidate operation:

```text
Candidate image
      ↓
Cull for focus, relevance, aesthetic uniqueness, and edit potential
      ↓
For each mandatory correction:
      ↓
Is the correction present?
      ├── no  → skip
      └── yes
           ↓
      Is it batch-safe?
      ├── yes → batch operation candidate
      └── no
           ↓
      Can it be qualified on a representative subset?
      ├── yes → qualify, then promote if reliable
      └── no  → keep as manual refinement
```

Stage 2 focuses on corrections that can establish a reliable baseline
before creative edits: cleanup, luminance normalization, scene-level
color normalization, and rollback-safe branching. Stage 3 focuses on
semantic operations whose behavior depends on probabilistic AI
segmentation and therefore requires qualification, propagation
boundaries, and human review.

## Key Constraints

Across the documented stages, the shared engineering constraints and
design themes are:

- deterministic, stage-bounded workflow design
- batch-safe operations under tooling constraints
- deterministic orchestration around heterogeneous creative inputs
- bounded handling of probabilistic AI outputs
- reproducibility through clear validation checkpoints
- structured automation with human review at defined boundaries


## Pipeline Stages

The project is organized as a single multi-stage pipeline with supporting documentation for each major stage.

Stage 1 establishes the metadata and query foundation for the workflow.

- **Identity initialization:** Single-preset ingest establishes the protected authorship baseline
- **Semantic enrichment:** Post-import presets and keywords add non-overlapping descriptive metadata
- **Query layer:** Filter-based retrieval and Smart Collections derive reusable views over image records

After Stage 1, the image set is culled before image-processing
transformations begin. Culling selects the working set that should move
forward based on review criteria such as usable focus, aesthetic
uniqueness, subject relevance, and edit potential.

Stages 2 and 3 then form the image-processing portion of the pipeline, which currently follows this progression:

- **Culling boundary:** Review selects the usable working set after metadata ingest
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
- stable metadata state before subjective culling or image transformation begins

### 2. Baseline Conditioning and Rollback Pipeline
Location: [Stage 2](pipeline_stages/002_baseline-conditioning-and-rollback/README.md)

- local corrective cleanup and dataset-wide luminance normalization across heterogeneous images
- scene-level color normalization that preserves natural hue differences across scenes
- virtual copies for rollbackable experimentation while reducing operator cognitive load
- deterministic conditioning around creative/capture variance from changing light, scene, and camera conditions

### 3. Bulk AI Mask Definition Propagation 
Location: [Stage 3](pipeline_stages/003_bulk-ai-mask-definition-propagation/README.md)

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of AI-generated semantic masks to batch edit operations
- qualitative evaluation of mask quality and workflow reliability against manual editing results
- deterministic review boundaries around probabilistic AI segmentation behavior
