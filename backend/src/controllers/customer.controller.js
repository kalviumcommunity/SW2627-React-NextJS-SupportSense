import { Customer } from '../models/Customer.js';
import { Ticket } from '../models/Ticket.js';
import { Prediction } from '../models/Prediction.js';
import axios from 'axios';

const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000';

export const getCustomers = async (req, res) => {
  try {
    const { risk_level, plan, search, limit = 50, page = 1 } = req.query;
    const query = {};

    if (risk_level) query.risk_level = risk_level;
    if (plan) query.subscription_plan = plan;
    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { company: { $regex: search, $options: 'i' } },
        { email: { $regex: search, $options: 'i' } },
        { customer_id: { $regex: search, $options: 'i' } }
      ];
    }

    const customers = await Customer.find(query)
      .limit(Number(limit))
      .skip((Number(page) - 1) * Number(limit))
      .sort({ churn_risk_score: -1 });

    const total = await Customer.countDocuments(query);

    return res.status(200).json({
      success: true,
      total,
      page: Number(page),
      limit: Number(limit),
      customers
    });
  } catch (error) {
    return res.status(500).json({ success: false, message: error.message });
  }
};

export const getCustomerById = async (req, res) => {
  try {
    const customer = await Customer.findOne({ customer_id: req.params.id });
    if (!customer) {
      return res.status(404).json({ success: false, message: 'Customer not found.' });
    }

    const tickets = await Ticket.find({ customer_id: req.params.id }).sort({ created_at: -1 });
    const latestPrediction = await Prediction.findOne({ customer_id: req.params.id }).sort({ predicted_at: -1 });

    return res.status(200).json({
      success: true,
      customer,
      tickets,
      prediction: latestPrediction
    });
  } catch (error) {
    return res.status(500).json({ success: false, message: error.message });
  }
};

export const predictCustomerChurn = async (req, res) => {
  try {
    const customer = await Customer.findOne({ customer_id: req.params.id });
    if (!customer) {
      return res.status(404).json({ success: false, message: 'Customer not found.' });
    }

    // Call Python FastAPI ML Service
    const mlResponse = await axios.post(`${FASTAPI_URL}/predict`, {
      customer_id: customer.customer_id,
      mrr: customer.mrr,
      subscription_age_months: customer.subscription_age_months,
      total_tickets: customer.total_tickets,
      unresolved_tickets: customer.unresolved_tickets,
      escalated_tickets: customer.escalated_tickets,
      avg_csat: customer.avg_csat,
      avg_resolution_hours: customer.avg_resolution_hours,
      payment_delay_days: customer.payment_delay_days,
      product_usage_score: customer.product_usage_score
    });

    const predictionData = mlResponse.data;

    // Save prediction record
    const prediction = await Prediction.create({
      customer_id: customer.customer_id,
      churn_probability: predictionData.churn_probability,
      risk_level: predictionData.risk_level,
      health_score: predictionData.health_score,
      confidence_score: predictionData.confidence_score,
      churn_drivers: predictionData.churn_drivers,
      recommendations: predictionData.recommendations
    });

    // Update Customer Health & Risk metrics
    customer.health_score = predictionData.health_score;
    customer.churn_risk_score = roundToTwo(predictionData.churn_probability * 100);
    customer.risk_level = predictionData.risk_level;
    customer.churn_flag = predictionData.churn_probability >= 0.65 ? 1 : 0;
    await customer.save();

    return res.status(200).json({
      success: true,
      message: 'Churn risk updated successfully via AI Model.',
      prediction,
      customer
    });
  } catch (error) {
    return res.status(500).json({ success: false, message: `Prediction API failed: ${error.message}` });
  }
};

function roundToTwo(num) {
  return Math.round((num + Number.EPSILON) * 100) / 100;
}
