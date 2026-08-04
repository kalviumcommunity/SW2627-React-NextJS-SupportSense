import React, { useEffect, useState } from 'react';
import { Building2, AlertTriangle, DollarSign, Headset, TrendingUp, TrendingDown, Calendar, Sparkles, Eye, ShieldAlert, CheckCircle2, Activity } from 'lucide-react';
import { fetchDashboardKPIs, fetchAnalyticsCharts, runAIPrediction } from '../api';

export const DashboardView: React.FC = () => {
  const [kpis, setKpis] = useState<any>(null);
  const [charts, setCharts] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [predictingId, setPredictingId] = useState<string | null>(null);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const kpiData = await fetchDashboardKPIs();
      const chartData = await fetchAnalyticsCharts();
      setKpis(kpiData);
      setCharts(chartData);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const handlePredict = async (customerId: string) => {
    try {
      setPredictingId(customerId);
      await runAIPrediction(customerId);
      await loadDashboard();
    } catch (err) {
      console.error('Prediction failed:', err);
    } finally {
      setPredictingId(null);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
        <Activity size={32} className="spin" style={{ marginBottom: '12px', color: 'var(--primary)' }} />
        <p>Connecting to ChurnShield AI Engine & Fetching Telemetry Data...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Title Header Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--on-surface)', letterSpacing: '-0.01em' }}>
            Dashboard Overview
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
            AI-Powered Customer Retention & Risk Telemetry • Real-Time Predictions Active
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-secondary" onClick={loadDashboard}>
            <Calendar size={14} /> Refresh Data
          </button>
          <button className="btn btn-primary">
            Export Executive Summary
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid-4">
        {/* KPI 1 */}
        <div className="card-surface">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(197, 163, 88, 0.2)', color: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Building2 size={16} />
              </div>
              <span style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)', fontWeight: 500 }}>Active Accounts</span>
            </div>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--on-surface)' }}>
              {kpis?.totalCustomers?.toLocaleString() || '1,000'}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: 500, marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <TrendingUp size={14} /> Portfolio Monitored
            </div>
          </div>
        </div>

        {/* KPI 2 */}
        <div className="card-surface">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(207, 156, 132, 0.2)', color: 'var(--error)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <AlertTriangle size={16} />
              </div>
              <span style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)', fontWeight: 500 }}>High Risk Accounts</span>
            </div>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--error)' }}>
              {kpis?.highRiskCustomers || 0}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--error)', fontWeight: 500, marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <TrendingUp size={14} /> Critical Action Required
            </div>
          </div>
        </div>

        {/* KPI 3 */}
        <div className="card-surface">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(76, 175, 80, 0.2)', color: '#4caf50', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <DollarSign size={16} />
              </div>
              <span style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)', fontWeight: 500 }}>Revenue at Risk (MRR)</span>
            </div>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--on-surface)' }}>
              ${kpis?.revenueAtRisk?.toLocaleString() || '0'}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--error)', fontWeight: 500, marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <TrendingDown size={14} /> High-Risk Accounts Total MRR
            </div>
          </div>
        </div>

        {/* KPI 4 */}
        <div className="card-surface">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(197, 163, 88, 0.2)', color: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Headset size={16} />
              </div>
              <span style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)', fontWeight: 500 }}>Model Accuracy</span>
            </div>
          </div>
          <div>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--primary)' }}>
              {kpis?.predictionAccuracy || 93.5}%
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: 500, marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <CheckCircle2 size={14} /> Balanced Random Forest ML
            </div>
          </div>
        </div>
      </div>

      {/* Top High-Risk Customer Accounts Table */}
      <div className="card-surface" style={{ marginTop: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Critical Risk Accounts Requiring Intervention
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
              Sorted by Monthly Recurring Revenue & AI Churn Probability
            </p>
          </div>
          <span className="badge badge-error">
            <ShieldAlert size={12} /> {charts?.topRiskyCustomers?.length || 0} Accounts Monitored
          </span>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Customer / Company</th>
                <th>Plan</th>
                <th>MRR</th>
                <th>Health Score</th>
                <th>Risk Score</th>
                <th>Unresolved Tickets</th>
                <th>Escalations</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {charts?.topRiskyCustomers?.map((cust: any) => (
                <tr key={cust.customer_id}>
                  <td>
                    <div>
                      <strong style={{ color: 'var(--on-surface)' }}>{cust.name}</strong>
                      <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)' }}>{cust.company} • {cust.customer_id}</div>
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-secondary">{cust.subscription_plan}</span>
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--on-surface)' }}>${cust.mrr}/mo</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ flex: 1, height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', width: '60px', overflow: 'hidden' }}>
                        <div style={{ height: '100%', width: `${cust.health_score}%`, background: cust.health_score < 40 ? 'var(--error)' : 'var(--warning)' }}></div>
                      </div>
                      <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{cust.health_score}/100</span>
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-error" style={{ fontWeight: 700 }}>
                      {cust.churn_risk_score}%
                    </span>
                  </td>
                  <td>{cust.unresolved_tickets} open</td>
                  <td style={{ color: cust.escalated_tickets > 0 ? 'var(--error)' : 'inherit', fontWeight: cust.escalated_tickets > 0 ? 600 : 400 }}>
                    {cust.escalated_tickets} escalated
                  </td>
                  <td>
                    <button 
                      className="btn btn-primary" 
                      style={{ padding: '4px 10px', fontSize: '0.75rem' }}
                      disabled={predictingId === cust.customer_id}
                      onClick={() => handlePredict(cust.customer_id)}
                    >
                      <Sparkles size={12} /> {predictingId === cust.customer_id ? 'Analyzing...' : 'Recalculate AI'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
