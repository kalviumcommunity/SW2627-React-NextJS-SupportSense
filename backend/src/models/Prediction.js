import mongoose from 'mongoose';

const predictionSchema = new mongoose.Schema({
  customer_id: { type: String, required: true, index: true },
  churn_probability: { type: Number, required: true },
  risk_level: { type: String, enum: ['Low', 'Medium', 'High'], required: true },
  health_score: { type: Number, required: true },
  confidence_score: { type: Number, required: true },
  churn_drivers: [{ type: String }],
  recommendations: [{ type: String }],
  predicted_at: { type: Date, default: Date.now }
}, { timestamps: true });

export const Prediction = mongoose.model('Prediction', predictionSchema);
