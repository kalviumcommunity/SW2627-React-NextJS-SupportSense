import React, { useEffect, useState } from 'react';
import { Search, Filter, Sparkles, Building2, ShieldAlert, CheckCircle2, ChevronLeft, ChevronRight, Activity } from 'lucide-react';
import { fetchCustomers, runAIPrediction } from '../api';

export const CustomersView: React.FC = () => {
  const [customers, setCustomers] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [riskLevel, setRiskLevel] = useState('');
  const [plan, setPlan] = useState('');
  const [loading, setLoading] = useState(true);
  const [predictingId, setPredictingId] = useState<string | null>(null);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const res = await fetchCustomers({
        search,
        risk_level: riskLevel,
        plan,
        page,
        limit: 15
      });
      setCustomers(res.customers || []);
      setTotal(res.total || 0);
    } catch (err) {
      console.error('Failed to load customers:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCustomers();
  }, [page, search, riskLevel, plan]);

  const handlePredict = async (customerId: string) => {
    try {
      setPredictingId(customerId);
      await runAIPrediction(customerId);
      await loadCustomers();
    } catch (err) {
      console.error('Prediction failed:', err);
    } finally {
      setPredictingId(null);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>Customer Management</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
            Real-Time Customer Health Telemetry & Subscription Churn Modeling ({total} Total Accounts)
          </p>
        </div>
      </div>

      {/* Filter Controls */}
      <div className="card-surface" style={{ marginBottom: '20px', padding: '16px' }}>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center' }}>
          {/* Search */}
          <div style={{ flex: 1, minWidth: '240px', position: 'relative' }}>
            <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--on-surface-variant)' }} />
            <input 
              type="text" 
              placeholder="Search by name, company, email, or ID..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              style={{
                width: '100%',
                padding: '8px 12px 8px 36px',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                color: 'var(--on-surface)'
              }}
            />
          </div>

          {/* Risk Level Filter */}
          <select 
            value={riskLevel}
            onChange={(e) => { setRiskLevel(e.target.value); setPage(1); }}
            style={{
              padding: '8px 12px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
          >
            <option value="">All Risk Levels</option>
            <option value="High">High Risk</option>
            <option value="Medium">Medium Risk</option>
            <option value="Low">Low Risk</option>
          </select>

          {/* Plan Filter */}
          <select 
            value={plan}
            onChange={(e) => { setPlan(e.target.value); setPage(1); }}
            style={{
              padding: '8px 12px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
          >
            <option value="">All Plans</option>
            <option value="Enterprise">Enterprise ($799/mo)</option>
            <option value="Pro">Pro ($199/mo)</option>
            <option value="Starter">Starter ($49/mo)</option>
          </select>
        </div>
      </div>

      {/* Customer Data Table */}
      <div className="card-surface">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
            <Activity size={24} className="spin" style={{ marginBottom: '8px', color: 'var(--primary)' }} />
            <p>Loading Customer Portfolio...</p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Customer ID</th>
                  <th>Customer & Company</th>
                  <th>Plan & MRR</th>
                  <th>Health Score</th>
                  <th>Churn Probability</th>
                  <th>Tickets (Open/Total)</th>
                  <th>Escalations</th>
                  <th>AI Action</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((c) => (
                  <tr key={c.customer_id}>
                    <td>
                      <code style={{ fontSize: '0.8rem', color: 'var(--primary)' }}>{c.customer_id}</code>
                    </td>
                    <td>
                      <div>
                        <strong style={{ color: 'var(--on-surface)' }}>{c.name}</strong>
                        <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)' }}>{c.company} • {c.email}</div>
                      </div>
                    </td>
                    <td>
                      <span className="badge badge-secondary">{c.subscription_plan}</span>
                      <div style={{ fontSize: '0.8rem', fontWeight: 600, marginTop: '2px' }}>${c.mrr}/mo</div>
                    </td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ 
                          fontWeight: 700, 
                          color: c.health_score > 70 ? '#4caf50' : (c.health_score > 40 ? 'orange' : 'var(--error)') 
                        }}>
                          {c.health_score}/100
                        </span>
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${c.risk_level === 'High' ? 'badge-error' : (c.risk_level === 'Medium' ? 'badge-warning' : 'badge-success')}`}>
                        {c.risk_level} ({c.churn_risk_score}%)
                      </span>
                    </td>
                    <td>
                      {c.unresolved_tickets} open / {c.total_tickets} total
                    </td>
                    <td style={{ color: c.escalated_tickets > 0 ? 'var(--error)' : 'inherit', fontWeight: c.escalated_tickets > 0 ? 600 : 400 }}>
                      {c.escalated_tickets} escalated
                    </td>
                    <td>
                      <button 
                        className="btn btn-primary" 
                        style={{ padding: '4px 8px', fontSize: '0.75rem' }}
                        disabled={predictingId === c.customer_id}
                        onClick={() => handlePredict(c.customer_id)}
                      >
                        <Sparkles size={12} /> {predictingId === c.customer_id ? 'Scoring...' : 'Run AI'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Controls */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', paddingTop: '16px', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
            Showing {customers.length} of {total} accounts
          </span>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <button 
              className="btn btn-secondary" 
              disabled={page <= 1}
              onClick={() => setPage(p => p - 1)}
              style={{ padding: '4px 8px' }}
            >
              <ChevronLeft size={16} /> Prev
            </button>
            <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>Page {page}</span>
            <button 
              className="btn btn-secondary" 
              disabled={page * 15 >= total}
              onClick={() => setPage(p => p + 1)}
              style={{ padding: '4px 8px' }}
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
