import mongoose from 'mongoose';

const ticketSchema = new mongoose.Schema({
  ticket_id: { type: String, required: true, unique: true, index: true },
  customer_id: { type: String, required: true, index: true },
  category: { 
    type: String, 
    enum: ['Billing', 'Technical Bug', 'Account Access', 'Feature Request', 'Performance Issue'], 
    required: true 
  },
  priority: { 
    type: String, 
    enum: ['Low', 'Medium', 'High', 'Urgent'], 
    default: 'Medium' 
  },
  status: { 
    type: String, 
    enum: ['Open', 'In Progress', 'Escalated', 'Resolved', 'Closed'], 
    default: 'Open' 
  },
  escalated: { type: Boolean, default: false },
  resolution_hours: { type: Number, default: -1.0 },
  csat_score: { type: Number, min: 1.0, max: 5.0, default: null },
  assigned_agent: { type: String, default: 'Unassigned' },
  subject: { type: String, default: 'Customer Support Request' },
  description: { type: String, default: '' },
  comments: [{
    author: String,
    content: String,
    created_at: { type: Date, default: Date.now }
  }],
  created_at: { type: Date, default: Date.now }
}, { timestamps: true });

export const Ticket = mongoose.model('Ticket', ticketSchema);
