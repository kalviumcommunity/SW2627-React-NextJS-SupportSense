import express from 'express';
import healthRoutes from './health.routes.js';
import authRoutes from './auth.routes.js';
import customerRoutes from './customer.routes.js';
import ticketRoutes from './ticket.routes.js';
import analyticsRoutes from './analytics.routes.js';

const router = express.Router();

router.use('/health', healthRoutes);
router.use('/auth', authRoutes);
router.use('/customers', customerRoutes);
router.use('/tickets', ticketRoutes);
router.use('/analytics', analyticsRoutes);

export default router;
