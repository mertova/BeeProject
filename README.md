# BeeProject

[![Tests](https://github.com/mertova/BeeProject/actions/workflows/tests.yml/badge.svg)](https://github.com/mertova/BeeProject/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Paper](https://img.shields.io/badge/JCDL'24-10.1145/3677389.3702599-b31b1b.svg)](https://doi.org/10.1145/3677389.3702599)
[![Dataset](https://img.shields.io/badge/dataset-FAIRDOMHub-1abc9c.svg)](https://doi.org/10.15490/FAIRDOMHUB.1.DATAFILE.7415.1)

**Semi-automated digitization of historical handwritten tabular records.**

Reference implementation for the JCDL'24 paper *The BeeProject: Advanced Digitisation and Creation of a Dataset for the Monitoring of Beehives* [[1]](#references). BeeProject combines feature-based image alignment, Hough-transform grid detection, and cloud OCR to recover structured records from scanned paper forms — a setting where layout is irregular, ink degrades, and modern table-extraction models trained on born-digital PDFs fall over.

The pipeline was developed to digitize beekeeping observation records collected across five German states (Lower Saxony, Hesse, Mecklenburg-Vorpommern, Thuringia, Brandenburg) by the Institute of Bee Protection (JKI) under the [MonViA](https://www.julius-kuehn.de/en/institute-for-bee-protection/) project. The released ground-truth covers **3,819 scans and 30,552 annotated cells from 1998–2017**. On this benchmark the pipeline achieves **CER ≈ 5%** and **WER ≈ 13%** with TrOCR or Google Vision as the OCR backend, with SIFT-based alignment correctly registering 95% of forms.

> *Status: maintained for reproducibility of the JCDL'24 paper. Issues and PRs welcome.*

<p align="center">
  <img src="resources/readmeImgs/workflow.png" alt="Two-step digitization workflow" width="720">
</p>

---

## Contents

- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Installation](#installation)
- [CLI reference](#cli-reference)
  - [bee extract](#bee-extract)
  - [bee digitize](#bee-digitize)
- [Output format](#output-format)
- [OCR credentials](#ocr-credentials)
- [Project structure](#project-structure)
- [Dataset](#dataset)
- [References](#references)

---

## How it works

Digitization runs in two steps:

**Step 1 — Template extraction (`bee extract`)**
A clean, averaged template is recovered from a batch of handwritten sample scans using feature matching (SIFT or ORB). The Hough line transform then detects the table grid and produces a cell map in JSON.

**Step 2 — Digitization (`bee digitize`)**
Each scan is aligned to the template, preprocessed to remove handwriting from the background, and passed to an OCR backend (Google Vision, Azure, AWS Textract, or local Tesseract). Recognized text is mapped back to individual cells and exported as a structured JSON record.

---

## Quick start

Run the bundled sample dataset in three commands:

```shell
git clone https://github.com/mertova/BeeProject.git
cd BeeProject
pip install -e .
```

```shell
# Step 1 — extract template and table structure
bee extract \
  --dataset  resources/play-data/test_data_2014 \
  --reference resources/form1/reference.png \
  --output   resources/play-data/extracted_form

# Step 2 — digitize the filled forms (Tesseract runs locally, no credentials needed)
bee digitize \
  --dataset resources/play-data/test_data_2014 \
  --output  resources/play-data/results \
  --service tesseract \
  --table   resources/play-data/extracted_form/table.json
```

Tesseract needs the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) binary installed locally. For the cloud backends used to produce the paper's reported CER/WER numbers (Google Vision, Azure), see [OCR credentials](#ocr-credentials).

---

## Installation

Requires Python 3.10 or newer.

```shell
pip install -e .
```

This registers the `bee` command globally in your environment. Verify with:

```shell
bee --help
```

### Running tests

```shell
pip install -e ".[test]"
pytest
```

Tests that call live OCR services or reference the author's private full-size dataset skip automatically when credentials or that dataset aren't present.

---

## CLI reference

### `bee extract`

Recovers a clean empty template from a batch of sample scans and detects the table grid.

```
bee extract -d DIR -r FILE [options]
```

| Flag | Long form | Type | Default | Description |
|------|-----------|------|---------|-------------|
| `-d` | `--dataset` | path | **required** | Directory of sample scan images (`.png`) |
| `-r` | `--reference` | path | **required** | Representative reference image |
| `-o` | `--output` | path | `./resources/data/extraction` | Output directory |
| `-ev` | `--eps-v` | int | `15` | Epsilon for vertical grid lines |
| `-eh` | `--eps-h` | int | `20` | Epsilon for horizontal grid lines |
| `-l` | `--limit` | int | `15` | Maximum number of sample images to use |
| `-a` | `--algo` | `sift`\|`orb` | `sift` | Feature matching algorithm |
| | `--transform` / `--no-transform` | flag | on | Align samples to reference image |
| | `--averaging` / `--no-averaging` | flag | on | Enable pen elimination via averaging |

**Outputs** written to `--output`:

| File | Description |
|------|-------------|
| `template.png` | Clean averaged form image |
| `table.json` | Cell map with coordinates for every detected cell |

---

### `bee digitize`

Aligns, preprocesses, and OCR-processes each scan. Maps recognized text to table cells.

```
bee digitize -d DIR -o DIR -t FILE [-s SERVICE] [-c FILE] [options]
```

| Flag | Long form | Type | Default | Description |
|------|-----------|------|---------|-------------|
| `-d` | `--dataset` | path | **required** | Directory of filled form images (`.png`) |
| `-o` | `--output` | path | **required** | Output directory for results |
| `-t` | `--table` | path | **required** | Table definition `.json` from the extract step |
| `-s` | `--service` | `google`\|`azure`\|`aws`\|`tesseract` | `google` | OCR backend to run |
| `-c` | `--credentials` | path | required unless `--service tesseract` | OCR credentials `.json` file, shaped per [OCR credentials](#ocr-credentials) |
| | `--no-transform` | flag | off | Skip alignment to reference |
| `-D` | `--debug` | flag | off | Save intermediate images to `output/debug/` |

Each run digitizes with exactly one OCR backend. To compare backends on the same dataset, run `bee digitize` once per `--service` value into separate output directories.

**Output** written to `--output`:

| File | Description |
|------|-------------|
| `out_<dataset>.json` | Digitized records, keyed by image ID |
| `debug/` | Preprocessed and annotated images (only with `-D`) |

---

## Output format

### `table.json` — cell map

```json
{
  "template": "resources/play-data/extracted_form/template.png",
  "shape": [8, 35],
  "cells": [
    { "text": "A0", "pt1": { "x": 0,  "y": 0   }, "pt2": { "x": 71,  "y": 287 } },
    { "text": "B0", "pt1": { "x": 71, "y": 0   }, "pt2": { "x": 211, "y": 287 } }
  ]
}
```

Cell identifiers follow spreadsheet notation: column letter + row number (`A0`, `B3`, `F12`, …).

### `out_<dataset>.json` — digitized records

Records are keyed by image ID, then by the `--service` used for that run:

```json
{
  "1": {
    "google": [
      { "cell": "F3",  "text": "12.4", "confidence": 0.91 },
      { "cell": "F4",  "text": "11.8", "confidence": 0.87 }
    ]
  }
}
```

---

## OCR credentials

BeeProject supports three cloud OCR services and one local engine, selected per run with `--service`. Place credential files anywhere and point to them with `--credentials` (not needed for `--service tesseract`).

### Google Vision

1. Create a project at [Google Cloud Console](https://cloud.google.com/)
2. Enable the **Cloud Vision API**
3. Create a service account and download the JSON key file
4. Documentation: [Cloud Vision — Handwriting](https://cloud.google.com/vision/docs/handwriting)

```json
{
    "type": "service_account",
    "project_id": "your_project",
    "private_key_id": "...",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...",
    "client_email": "google-vision@your_project.iam.gserviceaccount.com",
    "client_id": "...",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "",
    "universe_domain": "googleapis.com"
}
```

### Microsoft Azure Computer Vision

1. Create a Computer Vision resource in the [Azure Portal](https://portal.azure.com/)
2. Copy your subscription key and endpoint
3. Guide: [Transcribing handwritten text with Azure](https://programminghistorian.org/en/lessons/transcribing-handwritten-text-with-python-and-azure)

```json
{
    "microsoft_api_key": {
        "SUBSCRIPTION_KEY": "your_subscription_key",
        "ENDPOINT": "https://your_resource.cognitiveservices.azure.com/"
    }
}
```

### Amazon AWS Textract

1. Sign in to the [AWS Console](https://aws.amazon.com)
2. Set up IAM with Textract permissions
3. Generate an access key pair
4. Documentation: [Getting started with Textract](https://docs.aws.amazon.com/textract/latest/dg/getting-started.html)

```json
{
    "ACCESS_KEY": "YOUR_KEY_ID",
    "SECRET_KEY": "YOUR_SECRET",
    "REGION": "eu-central-1"
}
```

### Tesseract (local, no credentials required)

Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) locally and make sure the `tesseract` binary is on your `PATH`. Run with `--service tesseract` and omit `--credentials` entirely.

---

## Project structure

```
BeeProject/
├── resources/
│   ├── credentials/            # OCR service credential files
│   ├── data/                   # Extraction and digitization output
│   └── play-data/              # Bundled sample dataset
│       ├── test_data_2014/     # Sample scans
│       └── extracted_form/     # Pre-computed template and table
├── src/
│   ├── cli.py                  # CLI entry point (bee command)
│   ├── tsr.py                  # Table structure recognition
│   ├── form_analysis.py        # Template extraction pipeline
│   ├── digitize.py             # Digitization pipeline
│   ├── geometry/               # Line, rectangle, vertex primitives
│   ├── image_processing/       # Image, form, and reference processing
│   ├── ocr_services/           # Google, Azure, AWS, Tesseract connectors
│   └── table/                  # Table and cell data model
├── test/                       # Unit tests
├── pyproject.toml              # Package config and CLI entry point
└── README.md
```

---

## Dataset

![BeeProject Collection](./resources/readmeImgs/dataset.png "Sample forms from the BeeProject Collection")

The dataset contains beekeeping observation records collected by the **Institute of Bee Protection (JKI)** from beekeeper associations in Lower Saxony, Hesse, Mecklenburg-Vorpommern, Thuringia, and Brandenburg as part of the [MonViA](https://www.julius-kuehn.de/en/institute-for-bee-protection/) project.

| Resource | Link |
|----------|------|
| Sample dataset | [GitHub — TheBeeProjectCollection](https://github.com/mertova/TheBeeProjectCollection.git) |
| Full dataset | [FAIRDOMHub](https://fairdomhub.org/data_files/7415?version=1) |

---

## References

<a id="1">[1]</a>
Lukrécia Mertová, Severin Polreich, Oleg Lewkowski, and Wolfgang Müller.
2024. The BeeProject: Advanced Digitisation and Creation of a Dataset
for the Monitoring of Beehives. In The 2024 ACM/IEEE Joint Conference on
Digital Libraries (JCDL ‘24), December 16–20, 2024, Hong Kong, China. ACM,
New York, NY, USA, 11 pages. https://doi.org/10.1145/3677389.3702599

<a id="2">[2]</a>
Mertová, L., Lewkowski, O., Polreich, S., & Müller, W. (2024).
*BeeProject-collection* [Data set].
FAIRDOMHub. https://doi.org/10.15490/FAIRDOMHUB.1.DATAFILE.7415.1
