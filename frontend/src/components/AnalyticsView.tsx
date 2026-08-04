import React, { useEffect, useState } from 'react';
import { TrendingUp, PieChart, AlertCircle, BarChart3, Activity } from 'lucide-react';
import { fetchAnalyticsCharts } from '../api';

export const AnalyticsView: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyticsCharts()
      .then(res => setData(res))
      .catch(err => console.error('Analytics load error:', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
        <Activity size={24} className="spin" style={{ marginBottom: '8px', color: 'var(--primary)' }} />
        <p>Loading Churn & Ticket Analytics Breakdown...</p>
      </div>
    );
  }

  const categoryBreakdown = data?.categoryBreakdown || [];
  const riskBreakdown = data?.riskBreakdown || [];
  const totalTicketsCount = categoryBreakdown.reduce((sum: number, c: any) => sum + c.count, 0) || 1;
  const totalRiskCount = riskBreakdown.reduce((sum: number, r: any) => sum + r.count, 0) || 1;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>Analytics & Root Cause Telemetry</h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
          Root Cause Driver Breakdown, Category Volume Distribution & High-Risk Portfolio Breakdown
        </p>
      </div>

      <div className="grid-2">
        {/* Support Ticket Category Volume */}
        <div className="card-surface">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <BarChart3 size={18} color="var(--primary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Support Issue Category Breakdown
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {categoryBreakdown.map((cat: any) => {
              const pct = Math.round((cat.count / totalTicketsCount) * 100);
              return (
                <div key={cat._id}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--on-surface)', fontWeight: 500 }}>{cat._id}</span>
                    <span style={{ color: 'var(--primary)', fontWeight: 600 }}>{cat.count} tickets ({pct}%)</span>
                  </div>
                  <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ width: `${pct}%`, height: '100%', background: 'var(--primary)' }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Portfolio Risk Distribution */}
        <div className="card-surface">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <PieChart size={18} color="var(--tertiary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Customer Portfolio Risk Level Segmentation
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {riskBreakdown.map((r: any) => {
              const pct = Math.round((r.count / totalRiskCount) * 100);
              const color = r._id === 'High' ? 'var(--error)' : (r._id === 'Medium' ? 'orange' : '#4caf50');
              return (
                <div key={r._id}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                    <span style={{ color: 'var(--on-surface)', fontWeight: 500 }}>{r._id} Risk Segment</span>
                    <span style={{ color, fontWeight: 600 }}>{r.count} Accounts ({pct}%)</span>
                  </div>
                  <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ width: `${pct}%`, height: '100%', background: color }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
