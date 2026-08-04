# Data Dictionary & Business Context Mapping

## Dataset Overview
This dataset contains customer profiles, transaction logs, and support ticket interaction records updated daily from the CRM and Customer Support systems. It serves as the primary data foundation for SupportSense analytics, revenue modeling, and churn prediction pipelines.

- **Last Updated**: 2025-05-21
- **Maintained By**: Data Engineering & Analytics Team
- **Primary Data Sources**: CRM Database, Support Ticketing System (Zendesk API), Billing Engine
- **Refresh Frequency**: Daily batch updates at 02:00 UTC

---

## Columns Specification

### customer_id
- **Type**: Integer / String
- **Business Meaning**: Unique customer identifier assigned in the CRM system.
- **Example**: `12456` or `CUST-501`
- **Unit**: N/A (Primary Key)
- **Null Handling**: Never null (Primary key integrity requirement)
- **Related KPI**: Customer tracking, Customer Lifetime Value (CLV), Churn Rate
- **Updates**: Assigned upon customer registration in CRM

### trnx_amt
- **Type**: Float
- **Business Meaning**: Revenue generated from a single transaction.
- **Example**: `150.99`
- **Unit**: USD ($)
- **Null Handling**: Very rare - flag and investigate if null
- **Related KPI**: Monthly Revenue, Average Order Value (AOV), Customer Spend Velocity
- **Updates**: Recorded at transaction completion

### purchase_date
- **Type**: Datetime
- **Business Meaning**: Precise timestamp when a sales transaction was completed.
- **Example**: `2025-01-15 14:30:00`
- **Unit**: YYYY-MM-DD HH:MM:SS (UTC)
- **Null Handling**: Never null
- **Related KPI**: Sales Velocity, Revenue Growth Rate, Purchase Recency
- **Updates**: Immutable after creation

### cust_segment
- **Type**: String
- **Business Meaning**: Business market classification of the customer account (B2B, B2C, SMB).
- **Valid Values**: `B2B`, `B2C`, `SMB`
- **Example**: `B2B`
- **Null Handling**: If null, classify default as `UNKNOWN`
- **Related KPI**: Segment Revenue, Segment Churn Rate, ARPU by Segment
- **Updates**: Updated monthly from CRM account tiering rules

### flag_churn
- **Type**: Integer (0/1) / Boolean
- **Business Meaning**: Binary indicator marking whether a customer churned (canceled service) within 90 days following a ticket or purchase event.
- **Example**: `0` (Active) or `1` (Churned)
- **Unit**: Binary (0 = Retained, 1 = Churned)
- **Null Handling**: Defaults to `0` (False) if active
- **Related KPI**: Churn Rate, Retention Rate, Risk Score Validation
- **Updates**: Evaluated and updated on a 90-day rolling window

### ticket_id
- **Type**: String
- **Business Meaning**: Unique support ticket reference number in Zendesk/Support portal.
- **Example**: `TICK-1001`
- **Unit**: Alpha-numeric Identifier
- **Null Handling**: Never null (Primary key for support dataset)
- **Related KPI**: Support Ticket Volume, Ticket Resolution Rate
- **Updates**: Auto-generated on support ticket creation

### created_at
- **Type**: Datetime
- **Business Meaning**: Timestamp when the customer submitted the support ticket.
- **Example**: `2025-01-10 08:30:00`
- **Unit**: YYYY-MM-DD HH:MM:SS (UTC)
- **Null Handling**: Never null
- **Related KPI**: First Response Time, Daily Support Ticket Load
- **Updates**: Set at ticket submission time

### resolved_at
- **Type**: Datetime
- **Business Meaning**: Timestamp when the support issue was marked closed/resolved by support personnel.
- **Example**: `2025-01-10 12:45:00`
- **Unit**: YYYY-MM-DD HH:MM:SS (UTC)
- **Null Handling**: Null for open, unresolved, or pending tickets
- **Related KPI**: Mean Time to Resolution (MTTR), SLA Compliance Rate
- **Updates**: Updated when ticket status transitions to RESOLVED

### category
- **Type**: String
- **Business Meaning**: Functional classification of customer inquiry or problem.
- **Valid Values**: `Billing`, `Technical`, `Account Access`, `Cancellation`, `Feature Request`, `General`
- **Example**: `Billing`
- **Null Handling**: Defaults to `General` if unassigned
- **Related KPI**: Category Ticket Volume, Category Resolution Time
- **Updates**: Set by customer or routing AI at ticket creation

### resolution_status
- **Type**: String
- **Business Meaning**: Lifecycle status of the support ticket.
- **Valid Values**: `RESOLVED`, `UNRESOLVED`, `PENDING`
- **Example**: `RESOLVED`
- **Null Handling**: Defaults to `PENDING`
- **Related KPI**: Resolution Efficiency Rate, Backlog Count
- **Updates**: Real-time status changes in ticket agent workflow

