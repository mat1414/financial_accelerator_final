# Financial Accelerator Classification Tool

Human validation tool for Claude's classifications of FOMC speaker beliefs about the financial accelerator/credit channel - how credit market conditions amplify economic shocks through feedback effects.

## Quick Links

- **GitHub Repo:** [TBD after push]
- **Live Tool:** [TBD after Streamlit deployment]

---

## Purpose

We used Claude to classify ~71,000 FOMC transcript quotes for beliefs about the financial accelerator mechanism. This tool allows human coders to independently classify a stratified sample of 200 quotes, enabling us to measure Claude's accuracy.

**What we're measuring:**
- Does the speaker believe credit market conditions **significantly amplify** economic shocks? (feedback effects)
- Does the speaker believe credit markets have **little amplifying effect**?
- Classification categories: STRONG, WEAK, MODERATE, NONE

---

## Folder Structure

```
accelerator/
├── README.md                              # This file
├── coding_interface.py                    # Streamlit app (deployed)
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Excludes large files from git
├── Financial_Accelerator_QuickStart.md   # Quick reference for coders
├── validation_samples/
│   └── production/
│       ├── coding_financial_accelerator.csv  # 200 sampled arguments
│       └── stats_financial_accelerator.json  # Sample statistics
└── sampler/                               # LOCAL ONLY (not deployed)
    └── financial_accelerator_sampler.py   # Script to generate samples
```

**Note:** The `sampler/` folder and `.pkl` files are in `.gitignore` and not pushed to GitHub. They contain large source data and are only needed to regenerate samples.

---

## For Coders

### Getting Started

1. Open the tool URL (provided separately)
2. Enter your name
3. Select "Use default sample"
4. Start classifying quotes

### Classification Categories

| Category | Meaning |
|----------|---------|
| **STRONG** | Credit markets SIGNIFICANTLY amplify economic shocks through feedback |
| **WEAK** | Credit markets have LITTLE/NO amplifying effect on shocks |
| **MODERATE** | Qualified or partial amplification mechanism |
| **NONE** | No financial accelerator belief expressed (default) |

### Key Concept: Amplification vs. Direct Effects

The financial accelerator is about **amplification through feedback**, not just direct effects:

- Direct effect: "Higher rates reduce borrowing" -> **NONE**
- Amplification: "Tighter credit weakens balance sheets, which further tightens credit" -> **STRONG**

### Important

- **Save often!** Download your CSV every 20-30 arguments
- To resume: upload your saved CSV via "Resume Session"
- When in doubt, select NONE

See `Financial_Accelerator_QuickStart.md` for detailed guidelines and examples.

---

## For Project Leads

### Deploying to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: `[your-username]/financial_accelerator`
   - Branch: `main`
   - Main file: `coding_interface.py`
5. Click "Deploy"

The app will rebuild automatically when you push changes to the GitHub repo.

### Updating the Sample Data

If you need to regenerate the 200-argument sample:

```bash
cd accelerator/sampler
python financial_accelerator_sampler.py
```

This will:
1. Load `../financial_accelerator_arguments_with_classification.pkl`
2. Deduplicate quotations
3. Create a stratified sample (50 per category)
4. Output to `../validation_samples/production/coding_financial_accelerator.csv`

Then commit and push:
```bash
cd ..
git add validation_samples/
git commit -m "Regenerate sample data"
git push origin main
```

### Analyzing Results

When coders complete their work, they'll download a CSV with these columns:

| Column | Description |
|--------|-------------|
| `coding_id` | Unique ID (e.g., FA_0042) |
| `original_index` | Index in source data for joining |
| `coder_name` | Who coded this |
| `classification` | Human's classification |
| `claude_credit_channel` | Claude's numeric value (1.0, 0.0, -1.0, NaN) |
| `claude_credit_channel_category` | Claude's category (strong, moderate, weak, none) |
| `quotation` | The quote text |
| `notes` | Coder's notes (if any) |

**To calculate agreement:**
```python
import pandas as pd

df = pd.read_csv('coded_results.csv')
df['agree'] = df['classification'] == df['claude_credit_channel_category']
print(f"Agreement rate: {df['agree'].mean():.1%}")
```

---

## Data Pipeline

```
financial_accelerator_arguments_with_classification.pkl (76K rows)
    │
    ▼ [Deduplicate on quotation]
    │
71K unique arguments
    │
    ▼ [sampler/financial_accelerator_sampler.py]
    │
coding_financial_accelerator.csv (200 rows, stratified sample)
    │
    ▼ [Human coders use Streamlit app]
    │
coded_[name]_financial_accelerator_[timestamp].csv
    │
    ▼ [Analysis]
    │
Agreement metrics, confusion matrix, etc.
```

---

## Classification Mapping

| Claude Value | Category | Meaning |
|--------------|----------|---------|
| 1.0 | strong | Significant amplification through feedback |
| 0.0 | moderate | Qualified/partial amplification |
| -1.0 | weak | Little/no amplification |
| NaN | none | No belief expressed |

---

## Contact

For technical issues with the tool, check the GitHub issues or contact the project lead.
