# fastapi-llm-agent
A FastAPI microservice that parses documents, processes them with an LLM, and returns structured insights

## Live Demo

Check out the live demo [here]().

## Overview

This project is a full-stack, LLM-integrated document processing system built with FastAPI and React. It enables users to upload documents (PDFs, DOCX, images..), automatically parse and clean the content, and extract summaries or insights using LLM such as OpenAI.

It is fully containerized, cloud-ready, and built with modern software development practices — ideal for AI agents, enterprise NLP workflows, or intelligent dashboards.

#### Tech Stack

- Backend: FastAPI (async) + Pydantic + OpenAI LLMs + OCR (AWS Textract)
- Frontend: React + Next.js
- Deployment: AWS (Lambda, S3, EC2, API Gateway), Docker, Kubernetes
- CI/CD: GitHub Actions or GitLab CI with multi-environment pipelines
- Load Balancer: Nginx
- Caching & Task Queue: Redis, Celery

#### Features

- Upload document
- Parse & clean text from uploaded docs
- Send cleaned text to LLM for summary
- Retrieve processed result
- Create a hash of the document to enable caching in memory

## Getting Started

Follow these steps to run the project locally:

### Prerequisites

* Docker & Docker Compose installed
* AWS credentials
* OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/mouhamaddev/fastapi-llm-agent.git
cd fastapi-llm-agent
```

### Running with Docker

```bash
docker-compose up --build
```

This will start backend and frontend services. Access the frontend at `http://localhost:3000`.

## About This Project

I created this project as a personal challenge to learn FastAPI (which was completely new to me) and Next.js (which I had only limited experience with before). I built this project within one week, trying to make it an MVP that actually works.

Thanks so much for taking the time to read this and check out my project! ❤️