# Creative Workflow Batch Transformation Pipeline

Systems engineering project showing how creative-production workflows can be structured as deterministic, scalable pipelines rather than ad hoc editing sequences.

<br>

## Project Structure

The project is structured as a workflow system design rather than a
standalone software package.

- **Stage prose:** primary system-design artifact
- **Scripts/tests:** supplementary validation and reproducibility support
- **Workflow evidence:** visual and operational proof carried by the documented stages
- **Not a packaged application:** expectation-setting for how to read the repository

<br>

## Evidence Model

The repository uses multiple evidence modes to explain the workflow.
These materials are not presented as controlled benchmarks; they are
used to explain why specific pipeline boundaries, validation steps,
review points, and design patterns exist.

- **Workflow Image Evidence:** visual evidence drawn from the workflow
  itself, such as Lightroom panels, before/after comparisons, lineage
  views, masks, taxonomy screenshots, and other observable system
  states.
- **Workflow Operational Evidence:** experience-derived notes from
  actually running the workflow in practice. These observations capture
  friction, exceptions, decision boundaries, tool behavior, and other
  operational nuances that are not always visible from images alone.
- **Stage-specific experiments:** narrower exploratory tests used when a
  stage benefits from a focused comparison or qualification exercise.
- **Scripts/tests:** supplementary validation and reproducibility
  support.

Stage documents define any stage-specific evidence framing near the
operations where that evidence is used.

<br>

## TL;DR

Use these entry points to inspect specific aspects of the project:

- [Shared terminology](docs/terminology.md) defines recurring systems and image-workflow language.
- [Batchability Cost Model](docs/batchability-cost-model.md) explains the operational value model.
- [Pipeline Overview Diagram](docs/creative-workflow-pipeline-overview-diagram.png) shows the full pipeline structure.

<br>

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

Across the documented stages, the project demonstrates how ingest-time
metadata application, image normalization, and semantic batch editing can be
composed into a deterministic workflow that scales more reliably than
repeated manual editing.

<br>

## Problem

Creative-production workflows often accumulate as several informal editing
habits inside GUI tools, making them hard to reproduce, audit, and
scale across large datasets. Without explicit stage boundaries and
validation checkpoints, small inconsistencies can compound into rework
and operator drift. Weak rollback safety then makes those inconsistencies
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
runtime: baseline conditioning responds to the state of each image,
while normalization specifically aligns luminance and scene-level color
where appropriate; AI mask propagation generates semantic selections
whose effective impact varies by image content.

<br>

## Operational Value

The pipeline is designed around a batchability cost model: identifying
which mandatory issues can be immediately handled through batch application, which
must be qualified first before batch, and which should remain manual.

See the [Batchability Cost Model](docs/batchability-cost-model.md)
for the issue/edit model and back-of-envelope time-savings framework
across the three stages.

<br>

## Key Constraints

Across the documented stages, the shared engineering constraints and
design themes are:

- deterministic, stage-bounded workflow design
- batch-safe operations under tooling constraints
- deterministic orchestration around heterogeneous creative inputs
- bounded handling of probabilistic AI outputs
- reproducibility through clear validation checkpoints
- structured automation with human review at defined boundaries

<br>

## Pipeline Stages

The project is organized as a single multi-stage pipeline with supporting documentation for each major stage.

<br>

### Stage 1
Establishes the metadata and query foundation for the workflow.

- **Identity initialization:** Single-preset ingest establishes the protected authorship baseline
- **Semantic enrichment:** Post-import presets and keywords add non-overlapping descriptive metadata
- **Query layer:** Filter-based retrieval and Smart Collections derive reusable views over image records

> **Pipeline boundary:** culling separates metadata preparation from
> image transformation.
>
> After Stage 1, the full image set is narrowed into the working set
> that moves forward to cleanup, normalization, and AI mask propagation.
> Selection is based on usable focus, aesthetic uniqueness, subject
> relevance, and edit potential.

<br>

### Stages 2 & 3
Forms the image-processing portion of the pipeline, which currently follows this progression:

- **Culling boundary:** Review selects the usable working set after ingest-time metadata application
- **Preprocessing:** Local corrective cleaning
- **Normalization:** Dataset-wide luminance standardization with scene-level color normalization
- **Semantic operations:** Batch AI masking
- **Human review:** Manual refinement pass

<br>

## Stage Details

<br>

### 1. Metadata Application, Enrichment, and Query Pipeline
Location: [Stage 1](pipeline_stages/001_metadata-application-enrichment-query-pipeline/README.md)

Focus areas:
- deterministic ingest behavior under single-preset constraints
- non-destructive metadata enrichment through non-overlapping field assignments
- metadata-driven indexing and retrieval patterns enabling both rapid ad-hoc queries and declarative views over image records
- stable metadata state before subjective culling or image transformation begins

<br>

### 2. Baseline Conditioning Pipeline
Location: [Stage 2](pipeline_stages/002_baseline-conditioning-pipeline/README.md)

- local corrective cleanup and dataset-wide luminance normalization across heterogeneous images
- scene-level color normalization that preserves natural hue differences across scenes
- virtual copies for rollbackable experimentation while reducing operator cognitive load
- deterministic conditioning around creative/capture variance from changing light, scene, and camera conditions

<br>

### 3. AI Mask Definition Propagation
Location: [Stage 3](pipeline_stages/003_ai-mask-definition-propagation/README.md)

Focus areas:
- procedural mask definitions propagated across datasets rather than copying pixel regions
- dataset-scale application of AI-generated semantic masks to batch edit operations
- qualitative evaluation of mask quality and workflow reliability against manual editing results
- deterministic review boundaries around probabilistic AI segmentation behavior
