---
title: sMCC40M
hide:
  - navigation
  - toc
---

<div class="smcc-hero" markdown>
<p class="kicker">NeurIPS 2026 · Dataset &amp; benchmark</p>

# sMCC40M

<p class="lede">A context-aware dataset and benchmark for single-cell spatial transcriptomics.
It links expression, masks, coordinates and source-backed sample context across Visium HD
and Xenium, with H&amp;E crops available for eligible cells.</p>

<div class="chips"><span class="chip scale">SCALE</span><span class="chip res">RESOLUTION</span><span class="chip ctx">CONTEXT</span></div>

[Get the data](dataset/download.md){ .md-button .md-button--primary }
[Tutorials](tutorials/index.md){ .md-button }
[Benchmark](benchmark.md){ .md-button }
[GitHub](https://github.com/aicb-ZhangLabs/sMMC40M){ .md-button }
</div>

<div class="smcc-stats">
<div class="smcc-stat"><div class="n">38.47M</div><div class="l">gene-positive cell / nucleus observations</div></div>
<div class="smcc-stat"><div class="n">124</div><div class="l">acquisitions · 53 Visium HD + 71 Xenium</div></div>
<div class="smcc-stat rust"><div class="n">32.68M</div><div class="l">cells with an eligible H&amp;E pairing</div></div>
<div class="smcc-stat purple"><div class="n">23 · 7</div><div class="l">reporting categories · source species</div></div>
<div class="smcc-stat amber"><div class="n">CC BY 4.0</div><div class="l">with per-sample attribution</div></div>
</div>

<figure markdown>
![sMCC40M overview: cells by organ, species and technology; hierarchical morphology; text descriptions; expression, metadata and cell-cell communication](assets/dataset.png)
<figcaption>Resource overview (author-supplied illustration). Numbers on this site follow the frozen
<b>2026-10-28</b> public release; see <a href="dataset/">Dataset</a> for exact counts and denominators.</figcaption>
</figure>

## What's new

<!-- LATEST_UPDATES -->

[All updates →](updates/index.md)

## Why sMCC40M

Spot-level measurements average signals from multiple cells and can hide differences between them.
sMCC40M provides cell-resolution data and is organized around three axes.

<div class="grid cards" markdown>

-   :material-chart-bubble:{ .lg } **Scale**

    ---

    124 acquisitions in 23 reporting categories and 7 species, so encoders and readouts can be
    compared under one matched protocol.

-   :material-grid:{ .lg } **Resolution**

    ---

    An observation represents a cell or a nucleus. Visium HD 2 µm bins are assigned to a
    segmented object only when it covers **more than 50%** of the bin. Xenium keeps its native
    cell assignments.

-   :material-tag-multiple:{ .lg } **Context**

    ---

    Tissue, diagnosis, age, sex and study fields keep explicit *reported / not-reported / not-applicable*
    status, so failures can be stratified instead of averaged away.

</div>

## Start in five minutes

=== "Read one sample"

    ```bash
    pip install huggingface_hub anndata pyarrow
    export REPO=zhang-lab/sMCC40M
    hf download "$REPO" examples/download_sample.py --repo-type dataset --local-dir .
    python examples/download_sample.py --repo "$REPO" --platform HD --sample HD-002
    python smcc_data/HD/samples/HD-002/read_example.py
    ```

=== "Try the benchmark offline"

    ```bash
    git clone https://github.com/aicb-ZhangLabs/sMMC40M.git
    cd sMMC40M
    python -m pip install -r benchmark/requirements-cpu.txt
    python benchmark/smcc_benchmark.py demo --output /tmp/smmc-demo
    python scripts/summarize_results.py
    ```

Then follow the [tutorials](tutorials/index.md), from reading one acquisition to
context-aware evaluation.
