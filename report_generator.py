def generate_report(df, report_date):
    """Generate structured text report from analysis output."""
    revenue = df["revenue"].sum()
    # If customer_id exists use it, else use index length
    customers = df["customer_id"].nunique() if "customer_id" in df.columns else len(df)
    avg_order = df["revenue"].mean() if len(df) > 0 else 0
    
    lines = []
    lines.append("WEEKLY ANALYTICS REPORT")
    lines.append("Date: " + str(report_date))
    lines.append("")
    
    # Section 1: KPI Summary
    lines.append("== KPI SUMMARY ==")
    lines.append("Total Revenue: $" + f"{revenue:,.0f}")
    lines.append("Active Customers: " + f"{customers:,}")
    lines.append("Average Order: $" + f"{avg_order:,.0f}")
    lines.append("")
    
    # Section 2: Key Finding
    lines.append("== KEY FINDING ==")
    if not df.empty and "segment" in df.columns:
        top_seg = df.groupby("segment")["revenue"].sum().idxmax()
        lines.append("Top segment: " + top_seg)
    else:
        lines.append("Top segment: N/A")
    lines.append("")
    
    # Section 3: Recommended Action
    lines.append("== RECOMMENDED ACTION ==")
    lines.append("Allocate resources to high-growth segments.")
    
    return "\n".join(lines)
