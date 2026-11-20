# Files and joins

## Release layout

```text
2026-10-28/
  release.json                 # version and exact counts
  manifest.json, SHA256SUMS     # versioned file inventory
  metadata/
    samples.parquet            # 124-row starting index; root-relative paths
    schema.json
    biological_context.parquet
    field_evidence.parquet
    eligibility/{HD,Xenium}/    # per-candidate technical flags
    source_material_relationships.json
  HD/
    metadata/{cells,nuclei}/    # Parquet observation shards
    samples/HD-001/ ...
  Xenium/
    metadata/cells/
    samples/HLDX010/ ...        # corrected image pair is the default
  benchmark/
    folds.json, tracks.json
    splits/, targets/, fixtures/, packets/
    reference/, provenance/, vendor/, validation/
  qc/
  provenance/
```

## Starting point: `metadata/samples.parquet`

One row per acquisition. Asset columns are **paths relative to the release root**:

| Column | Points to |
| --- | --- |
| `expression_file` | sample H5AD (raw counts) |
| `genes_file` | measured feature axis (`gene_id`, `feature_type`, symbols) |
| `cell_index_file` | per-candidate Parquet (`cell_id`, `h5ad_row`, `x_px`, `y_px`, …) |
| `image_file`, `mask_file` | native image and segmentation mask |
| `eligibility_file` | per-candidate technical flags |
| `mpp_x_um_per_px`, `mpp_y_um_per_px` | microns per pixel of the selected image |

## Join rules

- **Observation key:** `sample_id` + `cell_id`. **Sample key:** `sample_id`.
- `h5ad_row` is **nullable**: a candidate without RNA has no matrix row (not an all-zero vector).
- Preserved HD cell shards may say `platform = "Visium HD"`; the root table says `HD`.
  Aliases are declared in [`observation_views.json`](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/data/observation_views.json).
- Platform-global cell shards keep H5AD paths relative to `HD/` or `Xenium/`; resolve them with
  `cell_index_path_base` from the root sample record instead of concatenating paths.
- In a **sample-only download**, asset paths in `samples.parquet` and `cells.parquet` are relative to the
  acquisition folder, not its `metadata/` child.
- `obsm/spatial` is in selected-image pixels; `obsm/spatial_um` is in µm.

## Expression

H5AD stores raw non-negative integer counts as CSR on the original feature axis. Open it
**backed** to read metadata or a few rows; do not densify millions of observations.

```python
import anndata as ad
adata = ad.read_h5ad(path, backed="r")
row = adata.X[i:i+1]          # one sparse row
adata.file.close()
```

Full schema: [`data/schema.json`](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/data/schema.json) ·
release facts: [`data/release_summary.json`](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/data/release_summary.json).
