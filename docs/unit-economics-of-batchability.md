# Unit Economics of Batchability

This document explains the operational value of the pipeline: converting
repeated per-image issues into batch-safe operations, qualified batch
candidates, or intentionally manual review work.

The estimates here are directional rather than benchmarked. They model
how the cost shape changes when an edit operation moves from repeated
manual execution to setup, propagation, validation, and targeted exception
handling.

## Correction Model

A single deliverable image can contain many issues or edit requirements
that must be addressed before final review. Some are mandatory only when
a specific condition is present, such as dust, tilted framing, weak
luminance, foliage hue drift, or a semantic region that needs local
editing.

The pipeline value comes from separating issue categories by the
automation potential of the edit operation used to address them: which
operations can be safely batch-enabled, which require qualification and
review, and which must remain manual even when the same issue appears
many times.

Representative issue and edit categories include:

- **Local defects:** dust/distraction removal, with image-specific Spot Removal kept manual when the target changes per frame
- **Geometry:** straightening and crop decisions
- **Recovery:** AI-assisted recovery for borderline focus/noise cases when the image is otherwise worth keeping
- **Global visual baseline:** luminance and tonal adjustment
- **Scene-level visual baseline:** hue and color normalization within comparable scenes
- **Semantic local edits:** people, foliage, sky, background, foreground, or ground masks
- **Final artistic review:** manual refinement, crop finalization, and subjective delivery choices

## Batchability Matrix

Not every repeated issue can be addressed by a batch operation. Some
issues recur across a dataset but still require manual image-by-image
judgment because the target region, edit boundary, source pixels, or
aesthetic decision changes with each frame.

The useful distinction is not whether an edit is automated or manual,
but how much work can move from per-image execution into setup, batch
application, qualification, review, and exception handling.

| Issue / edit need | Pipeline handling | Review burden | Example stage |
|---|---|---|---|
| Identity metadata | Batch-applied through ingest preset | Low | Stage 1 |
| Semantic metadata enrichment | Batch-applied through post-import presets | Low to moderate | Stage 1 |
| Dust/distraction cleanup | Batch-applied after validation | Low to moderate | Stage 2 |
| Luminance normalization | Batch-applied across dataset | Moderate | Stage 2 |
| Scene-level color normalization | Batch-applied within comparable scene groups | Moderate | Stage 2 |
| AI masks for common semantic regions | Qualified, then batch-propagated | Moderate to high | Stage 3 |
| Uncertain semantic regions | Qualified on representative examples before promotion | High | Stage 3 |
| Failed straightening, masking, or normalization cases | Exception handling | High | Stage 2 / Stage 3 |
| Image-specific Spot Removal, blemish, or skin cleanup | Manual per-image edit | High | Manual review |
| Final crop and artistic emphasis | Manual editorial decision | High | Final review |

For example, sensor dust is a strong batch candidate because the defect
can be small, repeated, and safe to remove or omit with limited visual
risk. A large blemish on a primary subject, such as a pimple that
appears across many images, is different. It may be repeated, but the
face position, expression, lighting, skin texture, and healing source
change per frame, so the edit must remain manual. In this tested
workflow, Lightroom did not dynamically remove that recognized entity (pimple)
across images with reliable results using either Stage 2 conditioning
techniques or Stage 3 mask propagation techniques.

Stage 3 should not be treated as only partially batchable. Once a mask
definition has been qualified, propagation across the gallery is a batch
operation in the same economic sense as Stage 2 cleanup or
normalization: the operation is applied at dataset scale, then reviewed.
The difference is that probabilistic semantic detection can create a
higher exception-review burden because generated masks may succeed,
omit unavailable regions, bind to the wrong region, or produce
boundaries that need manual refinement.

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

Stage 2 focuses on edit operations that establish a reliable visual baseline
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

For each recurring issue and proposed edit operation, the savings can be
approximated as:

```text
manual_cost = image_count x issue_frequency x average_manual_time_editing

pipeline_cost =
  setup_time
  + qualification_time
  + batch_execution_time
  + review_time
  + exception_fix_time

estimated_savings = manual_cost - pipeline_cost
```

The pipeline is most valuable when an issue has high frequency,
high manual repetition, and predictable enough behavior to support batch
execution. It is less valuable when the issue is rare, highly subjective,
or cheaper to fix manually than to qualify.

## Interpretation

Batchability does not mean removing the editor from the process. It
means changing where the editor spends attention: less repeated
mechanical editing, more setup, validation, exception handling, and
final creative review.

Across the three stages, the accumulated value comes from stacking these
small cost-shape changes. Metadata becomes easier to retrieve, baseline
conditioning reduces visual comparison work, and semantic mask
propagation reduces repeated local editing effort.
