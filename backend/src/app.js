import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import cookieParser from 'cookie-parser';
import { rateLimit } from 'express-rate-limit';

import { config } from './config/environment.js';
import { morganMiddleware } from './middleware/logger.middleware.js';
import { requestIdMiddleware } from './middleware/request-id.middleware.js';
import { errorHandler, notFoundHandler } from './middleware/error.middleware.js';

import v1Routes from './routes/v1/index.js';

const app = express();

// Security Middlewares
app.use(helmet());
app.use(
  cors({
    origin: config.clientUrl,
    credentials: true,
  })
);

// Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per `window` (here, per 15 minutes)
  message: 'Too many requests from this IP, please try again after 15 minutes',
  standardHeaders: true, 
  legacyHeaders: false, 
});
app.use('/api', limiter);

// Request parsing and compression
app.use(express.json({ limit: '16kb' }));
app.use(express.urlencoded({ extended: true, limit: '16kb' }));
app.use(cookieParser());
app.use(compression());

// Custom Middlewares
app.use(requestIdMiddleware);
app.use(morganMiddleware);

// API Routes
app.use('/api/v1', v1Routes);

// Error Handling
app.use(notFoundHandler);
app.use(errorHandler);

export { app };
