# Case Study: Bulk AI Masking Batch Rebinding Experiment

## Status

Planned case study under the Creative Workflow Batch Transformation Pipeline umbrella project.

## Proposed Focus

This case study will evaluate whether AI-generated semantic masks can be treated as reusable batch artifacts that are rebound to downstream edit operations at scale.

## Core Questions

- How should mask generation outputs be represented so they can be rebound safely in batch workflows?
- Which parts of the workflow are deterministic enough for automation, and which require operator review?
- What failure modes emerge when masks are reused across scenes, subjects, or lighting conditions?
- How should confidence thresholds, rollback paths, and validation checkpoints be designed?

## Planned Sections

- Problem Statement
- Constraints and Assumptions
- System Architecture
- Batch Rebinding Flow
- Failure Modes and Recovery Strategy
- Validation Methodology
- Results and Tradeoffs

## Planned Assets

- `assets/diagrams/mask-rebinding-flow.png`
- `assets/diagrams/validation-gates.png`
- `assets/images/example-mask-overlays.png`



----

## Deep Dive

Bulk AI Mask Definition Propagation

Core concepts:

• Define mask logic once → apply across an entire dataset
• AI segmentation dynamically recomputes masks per image (people, sky, vegetation)
• Mask operations remain fault-tolerant when objects are missing


Experiment Objectives
	1.	Mechanism Verification
Confirm that Lightroom copies procedural mask definitions and recomputes semantic segmentation per image.
	2.	Qualitative Performance Assessment
Evaluate how closely batch-generated masks match the results of manual per-image masking in terms of boundary accuracy and subject detection.

Evaluation Criteria
	•	Boundary accuracy — how closely the generated mask boundaries align with the intended subject regions
	•	Subject detection completeness — whether relevant subjects (e.g., people, sky, foliage) are correctly detected and masked
	•	Failure modes — cases where masks are omitted, misaligned, or incorrectly applied



Canonical Image Selection
From a culled gallery, a single canonical image was selected.

A canonical image is defined as a photo containing a large number of semantic subject categories, including:
	•	multiple identifiable people
	•	foliage / vegetation
	•	sky
	•	background environmental regions

Selecting such an image ensures that the maximum number of mask types can be generated and tested during the batch operation.



Mask Definition Phase
On the canonical image, masks were created manually for each detected category.

The canonical image generated 7 total masks, representing different semantic regions within the scene.

These masks serve as the procedural mask definitions used for the batch experiment.

Importantly, Lightroom stores these masks as instructions describing how to detect and adjust regions, rather than static pixel selections.


Batch Mask Application
Only the mask definitions from the canonical image were copied.

These mask definitions were then pasted across all images in the gallery, without regard to whether the same semantic categories existed in each image.

Examples of variation within the dataset include:
	•	images containing fewer people than the canonical image
	•	images containing sky but no foliage
	•	images containing foliage but no sky
	•	images containing entirely different individuals

No per-image adjustments were made prior to the batch paste operation.

Expected Computational Workload
The canonical image produced: 7 masks

Applied across: 64 images

This yields a theoretical maximum of: 7 × 64 = 448 mask recomputation operations

The People and Environmental Mask Aggregates were not batch applied, they were only manually generated to properly highlight the semantic regions that were to be batch applied.

Observed System Behavior
During the paste operation, Lightroom displayed the progress indicator: `Updating AI Settings`

This stage represents the batch execution of semantic segmentation models across the selected images.

Rather than copying mask pixels directly, Lightroom performs the following process for each image:
mask_definition → semantic segmentation → region binding

This dynamically recomputes the mask boundaries based on the visual content of the target image.

Fault-Tolerant Mask Binding
When a mask definition does not correspond to a detectable region in a target image (for example, when fewer people are present), Lightroom does not generate that mask.

Instead, the mask operation is silently omitted for that image.

This results in:
	•	successful mask application where semantic regions exist
	•	automatic omission where they do not

This behavior demonstrates fault-tolerant mask generation, preventing erroneous mask application when a semantic category is absent.

Result
Only a subset of the theoretical 448 mask operations were generated.

The final mask set applied to each image depended entirely on the semantic content of that image, confirming that Lightroom’s masking pipeline copies procedural mask definitions and recomputes them per image using AI-driven segmentation.

