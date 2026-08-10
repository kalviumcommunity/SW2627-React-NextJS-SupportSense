# Enterprise Data Consistency & Validation Rules Framework

A modular, production-ready Python framework designed to run configurable validation rules against incoming datasets. It validates every record, isolates failed records along with explicit rule violation reasons, exports a clean dataset for downstream consumption, and outputs a complete JSON summary report and an appendable CSV audit trail.

---

## Core Principle
> **"Invalid records should be detected, isolated, explained, and traceable — not silently deleted."**
> 
> The pipeline makes it immediately clear which records failed, which rules they violated, why they failed, how many failed in total, and which records are safe to send to downstream processing.

---

## What is Data Validation & Why It Matters

**Data Validation** is the process of ensuring that data conforms to clean business and technical rules before ingestion or analysis. 
In modern data lakes and warehouses:
- **Prevents Garbage-in, Garbage-out**: Low-quality records can corrupt reports, cause division-by-zero or datatype errors in ETLs, and degrade machine learning model accuracy.
- **Isolates Errors Early**: By separating failed records into a quarantine file with specific failure descriptors, operators can immediately trace data entry issues or supplier data pipeline failures.
- **Traceability**: Audit trails guarantee that pipeline execution states are fully documented for data compliance and SLA validation.

---

## Five Validation Categories

This framework implements five primary types of data validations:

### 1. Range Validation
Ensures numeric values or dates fall within configured boundaries (minimum, maximum, or both).
- **Supports**: Minimum-only, Maximum-only, or Bounded ranges.
- **Dynamic Dates**: Can resolve dynamic dates like `now` or `today` to prevent future birth dates or registration dates.

### 2. Null Validation
Validates required columns to ensure no empty values, missing fields, or string-based null placeholders (such as `""`, `"NULL"`, `"None"`, or `"NaN"`) exist in key fields.

### 3. Format Validation
Uses regular expressions (Regex) to validate standard string formats like emails, phone numbers, customer IDs, and order numbers.

### 4. Referential Integrity
Ensures foreign keys in the incoming dataset (e.g. `orders.customer_id`) exist in a master reference dataset (e.g. `customers.customer_id`). If the parent record is missing, the child record is quarantined.

### 5. Business Rules
Handles custom domain-specific logical checks across columns (e.g., verifying `end_date >= start_date` or checking that the order `discount <= price`).

---

## Project Structure

```text
data_validation/
├── config/
│   └── rules.py                      # Configurations: required fields, ranges, patterns, lookups, business rules
├── validators/
│   ├── base_validator.py             # Base abstract class defining validate interface
│   ├── null_validator.py             # Required column checks (blanks, NaNs, sentinels)
│   ├── range_validator.py            # Min/max boundaries check for values and dates
│   ├── format_validator.py           # Regular expression format matches
│   ├── reference_validator.py        # Cross-dataset referential integrity checks
│   └── business_rule_validator.py    # Custom multi-column logical business rules
├── reports/
│   └── validation_report.py          # Summary JSON reports and CSV audit log generator
├── utils/
│   ├── logger.py                     # Logger setup for stdout and app log
│   ├── exceptions.py                 # Custom domain validation exception hierarchy
│   └── helpers.py                    # CSV and Excel loaders / savers
├── output/                           # Directory containing output datasets and logs
├── sample_data/                      # Realistic testing datasets
│   ├── customers.csv                 # Lookup reference customer profiles
│   └── orders.csv                    # Orders dataset containing intentional errors
├── main.py                           # CLI pipeline entrypoint
├── requirements.txt                  # Python package requirements
└── README.md                         # Framework documentation
```

---

## Installation

1. Navigate to the project directory:
   ```bash
   cd data_validation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

To execute the validation pipeline on the sample orders dataset:

```bash
python main.py sample_data/orders.csv
```

### Outputs Created:

Every execution writes results to the `output/` directory:

1. **`output/validated_data.csv`**: Contains only the records that passed **every** validation rule.
2. **`output/validation_failures.csv`**: Contains failed records, along with a validation status, failed rule names, explicit failure reasons, and execution timestamps.
3. **`output/validation_report.json`**: A structured JSON summary mapping statistics per rule.
4. **`output/validation_audit.log`**: A structured CSV audit trail recording execution metrics over time.

---

## Example JSON Validation Report (`output/validation_report.json`)

```json
{
    "status": "COMPLETED",
    "timestamp": "2026-08-10T12:00:00Z",
    "dataset_name": "orders.csv",
    "total_records": 10,
    "passed_records": 1,
    "failed_records": 9,
    "pass_percentage": 10.0,
    "failure_percentage": 90.0,
    "rules": {
        "order_id_required": { "passed": 10, "failed": 0 },
        "customer_id_required": { "passed": 9, "failed": 1 },
        "email_format": { "passed": 9, "failed": 1 },
        "customer_id_reference": { "passed": 9, "failed": 1 },
        "date_order": { "passed": 9, "failed": 1 }
    }
}
```

---

## How to Add a New Validation Rule

To add a new validation rule:

### 1. Simple Range, Null, or Format Checks
Update the dictionaries directly in `config/rules.py`:
- To make a column required, add it to `REQUIRED_COLUMNS`.
- To restrict ranges, add boundary objects to `RANGE_RULES`.
- To validate format, add a key and regex to `FORMAT_PATTERNS`.

### 2. Custom Business Rules
1. Define a rule function inside `config/rules.py` that takes a `pd.DataFrame` and returns a boolean `pd.Series` (matching the DataFrame index):
   ```python
   def validate_quantity_limit(df: pd.DataFrame) -> pd.Series:
       return df["quantity"] <= 100
   ```
2. Register your function in the `BUSINESS_RULES` list inside `config/rules.py`:
   ```python
   BUSINESS_RULES = [
       # ("rule_name", rule_callable, "failure_reason")
       ("quantity_limit", validate_quantity_limit, "quantity_exceeds_max_limit")
   ]
   ```

---

## Best Practices
- **Single Responsibility**: Each validator handles one specific type of check. Decoupling null values from range/format validators ensures that missing values are flagged cleanly without generating redundant failures.
- **Defensive Types**: Dates and numbers are converted safely using `to_datetime` and `to_numeric` with `errors="coerce"` to prevent parsing exceptions from crashing the pipeline.
