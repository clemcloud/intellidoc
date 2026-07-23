# IntelliDoc

An AI-powered document processing platform that extracts text from uploaded PDF and DOCX files, generates intelligent summaries using Google's Gemini model, and stores processed results in PostgreSQL. The application is fully containerized and deployed on AWS using a serverless, event-driven architecture.

---

## Demo

> **Screenshot:** IntelliDoc Homepage

```markdown
![Homepage](screenshots/demo.mp4)
```

**Demo Video:** *(Add your YouTube or Loom link here)*

---

## Architecture

The application combines modern backend development with cloud-native infrastructure. Documents are uploaded through the FastAPI application, stored in Amazon S3, processed asynchronously by AWS Lambda, analyzed with Gemini, and persisted in Amazon RDS.

> **Screenshot:** Architecture Diagram

```markdown
![Architecture](screenshots/architecture.png)
```

---

## Features

* Upload PDF and DOCX documents
* Automatic text extraction
* AI-powered document summarization
* Identification of key points
* Basic document classification
* PostgreSQL persistence
* Dockerized deployment
* AWS serverless architecture
* Infrastructure managed with Terraform
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

* Terraform
* Docker

---

## Project Documentation

Additional technical documentation is available in the `docs/` directory.

| Document            | Description                                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `backend.md`        | Backend architecture, extraction pipeline, Gemini integration, frontend, database, and local development workflow      |
| `infrastructure.md` | AWS architecture, Terraform infrastructure, networking, deployment process, monitoring, and operational considerations |
| `decisions.md`      | Architectural decisions, trade-offs, technology choices, and lessons learned                                           |
| `challenges.md`     | Major technical challenges encountered during development and how they were resolved                                   |

---

## Screenshots

### Homepage

```markdown
![Homepage](screenshots/homepage.png)
```

### Document Analysis

```markdown
![Analysis Result](screenshots/file-analysis.png)
```

### AWS Infrastructure

```markdown
![AWS Architecture](screenshots/architecture.png)
```

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

* Amazon Bedrock integration
* CI/CD with GitHub Actions
* Application Load Balancer (ALB)
* HTTPS using AWS Certificate Manager
* Route 53 custom domain
* Auto Scaling for ECS services
* Secrets Manager integration
* CloudWatch dashboards and alarms
* OCR support for scanned PDFs

---

## Author

**Umoru Clement**

Cloud Engineer | Backend Developer | AWS Solutions Architect Associate Candidate

LinkedIn: *(Add your profile link)*

---

## License

This project is provided for educational and portfolio purposes.
