import React, { useEffect, useState } from 'react';
import { HeartPulse, Check, AlertOctagon, Activity, Search, ShieldAlert } from 'lucide-react';
import { fetchCustomerDetails } from '../api';

export const CustomerHealthView: React.FC = () => {
  const [customerId, setCustomerId] = useState('CUST-0042');
  const [details, setDetails] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadDetails = async (id: string) => {
    try {
      setLoading(true);
      const res = await fetchCustomerDetails(id);
      if (res.success) {
        setDetails(res);
      }
    } catch (err) {
      console.error('Failed to load customer details:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDetails(customerId);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (customerId) loadDetails(customerId);
  };

  const customer = details?.customer;
  const prediction = details?.prediction;
  const tickets = details?.tickets || [];

  return (
    <div>
      <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>Customer Health Telemetry & Deep Audit</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
            Module 7 — Unified Customer Health Score (0-100) & Proactive Recovery Plan
          </p>
        </div>

        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '8px' }}>
          <input 
            type="text" 
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
            placeholder="Customer ID (e.g. CUST-0042)..."
            style={{
              padding: '8px 12px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
          />
          <button className="btn btn-primary" type="submit">
            <Search size={14} /> Audit Account
          </button>
        </form>
      </div>

      {loading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
          <Activity size={24} className="spin" style={{ marginBottom: '8px', color: 'var(--primary)' }} />
          <p>Analyzing Customer Telemetry Signals...</p>
        </div>
      ) : customer ? (
        <div>
          <div className="card-surface" style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ fontSize: '1.4rem', fontWeight: 600, color: 'var(--on-surface)' }}>
                  {customer.name} ({customer.company})
                </h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
                  {customer.email} • {customer.subscription_plan} Plan (${customer.mrr}/mo MRR) • Account Age: {customer.subscription_age_months} Months
                </p>
              </div>
              <div style={{ textAlign: 'right' }}>
                <span className={`badge ${customer.risk_level === 'High' ? 'badge-error' : (customer.risk_level === 'Medium' ? 'badge-warning' : 'badge-success')}`} style={{ fontSize: '0.9rem', padding: '6px 12px' }}>
                  {customer.risk_level} Risk Level ({customer.churn_risk_score}%)
                </span>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, marginTop: '6px', color: 'var(--primary)' }}>
                  Health Score: {customer.health_score}/100
                </div>
              </div>
            </div>
          </div>

          <div className="grid-4" style={{ marginBottom: '20px' }}>
            <div className="card-surface">
              <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)' }}>Product Usage Activity</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: customer.product_usage_score < 40 ? 'var(--error)' : 'var(--on-surface)' }}>
                {customer.product_usage_score} / 100
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
                Product Adoption Index
              </div>
            </div>

            <div className="card-surface">
              <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)' }}>Average CSAT Score</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: customer.avg_csat < 3.0 ? 'var(--error)' : '#4caf50' }}>
                ★ {customer.avg_csat} / 5.0
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
                Support Sentiment Score
              </div>
            </div>

            <div className="card-surface">
              <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)' }}>Unresolved Complaints</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: customer.unresolved_tickets > 1 ? 'var(--error)' : 'var(--on-surface)' }}>
                {customer.unresolved_tickets} Open
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
                {customer.escalated_tickets} Ticket Escalation(s)
              </div>
            </div>

            <div className="card-surface">
              <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)' }}>Billing & Payment Status</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: customer.payment_delay_days > 7 ? 'var(--error)' : '#4caf50' }}>
                {customer.payment_delay_days > 0 ? `${customer.payment_delay_days} Days Late` : 'On Time'}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
                Payment Schedule Status
              </div>
            </div>
          </div>

          {/* Action Plan */}
          <div className="card-surface">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <AlertOctagon size={18} color="var(--primary)" />
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
                AI Recommended Action & Recovery Plan
              </h3>
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', padding: 0, margin: 0 }}>
              {prediction?.recommendations?.map((rec: string, idx: number) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.875rem', color: 'var(--on-surface)' }}>
                  <Check size={16} color="#4caf50" />
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
          Customer account not found. Try searching for IDs like CUST-0001, CUST-0042, etc.
        </div>
      )}
    </div>
  );
};
