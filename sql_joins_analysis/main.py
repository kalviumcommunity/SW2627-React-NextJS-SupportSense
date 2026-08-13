import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.database import setup_database
from src.task_runner import TaskRunner
from src.utils import setup_logger

def main():
    logger = setup_logger()
    logger.info("==================================================")
    logger.info("SQL JOINS & MULTI-TABLE ANALYSIS PIPELINE")
    logger.info("==================================================\n")
    
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / 'data'
    sql_dir = project_root / 'sql'
    output_dir = project_root / 'output'
    
    try:
        engine = setup_database(data_dir)
        runner = TaskRunner(engine, sql_dir, output_dir)
        runner.run_all()
    except Exception as e:
        logger.error("Pipeline failed. See trace above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
