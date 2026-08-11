import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import mongoose from 'mongoose';

import routes from './routes/v1/index.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/churnshield';

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/v1', routes);

// Centralized error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled Error:', err);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Internal Server Error'
  });
});

async function startServer() {
  try {
    await mongoose.connect(MONGODB_URI);
    console.log(`✅ Connected to MongoDB at ${MONGODB_URI}`);
    app.listen(PORT, () => {
      console.log(`🚀 ChurnShield Backend API running on http://localhost:${PORT}`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
  }
}

startServer();
