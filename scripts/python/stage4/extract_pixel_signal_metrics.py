"""Stage 4: extract RAW pixel-signal metrics from source assets."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.python.common import write_json


DEFAULT_INPUT_ROOT = "data/live_workspace"
DEFAULT_OUTPUT = "outputs/stage4/stage4_extracted_pixel_signal_metrics.json"
DEFAULT_INPUT_MODEL = "stage4_live_workspace_raw_pixel_signal_probe"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Stage 4 pixel-signal extraction."""
    parser = argparse.ArgumentParser(
        description="Extract RAW pixel-signal metrics from ARW assets."
    )
    parser.add_argument(
        "--input-root",
        default=DEFAULT_INPUT_ROOT,
        help="Directory containing RAW source assets.",
    )
    parser.add_argument(
        "--input-model",
        default=DEFAULT_INPUT_MODEL,
        help="Label describing the input asset state.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Destination JSON file for extracted Stage 4 pixel metrics.",
    )
    parser.add_argument(
        "--histogram-bins",
        type=int,
        default=16,
        help="Number of bins for compact histogram summaries.",
    )
    return parser.parse_args()


def require_dependencies() -> tuple[Any, Any]:
    """Load optional RAW-processing dependencies with an actionable error."""
    try:
        import numpy as np
        import rawpy
    except ImportError as exc:
        raise SystemExit(
            "Stage 4 pixel extraction requires rawpy and numpy. "
            "Create a local environment and install them with: "
            "python3 -m venv .venv && .venv/bin/python -m pip install rawpy numpy"
        ) from exc
    return rawpy, np


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_array(array: Any) -> str:
    """Return the SHA-256 digest for a contiguous array representation."""
    digest = hashlib.sha256()
    digest.update(array.tobytes())
    return digest.hexdigest()


def raw_paths(folder: Path) -> list[Path]:
    """Return supported RAW files in a flat folder."""
    if not folder.is_dir():
        raise SystemExit(f"Input root not found: {folder}")
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in {".arw"}
    )


def json_scalar(value: Any) -> Any:
    """Convert numpy scalar-ish values into JSON-compatible scalars."""
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, bytes):
        return value.decode("ascii", errors="replace")
    return value


def json_list(values: Any) -> list[Any]:
    """Convert array-like values into JSON-compatible lists."""
    if values is None:
        return []
    if hasattr(values, "tolist"):
        values = values.tolist()
    return [json_scalar(value) for value in values]


def numeric_summary(np: Any, values: Any) -> dict[str, object]:
    """Return compact descriptive statistics for an array."""
    flattened = values.astype("float64", copy=False).reshape(-1)
    percentiles = np.percentile(flattened, [0, 1, 5, 25, 50, 75, 95, 99, 100])
    return {
        "count": int(flattened.size),
        "min": float(percentiles[0]),
        "p01": float(percentiles[1]),
        "p05": float(percentiles[2]),
        "p25": float(percentiles[3]),
        "median": float(percentiles[4]),
        "p75": float(percentiles[5]),
        "p95": float(percentiles[6]),
        "p99": float(percentiles[7]),
        "max": float(percentiles[8]),
        "mean": float(np.mean(flattened)),
        "std": float(np.std(flattened)),
    }


def normalized_raw_mosaic(np: Any, raw_image: Any, black_level: float, white_level: float) -> Any:
    """Normalize RAW mosaic values using coarse black and white reference levels."""
    denominator = max(float(white_level) - float(black_level), 1.0)
    return np.clip((raw_image.astype("float64") - float(black_level)) / denominator, 0.0, 1.0)


def histogram_summary(np: Any, values: Any, bins: int, range_: tuple[float, float]) -> dict[str, object]:
    """Return histogram bins and coverage checks for an array."""
    counts, edges = np.histogram(values.reshape(-1), bins=bins, range=range_)
    expected_count = int(values.size)
    observed_count = int(counts.sum())
    return {
        "bin_count": bins,
        "range_min": float(range_[0]),
        "range_max": float(range_[1]),
        "bin_edges": [float(edge) for edge in edges],
        "counts": [int(count) for count in counts],
        "observed_count": observed_count,
        "expected_count": expected_count,
        "coverage_status": (
            "complete" if observed_count == expected_count else "incomplete"
        ),
    }


