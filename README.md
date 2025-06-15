# fastapi-llm-agent
**A FastAPI microservice that parses documents, processes them with an LLM, and returns structured insights**

I come from a heavy Django and DRF background (over 3 YOE).
I am very passionate about it and I write and maintain Python libraries that are available on pip that I made to solve personal issues and that might be beneficial for other developers too. These projects include: DAF (Django Async Framework) and another one that I'm working on right now which is used to automatically fix and handle migrations issues like manage.py migrate --check instead of wasting hours on manual migration conflict fixing.

Over the past week I dedicated most of my free time to learn FastAPI and create a microservice similar to AnyParser that parses documents and processes them with an LLM, and then returns structured insights and summary about the uploaded doc.

## Live Demo

Check out the live demo [here]().

## Overview

This project is a full-stack, LLM-integrated document processing system built with FastAPI and React. It enables users to upload documents (PDFs, docx..), automatically parse and clean the content, and extract summaries or insights using LLM such as OpenAI.

It is fully containerized, cloud-ready, and built with modern software development practices — ideal for AI agents, enterprise NLP workflows, or intelligent dashboards.

#### Tech Stack

- **Backend**: FastAPI (async) + Pydantic + OpenAI LLMs + OCR
- **Frontend**: React + Next.js
- **Deployment**: AWS (Lambda, S3, EC2, API Gateway), Docker, Kubernetes
- **CI/CD**: GitHub Actions or GitLab CI with multi-environment pipelines
- **Monitoring & Logging**: TBD (CloudWatch, Sentry, Prometheus)

#### Features

##### API Endpoints
- Upload document
- Parse & clean text from uploaded docs
- Send cleaned text to LLM for summary or Q&A
- Retrieve processed results (summary, extracted info)
- Health check & status endpoints

##### LLM Integration
- Async LLM calls to OpenAI
- Prompt optimization and text chunking

##### Data Pipeline
- Parse PDF or text files
- Clean text with regex/NLP libs
- Chunk data for prompt token limits
- Cache LLM responses for repeat queries

#### Auto CI/CD Deployment

- Backend: Dockerized FastAPI app deployed to AWS Lambda via Amazon API Gateway
- Frontend: React + Next.js on EC2 or S3 (static)
- S3 for persistent document and result storage
- Kubernetes manifests provided for optional multi-service deployment
- Environment support: `dev`, `staging`, `testing`, `prod`
- Includes automated testing and deployment scripts

#### Frontend (React + Next.js)

- Upload documents via UI
- View summaries and extracted insights
- Auth integration (JWT or OAuth2)
- Responsive design

#### Testing

- Unit tests for:
  - File upload and parsing
  - LLM interaction logic
- Integration tests for:
  - End-to-end document processing
  - API contract and response validation

#### Monitoring & Logging (Coming Soon)

- Structured logs using `loguru` or `structlog`
- Centralized logging to AWS CloudWatch or Sentry
- Metrics collection via Prometheus & Grafana (optional)

#### Docs & Environments

- **API Documentation**: auto-generated via FastAPI (Swagger & ReDoc)
- **Dev Environment**: `docker-compose` for local development
- **Branch Strategy**:
  - `main` – production-ready
  - `dev` – active development
  - `staging` – pre-release testing
  - `testing` – CI/CD environment
