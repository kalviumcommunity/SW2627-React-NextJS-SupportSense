const logger = {
  info: (message, meta = {}) => {
    console.log(`[INFO] ${new Date().toISOString()} - ${message}`, Object.keys(meta).length ? meta : '');
  },
  error: (message, meta = {}) => {
    console.error(`[ERROR] ${new Date().toISOString()} - ${message}`, Object.keys(meta).length ? meta : '');
  },
  warn: (message, meta = {}) => {
    console.warn(`[WARN] ${new Date().toISOString()} - ${message}`, Object.keys(meta).length ? meta : '');
  },
  debug: (message, meta = {}) => {
    console.debug(`[DEBUG] ${new Date().toISOString()} - ${message}`, Object.keys(meta).length ? meta : '');
  },
};

export { logger };
