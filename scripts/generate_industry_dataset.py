"""
ChurnShield Industry-Grade Dataset Generator
============================================
Generates realistic multi-entity relational datasets matching ChurnShield PRD:
- Customers (1,000 records)
- Subscriptions (MRR, Tiers, Billing history)
- Support Tickets (5,000 records with response times, escalations, CSAT)
- Ground Truth Churn & Health Scores with realistic correlations.
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Configurations
NUM_CUSTOMERS = 1000
TICKETS_PER_CUSTOMER_RANGE = (2, 10)
CATEGORIES = ["Billing", "Technical Bug", "Account Access", "Feature Request", "Performance Issue"]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]
STATUSES = ["Resolved", "Closed", "In Progress", "Escalation Pending"]
PLANS = ["Starter", "Pro", "Enterprise"]
PLAN_MRR = {"Starter": 49.0, "Pro": 199.0, "Enterprise": 799.0}

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Casey", "Dakota",
               "Aarav", "Priya", "Ananya", "Rohan", "Siddharth", "Emily", "Liam", "Sophia", "Noah", "Olivia"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
              "Mahato", "Sharma", "Patel", "Verma", "Chen", "Kim", "Taylor", "Anderson", "Thomas", "Jackson"]
COMPANIES = ["Acme Corp", "Apex Global", "TechPulse", "CloudScale", "DataFlow", "InnoWave", "ByteWorks",
             "Nexus Solutions", "Synergy Tech", "Vanguard AI", "QuantumSoft", "Horizon Labs", "Starlight Systems"]

def generate_dataset():
    print("🚀 Generating ChurnShield Industry Dataset...")
    
    customers = []
    tickets = []
    subscriptions = []
    
    base_date = datetime(2025, 1, 1)

    for i in range(1, NUM_CUSTOMERS + 1):
        cust_id = f"CUST-{i:04d}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        company = random.choice(COMPANIES)
        email = f"{name.lower().replace(' ', '.')}@{company.lower().replace(' ', '')}.com"
        plan = random.choice(PLANS)
        mrr = PLAN_MRR[plan]
        signup_date = base_date + timedelta(days=random.randint(0, 300))
        subscription_age_months = max(1, int((datetime(2026, 7, 1) - signup_date).days / 30))
        
        num_tickets = random.randint(*TICKETS_PER_CUSTOMER_RANGE)
        
        # Calculate latent risk drivers for correlation
        unresolved_count = 0
        escalation_count = 0
        csat_scores = []
        resolution_times = []
        
        cust_tickets = []
        for t in range(1, num_tickets + 1):
            ticket_id = f"TCK-{i:04d}-{t:02d}"
            category = random.choice(CATEGORIES)
            priority = random.choice(PRIORITIES)
            
            # Correlate urgent/billing complaints with higher escalation probability
            is_escalated = random.random() < (0.35 if priority in ["High", "Urgent"] or category == "Billing" else 0.10)
            if is_escalated:
                escalation_count += 1
                
            status = random.choice(STATUSES)
            if status != "Resolved" and status != "Closed":
                unresolved_count += 1
                resolution_hours = -1.0
            else:
                resolution_hours = round(random.uniform(2.0, 72.0 if priority in ["High", "Urgent"] else 24.0), 1)
                resolution_times.append(resolution_hours)
                
            # CSAT score (1 to 5) - lower if escalated or unresolved
            if is_escalated or status not in ["Resolved", "Closed"]:
                csat = random.choice([1.0, 2.0, 3.0])
            else:
                csat = random.choice([3.0, 4.0, 5.0, 5.0])
            csat_scores.append(csat)
            
            created_at = signup_date + timedelta(days=random.randint(1, max(2, (datetime(2026, 7, 1) - signup_date).days)))
            
            cust_tickets.append({
                "ticket_id": ticket_id,
                "customer_id": cust_id,
                "category": category,
                "priority": priority,
                "status": status,
                "escalated": is_escalated,
                "resolution_hours": resolution_hours,
                "csat_score": csat,
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        tickets.extend(cust_tickets)
        
        avg_csat = float(np.mean(csat_scores)) if csat_scores else 4.0
        avg_res_time = float(np.mean(resolution_times)) if resolution_times else 24.0
        payment_delay_days = random.choice([0, 0, 0, 0, 3, 7, 14, 25]) if escalation_count > 0 else 0
        product_usage_score = round(random.uniform(15.0, 95.0), 1)
        
        # Calculate realistic Churn Flag ground truth based on features
        churn_risk_score = 0.0
        churn_risk_score += escalation_count * 10.0
        churn_risk_score += unresolved_count * 8.0
        churn_risk_score += (5.0 - avg_csat) * 8.0
        churn_risk_score += (payment_delay_days / 5.0) * 3.0
        churn_risk_score += (100.0 - product_usage_score) * 0.1
        if avg_res_time > 48.0:
            churn_risk_score += 8.0
            
        churn_risk_score = float(np.clip(churn_risk_score, 0.0, 100.0))
        
        # Churn Probability & Flag (~22.5% industry benchmark churn rate)
        churn_flag = 1 if churn_risk_score >= 82.0 else 0
        health_score = int(100.0 - churn_risk_score)
        
        customers.append({
            "customer_id": cust_id,
            "name": name,
            "company": company,
            "email": email,
            "subscription_plan": plan,
            "mrr": mrr,
            "signup_date": signup_date.strftime("%Y-%m-%d"),
            "subscription_age_months": subscription_age_months,
            "total_tickets": num_tickets,
            "unresolved_tickets": unresolved_count,
            "escalated_tickets": escalation_count,
            "avg_csat": round(avg_csat, 2),
            "avg_resolution_hours": round(avg_res_time, 2),
            "payment_delay_days": payment_delay_days,
            "product_usage_score": product_usage_score,
            "health_score": health_score,
            "churn_risk_score": round(churn_risk_score, 2),
            "churn_flag": churn_flag
        })
        
        subscriptions.append({
            "subscription_id": f"SUB-{i:04d}",
            "customer_id": cust_id,
            "plan": plan,
            "mrr": mrr,
            "status": "Canceled" if churn_flag == 1 and random.random() < 0.5 else "Active",
            "auto_renew": True if churn_flag == 0 else False,
            "start_date": signup_date.strftime("%Y-%m-%d")
        })

    # Save to CSV
    df_cust = pd.DataFrame(customers)
    df_tickets = pd.DataFrame(tickets)
    df_subs = pd.DataFrame(subscriptions)
    
    df_cust.to_csv(os.path.join(RAW_DATA_DIR, "customers.csv"), index=False)
    df_tickets.to_csv(os.path.join(RAW_DATA_DIR, "customer_support_tickets.csv"), index=False)
    df_subs.to_csv(os.path.join(RAW_DATA_DIR, "subscriptions.csv"), index=False)
    
    print(f"✅ Generated {len(df_cust)} customers in customers.csv")
    print(f"✅ Generated {len(df_tickets)} support tickets in customer_support_tickets.csv")
    print(f"✅ Generated {len(df_subs)} subscription records in subscriptions.csv")
    print(f"📊 Dataset Churn Rate: {df_cust['churn_flag'].mean() * 100:.1f}%")

if __name__ == "__main__":
    generate_dataset()
