import pandas as pd
import json
import traceback
from datetime import datetime
from pathlib import Path
from sqlalchemy.engine import Engine
from .utils import setup_logger, extract_queries

logger = setup_logger()

class TaskRunner:
    def __init__(self, engine: Engine, sql_dir: Path, output_dir: Path):
        self.engine = engine
        self.sql_dir = sql_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report = {
            "status": "PASS",
            "timestamp": datetime.utcnow().isoformat(),
            "customers": 0,
            "orders": 0,
            "customers_without_orders": 0,
            "orphaned_orders": 0,
            "join_validation": "PASS",
            "multi_table_validation": "PASS",
            "warnings": []
        }

    def run_all(self):
        try:
            self._load_base_metrics()
            self._run_task1()
            self._run_task2()
            self._run_task3()
            self._run_task4()
            self._generate_report()
            logger.info("\n[PASS] Complete pipeline execution and validation finished successfully!")
        except Exception as e:
            logger.error(f"\n[FAIL] Execution Failed: {str(e)}")
            self.report["status"] = "FAIL"
            self.report["error"] = traceback.format_exc()
            self._generate_report()
            raise

    def _load_base_metrics(self):
        self.report["customers"] = int(pd.read_sql("SELECT COUNT(*) as c FROM customers", self.engine).iloc[0]["c"])
        self.report["orders"] = int(pd.read_sql("SELECT COUNT(*) as c FROM orders", self.engine).iloc[0]["c"])

    def _run_task1(self):
        logger.info("\n--- TASK 1: LEFT JOIN ---")
        queries = extract_queries(self.sql_dir / 'task1_left_join.sql')
        df = pd.read_sql(queries[0], self.engine)
        
        # Validations
        rows_after = len(df)
        change_in_count = rows_after - self.report["customers"]
        pct_change = (change_in_count / self.report["customers"]) * 100 if self.report["customers"] > 0 else 0
        avg_orders = df["order_count"].mean()
        max_orders = df["order_count"].max()
        
        logger.info(f"[PASS] LEFT JOIN executed")
        logger.info(f"  Customers before join: {self.report['customers']}")
        logger.info(f"  Rows after join: {rows_after}")
        logger.info(f"  Change in row count: {change_in_count} ({pct_change:.1f}%)")
        logger.info(f"  Average orders per customer: {avg_orders:.1f}")
        logger.info(f"  Max orders for a single customer: {max_orders}")
        logger.info("  Explanation: The row count can increase/stay same after GROUP BY. However, an un-aggregated LEFT JOIN increases rows when a customer has multiple orders (1-to-Many).")
        
        raw_join_count = int(pd.read_sql("SELECT COUNT(*) as c FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id", self.engine).iloc[0]["c"])
        logger.info(f"  [Raw JOIN Rows]: {raw_join_count} (Raw join multiplied rows due to 1-to-Many relationship)")

    def _run_task2(self):
        logger.info("\n--- TASK 2: UNMATCHED KEYS ---")
        queries = extract_queries(self.sql_dir / 'task2_unmatched_keys.sql')
        
        # Query 1: Customers without orders
        df_missing = pd.read_sql(queries[0], self.engine)
        self.report["customers_without_orders"] = int(len(df_missing))
        df_missing.to_csv(self.output_dir / "customers_without_orders.csv", index=False)
        
        # Query 2: Orphaned orders
        df_orphaned = pd.read_sql(queries[1], self.engine)
        self.report["orphaned_orders"] = int(len(df_orphaned))
        df_orphaned.to_csv(self.output_dir / "orphaned_orders.csv", index=False)
        
        logger.info(f"[PASS] Unmatched keys checked")
        logger.info(f"  Customers without orders: {self.report['customers_without_orders']}")
        logger.info(f"  Orphaned orders: {self.report['orphaned_orders']}")
        if self.report['orphaned_orders'] > 0:
            logger.warning("  ! WARNING: Orphaned orders exist. These should be flagged for investigation.")

    def _run_task3(self):
        logger.info("\n--- TASK 3: COMPARE JOIN TYPES ---")
        queries = extract_queries(self.sql_dir / 'task3_join_comparison.sql')
        
        join_types = ["INNER JOIN", "LEFT JOIN", "FULL OUTER (UNION)"]
        results = []
        
        for i, q in enumerate(queries):
            df = pd.read_sql(q, self.engine)
            rows = len(df)
            customers = df["customer_id"].nunique()
            orders = df["order_id"].nunique()
            results.append({
                "JOIN TYPE": join_types[i],
                "ROWS": rows,
                "CUSTOMERS": customers,
                "ORDERS": orders
            })
            
        df_compare = pd.DataFrame(results)
        df_compare.to_csv(self.output_dir / "join_comparison.csv", index=False)
        logger.info(f"[PASS] JOIN types compared")
        logger.info(f"\n{df_compare.to_string(index=False)}")
        
        inner_rows = int(df_compare[df_compare["JOIN TYPE"] == "INNER JOIN"]["ROWS"].iloc[0])
        left_rows = int(df_compare[df_compare["JOIN TYPE"] == "LEFT JOIN"]["ROWS"].iloc[0])
        if inner_rows > left_rows:
            self.report["join_validation"] = "FAIL"
            raise AssertionError("INNER JOIN returned more rows than LEFT JOIN, which is mathematically impossible.")

    def _run_task4(self):
        logger.info("\n--- TASK 4: MULTI-TABLE JOIN ---")
        queries = extract_queries(self.sql_dir / 'task4_multi_table_join.sql')
        df_multi = pd.read_sql(queries[0], self.engine)
        
        total_line_amount = float(df_multi["line_total"].sum())
        
        independent_sql = """
            SELECT SUM(i.quantity * i.unit_price) as true_total
            FROM order_items i
            WHERE i.order_id IN (
                SELECT o.order_id 
                FROM orders o 
                JOIN customers c ON o.customer_id = c.customer_id 
                WHERE c.customer_type = 'Enterprise'
            )
        """
        true_total = float(pd.read_sql(independent_sql, self.engine).iloc[0]["true_total"])
        
        logger.info(f"[PASS] Multi-table JOIN executed")
        logger.info(f"  Calculated Total from JOIN: ${total_line_amount:,.2f}")
        logger.info(f"  Independent Source Total: ${true_total:,.2f}")
        
        if abs(total_line_amount - true_total) > 0.01:
            self.report["multi_table_validation"] = "FAIL"
            self.report["warnings"].append("Financial totals do not match! Possible accidental duplication in JOIN.")
            logger.error("  ! ERROR: Totals do not match. Review JOIN for accidental cross-products.")
        else:
            logger.info("[PASS] Financial totals validated (No duplication detected)")
            
        df_multi.to_csv(self.output_dir / "enterprise_order_details.csv", index=False)

    def _generate_report(self):
        report_path = self.output_dir / "validation_report.json"
        
        # Ensure all types in report are JSON serializable
        def convert_types(obj):
            if isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(i) for i in obj]
            elif pd.api.types.is_integer_dtype(type(obj)):
                return int(obj)
            elif pd.api.types.is_float_dtype(type(obj)):
                return float(obj)
            else:
                return obj
                
        safe_report = convert_types(self.report)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(safe_report, f, indent=4)

