"""
Main CLI entry point for the Dataset Profiling Framework.
Orchestrates loading data, profiling, and reporting.
"""

import sys
import json
import argparse
from pathlib import Path
import pandas as pd

from dataset_profiling.utils.logger import get_logger
from dataset_profiling.utils.helpers import format_memory_size
from dataset_profiling.config.settings import SETTINGS

from dataset_profiling.profiler.null_profiler import NullProfiler
from dataset_profiling.profiler.duplicate_profiler import DuplicateProfiler
from dataset_profiling.profiler.numerical_profiler import NumericalProfiler
from dataset_profiling.profiler.categorical_profiler import CategoricalProfiler
from dataset_profiling.profiler.datatype_profiler import DataTypeProfiler
from dataset_profiling.profiler.quality_assessor import QualityAssessor

logger = get_logger(__name__)

def load_dataset(file_path: str) -> pd.DataFrame:
    """Loads a dataset from a file path."""
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
        
    try:
        logger.info(f"Loading dataset from {file_path}...")
        if path.suffix.lower() == '.csv':
            return pd.read_csv(path)
        elif path.suffix.lower() == '.json':
            return pd.read_json(path)
        else:
            logger.error(f"Unsupported file extension: {path.suffix}")
            sys.exit(1)
    except pd.errors.EmptyDataError:
        logger.error("Dataset is empty.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Dataset Profiling Framework")
    parser.add_argument("file_path", help="Path to the dataset file (CSV/JSON)")
    args = parser.parse_args()
    
    df = load_dataset(args.file_path)
    
    # Generate Dataset Overview
    memory_usage = df.memory_usage(deep=True).sum()
    overview = {
        "rows": len(df),
        "columns": len(df.columns),
        "memory": format_memory_size(memory_usage),
        "column_names": list(df.columns),
        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    
    # Run Profilers
    null_results = NullProfiler.profile(df)
    duplicate_results = DuplicateProfiler.profile(df)
    numerical_results = NumericalProfiler.profile(df)
    categorical_results = CategoricalProfiler.profile(df)
    datatype_results = DataTypeProfiler.profile(df)
    
    # Assess Quality
    assessment = QualityAssessor.assess(
        null_results,
        duplicate_results,
        numerical_results,
        categorical_results,
        datatype_results
    )
    
    # Construct Final Report
    report = {
        "status": "SUCCESS",
        "dataset": overview,
        "null_analysis": null_results,
        "duplicates": duplicate_results,
        "numerical_summary": numerical_results,
        "categorical_summary": categorical_results,
        "data_type_analysis": datatype_results,
        "quality_issues": assessment["quality_issues"],
        "health_score": assessment["health_score"],
        "warnings": assessment["warnings"],
        "errors": assessment["errors"],
        "recommendations": assessment["recommendations"]
    }
    
    # Save Report
    reports_dir = Path("dataset_profiling") / SETTINGS.REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / SETTINGS.DEFAULT_REPORT_FILENAME
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        logger.info(f"Profiling completed successfully. Report saved to {report_path}")
        print(f"Profiling successful. Report generated at: {report_path}")
        print(f"Dataset Health Score: {assessment['health_score']}/100")
        
        if assessment['errors']:
            print(f"Found {len(assessment['errors'])} critical errors.")
        if assessment['warnings']:
            print(f"Found {len(assessment['warnings'])} warnings.")
            
    except Exception as e:
        logger.error(f"Failed to write report to JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
