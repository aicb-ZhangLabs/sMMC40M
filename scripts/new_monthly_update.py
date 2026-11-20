#!/usr/bin/env python
"""Write a monthly data-update post for the website.

Give it a CSV of the acquisitions added this month, using the columns of
data/sample_catalog.csv (at least sample_id, platform, species, reporting_categories,
gene_positive_observations; tissue, sample_condition, age_text and sex are shown when present).

    python scripts/new_monthly_update.py --month 2026-12 --samples new_2026-12.csv \
        --version 2026-12-01 --hf-revision <commit sha>

It writes website/updates/posts/<month>-data-update.md. Review the text, add a sentence on what is
notable, then commit. With --update-catalog it also appends the rows to data/sample_catalog.csv.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["sample_id", "platform", "species", "reporting_categories", "gene_positive_observations"]
PLATFORM_NAME = {"HD": "Visium HD", "Xenium": "Xenium"}


def categories(value):
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else [str(parsed)]
    except (TypeError, ValueError):
        return [s.strip() for s in str(value).split(";") if s.strip()]


def fmt(n):
    return f"{int(n):,}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--month", required=True, help="YYYY-MM of the update")
    ap.add_argument("--samples", required=True, type=Path, help="CSV of newly added acquisitions")
    ap.add_argument("--date", help="post date YYYY-MM-DD (default: today)")
    ap.add_argument("--version", help="data version label, e.g. 2026-12-01")
    ap.add_argument("--hf-revision", help="Hugging Face commit to pin for this version")
    ap.add_argument("--title", help="custom post title")
    ap.add_argument("--note", default="", help="one or two sentences on what is notable this month")
    ap.add_argument("--catalog", type=Path, default=ROOT / "data/sample_catalog.csv")
    ap.add_argument("--update-catalog", action="store_true", help="append the new rows to the catalog")
    ap.add_argument("--force", action="store_true", help="overwrite an existing post")
    args = ap.parse_args()

    month = dt.datetime.strptime(args.month, "%Y-%m")
    date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    new = pd.read_csv(args.samples)
    missing = [c for c in REQUIRED if c not in new.columns]
    if missing:
        raise SystemExit(f"{args.samples} is missing columns: {missing}")
    old = pd.read_csv(args.catalog)
    dup = sorted(set(new.sample_id) & set(old.sample_id))
    if dup:
        raise SystemExit(f"sample_id already in the catalog: {dup}")
    if new.sample_id.duplicated().any():
        raise SystemExit("duplicate sample_id in the new samples file")

    new["_cats"] = new.reporting_categories.apply(categories)
    old["_cats"] = old.reporting_categories.apply(categories)
    both = pd.concat([old, new], ignore_index=True)

    n_new, obs_new = len(new), new.gene_positive_observations.sum()
    by_platform = new.groupby("platform").agg(n=("sample_id", "size"), obs=("gene_positive_observations", "sum"))
    new_cats = sorted(set(new._cats.explode()) - set(old._cats.explode()))
    new_species = sorted(set(new.species) - set(old.species))

    title = args.title or f"{month:%B %Y} data update: {n_new} new acquisition{'s' if n_new != 1 else ''}"
    summary = (f"{n_new} acquisition{'s' if n_new != 1 else ''} and **{fmt(obs_new)}** gene-positive "
               f"observations added; the release now has **{len(both)} acquisitions** and "
               f"**{fmt(both.gene_positive_observations.sum())}** gene-positive observations.")

    lines = ["---", f"date: {date.isoformat()}", f"slug: data-update-{args.month}",
             "categories:", "  - Data update", "---", "", f"# {title}", "", summary]
    if args.note:
        lines += ["", args.note]
    lines += ["", "<!-- more -->", "", "## Added this month", "",
              "| Platform | Acquisitions | Gene-positive observations |", "| --- | ---: | ---: |"]
    for platform, row in by_platform.iterrows():
        lines.append(f"| {PLATFORM_NAME.get(platform, platform)} | {row.n} | {fmt(row.obs)} |")
    lines.append(f"| **Total** | **{n_new}** | **{fmt(obs_new)}** |")
    if new_cats:
        lines += ["", f"New reporting categories: {', '.join(new_cats)}."]
    if new_species:
        lines += ["", f"New species: {', '.join(new_species)}."]

    cols = [c for c in ["sample_id", "platform", "species", "tissue", "sample_condition", "sex", "age_text",
                        "gene_positive_observations"] if c in new.columns]
    header = {"sample_id": "Sample", "platform": "Platform", "species": "Species", "tissue": "Tissue",
              "sample_condition": "Condition", "sex": "Sex", "age_text": "Age",
              "gene_positive_observations": "Gene-positive obs."}
    lines += ["", "## Samples", "", "| " + " | ".join(header[c] for c in cols) + " | Categories |",
              "| " + " | ".join("---:" if c == "gene_positive_observations" else "---" for c in cols) + " | --- |"]
    for _, r in new.sort_values("sample_id").iterrows():
        cells = [fmt(r[c]) if c == "gene_positive_observations" else ("" if pd.isna(r[c]) else str(r[c]))
                 for c in cols]
        lines.append("| " + " | ".join(cells) + f" | {', '.join(r._cats)} |")

    lines += ["", "## Totals after this update", "",
              "| Platform | Acquisitions | Gene-positive observations |", "| --- | ---: | ---: |"]
    for platform, row in both.groupby("platform").agg(n=("sample_id", "size"),
                                                      obs=("gene_positive_observations", "sum")).iterrows():
        lines.append(f"| {PLATFORM_NAME.get(platform, platform)} | {row.n} | {fmt(row.obs)} |")
    lines.append(f"| **Total** | **{len(both)}** | **{fmt(both.gene_positive_observations.sum())}** |")

    lines += ["", "## Get it", ""]
    if args.version:
        lines.append(f"- Data version: **{args.version}**")
    if args.hf_revision:
        lines.append(f"- Pin this revision: [`{args.hf_revision[:12]}`]"
                     f"(https://huggingface.co/datasets/zhang-lab/sMCC40M/tree/{args.hf_revision})")
    lines.append("- Download one sample: `python examples/download_sample.py --repo zhang-lab/sMCC40M "
                 f"--platform {new.platform.iloc[0]} --sample {new.sort_values('sample_id').sample_id.iloc[0]}` "
                 "([details](../../dataset/download.md))")
    lines.append("- The frozen benchmark is unchanged; new acquisitions are not part of its reported scores "
                 "unless stated.")

    out = ROOT / "website/updates/posts" / f"{args.month}-data-update.md"
    if out.exists() and not args.force:
        raise SystemExit(f"{out} exists; use --force to overwrite")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")

    if args.update_catalog:
        merged = pd.concat([old.drop(columns="_cats"), new.drop(columns="_cats")], ignore_index=True)
        merged.to_csv(args.catalog, index=False)
        print(f"appended {n_new} rows to {args.catalog.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
