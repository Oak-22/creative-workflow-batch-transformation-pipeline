# Case Study: Metadata Ingestion and Enrichment Pipeline

Part of the **Creative Workflow Batch Transformation Pipeline** umbrella project.

## Executive Summary

- **Constraint:** The system/tooling supports only one metadata preset at ingest.
- **Risk:** Metadata collisions occur when multiple presets write the same fields, risking ownership overwrite.
- **Architecture:** Split metadata into an immutable Identity Layer and a mutable Semantic Layer.
- **Ingest:** Use a single authoritative preset to initialize ownership fields idempotently.
- **Enrichment:** Apply domain-specific presets post-ingest that write only classification fields.
- **Safety:** Field-level write boundaries prevent overwrites by design, not by operator caution.
- **Validation:** Deterministic IPTC-panel checklist used after ingest and after enrichment.
- **Querying:** Smart Collections are treated as declarative views (saved predicates), not folders.
- **Scalability:** Supports multi-domain classification without changing ingest guarantees.

## Problem Statement

Design a deterministic metadata ingestion and enrichment system for image assets operating under a hard tooling constraint: only one preset may be applied at ingest. The system must reliably initialize ownership metadata, prevent field-level collisions, and remain robust as classification requirements span multiple domains.

The core challenge is to maintain a stable, authoritative identity state while enabling iterative, revisable semantic enrichment. The solution must be non-destructive, auditable, and simple to validate in batch workflows.

## Key Constraints and Observations

- The system/tooling allows only one metadata preset at import, no native preset stacking.
- Post-import presets are additive when checked fields do not overlap.
- Conflicts occur only when two presets write to the same checked fields.
- Export options are reductive (include/exclude), not additive.

## Tooling Limitations

Lightroom provides no field‑level locking and metadata presets can overwrite existing fields if the same fields are checked. Because the system cannot rely on tooling guarantees to protect critical metadata, write isolation is enforced through schema design: each preset writes to a dedicated set of fields, preventing destructive collisions between identity and semantic metadata.


## Architecture

### Separation of Concerns

- **Identity Layer**: immutable, authoritative ownership/authorship state initialized at ingest.
- **Semantic Layer**: mutable, revisable classification/context state enriched post-ingest.
- **Query Layer**: declarative logical views derived from metadata predicates (Smart Collections).

```text
RAW Image
   ↓
[Global Import Preset]
   ↓
Identity Layer (Immutable)

   ↓ (post-import)
[Domain Presets]
   ↓
Semantic Layer (Mutable)

   ↓
[Smart Collections]
   ↓
Derived Logical Views
```

## Implementation Details

### 1) Single Global Import Preset (Authoritative)

**Preset name:** `[IMPORT] Global Copyright & Creator`

Included identity fields:
- IPTC Copyright
- Copyright Status
- Rights Usage Terms
- Creator Name
- Creator Email
- Creator Website
- Creator Job Title
- Credit Line

Excluded fields:
- Caption
- Headline
- IPTC Category
- Keywords
- Accessibility Alt Text
- Domain-specific descriptions

This ingest preset establishes the authoritative identity state at ingest. By excluding semantic fields, the design minimizes collision surface area and avoids embedding domain assumptions during ingest.

### 2) Domain-Specific Presets (Post-Import Only)

Domain presets are semantic enrichment presets applied after ingestion.

- All identity/authorship/copyright fields are unchecked.
- Only semantic fields are checked.
- Example semantic fields: Caption, Headline, IPTC Category, Accessibility Alt Text, contextual descriptions.

This enables safe batch enrichment while protecting authoritative metadata from accidental overwrite.

### 3) Keywords Managed Separately

Keywords are intentionally excluded from the global ingest preset.

- Taxonomy evolves incrementally during selection and review.
- Keyword assignment is explicit and post-ingest (Keyword List/Keyword Sets or semantic presets).
- This preserves deliberate classification rather than implicit ingest-time tagging.

## Verification (Critical)

**During import**
- Apply only `[IMPORT] Global Copyright & Creator` during ingest.

**After import**
- Open a sample set in the Library module.
- Switch the metadata panel to **IPTC**.
- Validate identity fields are populated (copyright + creator fields).
- Validate semantic/classification fields are still empty.

**Apply one domain-specific semantic preset to the same sample set post-import**
- Re-check the metadata panel in **IPTC**.
- Validate semantic fields are now populated.
- Validate identity fields *remain unchanged* from ingest baseline.
- Confirm resulting state is additive and non-destructive.

## Results / Benefits

- Single source of truth for identity metadata.
- Zero overwrite risk for ownership fields when boundaries are respected.
- Scalable enrichment workflow across multiple classification domains.
- Explicit, operator-visible classification decisions post-ingest.
- Reproducible metadata outcomes from deterministic initialization + checklist validation.

## Engineering Concepts Demonstrated

- Constraint-driven design
- Idempotent ingestion
- Separation of concerns
- Immutable vs mutable metadata layers
- Conflict avoidance via field-level write boundaries
- Deterministic initialization under tooling limits
- Post-ingest enrichment pipeline design
- Declarative views / logical indexing
- Non-destructive state transitions
- Auditability through explicit validation steps
- Reproducibility via stable ingest baseline
- Derived dataset modeling from metadata predicates

