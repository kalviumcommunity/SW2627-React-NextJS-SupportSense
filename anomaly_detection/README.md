# Anomaly Detection & Risk Identification

A production-grade Python pipeline designed to monitor business time-series metrics, identify unusual behavior using business thresholds and statistical techniques, classify severity, generate an audit trail, and visualize anomalies for further investigation.

> [!WARNING]
> An anomaly is a signal for investigation, not proof of an error. 
> Do not automatically delete, modify, or "fix" anomalous records based purely on statistical variance.

## Project Overview

### What is an Anomaly?
An anomaly is an observation that diverges significantly from the expected pattern. In a business context, this could be an extreme spike in revenue, a drop in active users, or an unexpected volume of support tickets. Identifying these quickly allows organizations to investigate whether they stem from genuine operational successes/failures, or data pipeline corruptions.

### Detection Methods

#### 1. Threshold-Based Detection
Uses known business limits configured in `config/alert_rules.py`. 
- **When it's appropriate:** When strict operational bounds are known (e.g. daily revenue must not fall below $5,000 to keep the servers running).
- **Behavior:** Fixed limits do not change based on recent trends.

#### 2. Statistical (Z-Score) Detection
Uses historical behavior to detect deviations. The pipeline computes a 7-day rolling average and standard deviation, and tests the most recent 30-day window.
- **When it's appropriate:** When the metric naturally fluctuates and you want to detect events that are extremely rare based on recent variance (e.g., flagging values more than 2 standard deviations away).
- **Behavior:** Dynamically adjusts to changing baselines.

## Severity Classification

For statistical anomalies, severity is assigned based on absolute standard deviation ($|z|$):
- $|z| \le 1.5 \rightarrow \text{LOW}$ (Normally ignored)
- $1.5 < |z| \le 2.0 \rightarrow \text{MEDIUM}$ (Normally ignored)
- $2.0 < |z| \le 3.0 \rightarrow \text{HIGH}$
- $|z| > 3.0 \rightarrow \text{CRITICAL}$

## Data Integrity 
The pipeline enforces strict immutability. It NEVER alters, deletes, or modifies the source dataset. Anomalies are flagged into a separate `anomalies_log.csv` and given an `OPEN` status, indicating they require human investigation.

## Project Structure

```text
anomaly_detection/
├── config/
│   └── alert_rules.py
├── detection/
│   ├── threshold_detector.py
│   ├── zscore_detector.py
│   └── severity.py
├── analysis/
│   ├── aggregation.py
│   └── rolling_metrics.py
├── visualization/
│   └── anomaly_plot.py
├── reports/
│   └── report_generator.py
├── utils/
│   ├── logger.py
│   └── helpers.py
├── output/
├── sample_data/
│   └── transactions.csv
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the pipeline by pointing it to a transaction dataset:

```bash
python main.py sample_data/transactions.csv
```

## Outputs
- `output/anomalies_log.csv`: Audit trail for case management.
- `output/anomaly_report.json`: Structured system integration payload.
- `output/anomaly_detection.png`: Visual chart.

## Limitations
- Z-score assumes normal distribution. Highly skewed data may produce false positives.
- Datasets with 0 variance will skip Z-score calculation to prevent division by zero errors.
- Small datasets (fewer than 7 days) will not compute full rolling metrics accurately.
