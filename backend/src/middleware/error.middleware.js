import mongoose from 'mongoose';
import { ApiError } from '../utils/ApiError.js';
import { config } from '../config/environment.js';
import { httpStatus } from '../constants/httpStatus.js';
import { logger } from '../utils/logger.js';

export const errorHandler = (err, req, res, next) => {
  let error = err;

  // If the error is not an instance of ApiError, convert it
  if (!(error instanceof ApiError)) {
    const statusCode =
      error.statusCode || error instanceof mongoose.Error
        ? httpStatus.BAD_REQUEST
        : httpStatus.INTERNAL_SERVER_ERROR;
    const message = error.message || 'Something went wrong';
    error = new ApiError(statusCode, message, [], error.stack);
  }

  // Handle specific Mongoose Errors
  if (err.name === 'CastError') {
    const message = `Resource not found with id of ${err.value}`;
    error = new ApiError(httpStatus.NOT_FOUND, message);
  }

  if (err.code === 11000) {
    const message = 'Duplicate field value entered';
    error = new ApiError(httpStatus.BAD_REQUEST, message);
  }

  if (err.name === 'ValidationError') {
    const message = Object.values(err.errors).map((val) => val.message).join(', ');
    error = new ApiError(httpStatus.BAD_REQUEST, message);
  }

  // Handle JWT Errors
  if (err.name === 'JsonWebTokenError') {
    const message = 'Invalid Token. Please log in again.';
    error = new ApiError(httpStatus.UNAUTHORIZED, message);
  }

  if (err.name === 'TokenExpiredError') {
    const message = 'Token expired. Please log in again.';
    error = new ApiError(httpStatus.UNAUTHORIZED, message);
  }

  const response = {
    success: false,
    statusCode: error.statusCode,
    message: error.message,
    errors: error.errors,
    timestamp: error.timestamp,
    ...(config.env === 'development' && { stack: error.stack }),
  };

  if (error.statusCode === httpStatus.INTERNAL_SERVER_ERROR) {
    logger.error(`${req.method} ${req.originalUrl} - ${error.message}`, { stack: error.stack });
  }

  res.status(error.statusCode).json(response);
};

export const notFoundHandler = (req, res, next) => {
  const error = new ApiError(httpStatus.NOT_FOUND, `Not Found - ${req.originalUrl}`);
  next(error);
};
