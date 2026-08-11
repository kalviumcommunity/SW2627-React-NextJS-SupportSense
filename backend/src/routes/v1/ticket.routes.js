import express from 'express';
import { getTickets, createTicket, updateTicketStatus, escalateTicket } from '../../controllers/ticket.controller.js';
import { authenticateJWT } from '../../middleware/auth.middleware.js';

const router = express.Router();

router.get('/', authenticateJWT, getTickets);
router.post('/', authenticateJWT, createTicket);
router.patch('/:id/status', authenticateJWT, updateTicketStatus);
router.post('/:id/escalate', authenticateJWT, escalateTicket);

export default router;
