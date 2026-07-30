"""
SupportSense Data Pipeline - Customer Support & Churn Analysis
=============================================================
This script processes customer support ticket data to connect unresolved
complaints and ticket escalation metrics with customer cancellation behavior.

Architecture:
    Follows the Three-Function Pattern (Ingest, Process, Output) to ensure
    separation of concerns, testability, and automation readiness.
"""

# 1. IMPORTS
import os
import sys
import logging
from datetime import datetime
import pandas as pd
import numpy as np

# 2. CONFIGURATION & CONSTANTS
# Absolute / relative file paths for script execution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

INPUT_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "customer_support_tickets.csv")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "processed_churn_tickets.csv")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "workflow.log")

# Business Thresholds & Filter Constants
MIN_MONTHLY_SPEND = 0.0
HIGH_RISK_THRESHOLD = 70.0
DEFAULT_SATISFACTION_FILL = 3.0

# 3. LOGGING SETUP
# Ensure logs directory exists before configuring log file
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)


# 4. MAIN FUNCTIONS

def ingest_data(filepath: str) -> pd.DataFrame:
    """
    Read raw customer support ticket CSV dataset into a Pandas DataFrame.

    This function is strictly responsible for data retrieval and basic file
    validation. It performs no business transformations or filtering.

    Args:
        filepath (str): Absolute or relative file path to the input CSV file.

    Returns:
        pd.DataFrame: Loaded raw DataFrame containing customer support records.

    Raises:
        FileNotFoundError: If the specified filepath does not exist.
        ValueError: If the ingested file is empty or corrupted.

    Example:
        >>> df = ingest_data("data/raw/customer_support_tickets.csv")
        >>> isinstance(df, pd.DataFrame)
        True
    """
    logging.info(f"Initiating data ingestion from: {filepath}")

    if not os.path.exists(filepath):
        error_msg = f"Input file not found at location: {filepath}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        logging.error(f"Failed to parse CSV file at {filepath}: {str(e)}")
        raise ValueError(f"Corrupted or invalid CSV file: {str(e)}") from e

    if df.empty:
        error_msg = f"Ingested dataset from {filepath} is empty."
        logging.error(error_msg)
        raise ValueError(error_msg)

    logging.info(f"Successfully ingested {len(df)} rows and {len(df.columns)} columns from {filepath}")
    return df


