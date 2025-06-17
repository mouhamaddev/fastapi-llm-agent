# fastapi-llm-agent
A FastAPI microservice that parses documents, processes them with an LLM, and returns structured insights

## Live Demo

Check out the live demo [here](https://d31yw2qefd409z.cloudfront.net/).

## Overview

This project is a full-stack, LLM-integrated document processing system built with FastAPI and Next.js. It enables users to upload documents (PDFs, DOCX, images..), automatically parse and clean the content using AWS Textract, and extract summaries using OpenAI LLMs.

Fully containerized, cloud-ready, and built with software development practices.

#### Tech Stack

- Backend: FastAPI (Dockerized) + Redis + API Gateway + OpenAI LLMs + OCR (AWS Textract)
- Frontend: Next.js deployed on S3 + CDN (CloudFront)
- Database: AWS DynamoDB
- CI/CD: GitHub Actions
- Task Queue: Celery + Lambda + WebSockets _(not implemented yet)_

#### Features

- Upload document
- Parse & clean text from uploaded docs
- Send cleaned text to LLM for summary
- Retrieve processed result
- Create a hash of the document to enable Redis caching in memory (one week)
- API throttling and rate limiting
- Auth + JWT
- History and older uploads tracking with their summaries


## About This Project

I created this project as a personal challenge to learn FastAPI (which was completely new to me) and Next.js. I built this project within one week, trying to make it an MVP that actually works.

Thanks so much for taking the time to read this and check out my project! ❤️