## Guiding Principle

> **Authorship metadata should be automatic and irreversible.**
> **Semantic metadata should be deliberate and revisable.**

## Addendum: Smart Collections as a Declarative Indexing Layer

### Motivation

Smart Collections can be modeled as a query/indexing abstraction over stable source data, not just an organizational UI feature. This framing makes their behavior legible in systems terms.

### Conceptual Model

- Photos = immutable source records
- Metadata fields (ratings, flags, keywords, dates, capture attributes) = structured columns
- Smart Collections = saved predicates / declarative views

Collections store selection logic, not copies of records. Membership is computed dynamically as metadata changes.

### Example: Highlights as Derived Dataset

A “Highlights” view can be defined as:
- Rating ≥ 4
- Flag = Pick
- Capture date within a target window
- Optional keyword/domain filters

This is equivalent to defining a curated high-signal derived dataset for downstream review.

### Why This Matters

- Decouples physical storage from access/query patterns.
- Reduces folder/namespace maintenance overhead.
- Makes selection logic explicit, inspectable, and repeatable.
- Enables fast reclassification without moving underlying files.

### Limitations

- No joins across entities
- Limited computed-field expressiveness
- No built-in versioning of query definitions
- No exportable formal schema for rules

### Takeaway

Smart Collections are best treated as a lightweight declarative indexing layer over metadata, enabling non-destructive, query-driven retrieval of image records.


---

#  Keyword Tags, Keyword Sets, and Keyword Lists


## Keyword Lists – Hierarchical Taxonomies for Scalable Metadata Management

![Screenshot of Lightroom Classic keyword panel interface showing keyword hierarchies and management tools organized in a tree structure with parent and child keyword entries](assets/images/lightroom-keyword-panel.png)


---

# Lightroom Catalog's Database Structure (SQL-Lite)

## Filesystem-Sturcture

Lightroom does **not store image pixel data inside the catalog**. Instead, the catalog functions as a metadata index that references image files stored on disk (local drives, external volumes, or network locations).

Image files remain in their filesystem locations, for example:

```
/Volumes/Photos/2025/Weddings/Juan_Nicole/RAW/DSC01234.ARW
```

The Lightroom catalog (`.lrcat`) stores structured metadata describing those files.  
This metadata can be divided into two broad categories: **pre‑import camera metadata** and **post‑import catalog metadata**

**1. Pre‑import metadata (camera‑generated EXIF/IPTC)**  
This metadata is written by the camera at shutter time and embedded directly in the image file. Lightroom reads these fields during import but does not originate them.

Examples include:

- Capture timestamp (`DateTimeOriginal`)
- Camera make and model
- Lens model and focal length
- Exposure settings (ISO, shutter speed, aperture)
- GPS coordinates (if enabled)

**2. Post‑import catalog metadata (Lightroom‑generated)**  
This metadata is created or modified after import and is stored in the Lightroom catalog (and optionally written to XMP sidecar files or embedded metadata) where:

Catalog = primary metadata store

XMP/embedded = optional synchronization layer



Examples include:

- File path references
- Ratings and flags
- Keyword associations
- Collection membership
- Editing history and develop settings

In systems terms, the catalog behaves like a **relational metadata database** that indexes external assets rather than storing the assets themselves. This design allows Lightroom to organize and query very large photo libraries without duplicating image data.


## Ad-hoc Library filtering vs Smart Collections 

After establishing a repeatable metadata schema strategy, users can query the catalog in two primary ways: **interactive ad-hoc filtering** and **Smart Collections**. This is similar in function to interactive one-off sql qeuries using database clients and views containing defined, saved predicate / conditional logic.  

### Ad‑hoc Library Filtering

The Library Filter bar performs **temporary metadata queries** against the catalog. Users can filter images based on fields such as:

- Rating
- Flags
- Capture date
- Camera model
- Lens metadata

Conceptually this behaves like a transient query over the metadata index:

[INSERT IMAGE OF GUI]

```
SELECT image_id
FROM images
WHERE rating >= 4
AND keyword = 'rings'
AND capture_year = 2023;
```

The filter is evaluated immediately and the results are displayed, but the query definition is not saved. Changing the filter simply executes a different query against the catalog.

### Smart Collections

Smart Collections store **query definitions** inside the catalog and automatically evaluate them against the metadata store.

Rather than storing copies of images, a Smart Collection stores a set of predicate rules such as:

- Keyword contains "rings"
- capture data between 2025-01-01 – 2025-12-31


Whenever metadata changes, Lightroom re-evaluates those rules and updates the collection membership automatically.

Conceptually this behaves similarly to a saved database view:

[INSERT IMAGE OF GUI]


```
CREATE VIEW rings_highlights AS
SELECT image_id
FROM images
WHERE keyword = 'rings'
AND rating >= 4
AND flag = 'pick';
```

This makes Smart Collections a **dynamic indexing layer** that allows photographers to maintain persistent logical groupings of images without physically reorganizing files or collections.

