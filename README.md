# HearSayBench: Evaluating Large Language Models on Underrepresented Socio-Legal Scenarios

[![License: CC BY 4.0](https://img.shields.io/badge/License_CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/aliIranmanesh/hearsay)

HearSayBench is a 400-scenario benchmark for testing whether language models can reason about lived constraints that are often absent from generic advice and web-based training data. It uses Amartya Sen's Capabilities Approach to evaluate pragmatic understanding, substantive freedom, register appropriateness, and honesty about uncertainty across underrepresented socio-legal situations.

## Dataset

The scenario dataset is available on [Hugging Face](https://huggingface.co/datasets/aliIranmanesh/hearsay):

```python
from datasets import load_dataset

dataset = load_dataset("aliIranmanesh/hearsay")
print(dataset["train"][0])
```

The train split contains 400 records with the fields `id`, `scenario`, `prompt`, `weird_prior`, `impediment`, `category`, and `subtype`. The GitHub repository also contains [`dataset_readable.csv`](dataset_readable.csv), a row-level evaluation table for the reported model results.

## Repository contents

```text
README.md
dataset_readable.csv       # Row-level evaluation table
entries.txt                 # Curated source entries
docs/data/scenarios.json    # Web scenario explorer data
docs/data/leaderboard.json  # Web leaderboard data derived from dataset_readable.csv
docs/charts/                # Camera-ready figures used by the project page
run_pipeline.py             # End-to-end evaluation pipeline
run_batch.py                # Response collection
run_judge.py                # Capability judging
harm_eval.py                # Harm evaluation
analyze.py                  # Analysis utilities
merge.py                    # Local result-merging utility
llm_client.py               # Provider clients using environment variables
```

The large intermediate response and merged-output directories are intentionally excluded from the public release. Run-time outputs can be generated locally with the pipeline when needed.

## Reproducing evaluations

Install dependencies and configure credentials from `.env.example`:

```bash
pip install -r requirements.txt
cp .env.example .env
python run_pipeline.py aliIranmanesh/hearsay --model gemini-2.5-flash
```

## Citation

```bibtex
@inproceedings{iranmanesh2026hearsaybench,
  title={HEARSAYBENCH: Can LLMs Navigate from Abstract Human Rights to Lived Lives?},
  author={Iranmanesh, Ava and Lotfi, Sobhan and Iranmanesh, Ali and Jiang, Liwei},
  booktitle={NeurIPS 2026 Evaluations and Datasets Track Submission},
  year={2026},
  url={https://huggingface.co/datasets/aliIranmanesh/hearsay}
}
```

## License

This benchmark dataset is distributed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.
