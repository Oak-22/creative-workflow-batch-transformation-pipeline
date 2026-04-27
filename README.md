# Creative Workflow Batch Transformation Pipeline

Systems engineering project showing how ambiguous, ad hoc creative production workflows can be structured as deterministic, scalable pipelines.  

<br>

## Executive Summary

Creative production work is modeled as a reproducible, multi-stage
pipeline with explicit boundaries, non-destructive state
transitions, and validation checkpoints. Even when executed inside
GUI-based tools, the workflow is designed with production system qualities rather
than an ad hoc editing sequence.

The core engineering pattern is deterministic orchestration around
uncertain inputs: creative image variance from heterogeneous capture
conditions, and probabilistic semantic segmentation behavior from AI
masking tools.

Across the documented stages, the project demonstrates how ingest-time
metadata application, image normalization, and semantic masking can be
composed into a deterministic workflow that scales more reliably than
repeated manual editing.

<br>

## TL;DR

Use these entry points to inspect specific aspects of the project:

- [Pipeline Overview Diagram](docs/creative-workflow-pipeline-overview-diagram.png) shows the full pipeline structure.
- [Shared terminology](docs/terminology.md) defines recurring systems and image-workflow language.
- [Batchability Cost Model](docs/batchability-cost-model.md) explains the operational value model.

<br>

## Project Structure

The project is structured as two parts:

`a) Workflow System Design`
- **Stage prose:** primary system-design artifact
- **Workflow evidence:** visual and operational proof carried by the documented stages

`b) Scripting to validate Design in Operation`
- **Scripts/tests:** validation and reproducibility support

This pipeline is **Not a packaged application:**. It augments an existing application (Adobe Lightroom)

<br>

## Evidence Model

The repository uses two equally important evidence modes that align with
the project structure above. Together they explain both the system
design and its runnable operation.

- **A) Workflow System Design Evidence:** the stage prose, workflow
  image evidence, workflow operational evidence, and any stage-specific
  experiments are used to explain why specific pipeline boundaries,
  validation steps, review points, and design patterns exist. In the
  stage documents, this evidence typically appears as explicit
  `Operational note:` callouts or as `Figure` sections with embedded
  images.
- **B) Runnable Script/Test Evidence:** scripts, tests, and sample-data
  execution support that make the pipeline operable, inspectable, and
  reproducible in practice rather than only described in prose.


<br>

## Problem

Creative production workflows often accumulate as several informal editing
habits inside GUI tools, making them hard to reproduce, audit, and
scale across large datasets. Without explicit stage boundaries and
validation checkpoints, small inconsistencies can compound into operator drift causing laborous rework. Weak rollback safety then makes those inconsistencies
more costly to contain once they spread through the working set.

The core systems problem is therefore not only how to optimally perform isolated
editing operations, but how to organize them into a stable pipeline
that remains batch-safe under real tooling limitations, heterogeneous
creative input data, and AI-assisted operations with partial,
non-binary failure modes.

<br>

## Solution Overview

The workflow addresses that problem through three documented stages:

1. Metadata application, enrichment, and query design
2. Baseline conditioning
3. AI mask definition propagation

Each stage isolates a specific class of transformations, defines clear
inputs and outputs, and introduces validation boundaries before later
operations are applied. The result is a workflow that is more
deterministic, easier to reason about, and safer to evolve over time.

The stages build a reliability layer around increasingly uncertain
workflow surfaces: Stage 1 establishes deterministic metadata state,
Stage 2 controls visual variance introduced by capture conditions, and
Stage 3 constrains probabilistic AI mask outputs through qualification,
bounded propagation, and human review.

In Stages 2 and 3, batch application does not imply a single static
transformation applied uniformly across every file. Both stages operate
at dataset scale while still producing image-specific results at
runtime: baseline conditioning responds to the state of each image; AI mask propagation generates semantic selections whose effective impact varies by image content.

<br>

## Operational Value

The pipeline is designed around a batchability cost model: identifying
which mandatory issues can be immediately handled through batch application, which
must be qualified first before batch, and which should remain manual.

See the [Batchability Cost Model](docs/batchability-cost-model.md)
for the issue/edit model and resulting back-of-envelope time-savings framework as 
the defining business benefit to the pipeline.

<br>

## Key Constraints

Across the documented stages, the shared engineering constraints and
design themes are:

- stage-bounded workflow design
- deterministic orchestration around heterogeneous creative inputs
- batch-safe operations under tooling constraints
- bounded handling of probabilistic outputs
- reproducibility through clear validation checkpoints
- human review at defined boundaries

<br>

## Pipeline Stages

The project is organized as a single multi-stage pipeline with supporting documentation for each major stage.

<br>

### Stage 1 – Metadata Application, Enrichment, and Query Pipeline
Location: [Stage 1](pipeline_stages/001_metadata-application-enrichment-query-pipeline/README.md)

Establishes the metadata and query foundation for the workflow.

- **Identity initialization:** Single-preset ingest establishes the protected authorship baseline
- **Semantic enrichment:** Post-import presets and keywords add non-overlapping descriptive metadata
- **Query layer:** Filter-based retrieval and Smart Collections derive reusable views over image records

Focus areas:
- deterministic ingest behavior under single-preset constraints
- non-destructive metadata enrichment through non-overlapping field assignments
- metadata-driven indexing and retrieval patterns enabling both rapid ad-hoc queries and declarative views over image records
- stable metadata state before subjective culling or image transformation begins

> **Boundary:** culling separates metadata preparation from image
> transformation.
>
> **Handoff state:** the full image set is narrowed into the working
> set that moves forward to cleanup, normalization, and AI mask
> propagation. Selection is based on usable focus, aesthetic
> uniqueness, subject relevance, and edit potential.

<br>

### Stage 2 – Baseline Conditioning Pipeline
Location: [Stage 2](pipeline_stages/002_baseline-conditioning-pipeline/README.md)

Establishes the conditioned image baseline for downstream semantic
operations.

The Stage 2 flow is:

1. **Input lineage boundary:** Initial virtual-copy branching protects
   the culled working set from the original RAW selection.
2. **Operation 1:** Local corrective cleanup.
3. **Boundary:** operator review separates cleanup from cleaned
   baseline inputs.
4. **Operation 2:** Dataset-wide luminance normalization with
   scene-level color normalization.
5. **Boundary:** review checkpoint separates normalization from
   normalized baseline images.
6. **Output lineage boundary:** Post-conditioning virtual-copy
   branching preserves the normalized baseline as a known-good handoff
   state.

Focus areas:
- local corrective cleanup and dataset-wide luminance normalization across heterogeneous images
- scene-level color normalization that preserves natural hue differences across scenes
- virtual copies for rollbackable experimentation while reducing operator cognitive load
- deterministic conditioning around creative/capture variance from changing light, scene, and camera conditions

> **Handoff state:** Stage 3 receives a cleaned, normalized, and
> lineage-protected working state rather than unresolved luminance and
> color variance.

<br>

### Stage 3 – AI Mask Definition Propagation
Location: [Stage 3](pipeline_stages/003_ai-mask-definition-propagation/README.md)

Applies semantic mask definitions across the conditioned working set and
introduces bounded review around probabilistic AI output.

- **Semantic operations:** Batch AI masking
- **Qualification boundary:** Semantic definitions are qualified before broad propagation
- **Human review:** Manual refinement pass

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of AI-generated semantic masks to batch edit operations
- qualitative evaluation of mask quality and workflow reliability against manual editing results
- deterministic review boundaries around probabilistic AI segmentation behavior

<br>
