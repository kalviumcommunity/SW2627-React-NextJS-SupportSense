import { Ticket } from '../models/Ticket.js';
import { Customer } from '../models/Customer.js';

export const getTickets = async (req, res) => {
  try {
    const { status, priority, category, customer_id, search, limit = 50, page = 1 } = req.query;
    const query = {};

    if (status) query.status = status;
    if (priority) query.priority = priority;
    if (category) query.category = category;
    if (customer_id) query.customer_id = customer_id;
    if (search) {
      query.$or = [
        { ticket_id: { $regex: search, $options: 'i' } },
        { customer_id: { $regex: search, $options: 'i' } },
        { subject: { $regex: search, $options: 'i' } }
      ];
    }

    const tickets = await Ticket.find(query)
      .limit(Number(limit))
      .skip((Number(page) - 1) * Number(limit))
      .sort({ created_at: -1 });

    const total = await Ticket.countDocuments(query);

    return res.status(200).json({
      success: true,
      total,
      page: Number(page),
      limit: Number(limit),
      tickets
    });
  } catch (error) {
    return res.status(500).json({ success: false, message: error.message });
  }
};

export const createTicket = async (req, res) => {
  try {
    const { customer_id, category, priority, subject, description, assigned_agent } = req.body;

    const ticket_id = `TCK-${Date.now().toString().slice(-6)}`;
    const ticket = await Ticket.create({
      ticket_id,
      customer_id,
      category,
      priority,
      subject,
      description,
      assigned_agent: assigned_agent || 'Unassigned'
    });

    // Update Customer Ticket metrics
    await Customer.updateOne(
      { customer_id },
      { $inc: { total_tickets: 1, unresolved_tickets: 1 } }
    );

    return res.status(201).json({ success: true, ticket });
  } catch (error) {
    return res.status(500).json({ success: false, message: error.message });
  }
};

export const updateTicketStatus = async (req, res) => {
  try {
    const { status, csat_score, resolution_hours } = req.body;
    const ticket = await Ticket.findOne({ ticket_id: req.params.id });

    if (!ticket) {
      return res.status(404).json({ success: false, message: 'Ticket not found.' });
    }

    const prevStatus = ticket.status;
    ticket.status = status || ticket.status;
    if (csat_score !== undefined) ticket.csat_score = csat_score;
    if (resolution_hours !== undefined) ticket.resolution_hours = resolution_hours;

    await ticket.save();

    // If resolved or closed, decrement unresolved tickets
    if ((prevStatus === 'Open' || prevStatus === 'In Progress' || prevStatus === 'Escalated') &&
        (status === 'Resolved' || status === 'Closed')) {
      await Customer.updateOne(
        { customer_id: ticket.customer_id },
        { $inc: { unresolved_tickets: -1 } }
      );
    }

    return res.status(200).json({ success: true, ticket });
  } catch (error) {
    return res.status(500).json({ success: false, message: error.message });
  }
};

export const escalateTicket = async (req, res) => {
  try {
    const ticket = await Ticket.findOne({ ticket_id: req.params.id });

    if (!ticket) {
      return res.status(404).json({ success: false, message: 'Ticket not found.' });
    }

    ticket.escalated = true;
    ticket.status = 'Escalated';
    ticket.priority = 'Urgent';
    await ticket.save();

    // Increment Customer escalated ticket count
    await Customer.updateOne(
      { customer_id: ticket.customer_id },
      { $inc: { escalated_tickets: 1 } }
    );

    return res.status(200).json({ success: true, message: 'Ticket escalated to Urgent tier.', ticket });
  } catch (error) {
    return res.status(500).json({ success: false, message: error.message });
  }
};
