import React, { useEffect, useState } from 'react';
import { Bell, Download, FileText, MessageSquare, AlertTriangle, ShieldAlert, Activity } from 'lucide-react';
import { fetchCustomers } from '../api';

export const NotificationsView: React.FC = () => {
  const [highRisk, setHighRisk] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCustomers({ risk_level: 'High', limit: 8 })
      .then(res => setHighRisk(res.customers || []))
      .catch(err => console.error('Alerts load error:', err))
      .finally(() => setLoading(false));
  }, []);

  const handleExportCSV = () => {
    if (!highRisk.length) return;
    const headers = 'Customer ID,Name,Company,Email,Plan,MRR,Health Score,Risk Score\n';
    const rows = highRisk.map(c => `"${c.customer_id}","${c.name}","${c.company}","${c.email}","${c.subscription_plan}",${c.mrr},${c.health_score},${c.churn_risk_score}`).join('\n');
    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ChurnShield_Executive_Risk_Report_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
  };

  return (
    <div>
      <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>Real-Time Alert Feed & Executive Reports</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
            Module 11 — High-Risk Alerts, Slack Integrations & Executive Summary Export
          </p>
        </div>

        <button className="btn btn-primary" onClick={handleExportCSV}>
          <Download size={15} /> Export Risk CSV Report
        </button>
      </div>

      <div className="grid-2">
        {/* Live Alerts Feed */}
        <div className="card-surface">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <MessageSquare size={18} color="var(--primary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Real-Time High Risk Alerts
            </h3>
          </div>

          {loading ? (
            <div style={{ padding: '20px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
              <Activity size={20} className="spin" style={{ marginBottom: '4px', color: 'var(--primary)' }} />
              <p>Fetching alerts...</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {highRisk.map((cust) => (
                <div key={cust.customer_id} style={{ padding: '12px', background: 'rgba(239, 68, 68, 0.08)', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--error)' }}>
                    [CRITICAL ALERT] {cust.name} ({cust.company}) Churn Risk Hit {cust.churn_risk_score}%
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)', marginTop: '4px' }}>
                    {cust.unresolved_tickets} open complaints • {cust.escalated_tickets} escalated • MRR at risk: ${cust.mrr}/mo
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Executive PDF / CSV Downloads */}
        <div className="card-surface">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <FileText size={18} color="var(--tertiary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Automated Executive Reports
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong style={{ color: 'var(--on-surface)', display: 'block' }}>Monthly Portfolio Risk Audit</strong>
                <span style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)' }}>Full breakdown of 1,000 enterprise accounts & model accuracy</span>
              </div>
              <button className="btn btn-secondary" onClick={handleExportCSV}>
                <Download size={14} /> Download
              </button>
            </div>

            <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong style={{ color: 'var(--on-surface)', display: 'block' }}>Support Escalation & SLA Performance</strong>
                <span style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)' }}>Resolution velocity, CSAT scores & department performance</span>
              </div>
              <button className="btn btn-secondary" onClick={handleExportCSV}>
                <Download size={14} /> Download
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