def channel_summaries(np: Any, raw: Any, raw_visible: Any) -> list[dict[str, object]]:
    """Return per-CFA-channel summaries for the visible RAW mosaic."""
    raw_colors = getattr(raw, "raw_colors_visible", None)
    if raw_colors is None:
        return []

    color_desc = json_scalar(getattr(raw, "color_desc", b""))
    summaries = []
    for channel_index in range(int(getattr(raw, "num_colors", 0) or 0)):
        mask = raw_colors == channel_index
        channel_values = raw_visible[mask]
        channel_label = (
            color_desc[channel_index]
            if isinstance(color_desc, str) and channel_index < len(color_desc)
            else str(channel_index)
        )
        summaries.append(
            {
                "channel_index": channel_index,
                "channel_label": channel_label,
                "pixel_count": int(channel_values.size),
                "raw_value_summary": numeric_summary(np, channel_values),
            }
        )
    return summaries


def rendered_preview_metrics(np: Any, raw: Any, bins: int) -> dict[str, object]:
    """Return compact metrics from a half-size rendered RGB preview."""
    rgb = raw.postprocess(
        half_size=True,
        output_bps=8,
        no_auto_bright=True,
        use_camera_wb=True,
    )
    rgb_float = rgb.astype("float64") / 255.0
    red = rgb_float[:, :, 0]
    green = rgb_float[:, :, 1]
    blue = rgb_float[:, :, 2]
    luminance = (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)
    saturation_proxy = rgb_float.max(axis=2) - rgb_float.min(axis=2)
    green_cast_proxy = green - ((red + blue) / 2.0)
    return {
        "render_model": "rawpy_half_size_camera_wb_no_auto_bright_8bit",
        "shape": [int(value) for value in rgb.shape],
        "pixel_count": int(rgb.shape[0] * rgb.shape[1]),
        "rgb_channel_means": {
            "red": float(np.mean(red)),
            "green": float(np.mean(green)),
            "blue": float(np.mean(blue)),
        },
        "luminance_summary": numeric_summary(np, luminance),
        "luminance_histogram": histogram_summary(np, luminance, bins, (0.0, 1.0)),
        "saturation_proxy_summary": numeric_summary(np, saturation_proxy),
        "green_cast_proxy_summary": numeric_summary(np, green_cast_proxy),
    }


def size_metadata(raw: Any) -> dict[str, object]:
    """Return RAW decoder size metadata when exposed by rawpy."""
    sizes = getattr(raw, "sizes", None)
    if sizes is None:
        return {}
    fields = [
        "raw_height",
        "raw_width",
        "height",
        "width",
        "top_margin",
        "left_margin",
        "iheight",
        "iwidth",
        "pixel_aspect",
        "flip",
    ]
    return {
        field: json_scalar(getattr(sizes, field))
        for field in fields
        if hasattr(sizes, field)
    }


