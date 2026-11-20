# Contributing

Please open a repository issue with the release version, protocol track,
sample/fold IDs, software environment, and a small reproducible example.
Do not attach patient data, credentials, model weights, whole slides, or the
full expression/feature cache to issues or Git commits.

For code changes, run:

```bash
python -m pip install -r benchmark/requirements-cpu.txt
python -m unittest discover -s tests -v
python benchmark/smcc_benchmark.py demo --output /tmp/smmc-demo
python scripts/summarize_results.py
```

With the complete data-side benchmark package, also replay the affected track
and compare a real predictor refit. Keep published source results immutable.
Changes to cell membership, target selection, image preprocessing, metric
arithmetic, biological annotation, or source-material exclusion define a new
version/protocol and should not silently replace an old score.

Use explicit missing/unsupported states rather than fabricated zeros or cell
labels. Sample context and predicted cell types are not cell-level clinical
ground truth. Preserve upstream source attribution and applicable usage terms.

## Website

The project website is built from `website/` with MkDocs Material. The Website workflow checks
the build when site files change. To publish it, select **GitHub Actions** as the source in
**Settings → Pages**, then run the **Website** workflow from `main`.

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve          # live preview at http://127.0.0.1:8000
mkdocs build --strict # what CI runs
```

Tutorials are Jupyter notebooks in `website/tutorials/`. Notebooks are rendered as saved, never
executed during the build: run a notebook and save it with outputs to show results on the site.

### Posting a monthly data update

1. Make a CSV of the acquisitions added this month with the columns of `data/sample_catalog.csv`
   (at least `sample_id`, `platform`, `species`, `reporting_categories`, `gene_positive_observations`).
2. Generate the post, then add a sentence on what is notable:

   ```bash
   python scripts/new_monthly_update.py --month 2026-12 --samples new_2026-12.csv \
       --version 2026-12-01 --hf-revision <hugging face commit> --update-catalog
   ```

3. Check it with `mkdocs serve`, commit the post (and the catalog if updated), and push.
   The home page shows the three newest updates automatically.

Posts live in `website/updates/posts/`. Any other news (code releases, papers, talks) can be a
hand-written post there with `date:`, `slug:`, a category, a `# Title` and a `<!-- more -->` line.
