# 🛡️ ChurnShield Enterprise System

> **AI-Powered Customer Churn Prediction & Support Intelligence Platform**

ChurnShield is an industry-grade SaaS intelligence platform designed to predict, analyze, and prevent customer churn by unifying support telemetry, billing indicators, customer CSAT ratings, product usage activity, and machine learning risk modeling.

---

## 🏛️ System Architecture

```
SW2627-React-NextJS-SupportSense/
├── frontend/               # React + Vite Enterprise Dashboard (Stitch Design System)
│   ├── src/
│   │   ├── components/     # UI Views (Dashboard, Customers, Tickets, AI Engine, Analytics)
│   │   ├── api.ts          # API Client Layer (FastAPI REST Integration)
│   │   ├── index.css       # Stitch v1.0 Warm Cream & Bronze Gold Design Tokens
│   │   └── App.tsx         # Main Viewport Shell & Navigation
│   └── package.json
│
├── ml_service/             # Machine Learning Service & FastAPI Backend API
│   ├── main.py             # FastAPI REST Server (Endpoints 1–11, Real-Time Inference)
│   ├── train_model.py      # Random Forest Classifier Training Engine (93.5% Accuracy)
│   └── models/             # Serialized Joblib ML Models
│
├── backend/                # Node.js / Express Microservices Layer
│   ├── src/                # Controllers, Routes, Services, Auth & Validation
│   └── package.json
│
├── data/                   # Calibrated Multi-Entity SaaS Dataset
│   └── raw/
│       ├── customers.csv   # 1,000 SaaS Enterprise Customer Profiles
│       ├── customer_support_tickets.csv  # 5,941 Granular Support Ticket Records
│       └── subscriptions.csv             # 1,000 Subscription Lifecycle Records
│
├── dataset_validation/     # Data Integrity & Schema Validation Suite
│   ├── config/             # Validation Rules & Schema Configs
│   ├── validators/         # Automated Null/Boundary/Outlier Checks
│   └── main.py             # Validation Pipeline Runner
│
├── scripts/                # Synthetic Data Generation & ETL Pipelines
│   ├── generate_industry_dataset.py
│   └── data_pipeline.py
│
├── tests/                  # Automated Test Suite (PyTest & Integration Tests)
├── requirements.txt        # Python ML & Backend Dependencies
├── DATA_PIPELINE.md        # Comprehensive ETL & Feature Engineering Spec
├── WORKFLOW.md             # Developer & System Operations Guide
└── README.md
```

---

## 📊 Key Platform Capabilities & Modules

1. **Dashboard Overview (Module 9)**: Real-time KPIs for Active Accounts, High-Risk Count, Total Revenue at Risk (MRR), and Model Accuracy.
2. **Customer Portfolio Telemetry (Module 2)**: Search, multi-criteria risk/plan filtering, pagination across 1,000 accounts.
3. **Support Ticket Queue (Module 3)**: Granular ticket tracking, resolution duration metrics, CSAT sentiment ratings, and 1-click SLA escalation.
4. **AI Risk Prediction Engine (Modules 5 & 6)**: Real-time Random Forest inference returning exact `churn_probability`, `risk_level`, root cause drivers, and health scores.
5. **Prescriptive Recommendations (Module 8)**: Automated AI retention playbooks for critical-risk accounts.
6. **Analytics & Root Cause Telemetry (Module 10)**: Category volume distributions and portfolio risk segmentation.
7. **Alerts & Executive Reporting (Module 11)**: High-risk alert feeds and executive CSV export.
8. **Real-Time Reactive KPI Dashboard**: A fully reactive multipage data exploration app.
   - **Reactive KPIs**: High-level metrics recalculate instantly upon filtering (Revenue, Orders, AOV, ACV).
   - **Upload Integration**: Upload new CSV datasets directly via the UI. Caching is automatically cleared and the SQLite engine is instantly rebuilt to show the fresh data.
   - **Interactive Filtering**: Date ranges, order amounts, and segment multiselects cross-filter the dataset before driving the 3 integrated Plotly charts (Line, Bar, and Histogram).
   - **Empty State Handling**: Gracefully catches over-filtered edge cases without silently crashing.

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+

### 2. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/SW2627-React-NextJS-SupportSense.git
cd SW2627-React-NextJS-SupportSense

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Launch Backend API (FastAPI Engine)

```bash
# Start the FastAPI ML & Telemetry Server on Port 8000
python3 ml_service/main.py
```
* Interactive API Documentation (Swagger): `http://localhost:8000/docs`
* API Health Endpoint: `http://localhost:8000/health`

### 4. Launch React Frontend App

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite Dev Server on Port 5173
npm run dev
```
* Access the web application at: `http://localhost:5173`

### 5. Launch Streamlit Multipage Dashboard

```bash
# Navigate to the root directory
# Start the interactive multipage analytics app
streamlit run app.py
```
* Access the analytics dashboard at: `http://localhost:8501`

---

## 🎯 Machine Learning Model Performance

| Metric | Score |
| :--- | :--- |
| **Model Type** | Balanced Random Forest Classifier |
| **Accuracy** | **93.50%** |
| **ROC-AUC** | **98.64%** |
| **F1-Score** | **85.71%** |
| **Primary Features** | Escalations, Unresolved Tickets, CSAT Rating, Payment Delays, Usage Score |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