def build_record(rawpy: Any, np: Any, raw_path: Path, input_root: Path, input_model: str, bins: int) -> dict[str, object]:
    """Build one Stage 4 pixel-signal metric record from a RAW source file."""
    with rawpy.imread(str(raw_path)) as raw:
        raw_full = np.ascontiguousarray(raw.raw_image.copy())
        raw_visible = np.ascontiguousarray(raw.raw_image_visible.copy())
        black_levels = json_list(getattr(raw, "black_level_per_channel", []))
        black_level_floor = float(min(black_levels)) if black_levels else 0.0
        white_level = float(getattr(raw, "white_level", 0) or 0)
        normalized_visible = normalized_raw_mosaic(
            np,
            raw_visible,
            black_level_floor,
            white_level,
        )
        raw_histogram = histogram_summary(np, normalized_visible, bins, (0.0, 1.0))
        full_pixel_count = int(raw_full.size)
        visible_pixel_count = int(raw_visible.size)

        return {
            "asset_key": raw_path.stem,
            "input_model": input_model,
            "input_root": str(input_root),
            "raw_path": str(raw_path),
            "file_provenance": {
                "file_size_bytes": raw_path.stat().st_size,
                "file_sha256": sha256_file(raw_path),
            },
            "decoder_provenance": {
                "decoder": "rawpy",
                "rawpy_version": str(getattr(rawpy, "__version__", "unknown")),
                "numpy_version": str(getattr(np, "__version__", "unknown")),
                "raw_type": str(getattr(raw, "raw_type", "unknown")),
                "color_desc": json_scalar(getattr(raw, "color_desc", b"")),
                "num_colors": json_scalar(getattr(raw, "num_colors", None)),
                "raw_pattern": json_list(getattr(raw, "raw_pattern", [])),
                "black_level_per_channel": black_levels,
                "black_level_floor_used": black_level_floor,
                "white_level": white_level,
                "camera_whitebalance": json_list(
                    getattr(raw, "camera_whitebalance", [])
                ),
                "daylight_whitebalance": json_list(
                    getattr(raw, "daylight_whitebalance", [])
                ),
                "sizes": size_metadata(raw),
            },
            "read_coverage": {
                "read_model": "full_decoded_raw_mosaic_with_visible_window",
                "raw_full_shape": [int(value) for value in raw_full.shape],
                "raw_full_pixel_count": full_pixel_count,
                "raw_full_dtype": str(raw_full.dtype),
                "raw_full_sha256": sha256_array(raw_full),
                "raw_visible_shape": [int(value) for value in raw_visible.shape],
                "raw_visible_pixel_count": visible_pixel_count,
                "raw_visible_dtype": str(raw_visible.dtype),
                "raw_visible_sha256": sha256_array(raw_visible),
                "nonvisible_margin_pixel_count": full_pixel_count
                - visible_pixel_count,
                "raw_histogram_observed_count": raw_histogram["observed_count"],
                "raw_histogram_expected_count": raw_histogram["expected_count"],
                "raw_histogram_coverage_status": raw_histogram["coverage_status"],
                "coverage_status": (
                    "complete"
                    if raw_histogram["observed_count"] == visible_pixel_count
                    else "incomplete"
                ),
            },
            "raw_mosaic_metrics": {
                "raw_value_summary": numeric_summary(np, raw_visible),
                "normalized_value_summary": numeric_summary(np, normalized_visible),
                "normalized_histogram": raw_histogram,
                "cfa_channel_summaries": channel_summaries(np, raw, raw_visible),
            },
            "rendered_preview_metrics": rendered_preview_metrics(np, raw, bins),
        }


def build_output(args: argparse.Namespace) -> dict[str, object]:
    """Build the Stage 4 pixel-signal extraction payload."""
    rawpy, np = require_dependencies()
    input_root = Path(args.input_root)
    records = [
        build_record(
            rawpy,
            np,
            raw_path,
            input_root,
            args.input_model,
            args.histogram_bins,
        )
        for raw_path in raw_paths(input_root)
    ]
    coverage_counts = {
        status: sum(
            1
            for record in records
            if record["read_coverage"]["coverage_status"] == status
        )
        for status in ("complete", "incomplete")
    }
    return {
        "stage": "stage4_pixel_signal_metrics",
        "status": "complete",
        "input_model": args.input_model,
        "input_root": str(input_root),
        "notes": {
            "scope": (
                "Stage 4 extracts numeric pixel-signal metrics from RAW source "
                "assets. It does not perform semantic computer vision or object "
                "recognition."
            ),
            "observability_boundary": (
                "The output does not print every pixel. Instead, it records the "
                "source file hash, decoded full RAW mosaic hash, decoded visible "
                "RAW mosaic hash, raster shapes, pixel counts, and histogram "
                "coverage checks so reviewers can verify the read boundary and "
                "the summarized visible-pixel population."
            ),
            "metric_boundary": (
                "RAW mosaic metrics summarize sensor-domain values. Rendered "
                "preview metrics summarize a half-size camera-white-balance RGB "
                "render and should be treated as a derived view, not as Lightroom's "
                "final edited rendering."
            ),
        },
        "summary": {
            "asset_count": len(records),
            "complete_coverage_asset_count": coverage_counts["complete"],
            "incomplete_coverage_asset_count": coverage_counts["incomplete"],
            "histogram_bins": args.histogram_bins,
        },
        "records": records,
    }


def main() -> None:
    """Extract Stage 4 pixel-signal metrics."""
    args = parse_args()
    output = build_output(args)
    write_json(args.output, output)
    print(
        f"Wrote {args.output} with "
        f"{output['summary']['asset_count']} RAW assets and "
        f"{output['summary']['complete_coverage_asset_count']} complete reads."
    )


if __name__ == "__main__":
    main()
