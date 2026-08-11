# Behavioural Analysis & User Segmentation Framework

A production-quality Python pipeline designed to load customer data, group customers into meaningful behavioral segments, calculate essential metrics, rank their performance, visualize comparisons, and generate automated, data-driven business insights.

## Project Overview

**Behavioural Segmentation** is the process of grouping customers based on their actions, lifecycle value, and engagement patterns rather than just static demographics. 

**Why aggregate averages hide the truth:**
Looking at a "global average churn rate" or "global average lifetime value (LTV)" often obscures deep structural problems. If enterprise users churn at 1% but SMB users churn at 20%, the global average might be 10%, leading stakeholders to misunderstand both segments. This framework breaks down those aggregates to uncover actionable realities.

## Core Capabilities

1. **Metrics Calculation**: Automatically calculates Average LTV, Churn Rate, Average Support Tickets, and Average Retention Days per segment.
2. **Segment Ranking**: Ranks segments across LTV, Churn, and Retention to identify top and bottom performers dynamically.
3. **Heatmap & Visualizations**: Uses Min-Max normalized heatmaps and individual bar charts to visually communicate magnitude differences between segments.
4. **Sample-Size Awareness**: Statistically safeguards insights by warning if segment populations drop below reliable thresholds (e.g., < 30 customers).
5. **Business Insights**: Translates numeric differences into plain-English behavioral characteristics, explaining *what it is*, *why it matters*, and *what action to take*.

## Project Structure

```text
behavioural_segmentation/
├── config/
│   └── settings.py
├── validation/
│   └── dataset_validator.py
├── analysis/
│   ├── segment_metrics.py
│   ├── segment_ranking.py
│   ├── segment_comparison.py
│   └── insight_generator.py
├── visualization/
│   ├── heatmap.py
│   └── comparison_charts.py
├── output/
├── sample_data/
│   └── customers.csv
├── utils/
│   ├── logger.py
│   └── helpers.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the primary segmentation analysis (defaulting to the `customer_type` column):

```bash
python main.py sample_data/customers.csv
```

Run secondary segmentation by specifying a different column:

```bash
python main.py sample_data/customers.csv --segment-by region
```

## Outputs Generated

All analysis artifacts are saved in the `output/` directory:

- **`segment_summary.csv`**: A data table containing customer counts, metric averages, and numeric rankings per segment.
- **`segment_insights.json`**: An array of segment-specific narrative insights, including the magnitude of metric differences.
- **`analysis_report.json`**: A comprehensive payload containing all raw metrics, size percentages, warnings, and top performers.
- **`segment_comparison_heatmap.png`**: A normalized seaborn heatmap for visual cross-metric comparison.
- **Individual metric charts**: `ltv_by_segment.png`, `churn_by_segment.png`, `tickets_by_segment.png`, `retention_by_segment.png`.

## How to Add a New Segmentation Column

The framework is built dynamically. You do not need to change code to segment by a new column. Simply ensure the column exists in your dataset and pass it via the CLI:

```bash
python main.py data.csv --segment-by product_tier
```

## Limitations

- **Correlation != Causation**: Insights generated point to strong associations between metrics (e.g., high ticket volume associated with high churn), but they do not prove direct causation.
- **Linear Scaling**: The heatmap uses Min-Max scaling. Extreme outliers in a specific segment can compress the color gradient for other segments.
