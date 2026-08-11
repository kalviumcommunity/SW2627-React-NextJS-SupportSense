import express from 'express';
import { getDashboardKPIs, getAnalyticsCharts } from '../../controllers/analytics.controller.js';
import { authenticateJWT } from '../../middleware/auth.middleware.js';

const router = express.Router();

router.get('/dashboard', authenticateJWT, getDashboardKPIs);
router.get('/charts', authenticateJWT, getAnalyticsCharts);

export default router;
