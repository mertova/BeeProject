# BeeProject

This work semi automate transcribing historical handwritten tables. Our presented method works on a mixture 
of computer vision tools and optical character recognition (OCR) to detect the grid and content of the table. 

![The Workflow Scheme]( ./resources/readmeImgs/workflow.png "Workflow Scheme")

## Quick start

Let's start a test run on the BeeProject dataset. 

Clone repository and navigate to the project: 
```shell
git clone https://github.com/mertova/BeeProject.git
cd BeeProject
```

```shell

```

-----------------------------------
## The BeeProject Collection
The dataset we collected contains records from beekeepers, consisting of hive weight gain and loss 
and meteorological conditions. The institute of bee protection from JKI  gathered this information from 
the German beekeeper associations of Lower Saxony, Hesse, Mecklenburg-Vorpommern, Thuringia, and Brandenburg 
in Germany within the collaborative research project MonViA. The sample of the dataset is available [here][1].

[1]: https://github.com/mertova/TheBeeProjectCollection.git        "The BeeProject Collection"


```
.
├── resources
│   ├── credentials   # place to store your credentials 
│   ├── data          # place to store your data to be digitized
│   └── play-data     # a sample from our BeeProject collection     
├── src
│   ├──
│   ├──
│   ├──
│   └──
├── test -- # test files
├── execute_digitalization.py
└── execute_extraction.py
```


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

--------------------------------------------

