# Stage 4 - ML Readiness Handoff

Stage 4 converts the earlier Lightroom-centered evidence chain into a
machine-learning handoff package. The stage organizes stage-bounded
evidence into a feature inventory, readiness report, and contract that
a future ML team could evaluate.


## Purpose

The prior stages create different evidence surfaces:

- Stage 1 establishes asset identity and metadata state.
- Stage 2 records global Develop-parameter changes across frozen XMP
  checkpoints.
- Stage 3 records semantic/local mask state and Lightroom write
  behavior across frozen sidecar checkpoints.
- Stage 4 adds RAW pixel-signal metrics and joins the evidence into an
  ML handoff view.

Stage 4's scope is **readiness and handoff evidence**. Model
performance belongs to a later workstream once labels, targets, and
evaluation protocol exist.


## Handoff Scope

Stage 4 establishes:

```text
The pipeline can materialize a structured, inspectable handoff package
for a future ML/data-science team.
```

Downstream modeling workstreams would establish separate evidence for:

```text
model training results
editing-style generalization
compute optimization impact
segmentation quality scoring
```


## Artifact Flow

The Stage 4 output sequence is:

```text
RAW source assets
  -> raw pixel-signal metrics
  -> cross-stage feature inventory
  -> dataset readiness report
  -> ML handoff contract
  -> compact Stage 4 manifest
```

The reader-facing entrypoint is:

```text
outputs/stage4/stage4_manifest.json
```

Detailed output guidance lives in:

```text
outputs/stage4/README.md
```


## Current Readiness Interpretation

The current dataset supports:

- validating the feature schema
- demonstrating cross-stage lineage
- showing what an ML handoff could contain
- identifying what is missing before model training

Advancing to the next readiness tier requires evidence for:

- credible supervised training
- model accuracy evaluation
- editing-style generalization
- compute optimization impact

The readiness report makes this explicit instead of hiding the gap:

```text
handoff_readiness = ready_for_ml_team_discovery
model_training_readiness = not_ready
```


## Feature Families

Stage 4 currently inventories four feature families:

```text
asset_identity_metadata
develop_parameter_deltas
semantic_local_mask_state
raw_pixel_signal_metrics
```

The complete cross-stage row count is lower than the total asset count
because Stage 2 Develop deltas and Stage 3 mask-state evidence exist for
smaller subsets. That gives a future ML team a clear coverage map before
they decide what additional data to collect.


## Next Evidence Needed

Before model training becomes credible, the project would need new
evidence artifacts such as:

- rendered before/after outputs
- accepted/rejected suggestion labels
- edit-session telemetry
- manual intervention counts
- correction counts
- train/validation split manifests
- broader cross-shoot coverage

Those artifacts define the next modeling contract for expanding beyond
handoff readiness.
