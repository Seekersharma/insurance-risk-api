# Insurance Risk Prediction API

## Overview

Insurance Risk Prediction API is a machine learning-powered REST service that predicts customer insurance risk based on demographic and policy information.

The application is built using:

* Python
* FastAPI
* Scikit-Learn
* Docker
* GitHub Actions
* Azure Container Registry
* Azure Container Apps


---

## Live Application

Base URL:

https://insurance-risk-api.gentleriver-feb62d64.westus3.azurecontainerapps.io

Swagger Documentation:

https://insurance-risk-api.gentleriver-feb62d64.westus3.azurecontainerapps.io/docs

---

## Features

* Real-time insurance risk scoring
* REST API endpoints
* Swagger/OpenAPI documentation
* Dockerized deployment
* Automated CI/CD pipeline
* Azure-hosted production environment

---

## API Endpoints

### Health Check

GET /

Response:

{
"message": "Insurance Risk API Running"
}

---

### Risk Prediction

POST /predict

Request:

{
"age": 45,
"premium": 1200,
"claim_count": 1,
"years_customer": 10
}

Response:

{
"risk": 0
}

Note: Actual prediction values depend on the trained model.

---

## Local Development

Clone repository:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Run application:

uvicorn src.app:app --reload

Open Swagger:

http://localhost:8000/docs

---
## Testing

Run tests locally:

```bash
python -m pytest
```

Current coverage:

- Health endpoint test
- Prediction endpoint test
--------
## CI/CD Pipeline

The application is automatically deployed when code is pushed to the main branch.

Pipeline:

GitHub
→ GitHub Actions
→ Azure Container Registry
→ Azure Container Apps

---

## Deployment Status

Production Ready

Platform: Azure Container Apps

Container Registry: Azure Container Registry

CI/CD: GitHub Actions

API Framework: FastAPI

Documentation: Swagger/OpenAPI
