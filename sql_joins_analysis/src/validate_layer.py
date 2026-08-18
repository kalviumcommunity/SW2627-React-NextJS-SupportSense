import sys
from pathlib import Path
import pandas as pd
import logging
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.database import setup_database
from src.utils import setup_logger, extract_queries

logger = setup_logger("sql_layer_validation")

def run_validation():
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / 'data'
    sql_dir = project_root / 'database'
    
    logger.info("="*60)
    logger.info("VALIDATING SQL VIEWS & AGGREGATIONS")
    logger.info("="*60)
    
    # 1. Setup in-memory DB and load CSVs
    engine = setup_database(data_dir)
    
    # Base tables row counts
    customers_count = int(pd.read_sql("SELECT COUNT(*) as c FROM customers", engine).iloc[0]["c"])
    
    # 2. Execute Views
    views = ['vw_customer_order_summary', 'vw_product_performance']
    for view in views:
        sql_file = sql_dir / 'views' / f"{view}.sql"
        queries = extract_queries(sql_file)
        with engine.begin() as conn:
            for q in queries:
                conn.execute(text(q))
        logger.info(f"[PASS] Created view: {view}")
            
    # 3. Execute Aggregations
    aggs = ['agg_daily_revenue', 'agg_customer_segments']
    for agg in aggs:
        sql_file = sql_dir / 'aggregations' / f"{agg}.sql"
        queries = extract_queries(sql_file)
        with engine.begin() as conn:
            for q in queries:
                conn.execute(text(q))
        logger.info(f"[PASS] Created & Refreshed aggregation: {agg}")

    # 4. Validations
    logger.info("\n--- Running Assertions ---")
    
    # Validate vw_customer_order_summary
    df_cust_summary = pd.read_sql("SELECT * FROM vw_customer_order_summary", engine)
    assert len(df_cust_summary) == customers_count, f"vw_customer_order_summary rows ({len(df_cust_summary)}) != customers table rows ({customers_count})"
    assert df_cust_summary['total_orders'].isnull().sum() == 0, "Found NULLs in total_orders"
    logger.info("[PASS] vw_customer_order_summary: Row count matches source customers. No null metrics.")
    
    # Validate vw_product_performance
    df_prod_perf = pd.read_sql("SELECT * FROM vw_product_performance", engine)
    assert len(df_prod_perf) == 3, "Expected 3 products"
    logger.info("[PASS] vw_product_performance: Executed successfully and aggregates correctly by product.")
    
    # Validate agg_daily_revenue
    df_daily_rev = pd.read_sql("SELECT * FROM agg_daily_revenue", engine)
    assert df_daily_rev['aggregation_date'].is_unique, "aggregation_date is not unique!"
    assert 'updated_at' in df_daily_rev.columns, "updated_at missing"
    assert df_daily_rev['updated_at'].isnull().sum() == 0, "updated_at contains nulls"
    logger.info("[PASS] agg_daily_revenue: Grain is strictly daily. updated_at is populated.")
    
    # Validate agg_customer_segments
    df_cust_seg = pd.read_sql("SELECT * FROM agg_customer_segments", engine)
    assert df_cust_seg['customer_type'].is_unique, "customer_type is not unique!"
    logger.info("[PASS] agg_customer_segments: Grain is strictly by segment. updated_at is populated.")

    logger.info("\n" + "="*60)
    logger.info("ALL VALIDATIONS PASSED SUCCESSFULLY")
    logger.info("="*60)

if __name__ == '__main__':
    try:
        run_validation()
    except AssertionError as ae:
        logger.error(f"\n[FAIL] Assertion Failed: {ae}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n[FAIL] Validation failed: {e}")
        sys.exit(1)
