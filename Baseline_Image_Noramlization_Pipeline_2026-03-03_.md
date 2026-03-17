Author: Julian Buccat<br/> 
Date: 2026-02-26<br/>
Category: Systems Design Case Study<br/>
Domain: Image Processing Pipeline

# Case Study: Designing a Baseline Image Normalization Pipeline for Heterogeneous Input Distributions

## Executive Summary

High-volume photo datasets captured over long time horizons (several hours) often contain significant lighting variance across scenes. Even when the subject matter remains similar, changing sunlight conditions alter how the camera sensor captures both color and brightness information.

These lighting differences change the [visual tone](#visual-tone) of an image—the overall balance of brightness, contrast, and color that shapes both the technical appearance of the image and the emotional perception of the viewer. For example, a couple photographed in strong midday sunlight may exhibit **warmer color tones and higher contrast** (technical attributes), which viewers often interpret as **vibrant and energetic** (emotional perception). The same couple photographed in shaded late‑afternoon light may exhibit **cooler tones and softer contrast**, which viewers often interpret as **calmer or more subdued** in mood.

Without normalization, these differences cause a [dataset](#dataset) of otherwise related photos to feel visually inconsistent.

[INSERT 2 image sets: Marina and Angel + unedited juan and nicole]

This case study describes a three-stage normalization pipeline that combines global luminance normalization, AI-assisted semantic segmentation, and exemplar-based canonical color calibration to establish an automated, consistent visual baseline across the dataset.

- **Goal:** Establish a consistent visual baseline while preserving natural scene variation.
- **Stage 1:** Global luminance normalization ([automated tonal analysis](#automated-tonal-analysis)) → Normalize input distribution (transforms luminance distribution, variance ↓) (feature scaling / normalization)
- **Stage 2:** AI-assisted semantic segmentation → Generate indexed features (semantic masks as queryable regions; metadata only, no state mutation) (feature extraction / indexing)
- **Stage 3:** [Exemplar](#exemplar-image)-based canonical color calibration → Apply deterministic transformations using reference mappings (transforms color distribution, variance ↓) (deterministic transformation)

- **Value:** The pipeline reduces two core pain points: (1) total image editing time and (2) cognitive load, by eliminating the need for continuous cross-image comparison during manual adjustments after baseline normalization.

## Pipeline Value - In depth

Stage 1 establishes a consistent luminance baseline across the [dataset](#dataset) through automated global normalization. This aligns exposure and tonal distribution so that each image begins from a comparable brightness and contrast profile before further corrections are applied.

Without this baseline, later color corrections interact differently with each image because their underlying luminance distributions vary. The same adjustment can therefore produce inconsistent results across scenes.

# Conceptual example (vegetation color calibration):

Raw foliage pixel values:

A — Underexposed foliage(no stage 1):      (0, 0, 0)
B — Properly exposed foliage (post-Stage 1):  (98, 68, 80)

Desired calibrated foliage tone:

If stage 3 calibration is applied directly:

A → large correction required → unstable / inaccurate result
B → small correction required → stable result

Stage 1 reduces this disparity by normalizing luminance first. Once tonal distributions are aligned, Stage 3 color adjustments operate on comparable input ranges and therefore produce consistent results across the dataset.

---

Stage 2 precomputes semantic masks to accelerate localized edits. Frequently used masks (such as skin, hair, clothing, and sky/ground) are generated automatically across the dataset. This eliminates the need to manually compute masks per image during editing, reducing repetitive actions and improving editing throughput.

---

Stage 3 applies [exemplar](#exemplar-image)-driven batch adjustments (e.g., foliage, clothing, and skin tones) to achieve gallery-wide visual coherence. Key visual domains should remain perceptually consistent across the [dataset](#dataset) even as lighting conditions change throughout the shoot. For example, a subject with tan skin should retain that tone across images rather than appearing significantly lighter or darker due to exposure and color shifts. Exemplar calibration prevents these artifacts by defining a canonical reference for each domain and propagating that correction across the dataset.

---

## Pipeline Diagrams

The following simplified diagrams illustrate the three pipeline stages described in this case study. Each stage progressively reduces variance while preserving scene‑level differences.

### Stage 1 — Global Luminance Normalization

```text
RAW Images (dataset)
      ↓
Global Luminance Normalization
(automated tonal analysis)
      ↓
Normalized Baseline Images
(reduced luminance variance)
```



---

### Stage 2 — AI Semantic Segmentation

```text
Normalized Images
      ↓
AI Segmentation Model
      ↓
Semantic Masks Generated

Example masks:

[ Facial Skin ]
[ Body Skin   ]
[ Eye Sclera  ]
[ Hair        ]
[ Clothing    ]
```

These masks act as **precomputed metadata** attached to each image and enable fast, localized transformations during editing.

---

### Stage 3 — Exemplar‑Based Canonical Color Calibration

This stage defines canonical color adjustments using a representative image and propagates those adjustments across the dataset.

```text
Representative Exemplar Image
        ↓
Manual Canonical Calibration
        ↓
Reference Transform Defined
        ↓
Applied via Stage 2 Semantic Masks
        ↓
Scene Image A   Scene Image B   Scene Image C
        ↓            ↓            ↓
Calibrated Output A  Calibrated Output B  Calibrated Output C
```

The [exemplar image](#exemplar-image) acts as a **reference transformation**. Adjustments derived from this representative image are batch‑applied using the semantic masks generated in Stage 2.

This approach maintains consistent foliage, clothing, and skin tone rendering across the dataset while preserving natural [scene](#scene) variation.

---

## Terminology

To clarify domain-specific language used throughout this case study, the following system concepts are defined:

### Dataset & Structural Concepts

<a id="dataset"></a>
- **Dataset:** A complete collection of images from a single photoshoot or capture session.

<a id="scene"></a>
- **Scene:** A distinct composition within the dataset defined by a particular foreground, subject, and background configuration. A single dataset typically contains multiple scenes.

### Perceptual Characteristics

<a id="visual-tone"></a>
- **Visual Tone:** The combined luminance, contrast, and color characteristics of an image that determine its perceived brightness, warmth/coolness, and overall visual consistency.

### Luminance Transformation Primitives

<a id="exposure"></a>
- **Exposure:** A global adjustment controlling overall image brightness by shifting the luminance distribution uniformly across all pixels.

<a id="contrast"></a>
- **Contrast:** A global adjustment controlling the separation between light and dark regions in an image, increasing or decreasing the intensity difference across the luminance distribution.

<a id="highlights-whites"></a>
- **Highlights / Whites:** Upper-range luminance regions of an image. *Highlights* refer to near-bright regions with recoverable detail, while *whites* represent the brightest values approaching clipping. Adjustments to these regions control brightness and detail retention in the upper portion of the luminance distribution.

<a id="shadows-blacks"></a>
- **Shadows / Blacks:** Lower-range luminance regions of an image. *Shadows* refer to darker regions with recoverable detail, while *blacks* represent the darkest values approaching clipping. Adjustments to these regions control detail visibility and depth in the lower portion of the luminance distribution.

<a id="clipping"></a>
- **Clipping:** Loss of recoverable image detail in highlights or shadows due to sensor saturation or underexposure, where pixel values are driven to their minimum or maximum limits and no additional tonal information can be retrieved.

### Pipeline Concepts

<a id="automated-tonal-analysis"></a>
- **Automated Tonal Analysis:** A global normalization step that analyzes image luminance distribution and applies coordinated adjustments to exposure, highlights/whites, shadows/blacks, and contrast in order to reduce inter-image luminance variance prior to downstream transformations.

<a id="exemplar-image"></a>
- **Exemplar Image:** A representative high-signal image selected from a scene or domain (e.g., foliage, clothing, or skin tones) used to define canonical adjustments that can be batch-applied across the dataset.

## Domain Background: RAW Capture and Signal Variance

Digital cameras typically offer two capture formats: **JPEG** and **RAW**. JPEG images are processed in‑camera using built‑in normalization, color profiles, and compression. While this produces visually pleasing images immediately, it also locks in tonal decisions made by the camera firmware and reduces the flexibility of downstream editing.

In contrast, **RAW images preserve the camera sensor's unnormalized luminance and color distribution**. This retains the full dynamic range of the captured signal and defers tonal interpretation to the post‑processing pipeline.

RAW capture therefore increases [dataset](#dataset) variance but enables **controlled, user‑defined normalization during post‑processing**, which motivates the normalization pipeline described in this case study.

Shooting in RAW is a deliberate decision because it preserves recoverable signal that would otherwise be lost in JPEG. RAW files retain significantly more highlight and shadow information from the sensor, allowing the editor to recover details from images that might initially appear unusable. For example, a frame with blown highlights or deep shadows can often be salvaged by recovering clipped highlight detail or lifting shadow information. In contrast, JPEG compression discards much of this recoverable signal and locks the image into a specific tone curve and color profile, making such recovery far more limited.

This background context explains why RAW datasets exhibit higher variance and why a normalization stage becomes necessary before consistent batch edits can be applied.

---

## Problem

Large photo sets captured across multiple lighting environments introduce
high variance in [visual attributes](#visual-tone). The pipeline must handle diverse
conditions and scale across datasets without introducing inconsistency.

Example capture conditions include:

- midday direct sunlight
- shaded environments
- late-afternoon or evening lighting

These conditions introduce variance in:

- exposure
- contrast
- color temperature
- vegetation and environmental tones
- skin tone rendering

A naive global editing strategy (e.g., applying identical exposure
adjustments across all images) yields inconsistent results. The same
parameter change interacts differently with each scene.

Example: vegetation color grading becomes difficult when exposure varies
across time-of-day conditions. Foliage shot in shaded evening light may
render a different hue than foliage in strong midday sun. Identical
adjustments therefore produce divergent effects.

The workflow goals are:

- establish a consistent visual baseline across the dataset
- preserve natural [scene](#scene) differences (e.g., time-of-day mood)
- minimize manual editing effort
- avoid repeated global transformations across the editing pipeline

Importantly, the pipeline does **not** eliminate all variation between images. Lighting differences across [scenes](#scene) (e.g., midday sun vs shaded evening light) still produce natural mood differences. The normalization stages instead constrain variance to a controlled range, ensuring that images remain visually related while still preserving authentic [scene](#scene) characteristics such as time‑of‑day lighting and environmental context.
---

## Initial Approach (Multi-Stage Global Presets)

The original workflow attempted multiple preset layers across the dataset:

```text
Import preset
→ secondary editing preset
→ additional correction preset
```

This introduced several issues:

- repeated global edits across the dataset
- increased pipeline complexity
- difficulty maintaining a consistent baseline
- additional manual intervention per image

The pipeline effectively introduced multiple global transformation stages,
increasing the risk of inconsistent results.

---

## Architecture

The pipeline collapses multiple global transformations into a single
deterministic normalization stage followed by localized corrections.

### Pipeline Overview

```text
RAW Images (dataset)
      ↓
Stage 1: Global luminance normalization
(automated tonal analysis)
      ↓
Stage 2: Semantic segmentation
(AI-generated masks as reusable metadata)
      ↓
Stage 3: Exemplar-based canonical color calibration
(region-scoped, reference-based transformations)
      ↓
Consistent dataset baseline with preserved scene variation
```

### Stage 1: Global Normalization

The first stage uses automated tonal analysis to normalize luminance and
contrast. It reduces dataset variance and establishes a common starting
state for all images.

This stage adjusts:

- [exposure](#exposure)
- [contrast](#contrast)
- [highlights / whites](#highlights-whites)
- [shadows / blacks](#shadows-blacks)

This is conceptually similar to feature scaling and histogram
normalization in data pipelines. The goal is not perfect grading per
image but a reduced variance baseline for downstream processing.



This stage reduces large luminance variance across the dataset so that downstream corrections behave predictably. Without this normalization step, later adjustments (such as color grading for foliage or human skin tones) interact inconsistently with each image because their underlying exposure and tonal distributions differ. *As a result, identical parameter changes can produce divergent outcomes across scenes.*

In practice, editors attempting to correct this manually are forced into a continuous cycle of per-image adjustments and cross-image comparison. They must repeatedly zoom into individual images to fine-tune exposure and tonal values, then zoom out to evaluate consistency across the broader dataset. This constant context switching introduces cognitive fatigue and increases the likelihood of drift from both scene-level and gallery-level consistency. 

By establishing a consistent luminance baseline upfront, the pipeline removes this instability. Subsequent adjustments operate on comparable tonal distributions, enabling batch edits and exemplar-based corrections to produce stable, repeatable results across the dataset without continuous manual recalibration.

**Outcome:**
- reduced luminance variance across the dataset
- predictable downstream transformations
- significant reduction in repeated per-image exposure correction (residual adjustments may still be required in edge cases)

### Stage 2: Semantic Segmentation (AI Mask Generation)

After normalization, the pipeline generates automated semantic masks. The
masks identify semantically defined regions within each image for targeted, region-aware corrections.

Detected regions include semantic classes such as:

- facial skin
- body skin
- eye sclera
- hair
- clothing
- background
- ground
- sky

**Outcome:**

- **Editing acceleration:** Precomputed masks remove per-image masking
  work and speed up localized edits.
- **Region-scoped transformations:** Masks enable targeted corrections without altering unrelated areas.

### Stage 3: Exemplar‑Based Canonical Color Calibration

After global normalization and mask generation, the pipeline introduces a third stage that establishes canonical color references for key visual domains within the dataset.

Rather than manually adjusting each key visual domain per image, the workflow selects **one high‑signal [exemplar image](#exemplar-image) per domain**. An [exemplar image](#exemplar-image) is defined as a single frame with strong lighting information and minimal [clipping](#clipping), providing sufficient tonal signal to define reliable adjustments.

Typical calibration domains include:

- vegetation / foliage tones
- clothing tones
- human skin tones

The editor performs controlled adjustments on the exemplar image to establish the **canonical look** for that domain. These calibrated adjustments are then batch‑applied across the dataset using the masks generated in Stage 2.

This approach creates **region-scoped normalization using globally consistent, exemplar-derived transformations**:

- edits remain globally consistent across the dataset
- corrections are constrained to semantically relevant regions
- natural scene variation is preserved

**Outcome:**
- consistent domain-specific appearance across the dataset (e.g., foliage, skin tones, clothing)
- deterministic, repeatable transformations derived from exemplar references
- reduced need for per-image manual color correction

**Engineering Analogy:**
This stage functions as a reference-based transformation system. Instead of computing adjustments independently per image, the pipeline derives corrections from representative exemplar frames and applies them deterministically across the dataset. Unlike Stage 1 global normalization, which operates on entire-image luminance distributions, this stage applies uniform transformations within semantically segmented regions only.

---


## System Constraints & Scale Considerations

The current implementation is designed as a **local, editor-in-the-loop batch pipeline** operating within Lightroom Desktop / Classic rather than as a cloud-native or distributed image-processing system. RAW files, semantic masks, and downstream edits are managed within a local catalog-centered workflow optimized for a single operator performing interactive review and refinement.

This design favors **editing throughput, controllability, and local responsiveness** over distributed scalability. Stage 1 and Stage 2 are primarily preprocessing operations that establish a normalized baseline and generate reusable metadata, while Stage 3 remains partially manual because exemplar selection and canonical color decisions still depend on editorial judgment.

In practical terms, the pipeline is intended to scale across **hundreds of RAW images per dataset**, not to serve as a real-time or horizontally distributed processing system. The relevant engineering question is therefore not formal algorithmic complexity in the abstract, but rather **observed operational latency, throughput, and reduction in manual intervention** as dataset size increases.

Future validation can benchmark representative datasets of different sizes (for example, 25, 100, and 250 RAW images) and record per-stage processing time, downstream manual correction time, and total editing time. This would provide an operational view of scaling behavior without overstating claims about algorithmic complexity inside vendor-controlled black-box tooling.

[INSERT benchmark table: dataset size, RAW count, total input GB, Stage 1 latency, Stage 2 latency, Stage 3 setup time, total manual correction time, end-to-end edit time]

[INSERT screenshots: Stage 1 batch run, Stage 2 mask generation view, Stage 3 exemplar selection + batch application]

## Failure Modes & Edge Cases

Although the pipeline reduces variance and improves editing consistency, each stage still has failure modes that require manual judgment or override.

### Stage 1 Failure Modes

Global luminance normalization can still produce imperfect results when scenes contain **extreme dynamic range**, strong backlighting, heavy [clipping](#clipping), or intentionally stylized lighting conditions. For example, a deliberately composed **silhouette image**—such as a wedding couple rendered primarily as shadow shapes with little or no recoverable facial or subject detail—may be interpreted by Lightroom’s automated tonal analysis as unintentionally underexposed and therefore brightened, even when the low-key silhouette treatment was the intended creative choice. In these cases, automated tonal analysis may reduce variance without fully establishing a sufficient baseline, and residual per-image exposure correction may still be required.

[INSERT screenshots: difficult backlit frame before/after Stage 1, clipped highlight example, deep-shadow recovery example]

### Stage 2 Failure Modes

Semantic segmentation depends on model-generated masks and may fail or degrade around **fine boundaries, partial occlusions, transparent materials (e.g., wedding veils), hair edges, or ambiguous foreground/background transitions**. In such cases, masks may spill into unrelated regions or omit portions of the intended subject domain, reducing the reliability of downstream region-scoped corrections.

[INSERT screenshots: hair-edge masking error, veil/transparent fabric masking miss, skin/background boundary issue]

### Stage 3 Failure Modes

Exemplar-based canonical calibration depends heavily on **correct exemplar selection**. If the [exemplar image](#exemplar-image) contains poor lighting information, meaningful [clipping](#clipping), or scene-specific color bias, those incorrect assumptions can propagate across the [dataset](#dataset). Similarly, some domains may vary legitimately across [scenes](#scene), and over-application of canonical adjustments can suppress authentic scene-specific variation.

[INSERT screenshots: weak exemplar vs strong exemplar, propagated foliage overcorrection, propagated skin-tone mismatch]

### System-Level Failure Modes

At the system level, failure can also occur when too many manual overrides are required. Excessive exception handling reduces the throughput benefit of the pipeline and can reintroduce the same cross-image comparison burden that the workflow is intended to remove. In practice, a weak Stage 1 baseline, unreliable Stage 2 masks, or poor Stage 3 exemplar choice can each increase downstream instability and reduce overall consistency.

[INSERT screenshot set: example where weak Stage 1 baseline destabilizes Stage 3 output]

## Observability & Validation

This case study combines **direct operational measurement**, **editor-observed workflow effects**, and clearly labeled inference. Because parts of the workflow depend on Lightroom’s internal heuristics, validation should focus on observable pipeline behavior rather than on formal claims about algorithmic internals.

### Operational Metrics

The most practical measurements for this workflow are:

- total editing time per dataset
- editing time per delivered image
- number of residual manual exposure corrections after Stage 1
- number of manual mask corrections after Stage 2
- number of per-image domain-specific color corrections remaining after Stage 3

These metrics capture whether the pipeline actually reduces manual intervention and improves throughput in practice.

[INSERT metrics table: dataset, images culled, delivered images, total edit time, edit time per delivered image, post-Stage-1 manual exposure corrections, post-Stage-2 mask corrections, post-Stage-3 color corrections]

### Stage 1 Validation

A lightweight validation approach is to sample a representative subset of images from the same [dataset](#dataset), record pre- and post-Stage 1 values for [exposure](#exposure), [contrast](#contrast), [highlights / whites](#highlights-whites), and [shadows / blacks](#shadows-blacks), and then compare the spread of those values before and after automated tonal analysis. The purpose is not to prove perfect normalization, but to evaluate whether Stage 1 reduces luminance variance sufficiently for more stable downstream transformations.

[INSERT screenshots: representative image sample before/after Stage 1]
[INSERT sample table: image ID, pre/post exposure, pre/post contrast, pre/post highlights-whites, pre/post shadows-blacks]

### Stage 3 Validation

Stage 3 can be validated by selecting one visual domain such as foliage or skin tones, applying exemplar-based calibration, and recording how many residual per-image corrections are still required afterward. The central engineering question is whether reference-based propagation reduces repetitive manual correction while preserving legitimate scene-level variation.

Validation here should be both **objective** and **subjective**. Objectively, the workflow should reduce repeated per-image corrections and total edit time. Subjectively, the editor should observe improved cross-image consistency without flattening authentic scene differences in lighting or mood.

[INSERT screenshots: domain before exemplar calibration, exemplar adjustment, batch-applied result across multiple images]

### Baseline Comparison

A known baseline from the prior workflow is approximately **42 hours of edit time** to complete a 1500-image RAW gallery that was ultimately culled to 375 edited images. That historical workflow included repeated global corrections, inconsistent convergence, and extensive manual adjustment.

Future validation can compare this baseline against either a newly edited gallery or a retrospective subset benchmark using the current pipeline. The goal is not a perfect experimental comparison across all variables, but a practical before/after measure of whether the redesigned workflow reduces editing time and manual correction frequency.

[INSERT comparison table: prior workflow vs pipeline workflow]

## Design Tradeoffs

The pipeline improves consistency and throughput, but it does so through explicit tradeoffs rather than through full automation.

### Automation vs Editorial Control

Stage 1 and Stage 2 automate high-frequency repetitive operations, but Stage 3 remains intentionally editor-guided. Full automation of canonical color decisions would increase speed, but it would also reduce control over context-sensitive domains such as skin tones, clothing, and vegetation.

This tradeoff is especially important for culturally or stylistically significant color decisions. For example, in a South Indian wedding ceremony with richly saturated traditional clothing, a fully automated canonical calibration step might converge toward a more muted or “balanced” palette that is technically consistent but misaligned with client preference and event context. In one real workflow, two gallery versions were delivered from the same edit base—one preserving the stronger Sony color rendering and one using a more desaturated look—and the client preferred the more saturated version. This illustrates why Stage 3 remains editor-guided: canonical consistency must still be constrained by situational, cultural, and client-specific judgment.

[INSERT screenshot: Communication with client (Kabir)]

### Consistency vs Authentic Scene Variation

The system is designed to reduce unwanted variance, not to eliminate all variance. Over-normalization would flatten meaningful differences between [scenes](#scene), especially when time-of-day lighting or environmental color legitimately changes the mood of an image.

### Upfront Preprocessing vs Downstream Speed

Stage 2 introduces additional upfront computation by generating masks across the [dataset](#dataset), but that cost is repaid through faster downstream localized editing. This is a deliberate trade of early processing overhead for reduced repeated work later in the pipeline.

In real editing workflows, the cost of skipping this preprocessing step is not limited to cumulative time alone. When masks must be created manually on a per-image basis, the editor must repeatedly remember which regions in a given [scene](#scene) require correction and then reapply those decisions across similar frames. As the number of required masks increases, this memory burden increases as well, making it easier to apply a correction inconsistently, place a mask differently across near-identical images, or omit a mask entirely where it should have been applied scene-wide. Precomputed semantic masks therefore improve not only downstream speed, but also workflow consistency by reducing dependence on repeated manual recall and per-image mask recreation, thereby reducing human error.

[INSERT screenshot set: similar scene frames with inconsistent manual masks vs precomputed masks]


### Reference Propagation vs Error Amplification

Stage 3 gains efficiency by propagating exemplar-derived transformations across many images, but this also increases the cost of poor reference selection. A weak [exemplar image](#exemplar-image) can amplify error rather than reduce it.

### Local Workflow Efficiency vs Cloud-Native Scalability

The current implementation is optimized for a local Lightroom workflow controlled by a single editor. This makes it practical and immediately useful, but it also means the system is not designed for distributed execution, real-time serving, or cloud-native orchestration.

### Vendor Heuristics vs Full Transparency

The workflow benefits from Lightroom’s built-in automation, but some stages depend on vendor-controlled black-box heuristics. This improves usability and speed while limiting transparency into the exact internal logic of automated tonal analysis and semantic masking.

## Precomputation Strategy

Segmentation masks are created once across the dataset on import (analogous to dataset ingestion in numerical data pipelines) rather than during editing. This trades upfront processing for much faster downstream edits.

This mirrors engineering patterns such as cached derived attributes,
precomputed embeddings, and secondary indexing. The masks function as
metadata attached to each image and enable fast transformations later.

---

## Controlled Manual Overrides

Manual masking remains available for edge cases but is intentionally
limited. Excessive masking granularity increases cognitive load and
reduces editing speed.

Design rationale:

- overly granular control increases cognitive load
- editing speed decreases with many masks
- most images need minimal localized adjustments after baseline

The workflow prioritizes addressable control rather than complete control.

---

## Resulting Benefits

- consistent visual baseline across heterogeneous input distributions
- reduced global editing passes
- faster editing due to segmentation mask precomputation
- reduced manual masking workload
- predictable editing pipeline mechanics
- preservation of natural scene tone differences

---

## Engineering Concepts Demonstrated

- baseline dataset normalization
- multi-stage transformation pipelines
- feature segmentation
- precomputed feature generation
- pipeline stage simplification
- batch processing optimization
- controlled override systems
- cognitive complexity management

---

## Key Design Principle

Establish a consistent global baseline first. Apply localized corrections
only where necessary.

---

## Takeaway

This photography workflow becomes a data transformation pipeline design
problem. By separating global normalization from localized corrections, the system achieves dataset
consistency and editing efficiency without sacrificing image fidelity and processing flexibility.
