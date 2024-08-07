# BeeProject
Our task is to convert PDF scans of handwritten documents to digital form.

![The Workflow Scheme]()

## Quick start with tesseract

Let's start a test run on the BeeProject dataset. 

todo 

--------------------------------------------
## Getting credentials from OCR Services

In order to get better results, use following OCR APIs: Amazon AWS Textract, Google Vision, Microsoft Azure. 
For each one of them you need to register and generate access keys.


### - AWS Textract:
AWS - Amazon Web Services 
**textract** for text analysis. For more information, visit: https://docs.aws.amazon.com/textract/latest/dg/what-is.html

For Boto3 python installation, visit: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

How to get credentials:
https://docs.aws.amazon.com/textract/latest/dg/getting-started.html
1. Get you account to the Amazon AWS Console via this link: https://aws.amazon.com
2. Set up your Identity and Access Management (IAM)
3. Find you key and endpoint (Note)


#### Example of the credentials file
```yaml
{
    "microsoft_api_key": {
        "SUBSCRIPTION_KEY": "your key goes here",
        "ENDPOINT": "https://your_project.cognitiveservices.azure.com/"
    }
}
```

### - Google vision 
1. create an account on Google Cloud: https://cloud.google.com/
2. create a project
3. and go to IAM & Admin and create a role: https://cloud.google.com/iam/docs/grant-role-console
4. generate a json credentials file

Document Text detection documentation: https://cloud.google.com/vision/docs/handwriting
All documentation is here: https://cloud.google.com/docs

#### Example of the credentials file
```yaml
{
    "type": "service_account",
    "project_id": "your_project",
    "private_key_id": "your key ID",
    "private_key": "your key",
    "client_email": "google-vision@your_project.iam.gserviceaccount.com",
    "client_id": "client_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "",
    "universe_domain": "googleapis.com"
}
```
### - Microsoft Azure
Guide:
https://programminghistorian.org/en/lessons/transcribing-handwritten-text-with-python-and-azure

#### Example of the credentials file

Find your key and endpoint (Note: Check that your location is set correctly.)
```yaml
{
    "microsoft_api_key": {
        "SUBSCRIPTION_KEY": "your key goes here",
        "ENDPOINT": "https://your_project.cognitiveservices.azure.com/"
    }
}
```

-----------------------------------
## The BeeProject Dataset
Our dataset contains data from beekeepers. Documents are only in german language and are a mixture of machine-written and hand-written text. 

Three types of documents:
1. tables 
2. question - answer 
3. free text

Source: 
```bash
.
├── data
│   |   ├── scans      -- #examples of scaned documents in different formats
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
