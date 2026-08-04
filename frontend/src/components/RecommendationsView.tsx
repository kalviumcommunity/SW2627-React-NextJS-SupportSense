import React, { useEffect, useState } from 'react';
import { Sparkles, Play, ShieldAlert, Activity, CheckCircle2 } from 'lucide-react';
import { fetchCustomers, runAIPrediction } from '../api';

export const RecommendationsView: React.FC = () => {
  const [highRiskAccounts, setHighRiskAccounts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [executingId, setExecutingId] = useState<string | null>(null);

  const loadHighRiskAccounts = async () => {
    try {
      setLoading(true);
      const res = await fetchCustomers({ risk_level: 'High', limit: 10 });
      setHighRiskAccounts(res.customers || []);
    } catch (err) {
      console.error('Failed to fetch recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHighRiskAccounts();
  }, []);

  const handleExecutePlaybook = async (customerId: string) => {
    try {
      setExecutingId(customerId);
      await runAIPrediction(customerId);
      await loadHighRiskAccounts();
    } catch (err) {
      console.error('Playbook execution failed:', err);
    } finally {
      setExecutingId(null);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>AI Retention Recommendation Engine & Playbooks</h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
          Module 8 — Real-Time AI Recommendations & Prescriptive Action Engine for High-Risk Accounts
        </p>
      </div>

      {loading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
          <Activity size={24} className="spin" style={{ marginBottom: '8px', color: 'var(--primary)' }} />
          <p>Generating Actionable Retention Playbooks...</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {highRiskAccounts.map((cust) => (
            <div key={cust.customer_id} className="card-surface">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
                      {cust.name} ({cust.company})
                    </h3>
                    <span className="badge badge-error">High Churn Risk ({cust.churn_risk_score}%)</span>
                    <span className="badge badge-secondary">{cust.subscription_plan} Plan</span>
                  </div>

                  <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)', marginBottom: '12px' }}>
                    MRR: <strong>${cust.mrr}/mo</strong> • Unresolved Tickets: <strong>{cust.unresolved_tickets} open</strong> • Escalations: <strong>{cust.escalated_tickets} escalated</strong> • Avg CSAT: <strong>★ {cust.avg_csat}</strong>
                  </div>

                  <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--primary)', marginBottom: '4px' }}>
                      <Sparkles size={12} style={{ display: 'inline', marginRight: '4px' }} />
                      Prescriptive AI Retention Playbook:
                    </div>
                    <ul style={{ margin: 0, paddingLeft: '16px', fontSize: '0.85rem', color: 'var(--on-surface)' }}>
                      <li>Assign Senior CSM for urgent check-in call within 24 hours</li>
                      {cust.mrr >= 199 && <li>Offer 15% retention billing discount on current ${cust.mrr}/mo subscription</li>}
                      {cust.escalated_tickets > 0 && <li>Escalate open tickets to Tier-3 Lead Architect for immediate resolution</li>}
                    </ul>
                  </div>
                </div>

                <button 
                  className="btn btn-primary"
                  disabled={executingId === cust.customer_id}
                  onClick={() => handleExecutePlaybook(cust.customer_id)}
                >
                  <Play size={14} /> {executingId === cust.customer_id ? 'Executing...' : 'Execute Playbook'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
