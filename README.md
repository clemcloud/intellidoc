# IntelliDoc

An AI-powered document processing platform that extracts text from uploaded PDF and DOCX files, generates intelligent summaries using Google's Gemini model, and stores processed results in PostgreSQL.

The application combines **containerized services** with **serverless event processing**, using Amazon ECS Fargate to host the FastAPI application while AWS Lambda asynchronously processes uploaded documents through an event-driven pipeline.

---

## Demo

### Demo Video

> **Watch the application in action:**

https://youtu.be/EkhCu01H2Ow

---

## Architecture

IntelliDoc follows a hybrid cloud architecture that combines long-running containerized services with serverless event processing.

The user uploads a document through the FastAPI application running on Amazon ECS Fargate. The application stores the file in Amazon S3, which automatically triggers an AWS Lambda function. Lambda extracts the document text, sends it to the Google Gemini API for analysis, stores the processed result in Amazon RDS PostgreSQL, and the FastAPI application later retrieves the result when the client polls for completion.

![Architecture Diagram](screenshots/architectural.png)

---

## Features

* Upload PDF and DOCX documents
* Automatic text extraction
* AI-powered document summarization
* Key point extraction
* Basic document classification
* PostgreSQL persistence
* Dockerized deployment
* Event-driven document processing
* Infrastructure as Code using Terraform
* CloudWatch monitoring and logging

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Uvicorn

### AI

* Google Gemini 2.5 Flash

### Cloud

* Amazon ECS (Fargate)
* Amazon ECR
* Amazon S3
* AWS Lambda
* Amazon RDS (PostgreSQL)
* Amazon CloudWatch
* IAM
* Amazon VPC

### Infrastructure

* Docker
* Terraform

---

## Project Documentation

Detailed technical documentation is available inside the **docs** directory.

| Document                                                   | Description                                                                                                                              |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **[Backend Documentation](docs/backend.md)**               | Backend architecture, extraction pipeline, Gemini integration, frontend implementation, database design, and local development workflow. |
| **[Infrastructure Documentation](docs/infrastructure.md)** | AWS architecture, networking, Terraform infrastructure, deployment process, monitoring, and operational considerations.                  |
| **[Challenges & Debugging](docs/challenges.md)**           | Major technical challenges encountered during development and how they were diagnosed and resolved.                                      |

---

## Screenshots

### Homepage

![Homepage](screenshots/homepage.png)

### Document Analysis

![Analysis Result](screenshots/file-analysis.png)

### AWS Architecture

![AWS Architecture](screenshots/architectural.png)

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/clemcloud/intellidoc.git
cd intellidoc
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your-api-key
DATABASE_URL=postgresql://user:password@localhost:5432/intellidoc
```

Run the application:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Future Improvements

* Integrate Amazon Bedrock as an alternative AI provider
* HTTPS using AWS Certificate Manager
* Route 53 custom domain
* ECS Service Auto Scaling
* AWS Secrets Manager integration
* CloudWatch dashboards and alarms
* OCR support for scanned PDF documents

---

## Author

**Umoru Clement**

Cloud Engineer | Backend Developer | AWS Solutions Architect Associate Candidate

**LinkedIn:** *www.linkedin.com/in/clementcloud*

---

## License

This project is provided for educational and portfolio purposes.
