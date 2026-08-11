import express from 'express';
import { getCustomers, getCustomerById, predictCustomerChurn } from '../../controllers/customer.controller.js';
import { authenticateJWT } from '../../middleware/auth.middleware.js';

const router = express.Router();

router.get('/', authenticateJWT, getCustomers);
router.get('/:id', authenticateJWT, getCustomerById);
router.post('/:id/predict', authenticateJWT, predictCustomerChurn);

export default router;
