# Financial Accelerator / Credit Channel Classification Tool

Human validation tool for Claude's classifications of FOMC speaker beliefs about the credit channel - whether credit market conditions affect or amplify economic activity.

## Quick Links

- **GitHub Repo:** [TBD after push]
- **Live Tool:** [TBD after Streamlit deployment]

---

## Purpose

We used Claude to classify ~64,000 FOMC transcript quotes for beliefs about the credit channel mechanism. This tool allows human coders to independently classify a stratified sample of ~200 quotes, enabling us to measure Claude's accuracy.

**What we're measuring:**
- Does the speaker believe credit conditions **significantly amplify** economic shocks through feedback?
- Does the speaker believe credit conditions **directly affect** economic activity?
- Does the speaker believe credit has **little/no effect** on activity?
- Classification categories: STRONG, MODERATE, WEAK, NULL

---

## Folder Structure

```
accelerator/
├── README.md                              # This file
├── coding_interface.py                    # Streamlit app (deployed)
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Excludes large files from git
├── Financial_Accelerator_QuickStart.md   # Quick reference for coders
├── financial_accelerator_prompt.txt       # Claude's classification prompt
├── validation_samples/
│   └── production/
│       ├── coding_financial_accelerator.csv  # ~200 sampled arguments
│       └── stats_financial_accelerator.json  # Sample statistics
└── sampler/                               # LOCAL ONLY (not deployed)
    └── financial_accelerator_sampler.py   # Script to generate samples
```

**Note:** The `sampler/` folder and `.pkl` files are in `.gitignore` and not pushed to GitHub.

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
| **STRONG** | Credit conditions SIGNIFICANTLY AMPLIFY shocks through feedback effects |
| **MODERATE** | Qualified amplification OR direct credit effects on activity |
| **WEAK** | Credit conditions have LITTLE/NO effect on economic activity |
| **NULL** | No credit channel belief expressed (default) |

### Key Concept: Three Types of Relationships

1. **Amplification (STRONG/MODERATE):** Credit conditions amplify shocks through feedback
2. **Direct Effect (MODERATE):** Credit affects activity, but no feedback language
3. **Denial (WEAK):** Credit doesn't meaningfully affect activity

### Important

- **Save often!** Download your CSV every 20-30 arguments
- To resume: upload your saved CSV via "Resume Session"
- When in doubt, select NULL

See `Financial_Accelerator_QuickStart.md` for detailed guidelines and examples.

---

## For Project Leads

### Deploying to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: `[your-username]/accelerator`
   - Branch: `main`
   - Main file: `coding_interface.py`
5. Click "Deploy"

### Updating the Sample Data

If you need to regenerate the sample:

```bash
cd accelerator
python sampler/financial_accelerator_sampler.py
```

This will:
1. Load `financial_accelerator_classifications.pkl` and join with source data
2. Deduplicate quotations
3. Create a stratified sample (60 STRONG, 29 MODERATE, 60 WEAK, 50 NULL)
4. Output to `validation_samples/production/coding_financial_accelerator.csv`

Then commit and push:
```bash
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
| `claude_credit_channel_category` | Claude's category (strong, moderate, weak, null) |
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

## Classification Mapping

| Claude Value | Category | Meaning |
|--------------|----------|---------|
| 1.0 | strong | Significant amplification through feedback |
| 0.0 | moderate | Qualified amplification OR direct credit effects |
| -1.0 | weak | Little/no effect on activity |
| NaN | null | No belief expressed |

---

## Contact

For technical issues with the tool, check the GitHub issues or contact the project lead.
