import pandas as pd
from sqlalchemy import create_engine
import logging
from pathlib import Path

logger = logging.getLogger("sql_joins.database")

def setup_database(data_dir: Path):
    """
    Sets up an in-memory SQLite database and loads the CSV datasets into it.
    Returns the SQLAlchemy engine.
    """
    logger.info("Setting up in-memory SQLite database...")
    engine = create_engine('sqlite:///:memory:', echo=False)
    
    csv_files = {
        'customers': data_dir / 'customers.csv',
        'orders': data_dir / 'orders.csv',
        'order_items': data_dir / 'order_items.csv',
        'products': data_dir / 'products.csv'
    }
    
    for table_name, file_path in csv_files.items():
        if not file_path.exists():
            raise FileNotFoundError(f"Missing dataset: {file_path}")
            
        df = pd.read_csv(file_path)
        df.to_sql(table_name, con=engine, index=False, if_exists='replace')
        logger.info(f"[PASS] {table_name.capitalize()} table loaded ({len(df)} rows)")
        
    return engine
