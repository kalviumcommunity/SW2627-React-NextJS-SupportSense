# Enterprise Outlier Detection & Handling Framework

A production-ready, modular, and reusable Python framework for detecting and handling statistical outliers in numerical dataset columns. The framework enforces data integrity by performing non-destructive operations (preserving the original dataset) and generates detailed JSON reports and CSV cleaning logs to maintain a complete audit trail.

---

## What is an Outlier?

An **outlier** is a data point that differs significantly from other observations in a dataset. Outliers can arise due to:
1. **Measurement or entry errors** (e.g. typing an extra zero).
2. **True extreme variations** in the natural distribution of data (e.g. billionaire salaries in customer data).

> [!IMPORTANT]
> **An outlier is not automatically an error.** An outlier is only an unusual value, not automatically an invalid value. The decision to cap, remove, or flag outliers should be driven entirely by the business context and the downstream analytical/modeling objectives.

---

## Statistical Detection Methods

This framework supports two independent detection methods:

### 1. Z-Score Method
The **Z-score** represents the number of standard deviations a given data point is from the column mean.
- **Formula**: $Z = \frac{x - \mu}{\sigma}$
- **Default Threshold**: Absolute Z-score $> 3.0$
- **When to Use Z-Score**: Best suited for **normally distributed** (Gaussian) columns. Since it relies on the mean and standard deviation, it is sensitive to extremely large outliers, which can skew the mean and standard deviation themselves.

### 2. Interquartile Range (IQR) Method
The **IQR** method flags values that lie outside boundaries computed using the middle 50% range of the data.
- **Formulas**:
  - $IQR = Q3 - Q1$
  - $\text{Lower Bound} = Q1 - (1.5 \times IQR)$
  - $\text{Upper Bound} = Q3 + (1.5 \times IQR)$
- **Default Multiplier**: $1.5$
- **When to Use IQR**: Best suited for **skewed distributions** or datasets where variance is non-uniform, as percentiles are highly robust to extreme values and do not get easily skewed by them.

---

## Handling Strategies

The framework offers three selectable handling strategies to handle identified outliers:

| Strategy | Description | Best For | Data Preservation |
|---|---|---|---|
| **`flag`** | Keeps original values; creates a binary indicator column `is_<column>_outlier` (0 = normal, 1 = outlier). | Default choice. Best for ML feature engineering and explorative data analysis where raw values must not be lost. | 100% Preserved (Safest) |
| **`cap`** | Clips values below the lower boundary to the lower bound, and values above the upper boundary to the upper bound. | Reducing the leverage of extreme values without dropping rows (Winsorization). | Modified in-place (Non-destructive copy) |
| **`remove`** | Completely drops rows containing detected outliers in any target column. | Cleaning datasets from obvious input errors or preparing data for sensitive linear models. | Rows Removed |

---

## Project Structure

```text
outlier_detection/
├── config/
│   └── settings.py          # Central configurations and path variables
├── detectors/
│   ├── base_detector.py     # OutlierResult dataclass and detector interface
│   ├── zscore_detector.py   # Z-Score detection logic
│   └── iqr_detector.py      # IQR detection logic
├── handlers/
│   ├── base_handler.py      # Base handler interface
│   ├── cap_handler.py       # Capping strategy implementation
│   ├── remove_handler.py    # Row removal strategy implementation
│   └── flag_handler.py      # Flag/indicator strategy implementation
├── reports/
│   └── report_generator.py  # Formats JSON statistics and CSV cleaning logs
├── utils/
│   ├── logger.py            # Console and file logger config
│   └── helpers.py           # File loading/saving and datatype utils
├── main.py                  # CLI pipeline entrypoint
├── requirements.txt         # Package dependencies
└── README.md                # Project documentation
```

---

## Installation

1. Navigate to the project directory:
   ```bash
   cd outlier_detection
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the pipeline from the command line by executing `main.py` with the path to your dataset:

```bash
python main.py sample_data/customer_data.csv
```

### CLI Options

- `--method`: Outlier detection method. Choices: `zscore`, `iqr` (default: `zscore`).
- `--strategy`: Outlier handling strategy. Choices: `cap`, `remove`, `flag` (default: `flag`).
- `--keys`: Explicit list of numerical columns to process (separated by spaces). If omitted, the pipeline automatically detects all numerical columns.
- `--threshold`: Custom statistical threshold (overrides Z-score limit or IQR multiplier).
- `--output-file`: Custom path to save the processed dataset.

### Examples

**Run IQR detection and cap outliers on specific columns:**
```bash
python main.py sample_data/customer_data.csv --method iqr --strategy cap --keys salary age
```

**Run Z-Score detection and remove rows containing outliers:**
```bash
python main.py sample_data/customer_data.csv --method zscore --strategy remove --threshold 2.5
```

---

## Example Config & Outputs

### Configuration (`config/settings.py`)
Allows specifying the default methods, multipliers, and default path strings.

### Example Summary JSON Report (`output/outlier_report.json`)
```json
{
    "status": "SUCCESS",
    "detection_method": "iqr",
    "handling_strategy": "flag",
    "rows_before": 10,
    "rows_after": 10,
    "timestamp": "2026-08-07T08:00:00.000Z",
    "columns": {
        "age": {
            "lower_bound": 3.75,
            "upper_bound": 69.75,
            "outlier_count": 1,
            "outlier_percentage": 0.1
        }
    }
}
```

### Audit Log CSV (`output/outlier_cleaning_log.csv`)
Logs a trace of every action:
`timestamp,column,detection_method,handling_strategy,threshold,lower_bound,upper_bound,outlier_count,outlier_percentage,rows_removed,reason/action`
