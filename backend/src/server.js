import { app } from './app.js';
import { config } from './config/environment.js';
import { connectDB } from './config/database.js';
import { logger } from './utils/logger.js';

let server;

const startServer = async () => {
  try {
    // Connect to Database
    await connectDB();

    // Start listening
    server = app.listen(config.port, () => {
      logger.info(`Server is running in ${config.env} mode on port ${config.port}`);
    });
  } catch (error) {
    logger.error(`Failed to start server: ${error.message}`);
    process.exit(1);
  }
};

startServer();

// Handle Unhandled Promise Rejections
process.on('unhandledRejection', (err) => {
  logger.error(`Unhandled Rejection: ${err.message}`);
  logger.error('Shutting down the server due to Unhandled Promise Rejection');
  if (server) {
    server.close(() => {
      process.exit(1);
    });
  } else {
    process.exit(1);
  }
});

// Handle Uncaught Exceptions
process.on('uncaughtException', (err) => {
  logger.error(`Uncaught Exception: ${err.message}`);
  logger.error('Shutting down the server due to Uncaught Exception');
  process.exit(1);
});

// Graceful Shutdown on SIGTERM
process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down gracefully...');
  if (server) {
    server.close(() => {
      logger.info('Process terminated.');
      process.exit(0);
    });
  } else {
    process.exit(0);
  }
});
