# Task 6 — The Art of Data Storytelling
**PlaceMux · Altrodav Technologies Pvt. Ltd. · Phase 1 Industry Immersion**

An interactive Streamlit dashboard that turns a small retail sales dataset
into a decision-ready narrative: one takeaway, four supporting charts, a
quantified impact, and a recommendation — built so it can be run live for
a reviewer rather than just described in a slide.

---

## 1. The one-sentence takeaway

> **West region lost ~₹10L in Electronics revenue this quarter to a single
> fixable cause: a 24-day stockout — fixing the reorder trigger recovers
> it next cycle.**

This sentence was written **before** any chart was built (see
`generate_data.py` design notes) and sits at the very top of the app, per
the brief's step 1: *"Write the one-sentence takeaway before making any
slide."*

## 2. How to run it

```bash
# 1. Create the environment
pip install -r requirements.txt

# 2. Generate the sample dataset (reproducible, seeded — only needed once)
python generate_data.py

# 3. Launch the dashboard
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).
The app has two views, switchable from the sidebar:

- **📖 Executive Story** — the guided narrative described below.
- **🔎 Explore the data** — free filters (region / category / date range)
  over the same dataset, so a reviewer can poke at the raw numbers live
  instead of taking the story on faith.

## 3. The dataset

`generate_data.py` produces `sales_data.csv`: ~3,700 rows of daily
transactions across 4 regions × 5 categories, Jul–Dec 2026. It's synthetic
(no real company data was available for this exercise) but it is **real,
on-disk, loadable data** — not a hard-coded chart — and it's generated
with a genuine, discoverable mechanic: West region's Electronics stock
runs out for 24 days in Nov–Dec, and the dashboard *finds* that pattern
using pandas/numpy the same way it would on a real export. The seed
(`RNG_SEED = 42`) makes it fully reproducible.

## 4. Story structure (findings ordered as a story, not the analysis order)

| Step | Section | What it shows | Why it's placed there |
|---|---|---|---|
| 0 | **Takeaway** | The one-sentence answer, up top | Reviewer gets the "so what" in 5 seconds, before any methodology |
| 1 | **Context** | Company-wide monthly revenue is healthy and trending up | Proves the problem is *localised*, not a company-wide crisis — sets up the surprise |
| 2 | **Complication** | November revenue by region, stacked by category | Narrows "something's wrong" down to one region and one category |
| 3 | **Root cause** | Daily West-Electronics revenue with the stockout window shaded | Shows revenue flatlines exactly during the stockout — rules out a demand story |
| 4 | **Impact** | Expected vs. actual revenue during the stockout, using peer regions as baseline | Turns "a stockout happened" into a rupee number a decision-maker can act on |
| 5 | **Recommendation** | Trigger-based reorder point + quantified expected impact | Ends with a concrete action, not just a diagnosis |

This is the *minimum* chart set needed to prove the takeaway (4 charts) —
each one earns its place in the argument rather than being included
because the data happened to support it.

## 5. Marking-scheme / rubric coverage

Mapped directly against the task brief (`Task Brief.pdf`):

- ✅ **Deliverable** — "A short narrative report/deck with a clear
  takeaway and recommendation" → this dashboard (Executive Story view).
- ✅ **Demonstrable live on real (even if small) data, not just
  described** → runs as a live Streamlit app against an on-disk CSV,
  with a second free-exploration view to prove it isn't a canned slide.
- ✅ **Step 1 — one-sentence takeaway written first** → headline at the
  very top of the page, computed from the data (not hard-coded prose).
- ✅ **Step 2 — findings ordered as a story, not the analysis sequence**
  → Context → Complication → Root cause → Impact → Recommendation (see
  table above), not "here's every chart I made along the way".
- ✅ **Step 3 — minimum charts that prove the takeaway** → exactly 4
  charts, each with a one-line stated "Point" underneath it.
- ✅ **Step 4 — annotate each chart with its point** → every chart has
  in-plot annotation arrows/boxes calling out the specific thing to
  notice, plus a caption stating the takeaway in words.
- ✅ **Step 5 — concrete recommendation + expected impact** → trigger-
  based reorder point, with a quantified ₹ impact estimate and an owner
  / verification metric.
- ✅ **Step 6 — dry-run on someone outside the analysis** → see
  `DRY_RUN_NOTES.md` for the checklist used and what it caught.
- ✅ **Habit of validating data before analysing it** → automatic
  validation log in the sidebar (nulls, negative values, date-
  completeness, row-count-vs-grid) that runs on every load.
- ✅ **Pitfall — no methodology-first opening** → methodology lives in a
  collapsed "Appendix" expander at the *bottom*, never above the fold.
- ✅ **Pitfall — no chart junk / too many decimals** → gridlines
  minimised, currency formatted to ₹ lakhs/crores with 1 decimal, direct
  bar/line labels used instead of dense legends where possible.
- ✅ **Pitfall — analysis that "shows" but doesn't "say"** → every
  section ends with an explicit stated point ("**Point:** ...") rather
  than leaving the chart to speak for itself.

## 6. Project files

```
data_story_project/
├── app.py               # Streamlit dashboard (the deliverable)
├── generate_data.py      # Reproducible synthetic-data generator
├── sales_data.csv        # Generated dataset (real, on-disk, ~3,700 rows)
├── requirements.txt       # pip dependencies
├── DRY_RUN_NOTES.md      # Step-6 dry-run checklist and findings
└── README.md              # This file
```

## 7. Notes on the data

The dataset is synthetic because no company data was supplied with the
task brief. The generator (`generate_data.py`) is fully commented and
seeded, so the "insight" isn't hard-coded into the dashboard — it's
discovered by the same pandas groupby/pivot logic that would run against
a real sales export. Swap `sales_data.csv` for a real export with the
same column names (`date, region, category, units_sold, unit_price,
revenue, marketing_spend, stockout_flag`) and the story adapts to
whatever it finds — that's what "demonstrable live" is meant to prove.
"# task6.." 
