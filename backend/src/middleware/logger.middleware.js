import morgan from 'morgan';
import { logger } from '../utils/logger.js';
import { config } from '../config/environment.js';

const stream = {
  write: (message) => logger.info(message.trim()),
};

const skip = () => {
  const env = config.env || 'development';
  return env !== 'development';
};

const morganMiddleware = morgan(
  ':remote-addr - :remote-user [:date[clf]] ":method :url HTTP/:http-version" :status :res[content-length] ":referrer" ":user-agent" - :response-time ms',
  { stream, skip }
);

export { morganMiddleware };
