"""
Quality Assessor
Aggregates profiling results, calculates a health score, and generates warnings and recommendations.
"""

from typing import Dict, Any, List
from dataset_profiling.utils.logger import get_logger

logger = get_logger(__name__)

class QualityAssessor:
    """Class to assess the overall quality of a dataset based on profiling results."""

    @staticmethod
    def assess(
        null_results: Dict[str, Any],
        duplicate_results: Dict[str, Any],
        numerical_results: Dict[str, Any],
        categorical_results: Dict[str, Any],
        datatype_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assesses quality and generates health score, warnings, errors, and recommendations.
        
        Args:
            null_results (Dict): Output from NullProfiler.
            duplicate_results (Dict): Output from DuplicateProfiler.
            numerical_results (Dict): Output from NumericalProfiler.
            categorical_results (Dict): Output from CategoricalProfiler.
            datatype_results (Dict): Output from DataTypeProfiler.
            
        Returns:
            Dict[str, Any]: Assessment results including health score and issues.
        """
        logger.info("Starting Quality Assessment...")
        
        warnings: List[str] = []
        errors: List[str] = []
        recommendations: List[str] = []
        quality_issues: List[Dict[str, Any]] = []
        
        health_score = 100
        
        # 1. Null Analysis
        high_null_cols = null_results.get("columns_exceeding_threshold", [])
        if high_null_cols:
            score_penalty = len(high_null_cols) * 2
            health_score -= min(score_penalty, 20)  # Max 20 points penalty for nulls
            errors.append(f"High missing values in columns: {', '.join(high_null_cols)}")
            recommendations.append("Impute or drop columns with high missing value percentages.")
            for col in high_null_cols:
                quality_issues.append({"type": "High Missing Values", "column": col})
                
        # 2. Duplicate Analysis
        if duplicate_results.get("exceeds_threshold"):
            health_score -= 15
            errors.append(f"High duplicate rows percentage: {duplicate_results.get('duplicate_percentage')}%")
            recommendations.append("Remove exact duplicate rows to prevent bias.")
            quality_issues.append({"type": "Duplicate Records", "details": "Exceeds threshold"})
            
        # 3. Categorical Analysis
        for col, metrics in categorical_results.items():
            if metrics.get("is_constant"):
                health_score -= 1
                warnings.append(f"Column '{col}' has a constant value.")
                recommendations.append(f"Drop constant column '{col}' as it provides no variance.")
                quality_issues.append({"type": "Constant Column", "column": col})
            elif metrics.get("cardinality") == "High":
                health_score -= 1
                warnings.append(f"Column '{col}' has high cardinality.")
                quality_issues.append({"type": "High Cardinality", "column": col})
                
        # 4. Numerical Analysis
        for col, metrics in numerical_results.items():
            min_val = metrics.get("minimum")
            if min_val is not None and min_val < 0:
                warnings.append(f"Column '{col}' contains negative values.")
                quality_issues.append({"type": "Negative Values", "column": col})
                
        # 5. Data Type Analysis
        suspicious_cols = datatype_results.get("suspicious_columns", [])
        for issue in suspicious_cols:
            health_score -= 2
            col = issue["column"]
            reason = issue["reason"]
            warnings.append(f"Column '{col}' has suspicious type: {reason}")
            recommendations.append(f"Convert column '{col}' to appropriate native data type.")
            quality_issues.append({"type": "Suspicious Data Type", "column": col, "reason": reason})
            
        # Ensure health score is within 0-100
        health_score = max(0, min(health_score, 100))
        
        logger.info(f"Quality Assessment completed. Health Score: {health_score}")
        
        return {
            "health_score": health_score,
            "quality_issues": quality_issues,
            "warnings": warnings,
            "errors": errors,
            "recommendations": recommendations
        }
