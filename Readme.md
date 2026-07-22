# Overview

Businesses generate and process large volumes of documents every day, including invoices, contracts, reports, resumes, and financial records. Extracting valuable information from these documents is often a manual and time-consuming task that slows down decision-making and reduces productivity.

IntelliDoc solves this problem by providing an AI-powered document processing platform that enables users to upload PDF and DOCX documents and automatically receive meaningful insights from their contents. Instead of manually reviewing lengthy documents, users can quickly obtain AI-generated analysis through a simple and intuitive web interface.

Built on a cloud-native, event-driven architecture, uploaded documents are stored in Amazon S3, which automatically triggers an AWS Lambda function to process the file using the Google Gemini API. The generated analysis is stored in Amazon RDS and made available to users through a FastAPI backend running on Amazon ECS Fargate. The platform is built with Python, FastAPI, HTML, CSS, JavaScript, Docker, and Terraform, demonstrating modern cloud engineering practices, event-driven computing, Infrastructure as Code (IaC), and AI integration.
