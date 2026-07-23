# Challenges & Lessons Learned

## Overview

Building IntelliDoc involved far more than writing application code. Throughout development, several infrastructure, deployment, and application-level issues were encountered while moving from a locally working prototype to a fully deployed cloud-native application.

Each challenge strengthened my understanding of AWS, Docker, networking, backend development, and cloud-native architecture. Rather than documenting every issue encountered, this document focuses on the most significant engineering problems, how they were diagnosed, and the lessons learned from resolving them.

---

# Challenge 1 — Docker Daemon Crash During Image Build

## Problem

While rebuilding the Docker image, the build consistently failed during the `COPY . .` stage. After the failed build, even simple Docker commands such as `docker tag` began crashing unexpectedly.

## Symptoms

```text
unexpected fault address
fatal error: fault
SIGBUS: bus error
Segmentation fault
```

## Root Cause

The issue was not caused by the Dockerfile or application code. Instead, the Docker daemon had crashed due to resource exhaustion inside the WSL environment after a long development session.

## Solution

The Docker daemon was restarted, followed by a complete WSL shutdown to clear the environment and recover system resources.

```bash
sudo service docker restart
```

If necessary:

```powershell
wsl --shutdown
```

After restarting Docker and WSL, the image built successfully without any changes to the application code.

## Lesson Learned

Not every deployment failure originates from the application itself. Before debugging containers or Dockerfiles, it's important to verify that the development environment and tooling are functioning correctly.

---

# Challenge 2 — Frontend Failed to Communicate with the Backend

## Problem

After deploying IntelliDoc to Amazon ECS Fargate, the application loaded successfully in the browser, but every document upload failed with a generic **"Failed to fetch"** error.

## Symptoms

* The frontend loaded correctly.
* Every upload request failed immediately.
* No requests reached the FastAPI backend.
* Document analysis never started.

## Root Cause

During local development, the frontend's JavaScript contained a hardcoded API endpoint:

```javascript
const API_URL = "http://127.0.0.1:8000";
```

After deployment, users' browsers attempted to send requests to their own localhost instead of the deployed ECS application.

## Solution

The frontend was updated to use a relative URL instead.

```javascript
const API_URL = "";
```

The Docker image was rebuilt, pushed to Amazon ECR, and a new ECS deployment was triggered.

Using a relative URL allows the frontend to automatically communicate with whichever host serves the application, making the same codebase work in both local and production environments.

## Lesson Learned

Avoid hardcoding environment-specific URLs. Relative URLs simplify deployments and eliminate unnecessary configuration differences between development and production.

---

# Challenge 3 — SQLAlchemy DetachedInstanceError

## Problem

While retrieving processed documents from PostgreSQL, the application occasionally raised a `DetachedInstanceError`.

## Root Cause

The application attempted to access SQLAlchemy model attributes after the database session had already been closed.

## Solution

The required values were copied into a plain Python dictionary before closing the database session, ensuring the response no longer depended on an active SQLAlchemy object.

## Lesson Learned

Understanding the lifecycle of ORM objects is essential when working with SQLAlchemy. Database sessions should remain active only while objects are being accessed.

---

# Challenge 4 — Amazon Bedrock Free Tier Limitations

## Problem

Amazon Bedrock was originally planned as the AI service powering IntelliDoc's document analysis.

## Root Cause

Although Bedrock was the preferred solution because of its native AWS integration, practical access to the required foundation models exceeded the project's free-tier budget during development.

## Solution

The AI layer was redesigned to use the Google Gemini API while keeping the integration modular so that Amazon Bedrock can be adopted later with minimal changes to the application.

## Lesson Learned

Engineering decisions are often influenced by practical constraints such as cost. Designing loosely coupled integrations makes replacing external services significantly easier when project requirements change.

---

# Key Takeaways

Developing IntelliDoc reinforced several important engineering principles:

* Build and validate application logic locally before introducing cloud infrastructure.
* Separate infrastructure issues from application issues during debugging.
* Verify the health of development tools before assuming application failures.
* Avoid hardcoding environment-specific configuration.
* Design cloud applications to be modular and loosely coupled.
* Consider operational constraints such as cost when selecting cloud services.
* Treat every production issue as an opportunity to improve both the system and the development process.

These challenges highlight that building cloud-native applications extends beyond writing code. Successful cloud engineering also requires effective debugging, deployment, operational awareness, and sound architectural decision-making.
