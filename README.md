# SupportSense – AI-Powered Customer Churn Prediction & Support Intelligence Platform

## Overview

SupportSense is a full-stack AI-powered customer support intelligence platform designed to help businesses proactively identify customers who are likely to churn. By combining customer support interactions, subscription history, feedback, and machine learning, SupportSense enables organisations to take preventive actions before customers leave.

The platform predicts churn probability, identifies the key drivers behind customer dissatisfaction, calculates customer health scores, and recommends retention strategies through an interactive analytics dashboard.

---

## Problem Statement

Traditional customer support systems focus on operational metrics such as ticket volume, resolution time, escalation rate, and customer satisfaction (CSAT). However, these metrics are often disconnected from customer retention, making it difficult for businesses to identify customers at risk of churn.

SupportSense bridges this gap by transforming customer support data into actionable business intelligence using predictive analytics and machine learning.

---

## Key Features

### Authentication

* User Registration & Login
* JWT Authentication
* Role-Based Access Control (RBAC)
* Forgot Password

### Customer Management

* Customer Profiles
* Subscription History
* Customer Segmentation
* Lifetime Value Tracking
* Customer Search

### Support Ticket Management

* Create & Manage Tickets
* Ticket Assignment
* Priority & Category Management
* Resolution Tracking
* Escalation History
* Comments & Attachments

### AI Churn Prediction

* Churn Probability Prediction
* Risk Classification (Low, Medium, High)
* Churn Driver Analysis
* Confidence Score

### Customer Health Score

* Health Score (0–100)
* Customer Risk Monitoring
* Behavioural Insights

### Recommendation Engine

* AI-Based Retention Recommendations
* Discount Suggestions
* Escalation Recommendations
* Priority Support Suggestions

### Dashboard & Analytics

* Active Customers
* Open & Resolved Tickets
* Average Resolution Time
* Customer Satisfaction (CSAT)
* High-Risk Customers
* Revenue at Risk
* Monthly Churn Trends
* Agent Performance
* Root Cause Analysis

### Notifications

* Email Alerts
* Dashboard Notifications
* High-Risk Customer Alerts

---

# Tech Stack

## Frontend

* React
* TypeScript
* Tailwind CSS
* Redux Toolkit
* React Query
* Recharts

## Backend

* Node.js
* Express.js
* MongoDB
* Mongoose
* JWT
* bcrypt

## AI & Machine Learning

* Python
* FastAPI
* Scikit-learn
* XGBoost / Random Forest
* Pandas
* NumPy

## DevOps & Deployment

* Docker
* GitHub Actions
* Render / Railway
* AWS EC2

---

# System Architecture

```text
React Frontend
        │
        ▼
Express Backend API
        │
        ▼
Business Logic
        │
        ▼
MongoDB Database
        │
        ▼
FastAPI ML Service
        │
        ▼
Churn Prediction Model
        │
        ▼
Analytics Dashboard
```

---

# Repository Structure

```text
SupportSense/
│
├── frontend/
├── backend/
├── ml-service/
├── docs/
├── README.md
```

---

# Getting Started

## Clone the Repository

```bash
git clone <repository-url>
```

## Navigate to the Project

```bash
cd SupportSense
```

## Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b feature/backend-setup
```

---

# Git Workflow

1. Clone the repository.
2. Create a new feature branch.
3. Implement your assigned task.
4. Commit your changes using meaningful commit messages.
5. Push your branch to GitHub.
6. Create a Pull Request.
7. Merge only after review and approval.

> **Do not commit directly to the `main` branch.**

---

# Branch Naming Convention

```text
feature/backend-setup
feature/authentication
feature/customer-module
feature/ticket-module
feature/dashboard
feature/ml-service
feature/docker
bugfix/issue-name
hotfix/issue-name
```

---

# Commit Message Convention

```text
feat: add authentication module
fix: resolve JWT middleware issue
docs: update project documentation
refactor: optimise ticket service
test: add authentication tests
chore: update dependencies
```

---

# Development Guidelines

* Follow the MVC architecture.
* Keep business logic inside service layers.
* Write clean, modular, and reusable code.
* Use environment variables for secrets.
* Follow REST API standards.
* Write meaningful commit messages.
* Create a Pull Request for every completed feature.
* Review code before merging into `main`.

---

# Future Enhancements

* CRM Integrations
* Real-Time Churn Prediction
* WhatsApp Integration
* Email & Chat Sentiment Analysis
* Voice Call Transcription Analysis
* LLM-Based Support Summaries
* Predictive Workforce Planning

---

# Contributors

Developed collaboratively as part of a Full-Stack AI Capstone Project.

---

# License

This project is intended for educational and learning purposes.
