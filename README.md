# fastapi-llm-agent
A FastAPI microservice that parses documents, processes them with an LLM, and returns structured insights

## Live Demo

Check out the live demo [here]().

## Overview

This project is a full-stack, LLM-integrated document processing system built with FastAPI and React. It enables users to upload documents (PDFs, docx..), automatically parse and clean the content, and extract summaries or insights using LLM such as OpenAI.

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
- Send cleaned text to LLM for summary or Q&A
- Retrieve processed results (summary, extracted info)
- Health check & status endpoints
