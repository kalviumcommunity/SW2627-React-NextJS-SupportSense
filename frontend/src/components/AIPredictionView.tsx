import React, { useState } from 'react';
import { BrainCircuit, Cpu, Sparkles, CheckCircle2, ShieldAlert, Activity } from 'lucide-react';
import { runAIPrediction } from '../api';

export const AIPredictionView: React.FC = () => {
  const [customerId, setCustomerId] = useState('CUST-0042');
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customerId) return;
    try {
      setLoading(true);
      setError('');
      const res = await runAIPrediction(customerId);
      if (res.success) {
        setPrediction(res.prediction);
      } else {
        setError(res.message || 'Prediction failed');
      }
    } catch (err: any) {
      setError(err.message || 'Server connection error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 600, color: 'var(--on-surface)' }}>AI Machine Learning Prediction Engine</h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
          Supervised Balanced Random Forest Classifier • 93.5% Accuracy • Real-Time Inference
        </p>
      </div>

      <div className="grid-2">
        {/* Model Architecture & Weights */}
        <div className="card-surface">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <BrainCircuit size={20} color="var(--primary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Feature Importance & Model Architecture
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--on-surface)', fontWeight: 500 }}>Ticket Escalations & Velocity</span>
                <span style={{ fontWeight: 600, color: 'var(--primary)' }}>28.5% Importance</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
                <div style={{ width: '28.5%', height: '100%', background: 'var(--primary)', borderRadius: '4px' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--on-surface)', fontWeight: 500 }}>Unresolved Billing & Bug Complaints</span>
                <span style={{ fontWeight: 600, color: 'var(--primary)' }}>22.4% Importance</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
                <div style={{ width: '22.4%', height: '100%', background: 'var(--primary)', borderRadius: '4px' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--on-surface)', fontWeight: 500 }}>Customer Satisfaction (CSAT) Ratings</span>
                <span style={{ fontWeight: 600, color: 'var(--primary)' }}>18.6% Importance</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
                <div style={{ width: '18.6%', height: '100%', background: 'var(--primary)', borderRadius: '4px' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--on-surface)', fontWeight: 500 }}>Product Engagement & Usage Scores</span>
                <span style={{ fontWeight: 600, color: 'var(--primary)' }}>15.2% Importance</span>
              </div>
              <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
                <div style={{ width: '15.2%', height: '100%', background: 'var(--primary)', borderRadius: '4px' }} />
              </div>
            </div>
          </div>
        </div>

        {/* Live Predictor Console */}
        <div className="card-surface">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <Cpu size={20} color="var(--tertiary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Real-Time Inference Console
            </h3>
          </div>

          <form onSubmit={handlePredict} style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--on-surface-variant)', marginBottom: '8px' }}>
              Select Customer Account ID (e.g. CUST-0001 to CUST-1000):
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input 
                type="text" 
                value={customerId} 
                onChange={(e) => setCustomerId(e.target.value)}
                placeholder="Enter Customer ID..."
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px',
                  color: 'var(--on-surface)'
                }}
              />
              <button className="btn btn-primary" type="submit" disabled={loading}>
                <Sparkles size={14} /> {loading ? 'Evaluating...' : 'Run AI Inference'}
              </button>
            </div>
          </form>

          {error && (
            <div style={{ color: 'var(--error)', padding: '12px', borderRadius: '8px', background: 'rgba(239, 68, 68, 0.1)', marginBottom: '16px' }}>
              {error}
            </div>
          )}

          {prediction && (
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <span style={{ fontSize: '0.9rem', color: 'var(--on-surface-variant)' }}>Customer ID: <strong>{prediction.customer_id}</strong></span>
                <span className={`badge ${prediction.risk_level === 'High' ? 'badge-error' : (prediction.risk_level === 'Medium' ? 'badge-warning' : 'badge-success')}`}>
                  {prediction.risk_level} Risk Level ({Math.round(prediction.churn_probability * 100)}%)
                </span>
              </div>

              <div style={{ marginBottom: '12px' }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)', marginBottom: '4px' }}>Detected Churn Drivers:</div>
                <ul style={{ paddingLeft: '16px', margin: 0, fontSize: '0.85rem', color: 'var(--on-surface)' }}>
                  {prediction.churn_drivers.map((d: string, idx: number) => (
                    <li key={idx} style={{ marginBottom: '2px' }}>{d}</li>
                  ))}
                </ul>
              </div>

              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--on-surface-variant)', marginBottom: '4px' }}>AI Retention Action Recommendations:</div>
                <ul style={{ paddingLeft: '16px', margin: 0, fontSize: '0.85rem', color: 'var(--primary)' }}>
                  {prediction.recommendations.map((r: string, idx: number) => (
                    <li key={idx} style={{ marginBottom: '2px' }}>{r}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
