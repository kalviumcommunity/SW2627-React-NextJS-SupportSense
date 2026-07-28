import { asyncHandler } from '../utils/asyncHandler.js';
import { ApiResponse } from '../utils/ApiResponse.js';
import { httpStatus } from '../constants/httpStatus.js';
import { successMessages } from '../constants/successMessages.js';
import { config } from '../config/environment.js';

export const getHealthStatus = asyncHandler(async (req, res) => {
  const data = {
    environment: config.env,
    uptime: process.uptime(),
    memoryUsage: process.memoryUsage(),
    timestamp: new Date().toISOString(),
  };

  res.status(httpStatus.OK).json(new ApiResponse(httpStatus.OK, data, successMessages.HEALTH_CHECK));
});