### escalated
- **Type**: Boolean
- **Business Meaning**: Indicates whether the support ticket required manager intervention or Tier-2 support escalation.
- **Example**: `True` / `False`
- **Unit**: Boolean
- **Null Handling**: Defaults to `False`
- **Related KPI**: Support Escalation Rate, High-Risk Complaint Ratio
- **Updates**: Set to True when ticket is transferred to Tier-2 team

### satisfaction_score
- **Type**: Float
- **Business Meaning**: Post-ticket CSAT survey rating provided by customer (1.0 = Very Dissatisfied, 5.0 = Very Satisfied).
- **Example**: `4.0`
- **Unit**: Score Scale (1.0 to 5.0)
- **Null Handling**: Imputed with dataset median score (e.g. 3.0) to maintain model stability
- **Related KPI**: Customer Satisfaction Score (CSAT), Net Promoter Score Proxy
- **Updates**: Recorded upon survey completion

### monthly_spend
- **Type**: Float
- **Business Meaning**: Customer's total monthly recurring subscription spend (MRR contribution).
- **Example**: `120.50`
- **Unit**: USD ($)
- **Null Handling**: Defaults to `0.00`
- **Related KPI**: Monthly Recurring Revenue (MRR), High-Value Customer Identification
- **Updates**: Updated monthly from billing engine

### churn_risk_score
- **Type**: Float
- **Business Meaning**: Composite risk metric (0-100) quantifying predicted customer churn probability based on support interaction severity.
- **Example**: `75.0`
- **Unit**: Risk Index Points (0 to 100)
- **Null Handling**: Calculated programmatically during pipeline run
- **Related KPI**: At-Risk Customer Count, High-Risk Revenue Exposure
- **Updates**: Generated dynamically by SupportSense data pipeline

### churn_risk_category
- **Type**: String
- **Business Meaning**: Operational risk tier classification for customer success team intervention.
- **Valid Values**: `LOW`, `MEDIUM`, `HIGH`
- **Example**: `HIGH`
- **Null Handling**: Computed from `churn_risk_score`
- **Related KPI**: High-Risk Account Percentage, Intervention Success Rate
- **Updates**: Re-evaluated on every pipeline execution

### resolution_hours
- **Type**: Float
- **Business Meaning**: Total elapsed duration in hours between ticket creation and ticket resolution.
- **Example**: `4.25`
- **Unit**: Hours
- **Null Handling**: Set to `-1.0` or null for unresolved/pending tickets
- **Related KPI**: Mean Time to Resolution (MTTR), Support Bottleneck Ratio
- **Updates**: Computed upon ticket resolution

---

## Column to KPI Mapping

### 1. Monthly Revenue
- **Formula**: `SUM(trnx_amt)` or `SUM(monthly_spend)`
- **Related Columns**: `trnx_amt`, `monthly_spend`, `purchase_date`
- **Why It Matters**: Tracks core company top-line financial performance and monthly recurring revenue growth.
- **Update Frequency**: Daily batch update

### 2. Sales Velocity
- **Formula**: `COUNT(transactions) / days`
- **Related Columns**: `purchase_date`, `trnx_amt`
- **Why It Matters**: Measures sales activity rate, transaction throughput, and revenue generation momentum.
- **Update Frequency**: Weekly rollup

### 3. Segment Revenue & ARPU
- **Formula**: `SUM(trnx_amt) / COUNT(DISTINCT customer_id)` grouped by `cust_segment`
- **Related Columns**: `trnx_amt`, `cust_segment`, `customer_id`
- **Why It Matters**: Identifies most profitable market segments (B2B vs SMB vs B2C) to optimize marketing spend.
- **Update Frequency**: Monthly

### 4. Churn Rate
- **Formula**: `(SUM(flag_churn) / COUNT(DISTINCT customer_id)) * 100`
- **Related Columns**: `flag_churn`, `customer_id`, `monthly_spend`
- **Why It Matters**: Critical customer retention metric directly driving Customer Lifetime Value (CLV) and net expansion.
- **Update Frequency**: Monthly & Quarterly

### 5. Support Escalation Rate & CSAT Impact
- **Formula**: `(COUNT(tickets where escalated = True) / COUNT(total_tickets)) * 100`
- **Related Columns**: `escalated`, `ticket_id`, `satisfaction_score`, `category`
- **Why It Matters**: Highlights support operational friction; high escalation rate directly correlates with reduced CSAT and increased churn risk.
- **Update Frequency**: Daily

---

## Ambiguous Columns & Resolutions

