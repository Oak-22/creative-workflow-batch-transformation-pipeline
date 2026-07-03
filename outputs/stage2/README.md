## Stage 2 Output Order

Stage 2 proves baseline Develop conditioning through frozen XMP
checkpoints, extracted Develop-setting state, and a final pre/post
comparison.

The front-door artifact is:

```text
stage2_manifest.json
```

That manifest is intentionally compact. It references the verbose JSON
artifacts by path, size, SHA-256 hash, role, and producing script.

Read or regenerate the JSON artifacts in this order:

```text
1. checkpoints/stage2_preconditioning_checkpoint_manifest.json
   proves the frozen preconditioning XMP checkpoint identity

2. extracts/stage2_extracted_preconditioning_develop_settings.json
   extracts Develop settings from the frozen preconditioning checkpoint

3. checkpoints/stage2_postconditioning_checkpoint_manifest.json
   proves the frozen postconditioning XMP checkpoint identity

4. extracts/stage2_extracted_postconditioning_develop_settings.json
   extracts Develop settings from the frozen postconditioning checkpoint

5. comparisons/stage2_develop_parameter_comparison.json
   compares preconditioning vs postconditioning Develop settings

6. stage2_manifest.json
   collates the Stage 2 evidence chain for review
```

The detailed Stage 2 proof artifact is:

```text
comparisons/stage2_develop_parameter_comparison.json
```

The reader-facing Stage 2 index is:

```text
stage2_manifest.json
```

That manifest should be read first during review, then the comparison
and upstream checkpoint/extract artifacts can be opened as drilldown
evidence.


## Production Boundary

The checkpoint manifests should be produced after the corresponding
checkpoint folders are frozen:

```text
data/stage2/reference_state/xmp_preconditioning/
data/stage2/conditioned_state/xmp_postconditioning/
```

The extracts should be produced from those frozen folders, not from
`data/live_workspace/`.

If a checkpoint folder changes, regenerate its manifest, regenerate its
extract, regenerate the final comparison, and then regenerate
`stage2_manifest.json`.
