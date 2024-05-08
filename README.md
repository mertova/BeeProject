# BeeProject
Our task is to convert PDF scans of hand-written documents to digital form.

![The Workflow Scheme](/github_img/BeeProject-Diagram.png)

## Our Dataset Specification
Our dataset contains data from beekeepers. Documents are only in german language and are a mixture of machine-written and hand-written text. 

Three types of documents:
1. tables 
2. question - answer 
3. free text

Source: 
```bash
.
├── data
│   ├── scans      -- #examples of scaned documents in different formats
|   |   ├── pdf
|   |   └── png
│   ├── form1  -- #digitalized form1 (.xlsx - temporary)
|   └── ocr_results-form2    -- #outputs of different models applied on our scan examples
|       ├── HTSNet
|       └── Martine-DeepCurate
```

### Related projects (models)
Tobias Martine (DeepCurate) - https://github.com/TobiasMartine/DeepCurate

EDD-architecture - https://github.com/ibm-aur-nlp/EDD

HTSNet - https://github.com/jottue/HTSNet --> Does not work!!!

### Available datasets
IAM Handwriting Database - https://fki.tic.heia-fr.ch/databases/iam-handwriting-database

PubTabNet - https://github.com/ibm-aur-nlp/PubTabNet

https://www.primaresearch.org/datasets

https://drive.google.com/file/d/1Q4kDiJts-yi9IhsYT6ku5Y4WNhwagnPJ/view

https://www.primaresearch.org/datasets

https://drive.google.com/file/d/1Q4kDiJts-yi9IhsYT6ku5Y4WNhwagnPJ/view


### Resource Articles
EDD - https://arxiv.org/pdf/1911.10683.pdf

Handwritten Text Segmentation via End-to-End Learning of Convolutional Neural Networks - https://link.springer.com/article/10.1007/s11042-020-09624-9
