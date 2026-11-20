# Benchmark

**Task:** predict each cell's gene expression from its own H&E crop.
**Reference model:** frozen CONCH features from a 150 × 150 native-pixel crop →
StandardScaler → randomized PCA (≤128) → Ridge (`alpha = 10`), on `log1p` raw counts.
**Controls:** quadratic-coordinate Ridge and training-only 8-neighbour expression averaging.

## Snapshot

The coverage summary uses **18 Visium HD categories / 48 acquisitions** and **5 additional
Xenium-only categories / 13 acquisitions**, with four directional spatial holdouts and
50 training-only highly variable genes per fold. It is a descriptive category-weighted
combination, not a controlled comparison between assays.

| Coverage | Acquisitions | Gene Pearson | Gene Spearman | Cell Pearson | F1 | R² | RMSE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| HD: 18 categories | 48 | 0.365 | 0.333 | 0.445 | 0.411 | −0.090 | 0.458 |
| Xenium-only: 5 categories | 13 | 0.303 | 0.263 | 0.419 | 0.289 | −0.152 | 0.399 |
| **Combined: 23 categories** | **61** | **0.351** | **0.318** | **0.439** | **0.385** | **−0.103** | **0.445** |

- Spatial controls reach a combined Gene Pearson of only **0.049** (coordinates) and **0.057** (KNN).
- Negative R² means the model recovers **relative patterns**, not calibrated magnitudes.
- **Across acquisitions** (matched cells and genes): Gene Pearson **0.354 → 0.248**, Cell Pearson
  **0.563 → 0.349**, with drops in all 10 organ/species strata. Whole-acquisition validation over
  34 held-out HD acquisitions gives macro Gene Pearson **0.260**.

[All 23 categories](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/results/benchmark_23_categories.md) ·
[Full tables](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/results/README.md) ·
[Protocols and uncertainty](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/docs/protocols.md)

## Tracks

| Track | Scope | Test design |
| --- | --- | --- |
| `hd18` | 48 H&E acquisitions in 18 categories (+ auxiliary mixed TMA) | Four spatial holdouts, 50 training-only HVGs |
| `hd_cross` | 34 targets in 10 organ/species strata | Leave-one-acquisition-out, matched-edge, source-page-out |
| `xenium5` | 13 acquisitions in 5 extra categories | Native Xenium RNA, four spatial holdouts |
| `xenium_legacy`, `xenium_legacy_cross` | Historical campaigns | Preserved separately; never pooled |

Counts are acquisitions, not independent patients.

## Reproduce

```bash
# no data, no GPU
python benchmark/smcc_benchmark.py demo --output /tmp/smmc-demo
python scripts/summarize_results.py

# with the frozen release
export SMMC_RELEASE_ROOT=/path/to/2026-10-28
python benchmark/smcc_benchmark.py replay --track hd18 --sample HD-001 --output /tmp/smmc-replay
python benchmark/smcc_benchmark.py refit --fold hd18_HD-001_seed0 --output /tmp/smmc-refit
```

`replay` recomputes metrics from the original saved predictions (no retraining);
`refit` refits on exactly the frozen rows and targets from cached CONCH features.
Walkthrough: [Tutorial 5](tutorials/05_benchmark.ipynb). Full instructions:
[benchmark README](https://github.com/aicb-ZhangLabs/sMMC40M/blob/main/benchmark/README.md).
