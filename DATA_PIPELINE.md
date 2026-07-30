# Python Data Workflow Foundations (Lesson 2.13)

## 1. Overview & Architectural Philosophy

In production data engineering, exploratory notebooks (e.g. Jupyter) serve as thinking and rapid-prototyping environments. However, automated, scheduled pipelines and production data products require **modular, parameterizable, and repeatable Python scripts**.

This module implements the **Three-Function Pattern (Ingest, Process, Output)** for SupportSense to transform raw customer support ticket data into actionable churn risk scores.

---

## 2. Core Concepts: Notebooks vs. Production Scripts

| Feature | Jupyter Notebooks | Production Python Scripts |
| :--- | :--- | :--- |
| **Primary Use Case** | Rapid exploration, visualization, interactive trial | Automated pipelines, CI/CD integration, batch jobs |
| **Execution** | Manual cell-by-cell execution | Headless execution from command line / cron schedule |
| **Structure** | Sequential cells mixing state and output | Modular functions with explicit inputs/outputs |
| **Testing** | Difficult to unit test | Highly testable via isolated unit test runners (`pytest`) |
| **Logging** | Printed cell stdout | Structured file & stream logging (`logging` module) |

---

## 3. The Three-Function Pattern

Our production script [`scripts/data_pipeline.py`](file:///Users/nikunj/Documents/development/Queue-Away/scripts/data_pipeline.py) strictly enforces separation of concerns through three primary functions:

```mermaid
graph LR
    A["Raw Dataset (CSV)"] --> B["ingest_data()"]
    B --> C["process_data()"]
    C --> D["output_results()"]
    D --> E["Processed Dataset (CSV)"]
```

### Function 1: Ingest Data (`ingest_data`)
- **Responsibility**: Reads raw data from source (e.g., CSV, database, API).
- **Rule**: Performs zero business transformations or filtering. Returns a raw `pd.DataFrame`.
- **Error Handling**: Validates file existence and verifies data is non-empty.

### Function 2: Process Data (`process_data`)
- **Responsibility**: Applies business rules, cleaning, feature engineering, and model/risk scoring.
- **Rule**: Pure data transformation logic without file I/O or external side effects.
- **Transformations**:
  1. Deduplicates tickets by `ticket_id`.
  2. Imputes missing satisfaction scores using median value.
  3. Calculates ticket resolution duration in hours.
  4. Engineers `churn_risk_score` (0-100) and risk category (`HIGH`, `MEDIUM`, `LOW`).

### Function 3: Output Results (`output_results`)
- **Responsibility**: Exports transformed DataFrame to destination (CSV, database, storage bucket).
- **Rule**: Performs zero data modifications. Manages output directory creation and write verification.

---

## 4. Script Organization

[`scripts/data_pipeline.py`](file:///Users/nikunj/Documents/development/Queue-Away/scripts/data_pipeline.py) follows standard production script ordering:

1. **Imports**: Top-level library dependencies (`pandas`, `numpy`, `logging`, `datetime`, `os`, `sys`).
2. **Configuration & Constants**: Uppercase variables defining file paths and business thresholds (`INPUT_FILE`, `OUTPUT_FILE`, `LOG_FILE`, `MIN_MONTHLY_SPEND`).
3. **Logging Setup**: Configured with `logging.basicConfig()` outputting to both `logs/workflow.log` and stdout.
4. **Main Functions**: Decorated with Google-style docstrings, type annotations, and inline rationale comments.
5. **Main Execution Block**: Entry point `if __name__ == "__main__":` orchestrating steps within a robust try-except handler.

---

## 5. Execution & Verification

### Running the Pipeline
Execute the data pipeline script directly from the terminal:

```bash
python3 scripts/data_pipeline.py
```

### Running Unit Tests
Execute the unit test suite with `pytest`:

```bash
pytest tests/test_data_pipeline.py
```

---

## 6. Automating Execution (Cron Scheduling)

To schedule the script to run automatically every Monday morning at 6:00 AM:

```bash
0 6 * * 1 /usr/bin/python3 /Users/nikunj/Documents/development/Queue-Away/scripts/data_pipeline.py >> /Users/nikunj/Documents/development/Queue-Away/logs/cron_execution.log 2>&1
```
