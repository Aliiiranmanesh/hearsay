# HearSayBench: Evaluating Large Language Models on Underrepresented Socio-Legal Scenarios

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/aliIranmanesh/hearsay)
[![Croissant Metadata](https://img.shields.io/badge/Metadata-Croissant_1.0-blue)](https://mlcommons.org/croissant/)
[![NeurIPS Submission](https://img.shields.io/badge/NeurIPS-Datasets_&_Benchmarks_2026-brightgreen)](#)

**HearSayBench** is a specialized evaluation benchmark designed to assess whether Large Language Models (LLMs) maintain accurate world models for individuals whose real-world struggles are structurally underrepresented in web training corpora.

Applying the **Capabilities Approach** (Sen, 1999; Nussbaum, 2011) as a theoretical framework, HearSayBench models situations where individuals' substantive freedom is restricted by latent, non-demographic barriers (totalitarian controls, travel bans, localized customs, caste systems).

---

## Dataset Access (Hugging Face)

The complete **400-scenario benchmark dataset** is hosted on Hugging Face Datasets and can be loaded directly in Python:

```python
from datasets import load_dataset

# Load HearSayBench dataset (400 hand-curated socio-legal scenarios)
dataset = load_dataset("aliIranmanesh/hearsay")
print(dataset["train"][0])
```

The published dataset has one `train` split containing 400 records. Hugging Face loads it from [`data/train-00000-of-00001.parquet`](https://huggingface.co/datasets/aliIranmanesh/hearsay/blob/main/data/train-00000-of-00001.parquet).

The published `scenario` and `prompt` fields were synchronized with the corrected `entries.txt`. The `category`, `impediment`, and `subtype` annotations were checked against the reference workbook and match all 400 entries. The `weird_prior` annotations were retained from the existing dataset; the reference workbook does not contain that field.

### Key Features
Each record in the dataset contains:

1. `id`: Unique scenario identifier (`entry_0001` to `entry_0400`).
2. `scenario`: Ground-truth real-world context of the underrepresented individual's situation.
3. `prompt`: First-person natural text query representing the individual's request (without demographic labels or explicit jargon).
4. `weird_prior`: Standard Western-centric recommendation (formal legal/institutional resources) that generic models tend to suggest but are dangerous or ineffective.
5. `impediment`: The specific social, personal, or legal conversion factor that negates the Western resource.
6. `category`: Broader social constraint domain classification (`Social`, `Personal`, `Environmental`).
7. `subtype`: Subclass of the social impediment (`Public Policy & Law`, `Social Norms`, `Power Relations`, etc.).

---

## Repository Structure

```text
hearSay/
├── docs/                          # Web presentation, leaderboard data, and charts
├── .env.example                   # API credentials template
├── .gitignore                     # Git ignore rules
├── README.md                      # Dataset access, benchmark results, and usage
├── analyze.py                     # Scoring and statistical analysis
├── croissant.json                 # Machine-readable dataset metadata
├── evaluator.py                   # Capability evaluation prompts and templates
├── harm_eval.py                   # Immediate and societal harm evaluation
├── llm_client.py                  # Model provider API clients
├── merge.py                       # Merge per-model evaluation results
├── metadata.json                  # Dataset metadata
├── requirements.txt               # Python dependencies
├── run_batch.py                   # Collect model responses
├── run_judge.py                   # Grade model responses
└── run_pipeline.py                # Run the evaluation pipeline
```

The `docs/` directory contains the web presentation (`index.html`, `app.js`, and `style.css`), supporting data in `docs/data/`, and visualizations in `docs/charts/`. Pipeline runs write responses to `responses/` and consolidated scores, reports, and charts to `merged/` by default.


---

## Quick Start & Pipeline Usage

### Prerequisites & Installation

1. **Clone Repository & Install Dependencies**:
   ```bash
   git clone https://github.com/Aliiiranmanesh/hearSay.git
   cd hearSay
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   Copy `.env.example` to `.env` and fill in your API credentials:
   ```bash
   cp .env.example .env
   ```

---

### Running the Pipeline

To run the pipeline using the live Hugging Face dataset:

```bash
# Full pipeline execution
python run_pipeline.py aliIranmanesh/hearsay --model gemini-3.5-flash

# Run specific steps (e.g. gather responses or run judge)
python run_pipeline.py aliIranmanesh/hearsay --steps responses --delay 1.5
python run_pipeline.py aliIranmanesh/hearsay --steps judge --model gemini-3.5-flash
```

---

## Citation

If you use **HearSayBench** in your research, please cite our paper:

```bibtex
@inproceedings{iranmanesh2026hearsaybench,
  title={HEARSAYBENCH: Can LLMs Navigate from Abstract Human Rights to Lived Lives?},
  author={Iranmanesh, Ava and Lotfi, Sobhan and Iranmanesh, Ali and Jiang, Liwei},
  booktitle={NeurIPS 2026 Evaluations and Datasets Track Submission},
  year={2026},
  url={https://huggingface.co/datasets/aliIranmanesh/hearsay}
}
```


---

## License
This benchmark dataset is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
