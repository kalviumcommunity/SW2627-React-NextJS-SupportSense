const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function fetchDashboardKPIs() {
  const res = await fetch(`${API_BASE_URL}/analytics/dashboard`);
  const data = await res.json();
  return data.kpis;
}

export async function fetchAnalyticsCharts() {
  const res = await fetch(`${API_BASE_URL}/analytics/charts`);
  return await res.json();
}

export async function fetchCustomers(params: { risk_level?: string; plan?: string; search?: string; limit?: number; page?: number }) {
  const query = new URLSearchParams();
  if (params.risk_level) query.append('risk_level', params.risk_level);
  if (params.plan) query.append('plan', params.plan);
  if (params.search) query.append('search', params.search);
  if (params.limit) query.append('limit', params.limit.toString());
  if (params.page) query.append('page', params.page.toString());

  const res = await fetch(`${API_BASE_URL}/customers?${query.toString()}`);
  return await res.json();
}

export async function fetchCustomerDetails(id: string) {
  const res = await fetch(`${API_BASE_URL}/customers/${id}`);
  return await res.json();
}

export async function runAIPrediction(customerId: string) {
  const res = await fetch(`${API_BASE_URL}/customers/${customerId}/predict`, {
    method: 'POST'
  });
  return await res.json();
}

export async function fetchTickets(params: { status?: string; priority?: string; category?: string; search?: string; limit?: number; page?: number }) {
  const query = new URLSearchParams();
  if (params.status) query.append('status', params.status);
  if (params.priority) query.append('priority', params.priority);
  if (params.category) query.append('category', params.category);
  if (params.search) query.append('search', params.search);
  if (params.limit) query.append('limit', params.limit.toString());
  if (params.page) query.append('page', params.page.toString());

  const res = await fetch(`${API_BASE_URL}/tickets?${query.toString()}`);
  return await res.json();
}

export async function createTicket(ticket: { customer_id: string; category: string; priority: string; subject: string; description?: string }) {
  const res = await fetch(`${API_BASE_URL}/tickets`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ticket)
  });
  return await res.json();
}

export async function escalateTicket(ticketId: string) {
  const res = await fetch(`${API_BASE_URL}/tickets/${ticketId}/escalate`, {
    method: 'POST'
  });
  return await res.json();
}