### Column 1: `flag_churn` / `churn_flag`
- **Original Ambiguity**: Unclear temporal scope. Does it mean "currently churned today", "account canceled on ticket date", or "will churn in future"?
- **Resolved Meaning**: Binary indicator marking whether the customer churned within the 90 days following this transaction or support ticket event.
- **Business Interpretation**: Historical target label used for training predictive customer retention and churn risk models.
- **Proposed Rename**: `has_churned_90d`
- **Risk If Misunderstood**: If interpreted as immediate churn, retention teams will reach out to already churned customers or miss customers currently in the 90-day churn window.

### Column 2: `cust_segment` / `segment`
- **Original Ambiguity**: Overloaded term. Could represent customer firmographic size (B2B/SMB), product tier level (Free/Pro/Enterprise), or geographic region.
- **Resolved Meaning**: Customer market segment classification (`B2B`, `B2C`, `SMB`) that defines service levels and sales strategy.
- **Business Interpretation**: Informs account management routing, SLA priority, and pricing tier strategy.
- **Proposed Rename**: `market_segment`
- **Risk If Misunderstood**: Revenue and support bottleneck analysis grouped by the wrong dimension produces misleading segment profitability conclusions.

### Column 3: `trnx_amt` vs `monthly_spend`
- **Original Ambiguity**: Both represent dollar amounts. Is `trnx_amt` a single one-off payment or monthly recurring revenue? Is `monthly_spend` trailing 30 days total or contracted MRR?
- **Resolved Meaning**: `trnx_amt` is the discrete revenue from one specific order/transaction. `monthly_spend` is the customer's recurring monthly subscription commitment (MRR).
- **Business Interpretation**: Distinguishes transactional expansion revenue from baseline subscription account health.
- **Proposed Rename**: `transaction_revenue_usd` and `monthly_recurring_spend_usd`
- **Risk If Misunderstood**: Summing both fields leads to double-counting customer revenue and overstating financial metrics.

---

## Column Relationships

### 1. Revenue per Customer
- **Definition**: `SUM(trnx_amt)` grouped by `customer_id` combined with `monthly_spend` and `cust_segment`.
- **How It Matters**: Identifies high-value enterprise accounts (top 10% generating 50%+ revenue) for priority support routing and proactive retention management.
- **Example**: "B2B customers spend an average of $450/month compared to $29.99/month for B2C accounts."
- **Related Columns**: `customer_id`, `trnx_amt`, `monthly_spend`, `cust_segment`

### 2. Churn Rate by Customer Segment
- **Definition**: `(SUM(flag_churn) / COUNT(customer_id))` grouped by `cust_segment`.
- **How It Matters**: Pinpoints market segments experiencing retention drops, enabling targeted product or customer success interventions.
- **Example**: "SMB segment exhibits a 25% 90-day churn rate compared to 8% for B2B enterprise accounts."
- **Related Columns**: `flag_churn`, `cust_segment`, `customer_id`

### 3. Resolution Time vs Customer Satisfaction (CSAT) & Churn Risk
- **Definition**: Correlation between `resolution_hours`, `escalated`, `satisfaction_score`, and `churn_risk_score`.
- **How It Matters**: Proves how operational support delays directly lower customer satisfaction and increase predicted churn risk.
- **Example**: "Tickets requiring >48 hours to resolve with escalation result in an average CSAT of 1.2 and a 78% churn risk score."
- **Related Columns**: `resolution_hours`, `escalated`, `satisfaction_score`, `churn_risk_score`, `churn_risk_category`

---

## Governance & Maintenance Protocol

### Handling Future Dataset Updates & New Columns
To ensure the data dictionary remains the single source of truth as the dataset evolves, the following processes and governance rules must be enforced:

1. **Automated Schema Linting & Validation**:
   - Every Data Engineering PR modifying ingest scripts (`ingest_data.py`, `data_pipeline.py`) must run `scripts/validate_data_dictionary.py`.
   - CI/CD pipeline checks that any newly added column in raw data or engineered output is documented in `docs/data_dictionary.csv` and `docs/DATA_DICTIONARY.md` before merging.

2. **Standardized PR Approval Checklist**:
   - All schema changes require approval from both a Data Engineer and a Domain Business Analyst.
   - PR template must include:
     - New Column Name & Data Type
     - Business Context & Related KPIs
     - Sample Values & Null Handling Strategy
     - Proposed Rename / Resolution if name is ambiguous

3. **Version Control & Deprecation Strategy**:
   - Data dictionary updates are version-tracked alongside code releases (e.g. v1.2.0).
   - If a column is deprecated, it is marked as `[DEPRECATED]` in the dictionary with a removal grace period (e.g., 90 days) rather than immediately deleted, preventing silent pipeline failures downstream.
