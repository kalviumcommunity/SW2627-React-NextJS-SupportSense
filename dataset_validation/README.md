# Dataset Intake & Source Validation

A professional, production-grade dataset validation module designed for enterprise ETL pipelines. This module strictly enforces separation of concerns: it performs **validation only**—no transformations, cleaning, or machine learning are performed here. If validation fails, execution halts immediately with a clear error report.

## Features

- **File Exists**: Checks if the file exists and is not empty.
- **Format Validation**: Ensures the dataset format is supported (CSV, JSON, .xlsx).
- **Encoding Detection**: Detects file encoding (with confidence scores) using `chardet`.
- **Schema Validation**: Validates the dataset structure against an expected schema (missing/extra columns).
- **Dataset Statistics**: Captures and reports basic metrics (row count, column count, file size, column names, data types).
- **Professional Reporting**: Generates a detailed JSON validation report.
- **Robust Logging**: Comprehensive file and console logging to track the validation lifecycle.

## Folder Structure

```text
dataset_validation/
├── validators/
│   ├── file_validator.py
│   ├── schema_validator.py
│   ├── encoding_validator.py
│   ├── format_validator.py
│   ├── statistics_validator.py
├── config/
│   ├── settings.py
├── reports/
│   ├── validation_report.json (Generated)
├── utils/
│   ├── logger.py
├── logs/
│   ├── dataset_validation.log (Generated)
├── main.py
├── requirements.txt
├── README.md
```

## Installation

Ensure you have Python 3.12+ installed. 

Install the required dependencies:

```bash
pip install -r dataset_validation/requirements.txt
```

## Configuration

You can configure supported formats, default output directories, and the expected dataset schema by modifying `dataset_validation/config/settings.py`.

## Usage

Run the validation script by pointing it to your dataset file:

```bash
# Ensure you are at the project root and PYTHONPATH is set correctly
export PYTHONPATH=$(pwd)

# Run the validation
python dataset_validation/main.py path/to/dataset.csv
```

### Expected Output

Upon successful validation, the script exits with `0` and generates a detailed report:

```json
{
    "status": "PASSED",
    "timestamp": "2026-07-30T10:15:00.123456",
    "file": "customer_support_tickets.csv",
    "checks": {
        "file_exists": true,
        "format": true,
        "encoding": "ascii (confidence: 1.00)",
        "schema": true
    },
    "statistics": {
        "rows": 10000,
        "columns": 8,
        "file_size_mb": 1.2,
        "column_names": [
            "ticket_id",
            "customer_name",
            "issue_type",
            "priority",
            "status",
            "created_at",
            "resolution_time_hrs",
            "satisfaction_score"
        ],
        "data_types": {
            "ticket_id": "int64",
            "customer_name": "object"
        }
    },
    "warnings": [],
    "errors": []
}
```

If validation fails, the script exits with `1` and outputs the specific errors. All errors, warnings, and system states are systematically written to `reports/validation_report.json` and `logs/dataset_validation.log`.
