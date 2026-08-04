import React, { useEffect, useState } from 'react';
import { MessageSquare, AlertTriangle, Search, Filter, ChevronLeft, ChevronRight, Activity, ShieldAlert, ArrowUpRight } from 'lucide-react';
import { fetchTickets, escalateTicket } from '../api';

export const TicketsView: React.FC = () => {
  const [tickets, setTickets] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [priority, setPriority] = useState('');
  const [loading, setLoading] = useState(true);
  const [escalatingId, setEscalatingId] = useState<string | null>(null);

  const loadTickets = async () => {
    try {
      setLoading(true);
      const res = await fetchTickets({
        search,
        category,
        priority,
        page,
        limit: 15
      });
      setTickets(res.tickets || []);
      setTotal(res.total || 0);
    } catch (err) {
      console.error('Failed to fetch tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTickets();
  }, [page, search, category, priority]);

  const handleEscalate = async (ticketId: string) => {
    try {
      setEscalatingId(ticketId);
      await escalateTicket(ticketId);
      await loadTickets();
    } catch (err) {
      console.error('Escalation failed:', err);
    } finally {
      setEscalatingId(null);
    }
  };

  const openTicketsCount = tickets.filter(t => t.status !== 'Resolved' && t.status !== 'Closed').length;
  const escalatedCount = tickets.filter(t => t.escalated).length;

  return (
    <div>
      {/* Overview Stats */}
      <div className="grid-4">
        <div className="card-surface">
          <div style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>Total Support Tickets</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--on-surface)', marginTop: '0.25rem' }}>
            {total.toLocaleString()}
          </div>
        </div>

        <div className="card-surface">
          <div style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>Active Open Tickets</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--primary)', marginTop: '0.25rem' }}>
            {openTicketsCount}
          </div>
        </div>

        <div className="card-surface">
          <div style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>Escalated Critical Tickets</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--error)', marginTop: '0.25rem' }}>
            {escalatedCount}
          </div>
        </div>

        <div className="card-surface">
          <div style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>Target SLA Compliance</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#4caf50', marginTop: '0.25rem' }}>
            94.2%
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card-surface" style={{ marginTop: '20px', marginBottom: '20px', padding: '16px' }}>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ flex: 1, minWidth: '240px', position: 'relative' }}>
            <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--on-surface-variant)' }} />
            <input 
              type="text" 
              placeholder="Search ticket ID, customer ID, or category..."
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

          <select 
            value={category}
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            style={{
              padding: '8px 12px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
          >
            <option value="">All Categories</option>
            <option value="Billing">Billing</option>
            <option value="Technical Bug">Technical Bug</option>
            <option value="Account Access">Account Access</option>
            <option value="Feature Request">Feature Request</option>
            <option value="Performance Issue">Performance Issue</option>
          </select>

          <select 
            value={priority}
            onChange={(e) => { setPriority(e.target.value); setPage(1); }}
            style={{
              padding: '8px 12px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              color: 'var(--on-surface)'
            }}
          >
            <option value="">All Priorities</option>
            <option value="Urgent">Urgent</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>
      </div>

      {/* Ticket List */}
      <div className="card-surface">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: 'var(--on-surface)' }}>
              Support Ticket Queue
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
              Real-time support telemetry & escalation tracking
            </p>
          </div>
        </div>

        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--on-surface-variant)' }}>
            <Activity size={24} className="spin" style={{ marginBottom: '8px', color: 'var(--primary)' }} />
            <p>Fetching Support Queue...</p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Ticket ID</th>
                  <th>Customer ID</th>
                  <th>Category</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Resolution Hours</th>
                  <th>CSAT Rating</th>
                  <th>Escalate Action</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map(t => (
                  <tr key={t.ticket_id}>
                    <td style={{ fontWeight: 600, color: 'var(--primary)' }}>{t.ticket_id}</td>
                    <td style={{ fontWeight: 600, color: 'var(--on-surface)' }}>{t.customer_id}</td>
                    <td>
                      <span className="badge badge-secondary">{t.category}</span>
                    </td>
                    <td>
                      <span className={`badge ${t.priority === 'Urgent' ? 'badge-error' : (t.priority === 'High' ? 'badge-warning' : 'badge-secondary')}`}>
                        {t.priority}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${t.status === 'Resolved' || t.status === 'Closed' ? 'badge-success' : 'badge-warning'}`}>
                        {t.status}
                      </span>
                    </td>
                    <td>{t.resolution_hours > 0 ? `${t.resolution_hours} hrs` : 'Pending'}</td>
                    <td>
                      {t.csat_score ? (
                        <span style={{ fontWeight: 600, color: t.csat_score >= 4 ? '#4caf50' : 'var(--error)' }}>
                          ★ {t.csat_score}/5
                        </span>
                      ) : 'N/A'}
                    </td>
                    <td>
                      {!t.escalated ? (
                        <button 
                          className="btn btn-secondary" 
                          style={{ padding: '4px 8px', fontSize: '0.75rem', color: 'var(--error)', borderColor: 'rgba(239, 68, 68, 0.3)' }}
                          disabled={escalatingId === t.ticket_id}
                          onClick={() => handleEscalate(t.ticket_id)}
                        >
                          <ShieldAlert size={12} /> {escalatingId === t.ticket_id ? 'Escalating...' : 'Escalate'}
                        </button>
                      ) : (
                        <span className="badge badge-error" style={{ fontSize: '0.7rem' }}>Escalated</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', paddingTop: '16px', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--on-surface-variant)' }}>
            Showing {tickets.length} of {total} tickets
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
