# Download

The data are hosted on Hugging Face at
[**zhang-lab/sMCC40M**](https://huggingface.co/datasets/zhang-lab/sMCC40M).
The complete versioned folder is about **931.6 GB** (images, masks, expression and
reproducibility assets), so most users start with one acquisition.

```bash
pip install huggingface_hub anndata pyarrow
export REPO=zhang-lab/sMCC40M
```

## One acquisition

The dataset ships a small helper that fetches a complete sample package:

```bash
hf download "$REPO" examples/download_sample.py --repo-type dataset --local-dir .

# Visium HD, mouse ovary
python examples/download_sample.py --repo "$REPO" --platform HD --sample HD-002
python smcc_data/HD/samples/HD-002/read_example.py

# Xenium
python examples/download_sample.py --repo "$REPO" --platform Xenium --sample HHDX011
python smcc_data/Xenium/samples/HHDX011/read_example.py
```

Each sample folder holds the expression matrix, image, segmentation mask, metadata,
mappings, eligibility table, sample-specific field evidence and checksums.

!!! tip "Expression only"
    `download_sample.py` also has an `--expression-only` mode for just the H5AD matrix,
    when you do not need images or masks. The
    [data card](https://huggingface.co/datasets/zhang-lab/sMCC40M) lists its options.

## Pick samples first

Download the 124-row sample index and choose acquisitions by platform, category,
species or context before fetching anything large:

```bash
hf download "$REPO" metadata/samples.parquet --repo-type dataset --local-dir .
```

The same information is in the repository's
[`data/sample_catalog.csv`](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/data/sample_catalog.csv).
[Tutorial 4](../tutorials/04_context_selection.ipynb) shows how to filter it.

## Everything

```bash
hf download "$REPO" --repo-type dataset --local-dir sMCC40M-2026-10-28
```

Pin the frozen version for exact reproduction:
[revision `0f6f6577…`](https://huggingface.co/datasets/zhang-lab/sMCC40M/tree/0f6f6577b0da8e00d2624e834aa6efc1c651b1ad).
The benchmark assets alone (~2.9 GB of sampled fixtures plus plans and predictions) are under
[`benchmark/`](https://huggingface.co/datasets/zhang-lab/sMCC40M/tree/0f6f6577b0da8e00d2624e834aa6efc1c651b1ad/benchmark).

## Verify

The root release manifest SHA256 is

```text
f4f20ea1a5acfe660f1988184337921a92e1f5fcb519609324bfb921cfbda460
```

Nested manifests and `SHA256SUMS` cover every file. Never modify a release folder in place;
write outputs elsewhere.

## License and attribution

Data are released under **CC BY 4.0**. The 124 acquisitions come from 10x Genomics dataset
pages that declare CC BY 4.0; keep the attribution notices when you share covered data. See the
[license manifest](https://huggingface.co/datasets/zhang-lab/sMCC40M/blob/main/licensing/license_manifest.csv)
and [attribution notes](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/docs/attribution.md).
