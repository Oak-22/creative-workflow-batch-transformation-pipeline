# Unit Economics of Batchability

This document explains the operational value of the pipeline: converting
repeated per-image corrections into batch-safe operations, qualified
batch candidates, or intentionally manual review work.

The estimates here are directional rather than benchmarked. They model
how the cost shape changes when a correction moves from repeated manual
execution to setup, propagation, validation, and targeted exception
handling.

## Correction Model

A single deliverable image can require many mandatory corrections before
it is ready for final review. Some corrections are mandatory only when a
specific condition is present, such as dust, tilted framing, weak
luminance, foliage hue drift, or a semantic region that needs local
editing.

The pipeline value comes from identifying which subset of those
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
      |
Cull for focus, relevance, aesthetic uniqueness, and edit potential
      |
For each mandatory correction:
      |
Is the correction present?
      |-- no  -> skip
      `-- yes
           |
      Is it batch-safe?
      |-- yes -> batch operation candidate
      `-- no
           |
      Can it be qualified on a representative subset?
      |-- yes -> qualify, then promote if reliable
      `-- no  -> keep as manual refinement
```

## Stage-Level Value

### Stage 1: Metadata Application, Enrichment, and Query

Stage 1 shifts metadata work from repeated manual record maintenance to
structured preset application, post-import enrichment, and reusable
query views. The savings come from reducing field-level rework,
avoiding metadata collisions, and making later retrieval faster through
filters and Smart Collections.

The main value is not only faster metadata entry. It is a cleaner state
layer: images become identifiable, queryable, and easier to segment into
working sets before visual editing begins.

### Stage 2: Baseline Conditioning and Rollback

Stage 2 focuses on corrections that establish a reliable visual baseline
before creative edits: local cleanup, luminance normalization,
scene-level color normalization, and rollback-safe branching.

The savings come from reducing repeated comparison loops. Instead of
manually trying to match brightness, tone, and color across many images
late in the edit, the workflow establishes a comparable baseline early
and protects it with Virtual Copy branches.

### Stage 3: AI Mask Definition Propagation

Stage 3 focuses on semantic operations whose behavior depends on
probabilistic AI segmentation. The savings come from defining reusable
mask logic once, propagating it across the gallery, and reviewing
generated results instead of manually brushing each semantic region on
each image.

Because AI mask quality can partially succeed or fail, the value model
depends on qualification and review. The pipeline does not remove human
judgment; it reduces the amount of repetitive manual masking that must
happen before judgment can be applied.

## Back-of-Envelope Savings Model

The pipeline changes the cost model from repeated per-image execution to
stage setup, batch application, validation, and targeted exception
handling.

| Workflow area | Manual cost shape | Pipeline-assisted cost shape | Savings driver |
|---|---|---|---|
| Metadata application | Repeated field entry, ad-hoc classification, manual searching | Ingest-time identity preset, post-import semantic enrichment, reusable queries | Fewer field collisions and faster retrieval |
| Baseline conditioning | Repeated cleanup, matching, comparison, and rollback recovery per image | Batch-safe cleanup, dataset/scene-level normalization, protected edit branches | Less comparison burden and safer experimentation |
| AI mask propagation | Manual semantic masking per region per image | Canonical mask definition, batch propagation, human review | Less repetitive masking before review |

## Directional Formula

For each candidate correction, the savings can be approximated as:

```text
manual_cost = image_count x correction_frequency x average_manual_time

pipeline_cost =
  setup_time
  + qualification_time
  + batch_execution_time
  + review_time
  + exception_fix_time

estimated_savings = manual_cost - pipeline_cost
```

The pipeline is most valuable when a correction has high frequency,
high manual repetition, and predictable enough behavior to support batch
execution or qualification. It is less valuable when the correction is
rare, highly subjective, or cheaper to fix manually than to qualify.

## Interpretation

Batchability does not mean removing the editor from the process. It
means changing where the editor spends attention: less repeated
mechanical correction, more setup, validation, exception handling, and
final creative review.

Across the three stages, the accumulated value comes from stacking these
small cost-shape changes. Metadata becomes easier to retrieve, baseline
conditioning reduces visual comparison work, and semantic mask
propagation reduces repeated local editing effort.
