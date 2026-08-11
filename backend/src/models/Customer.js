import mongoose from 'mongoose';

const customerSchema = new mongoose.Schema({
  customer_id: { type: String, required: true, unique: true, index: true },
  name: { type: String, required: true },
  company: { type: String, default: '' },
  email: { type: String, required: true, lowercase: true },
  subscription_plan: { type: String, enum: ['Starter', 'Pro', 'Enterprise'], default: 'Starter' },
  mrr: { type: Number, default: 0 },
  signup_date: { type: Date, default: Date.now },
  subscription_age_months: { type: Number, default: 1 },
  total_tickets: { type: Number, default: 0 },
  unresolved_tickets: { type: Number, default: 0 },
  escalated_tickets: { type: Number, default: 0 },
  avg_csat: { type: Number, default: 4.0 },
  avg_resolution_hours: { type: Number, default: 24.0 },
  payment_delay_days: { type: Number, default: 0 },
  product_usage_score: { type: Number, default: 50.0 },
  health_score: { type: Number, default: 100 },
  churn_risk_score: { type: Number, default: 0.0 },
  churn_flag: { type: Number, enum: [0, 1], default: 0 },
  risk_level: { type: String, enum: ['Low', 'Medium', 'High'], default: 'Low' },
  assigned_manager: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }
}, { timestamps: true });

export const Customer = mongoose.model('Customer', customerSchema);
