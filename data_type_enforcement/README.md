# Data Type Enforcement & Standardization Framework

A production-ready Python framework that enforces correct data types across datasets before downstream processing begins. Designed for enterprise ETL pipelines and data preprocessing frameworks.

## Project Overview

This framework is built to standardize data types while preserving data integrity and generating detailed conversion reports. It strictly acts as a gatekeeper to ensure proper data typing without performing data cleaning (like removing NaNs or dropping duplicates).

## Architecture

The system follows Clean Architecture principles:
- **Configuration**: Centralized definitions for types, formats, and settings.
- **Converters**: Single-responsibility modules (Date, Currency, Boolean) to handle specific logic.
- **Validators**: Verifies conversion results against schemas.
- **Utils**: Enterprise-grade logging and shared utilities.

## Folder Structure

```
data_type_enforcement/
├── converters/
│   ├── date_converter.py
│   ├── currency_converter.py
│   ├── boolean_converter.py
│   ├── datatype_converter.py
├── validators/
│   ├── dtype_validator.py
├── config/
│   ├── settings.py
├── reports/
├── utils/
│   ├── logger.py
│   ├── helpers.py
├── sample_data/
├── output/
├── main.py
├── requirements.txt
├── README.md
```

## Supported Data Types

- **Boolean**: Maps string variants ("yes", "y", "true", "1") to standard `bool`.
- **Datetime**: Strictly enforces specific datetime formats.
- **Currency**: Safely converts currency strings (removing symbols/spaces) to `float`.
- **Numeric/String**: Standard type casting via Pandas.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py sample_data/untyped_data.csv
```

## Configuration

Update `config/settings.py` to modify default behaviors, such as adding new currency symbols, updating target schemas, or configuring date formats.

## Conversion Reports

Every run generates comprehensive reports:
- `output/dtype_conversion_report.csv`
- `output/dtype_conversion_report.json`

## Future Improvements

- Streaming capabilities for larger-than-memory datasets.
- Support for distributed frameworks like PySpark or Dask.
- Real-time notification hooks for validation failures.
