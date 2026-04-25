# BeeProject

**Semi-automated digitization of historical handwritten tabular records.**

BeeProject combines computer vision and optical character recognition (OCR) to detect the grid structure of scanned paper forms and extract their handwritten content into structured JSON. It was developed to digitize beekeeping observation records collected across Germany as part of the MonViA research project.

![Workflow]( ./resources/readmeImgs/workflow.png "Two-step digitization workflow")

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
Each scan is aligned to the template, preprocessed to remove handwriting from the background, and passed to one or more OCR services. Recognized text is mapped back to individual cells and exported as a structured JSON record.

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

# Step 2 — digitize the filled forms
bee digitize \
  --dataset     resources/play-data/test_data_2014 \
  --output      resources/play-data/results \
  --credentials resources/credentials/credentials_google.json \
  --table       resources/play-data/extracted_form/table.json
```

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
bee digitize -d DIR -o DIR -c FILE -t FILE [options]
```

| Flag | Long form | Type | Default | Description |
|------|-----------|------|---------|-------------|
| `-d` | `--dataset` | path | **required** | Directory of filled form images (`.png`) |
| `-o` | `--output` | path | **required** | Output directory for results |
| `-c` | `--credentials` | path | **required** | OCR credentials `.json` file |
| `-t` | `--table` | path | **required** | Table definition `.json` from the extract step |
| | `--no-transform` | flag | off | Skip alignment to reference |
| `-D` | `--debug` | flag | off | Save intermediate images to `output/debug/` |

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

```json
{
  "1": {
    "google": [
      { "cell": "F3",  "text": "12.4", "confidence": 0.91 },
      { "cell": "F4",  "text": "11.8", "confidence": 0.87 }
    ],
    "azure": [
      { "cell": "F3",  "text": "12.4", "confidence": 0.95 }
    ]
  }
}
```

<!-- TODO: add annotated schema diagrams here -->

---

## OCR credentials

BeeProject supports three cloud OCR services and one local engine. Place credential files anywhere and point to them with `--credentials`.

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
    "aws_access_key_id": "YOUR_KEY_ID",
    "aws_secret_access_key": "YOUR_SECRET",
    "region_name": "eu-central-1"
}
```

### Tesseract (local, no credentials required)

Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) locally. No credential file needed — pass any valid `.json` file as a placeholder.

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
