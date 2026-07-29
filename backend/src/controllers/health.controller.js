import { asyncHandler } from '../utils/asyncHandler.js';
import { httpStatus } from '../constants/httpStatus.js';
import { successMessages } from '../constants/messages.js';
import { config } from '../config/environment.js';

export const getHealthStatus = asyncHandler(async (req, res) => {
  res.status(httpStatus.OK).json({
    success: true,
    message: successMessages.SERVER_RUNNING,
    environment: config.env,
    timestamp: new Date().toISOString()
  });
});
