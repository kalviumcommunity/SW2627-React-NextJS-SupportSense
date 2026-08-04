# Dataset Profiling & Quality Assessment Framework

A production-ready, enterprise-scale dataset profiling framework built with Python. This framework analyzes the quality of a dataset *before* any cleaning or preprocessing begins, identifying quality issues, generating detailed profiling reports, and providing actionable insights.

## Architecture

This project follows SOLID principles and Clean Architecture, separating the profiling logic into highly cohesive, modular components:

*   **NullProfiler**: Analyzes missing values, calculates percentages, and ranks them.
*   **DuplicateProfiler**: Identifies exact duplicate rows.
*   **NumericalProfiler**: Computes statistical metrics (min, max, mean, variance, IQR, etc.) for numeric data.
*   **CategoricalProfiler**: Computes frequencies, cardinality, and top categories for non-numeric data.
*   **DataTypeProfiler**: Detects suspicious column types (e.g., numeric values stored as objects).
*   **QualityAssessor**: Aggregates all profiling results to generate a comprehensive "Dataset Health Score", alongside actionable warnings and errors.

## Folder Structure

```
dataset_profiling/
│
├── profiler/
│   ├── null_profiler.py
│   ├── duplicate_profiler.py
│   ├── numerical_profiler.py
│   ├── categorical_profiler.py
│   ├── datatype_profiler.py
│   ├── quality_assessor.py
│
├── reports/
│   ├── logs/
│
├── config/
│   ├── settings.py
│
├── utils/
│   ├── logger.py
│   ├── helpers.py
│
├── sample_data/
│
├── main.py
├── requirements.txt
├── README.md
```

## Installation

1. Clone the repository or copy the `dataset_profiling` directory.
2. Ensure you have Python 3.12+ installed.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

You can configure thresholds for profiling in `config/settings.py`. Available settings include:
- `NULL_THRESHOLD`: Threshold for flagging columns with high null percentages (default: 30.0).
- `DUPLICATE_THRESHOLD`: Threshold for flagging high duplicate row percentages (default: 5.0).
- `HIGH_CARDINALITY_THRESHOLD`: Threshold for defining a column as high cardinality (default: 100).
- `MAX_DUPLICATE_SAMPLES`: Max number of duplicate samples included in the final report.

## Usage

Execute the framework by providing a path to a CSV or JSON dataset:

```bash
python main.py ../data/raw/customers.csv
```

### Example Commands
```bash
# Profile a CSV dataset
python main.py sample_data/customers.csv

# Profile a JSON dataset
python main.py sample_data/transactions.json
```

## Output

The framework generates a comprehensive JSON report at `reports/profile_report.json` containing:

*   **Dataset Overview**: Rows, columns, memory usage.
*   **Null Analysis**: Rankings and counts of missing values.
*   **Duplicate Analysis**: Counts, percentages, and samples of duplicate rows.
*   **Numerical & Categorical Summaries**: Deep statistical insights per column.
*   **Data Type Analysis**: Flags for suspicious types.
*   **Quality Assessment**: A final Health Score (0-100), accompanied by specific warnings, errors, and recommendations.

## Future Improvements

The modular design allows for seamless integration of future capabilities, such as:
- **Outlier Detection**: Interquartile range (IQR) and Z-score based outlier detection.
- **Correlation Analysis**: Pearson and Spearman correlation matrices for feature relationship insights.
- **Data Drift Detection**: Comparing new datasets against baseline statistics to detect distribution shifts.
- **Automated Quality Monitoring**: Integration with orchestrators (like Airflow) to automatically halt pipelines if the health score drops below a specific threshold.
