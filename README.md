# MexUniMCQ

[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.x-green.svg)](https://www.python.org/)

## Quick Links
- 📊 **Descriptive Statistics and Scripts:** `[LINK_OR_PATH]`  
- 📁 **Schema & Validation Scripts:** `[LINK_OR_PATH]`

## Table of Contents
- [Introduction](#introduction)
- [Dataset Overview](#dataset-overview)
- [Generation Process](#generation-process)
- [Descriptive Statistics](#descriptive-statistics)
- [Data Format & Schema](#data-format--schema)
- [Quality Checks](#quality-checks)
- [Limitations & Bias](#limitations--bias)
- [License](#license)
- [Citation](#citation)
- [Contact](#contact)

---

## Introduction

MexUniMCQ is a benchmark dataset of 3,500 multiple-choice questions (MCQs) in Spanish, intended for research in language models and educational evaluation. The dataset includes general academic subjects and topics requiring specific Mexican cultural, historical and legal context. All questions were generated using subject-specific prompts and multiple large language models; generation metadata and parameters are documented in this repository.

---

## Dataset Overview

- **Total number of questions:** `3, 500`  
- **Language:** Spanish  
- **Format:** JSONL (one JSON object per line)  
- **Options per question:** 4  
- **Difficulty labels:** `[PENDING]`  
- **Subject list:** `[LIST_OF_SUBJECTS]`  

This dataset is intended as an open research benchmark and not as an exam preparation tool.

---

## Generation Process

The dataset was generated using structured prompts tailored to each subject and executed with multiple large language models. Generation metadata — including model names, configuration parameters, and prompt templates — are stored in this repository under YAML specification files.

### Models and Configurations
| Model Identifier | Architecture | Parameters | Key Generation Settings |
|------------------|--------------|------------|--------------------------|
| `[MODEL_1]`       | `[ARCH]`     | `[SIZE]`   | `[TEMP / TOP_P / ETC.]`  |
| `[MODEL_2]`       | `[ARCH]`     | `[SIZE]`   | `[TEMP / TOP_P / ETC.]`  |
| ...              | ...          | ...        | ...                      |

Prompt templates per subject are in `subjects/[SUBJECT].txt`. Generation configurations are detailed in YAML files (e.g., `model_generation_info.yaml`, `model_specifications_[SUBJECT].yaml`).

---

## Descriptive Statistics

These descriptive statistics summarize the dataset contents; values should be filled once computed.

### Distribution by Subject
| Subject | Count | Percentage | Example Topics |
|---------|-------|------------|----------------|
| `[SUBJECT_1]` | `[N1]` | `[P1%]` | `[TOPICS]` |
| `[SUBJECT_2]` | `[N2]` | `[P2%]` | `[TOPICS]` |
| … | … | … | … |
| **Total** | 3,500 | 100% | — |

### Difficulty Distribution (pending)
| Difficulty Level | Count | % |
|------------------|-------|---|
| Easy | `[COUNT]` | `[P%]` |
| Medium | `[COUNT]` | `[P%]` |
| Hard | `[COUNT]` | `[P%]` |

### Correct Answer Balance
| Option | Count | % |
|--------|-------|---|
| A | `[COUNT_A]` | `[P_A%]` |
| B | `[COUNT_B]` | `[P_B%]` |
| C | `[COUNT_C]` | `[P_C%]` |
| D | `[COUNT_D]` | `[P_D%]` |

### Text Length Statistics
- **Average words per question:** `[AVG_Q_LEN]`  
- **Median words per question:** `[MED_Q_LEN]`  
- **Average words per option:** `[AVG_OPT_LEN]`

### Vocabulary
- **Unique terms:** `[VOCAB_COUNT]`  
- **Top frequent terms:** `[TOP_TERMS_LIST]`

Descriptive analysis was computed using the notebook provided on `[LINK_OR_PATH]`.

---

## Data Format & Schema

Each dataset entry is a JSON object with the following schema:

```json
{
  "id": "mxmcq_000123",
  "subject": "[SUBJECT]",
  "question": "[TEXT]",
  "options": {
    "A": "[OPTION_A]",
    "B": "[OPTION_B]",
    "C": "[OPTION_C]",
    "D": "[OPTION_D]"
  },
  "answer": "[CORRECT_OPTION]",
  "difficulty": "[LEVEL_IF_APPLICABLE]",
  "source": "synthetic_llm"
}
```

Field descriptions:

* `id`: Unique identifier
* `subject`: Academic/cultural subject
* `question`: The prompt text
* `options`: Answer choices (A–D)
* `answer`: Correct choice label
* `difficulty`: Optional difficulty label
* `source`: Origin of generation

---

## Quality Checks

Basic sanity checks completed:

* JSONL parsing: `[PASSED/FAILED]`
* Unique IDs: `[YES/NO]`
* All entries have 4 options: `[YES/NO]`
* Answers contained in options: `[YES/NO]`
* Duplicate entry count: `[NUMBER]`
* Schema validation errors: `[NUMBER]`


---

## Limitations & Bias

* This dataset is **synthetic** — patterns and biases from underlying language models may be present.
* Cultural and regional knowledge representation is not guaranteed comprehensive.

---

## License

This dataset and all accompanying documentation are licensed under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**. Users may share, adapt, and redistribute the dataset in any medium or format for any purpose, even commercially, provided appropriate credit is given, a link to the license is included, and changes are indicated if applicable. 

A copy of the full license is provided in `LICENSE-CC-BY-4.0.txt`.

---

## Citation

Please cite the dataset when used in research. A future arXiv preprint and evaluation results will be provided:

```bibtex
@dataset{mexunimcq_dataset,
  title     = {MexUniMCQ: A Multiple-Choice Question Benchmark in Spanish},
  author    = {[AUTHOR_LIST]},
  year      = {[YEAR]},
  publisher = {Creative Commons Attribution 4.0},
  url       = {[REPOSITORY_OR_DATASET_URL]}
}
```

Paper citation (to be added upon publication):

```bibtex
@article{mexunimcq_arxiv,
  title   = {MexUniMCQ: …},
  author  = {[AUTHOR_LIST]},
  journal = {arXiv preprint arXiv:[ID]},
  year    = {[YEAR]}
}
```

---

## Contact

* Maintainer: `GERMÁN HEBERTO PANCARDO ORTEGA`
* Email: `ghpancardo@gmail.com`
* GitHub Issues: Use this repository’s issue tracker
