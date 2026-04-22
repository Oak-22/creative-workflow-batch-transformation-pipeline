# Shared Terminology

These terms appear across the project. Stage-specific documents may define narrower terms closer to the
operation where they are used.

## Pipeline Concepts

### Issue

A recurring workflow need that creates manual effort, such as a metadata
task, visual defect, variance problem, semantic region, exception case,
or editorial decision that must be handled before the image set can move
forward.

### Deterministic Orchestration

A workflow design pattern that makes the order of operations, inputs,
outputs, validation points, and rollback boundaries explicit, even when
the underlying data or tool behavior is variable.

### Uncertain Inputs

Inputs whose exact state or behavior cannot be fully predicted before
runtime. In this project, the main uncertain inputs are image variance
from changing capture conditions at source and AI-generated semantic masks whose
quality depends on image content.

### Stage Boundary

A deliberate handoff point between workflow phases. Each stage has a
clear responsibility, expected input state, output state, and validation
role before later operations depend on it.

### Validation Checkpoint

A review point used to decide whether a transformed working set is safe
to carry forward. Validation can include metadata inspection, visual
review, before/after comparison, or mask-quality review.

### Batch-Safe Operation

An operation that can be applied across many images with predictable
enough behavior that it reduces manual work without creating excessive
cleanup. Batch-safe does not mean every image receives the same exact
runtime adjustment.

### Rollback Safety

The ability to return to a known-good prior state without discarding
valuable completed work. In this project, rollback safety is supported
by stage boundaries and non-destructive edit branches.

## Image Workflow Concepts

### Dataset

A complete collection of images from a single photoshoot or capture
session.

### Culling

The review step where the full capture set is narrowed to images worth
carrying forward based on focus, subject relevance, aesthetic value, and
edit potential.

### Conditioning

A broader preparation step that makes a working set safer and more
consistent for downstream operations. Conditioning may include cleanup,
normalization, reviewed edit operations, and rollback setup.

### Normalization

A specific kind of conditioning that reduces unwanted variance across
images by bringing luminance, tone, or color into a more comparable
operating range. In this workflow, normalization preserves meaningful
scene differences rather than forcing all images into one identical
look.

### Virtual Copy

A non-destructive derived edit state that preserves an independent edit
timeline while referencing the same underlying source image.

## Metadata And AI Concepts

### Metadata Application

The process of writing ownership, authorship, classification, or
descriptive fields onto image records. In Stage 1, identity metadata is
applied during ingest, while semantic enrichment is applied after
import.

### Smart Collection

A saved Lightroom query over metadata and image attributes. In this
project, Smart Collections are treated like declarative views over image
records.

### Semantic Region

An image area identified by meaning rather than manual pixel
coordinates, such as a person, sky, foliage, foreground, background, or
ground.

### AI Mask Definition

A procedural instruction used by Lightroom to detect and adjust a
semantic region. When propagated to another image, the definition is
recomputed against that image instead of copying fixed pixels.

### Semantic Segmentation

An AI-driven image analysis process that divides an image into
meaningful regions or object classes. In this project, segmentation
output is useful but probabilistic, so it requires qualification and
human review.
