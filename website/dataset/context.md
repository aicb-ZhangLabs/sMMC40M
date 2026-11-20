# Sample context

Context is what turns an unexplained failure into a testable question. Every acquisition
carries source-backed sample fields, each with an explicit status.

## Fields

| Field | Example values | Status column |
| --- | --- | --- |
| `reporting_categories` | `["Ovary"]`, `["Breast"]` | — |
| `tissue`, `organ`, `species` | Ovary · Mouse | — |
| `sample_diagnosis`, `sample_condition` | `neoplastic_tissue`, `non_diseased_or_normal` | `sample_diagnosis_status`, `sample_condition_status` |
| `age_text`, `age_value`, `age_unit` | `8 weeks` → 8.0 week | `age_*_status` |
| `sex` | female | `sex_status` |
| `tumor_stage`, `tumor_grade` | | `tumor_*_status` |
| `donor_id_public`, `study_id`, `source_material_group_id` | | `*_status` |

Status values distinguish **reported**, **not reported in checked sources**, **not applicable**,
**conflict** and **inherited**. *Unknown does not mean healthy.*

## Coverage

- Age is available for **34** acquisitions and sex for **41**.
- Sample condition: 67 neoplastic, 39 non-diseased/normal, 7 reactive or hyperplastic,
  3 neurodegenerative disease or model, 1 mixed tissue array, 2 not applicable.
- Five known source-material groups span **16** acquisitions. These relations cannot establish
  that all other acquisitions represent independent donors.

## Why it matters: an example

In the paper, an ovary model trained on a donor over 60 lost **75% of its F1** on a donor under 40,
and its output became about **six times sparser**. Yet global distribution distances said the
younger target looked *closer* to the training data. Without age metadata this looks like noise;
with it, it becomes a testable shift. (A descriptive example: it does not isolate age from other
sample differences.)

[Tutorial 4](../tutorials/04_context_selection.ipynb) shows how to build context-matched and
context-shifted comparisons from the catalog.
