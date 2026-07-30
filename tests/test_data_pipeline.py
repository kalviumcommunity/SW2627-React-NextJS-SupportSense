"""
Unit Tests for SupportSense Data Pipeline (scripts/data_pipeline.py)
=====================================================================
Validates ingestion, processing transformations, output writing, and
error handling behaviors of the Three-Function Pattern implementation.
"""

import os
import sys
import tempfile
import pytest
import pandas as pd

# Add project root directory to path to import data_pipeline script
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from scripts.data_pipeline import ingest_data, process_data, output_results


@pytest.fixture
def sample_raw_dataframe():
    """Fixture providing a sample DataFrame mimicking raw support tickets."""
    return pd.DataFrame({
        'ticket_id': ['T-1001', 'T-1002', 'T-1003', 'T-1001'],
        'customer_id': ['C-01', 'C-02', 'C-03', 'C-01'],
        'created_at': ['2025-01-01 10:00:00', '2025-01-02 11:00:00', '2025-01-03 12:00:00', '2025-01-01 10:00:00'],
        'resolved_at': ['2025-01-01 12:00:00', '2025-01-04 15:00:00', None, '2025-01-01 12:00:00'],
        'category': ['Billing', 'Technical', 'Cancellation', 'Billing'],
        'resolution_status': ['RESOLVED', 'RESOLVED', 'UNRESOLVED', 'RESOLVED'],
        'escalated': [False, True, True, False],
        'satisfaction_score': [5.0, 1.0, None, 5.0],
        'monthly_spend': [50.0, 300.0, 500.0, 50.0],
        'churn_flag': [0, 1, 1, 0]
    })


def test_ingest_data_success(sample_raw_dataframe):
    """Test ingest_data reads valid CSV files cleanly."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        sample_raw_dataframe.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    try:
        df = ingest_data(tmp_path)
        assert len(df) == 4
        assert 'ticket_id' in df.columns
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_ingest_data_file_not_found():
    """Test ingest_data raises FileNotFoundError for non-existent files."""
    with pytest.raises(FileNotFoundError):
        ingest_data("non_existent_directory/invalid_file.csv")


def test_ingest_data_empty_file():
    """Test ingest_data raises ValueError when given an empty CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write("")  # empty file
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError):
            ingest_data(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_process_data_deduplication(sample_raw_dataframe):
    """Test process_data removes duplicate tickets."""
    processed_df = process_data(sample_raw_dataframe)
    # Original has 4 rows with 1 duplicate ticket_id 'T-1001'
    assert len(processed_df) == 3


def test_process_data_imputation(sample_raw_dataframe):
    """Test missing satisfaction scores are imputed with median."""
    processed_df = process_data(sample_raw_dataframe)
    assert not processed_df['satisfaction_score'].isna().any()


def test_process_data_churn_risk_scoring(sample_raw_dataframe):
    """Test churn risk scores and risk categories are calculated."""
    processed_df = process_data(sample_raw_dataframe)
    assert 'churn_risk_score' in processed_df.columns
    assert 'churn_risk_category' in processed_df.columns
    
    # High risk ticket T-1003 (escalated, unresolved, high spend)
    t1003 = processed_df[processed_df['ticket_id'] == 'T-1003'].iloc[0]
    assert t1003['churn_risk_category'] == 'HIGH'
    assert t1003['churn_risk_score'] >= 70.0


def test_output_results_success(sample_raw_dataframe):
    """Test output_results writes processed DataFrame to CSV."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_path = os.path.join(tmp_dir, "output.csv")
        output_results(sample_raw_dataframe, output_path)
        assert os.path.exists(output_path)
        
        loaded_df = pd.read_csv(output_path)
        assert len(loaded_df) == len(sample_raw_dataframe)


def test_output_results_empty_df():
    """Test output_results raises ValueError when DataFrame is empty."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        output_results(empty_df, "dummy_path.csv")