def process_data(df: pd.DataFrame, min_monthly_spend: float = MIN_MONTHLY_SPEND) -> pd.DataFrame:
    """
    Apply cleaning, feature engineering, and churn risk scoring to support tickets.

    Business transformations performed:
    1. Deduplicates ticket records.
    2. Imputes missing satisfaction scores using median score (resilient to outliers).
    3. Calculates ticket resolution time in hours.
    4. Engineers composite churn risk score based on resolution delays, escalations,
       and satisfaction scores.
    5. Classifies customers into Churn Risk categories (HIGH, MEDIUM, LOW).

    Args:
        df (pd.DataFrame): Ingested raw DataFrame containing support ticket records.
        min_monthly_spend (float): Minimum monthly spend threshold for filtering active records.

    Returns:
        pd.DataFrame: Transformed DataFrame with engineered features and risk scores.

    Raises:
        ValueError: If required columns are missing from the input DataFrame.

    Example:
        >>> sample_df = pd.DataFrame({
        ...     'ticket_id': ['T1'], 'customer_id': ['C1'],
        ...     'created_at': ['2025-01-01 10:00:00'], 'resolved_at': ['2025-01-01 12:00:00'],
        ...     'category': ['Billing'], 'resolution_status': ['RESOLVED'],
        ...     'escalated': [True], 'satisfaction_score': [1.0],
        ...     'monthly_spend': [100.0], 'churn_flag': [1]
        ... })
        >>> processed_df = process_data(sample_df)
        >>> 'churn_risk_score' in processed_df.columns
        True
    """
    if df.empty:
        raise ValueError("Input DataFrame for processing cannot be empty.")

    required_cols = {'ticket_id', 'customer_id', 'created_at', 'category', 'resolution_status', 'escalated', 'monthly_spend'}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Input DataFrame is missing required columns: {missing_cols}")

    rows_initial = len(df)
    processed_df = df.copy()

    # Deduplicate records based on unique ticket ID
    processed_df = processed_df.drop_duplicates(subset=['ticket_id'])
    rows_deduped = len(processed_df)
    if rows_initial != rows_deduped:
        logging.info(f"Removed {rows_initial - rows_deduped} duplicate ticket records.")

    # Filter by minimum monthly spend threshold
    processed_df = processed_df[processed_df['monthly_spend'] >= min_monthly_spend]

    # Impute missing satisfaction scores using median value
    # Median is preferred over mean to avoid skewing by extreme negative ratings
    if 'satisfaction_score' in processed_df.columns:
        median_sat = processed_df['satisfaction_score'].median()
        fill_val = median_sat if not pd.isna(median_sat) else DEFAULT_SATISFACTION_FILL
        processed_df['satisfaction_score'] = processed_df['satisfaction_score'].fillna(fill_val)

    # Convert timestamps and calculate resolution duration in hours
    processed_df['created_at_dt'] = pd.to_datetime(processed_df['created_at'], errors='coerce')
    processed_df['resolved_at_dt'] = pd.to_datetime(processed_df['resolved_at'], errors='coerce')

    # Resolution time calculation: null for pending/unresolved tickets
    resolution_duration = (processed_df['resolved_at_dt'] - processed_df['created_at_dt']).dt.total_seconds() / 3600.0
    processed_df['resolution_hours'] = resolution_duration.fillna(-1.0)

    # Feature Engineering: Churn Risk Score Calculation (0-100)
    # Escalated tickets +30 points, low satisfaction (< 3.0) +30 points, unresolved +25 points, high monthly spend (> 200) +15 points
    risk_score = np.zeros(len(processed_df))

    # Add points for ticket escalation
    risk_score += np.where(processed_df['escalated'] == True, 30.0, 0.0)

    # Add points for low satisfaction scores
    if 'satisfaction_score' in processed_df.columns:
        risk_score += np.where(processed_df['satisfaction_score'] < 3.0, 30.0, 0.0)

    # Add points for unresolved complaints
    risk_score += np.where(processed_df['resolution_status'] != 'RESOLVED', 25.0, 0.0)

    # High spend customer at risk is high impact for business
    risk_score += np.where(processed_df['monthly_spend'] >= 200.0, 15.0, 0.0)

    processed_df['churn_risk_score'] = np.clip(risk_score, 0.0, 100.0)

    # Segment risk levels into categorical labels
    risk_conditions = [
        (processed_df['churn_risk_score'] >= 70.0),
        (processed_df['churn_risk_score'] >= 40.0) & (processed_df['churn_risk_score'] < 70.0),
        (processed_df['churn_risk_score'] < 40.0)
    ]
    risk_labels = ['HIGH', 'MEDIUM', 'LOW']
    processed_df['churn_risk_category'] = np.select(risk_conditions, risk_labels, default='LOW')

    # Clean up temporary datetime helper columns
    processed_df.drop(columns=['created_at_dt', 'resolved_at_dt'], inplace=True, errors='ignore')

    logging.info(
        f"Processing completed: {rows_initial} raw records -> {len(processed_df)} final clean records. "
        f"Identified {sum(processed_df['churn_risk_category'] == 'HIGH')} high-risk tickets."
    )
    return processed_df


def output_results(df: pd.DataFrame, filepath: str) -> None:
    """
    Write processed DataFrame to designated output destination (CSV file).

    This function handles file output, directory creation, and final logging.
    It does not perform data transformation or calculation.

    Args:
        df (pd.DataFrame): Processed DataFrame to export.
        filepath (str): Output destination file path.

    Raises:
        ValueError: If DataFrame is empty.
        IOError: If writing to destination fails.

    Example:
        >>> sample_df = pd.DataFrame({'ticket_id': ['T1'], 'churn_risk_score': [85.0]})
        >>> output_results(sample_df, "data/processed/test_output.csv")
    """
    if df.empty:
        error_msg = "Cannot output empty DataFrame to destination."
        logging.error(error_msg)
        raise ValueError(error_msg)

    # Ensure output destination directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        df.to_csv(filepath, index=False)
        logging.info(f"Successfully saved {len(df)} records to output destination: {filepath}")
        print(f"✓ Processed dataset saved successfully to: {filepath} ({len(df)} records)")
    except Exception as e:
        error_msg = f"Failed to write output results to {filepath}: {str(e)}"
        logging.error(error_msg)
        raise IOError(error_msg) from e


# 5. MAIN EXECUTION BLOCK
if __name__ == "__main__":
    logging.info("Starting SupportSense Data Workflow Pipeline...")
    print("Starting SupportSense Data Pipeline execution...")

    try:
        # Step 1: Ingest
        raw_data = ingest_data(INPUT_FILE)

        # Step 2: Process
        processed_data = process_data(raw_data, min_monthly_spend=MIN_MONTHLY_SPEND)

        # Step 3: Output
        output_results(processed_data, OUTPUT_FILE)

        logging.info("SupportSense Data Workflow Pipeline completed successfully.")
        print("✓ Workflow pipeline completed successfully.")
        sys.exit(0)

    except Exception as e:
        logging.error(f"SupportSense Data Workflow Pipeline failed: {str(e)}")
        print(f"❌ Workflow execution failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
