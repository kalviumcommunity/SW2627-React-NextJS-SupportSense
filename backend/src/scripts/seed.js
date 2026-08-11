import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import mongoose from 'mongoose';
import bcrypt from 'bcrypt';
import dotenv from 'dotenv';

import { User } from '../models/User.js';
import { Customer } from '../models/Customer.js';
import { Ticket } from '../models/Ticket.js';

dotenv.config();

function parseCSV(content) {
  const lines = content.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim());
    const row = {};
    headers.forEach((h, i) => {
      row[h] = values[i];
    });
    return row;
  });
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '../../..');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/churnshield';

async function seedDatabase() {
  console.log('🚀 Starting ChurnShield Database Ingestion & Seeding...');
  try {
    await mongoose.connect(MONGODB_URI);
    console.log('✅ Connected to MongoDB at:', MONGODB_URI);

    // Clear existing collections
    await User.deleteMany({});
    await Customer.deleteMany({});
    await Ticket.deleteMany({});
    console.log('🧹 Cleared existing database records.');

    // 1. Seed Demo Admin & Agent Users
    const hashedPassword = await bcrypt.hash('Password123!', 10);
    const demoUsers = [
      { name: 'Arbin Mahato', email: 'admin@churnshield.io', password: hashedPassword, role: 'admin' },
      { name: 'Sarah Manager', email: 'manager@churnshield.io', password: hashedPassword, role: 'manager' },
      { name: 'John Agent', email: 'agent@churnshield.io', password: hashedPassword, role: 'agent' },
      { name: 'Elena Analyst', email: 'analyst@churnshield.io', password: hashedPassword, role: 'analyst' }
    ];
    await User.insertMany(demoUsers);
    console.log(`✅ Created ${demoUsers.length} default user accounts.`);

    // 2. Load and Ingest Customers CSV
    const custCsvPath = path.join(PROJECT_ROOT, 'data', 'raw', 'customers.csv');
    if (!fs.existsSync(custCsvPath)) {
      throw new Error(`Customers CSV file not found at ${custCsvPath}`);
    }

    const custContent = fs.readFileSync(custCsvPath, 'utf8');
    const rawCustomers = parseCSV(custContent);

    const customerDocs = rawCustomers.map(c => {
      const churnRiskScore = parseFloat(c.churn_risk_score);
      let riskLevel = 'Low';
      if (churnRiskScore >= 70.0) riskLevel = 'High';
      else if (churnRiskScore >= 40.0) riskLevel = 'Medium';

      return {
        customer_id: c.customer_id,
        name: c.name,
        company: c.company,
        email: c.email,
        subscription_plan: c.subscription_plan,
        mrr: parseFloat(c.mrr),
        signup_date: new Date(c.signup_date),
        subscription_age_months: parseInt(c.subscription_age_months, 10),
        total_tickets: parseInt(c.total_tickets, 10),
        unresolved_tickets: parseInt(c.unresolved_tickets, 10),
        escalated_tickets: parseInt(c.escalated_tickets, 10),
        avg_csat: parseFloat(c.avg_csat),
        avg_resolution_hours: parseFloat(c.avg_resolution_hours),
        payment_delay_days: parseInt(c.payment_delay_days, 10),
        product_usage_score: parseFloat(c.product_usage_score),
        health_score: parseInt(c.health_score, 10),
        churn_risk_score: churnRiskScore,
        churn_flag: parseInt(c.churn_flag, 10),
        risk_level: riskLevel
      };
    });

    await Customer.insertMany(customerDocs);
    console.log(`✅ Successfully ingested ${customerDocs.length} customer records into MongoDB.`);

    // 3. Load and Ingest Support Tickets CSV
    const ticketCsvPath = path.join(PROJECT_ROOT, 'data', 'raw', 'customer_support_tickets.csv');
    if (!fs.existsSync(ticketCsvPath)) {
      throw new Error(`Tickets CSV file not found at ${ticketCsvPath}`);
    }

    const ticketContent = fs.readFileSync(ticketCsvPath, 'utf8');
    const rawTickets = parseCSV(ticketContent);

    const ticketDocs = rawTickets.map(t => ({
      ticket_id: t.ticket_id,
      customer_id: t.customer_id,
      category: t.category,
      priority: t.priority,
      status: t.status,
      escalated: t.escalated === 'True' || t.escalated === 'true',
      resolution_hours: parseFloat(t.resolution_hours),
      csat_score: t.csat_score ? parseFloat(t.csat_score) : null,
      subject: `${t.category} Issue - ${t.priority} Priority`,
      description: `Customer reported issue regarding ${t.category.toLowerCase()}.`,
      created_at: new Date(t.created_at)
    }));

    await Ticket.insertMany(ticketDocs);
    console.log(`✅ Successfully ingested ${ticketDocs.length} support tickets into MongoDB.`);

    console.log('--------------------------------------------------');
    console.log('🎉 Database Seeding & Ingestion Complete!');
    console.log('--------------------------------------------------');
    process.exit(0);
  } catch (error) {
    console.error('❌ Database Seeding Failed:', error);
    process.exit(1);
  }
}

seedDatabase();
