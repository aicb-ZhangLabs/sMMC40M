# Tutorials

Step-by-step notebooks, from opening one acquisition to context-aware evaluation.
Each page can be downloaded as a Jupyter notebook (button at the top right of the page).

<div class="grid cards" markdown>

-   <span class="smcc-step">Tutorial 1 · 10 min</span>

    **[Download and read a sample](01_download_and_read.ipynb)**

    ---

    Fetch one Visium HD acquisition, open the sample index and the raw-count H5AD,
    and link a cell to its matrix row.

-   <span class="smcc-step">Tutorial 2 · 20 min</span>

    **[Explore one acquisition](02_explore_acquisition.ipynb)**

    ---

    Gene-only counts, per-cell QC, spatial maps in µm, marker genes, and a
    standard normalize → PCA → UMAP → clustering workflow with Scanpy.

-   <span class="smcc-step">Tutorial 3 · 15 min</span>

    **[Pair cells with H&E](03_histology_crops.ipynb)**

    ---

    Read native-resolution crops around each cell, respect image eligibility,
    and build an image–expression training table.

-   <span class="smcc-step">Tutorial 4 · 10 min · no download</span>

    **[Choose samples by context](04_context_selection.ipynb)**

    ---

    Filter the 124-acquisition catalog by platform, category, species, condition
    and age; build matched and shifted evaluation pairs.

-   <span class="smcc-step">Tutorial 5 · 10 min · no download</span>

    **[Run the benchmark](05_benchmark.ipynb)**

    ---

    Run the offline demo, check the published 23-category numbers, then replay or
    refit a frozen fold.

</div>

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install huggingface_hub anndata pyarrow pandas matplotlib scanpy tifffile
git clone https://github.com/aicb-ZhangLabs/sMMC40M.git   # code, catalog and readers
```

Tutorials 1–3 use **HD-002** (Visium HD, mouse ovary, 20,262 gene-positive cells), which is
small enough for a laptop. Tutorials 4–5 run without downloading any data.
