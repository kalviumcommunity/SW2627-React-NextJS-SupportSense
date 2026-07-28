# SupportSense

**AI-Powered Customer Churn Prediction & Support Intelligence Platform**

SupportSense is an AI-powered SaaS platform that helps companies reduce customer churn by combining customer support operations with predictive machine learning. The system analyzes support tickets, customer profiles, subscription history, customer feedback, resolution history, and escalations to predict which customers are most likely to churn while recommending proactive retention actions.

This repository contains the Node.js / Express backend foundation which serves both a React Frontend and a Python ML Service (FastAPI) via REST APIs.

---

## Architecture

The backend follows **Clean Architecture** and **MVC (Model-View-Controller)** principles, designed to scale for 100+ REST APIs and multiple parallel developers. 

**Core Principles:**
- **Separation of Concerns**: Controllers only handle HTTP requests/responses, Services contain all business logic, and Repositories handle all database queries.
- **SOLID Principles**: Adherence to single responsibility and dependency inversion for highly maintainable code.
- **Security First**: Integrated with Helmet, Express Rate Limit, and CORS out-of-the-box.
- **Centralized Error Handling**: A robust error handler for catching operational and unhandled exceptions securely.

---

## Folder Structure

```
backend/
├── src/
│   ├── config/         # Environment, DB, Cloudinary, and Email configurations
│   ├── constants/      # HTTP status codes, standard success/error messages
│   ├── controllers/    # Route controllers (req/res handling only)
│   ├── routes/         # Express API routes (versioned)
│   ├── services/       # Core business logic
│   ├── repositories/   # Database queries and abstraction
│   ├── models/         # Mongoose schemas
│   ├── validators/     # Request payload validation
│   ├── middleware/     # Custom Express middlewares (error, logger, request-id)
│   ├── helpers/        # Reusable helper functions
│   ├── utils/          # Standard utilities (ApiResponse, ApiError, asyncHandler)
│   ├── errors/         # Custom error types
│   ├── responses/      # Response transformers
│   ├── jobs/           # Cron jobs and scheduled tasks
│   ├── events/         # Event emitters and listeners
│   ├── sockets/        # WebSockets implementation
│   ├── docs/           # API Documentation (Swagger/OpenAPI)
│   ├── types/          # TypeScript-like JSDoc or typedefs
│   ├── app.js          # Express app configuration
│   └── server.js       # Server bootstrap and DB connection
├── tests/              # Unit and integration tests
├── uploads/            # Local file uploads
├── logs/               # Application log files
├── .env.example        # Environment variables template
├── .eslintrc.json      # ESLint configuration
├── .prettierrc         # Prettier configuration
└── package.json        # Node dependencies and scripts
```

---

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

---

## Environment Variables

Create a `.env` file in the `backend/` directory based on the provided `.env.example`:

```env
PORT=5000
NODE_ENV=development
CLIENT_URL=http://localhost:3000

MONGO_URI=mongodb://localhost:27017/supportsense

JWT_SECRET=your_jwt_secret_here
JWT_EXPIRE=7d
COOKIE_EXPIRE=7

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USER=your_email_user
EMAIL_PASS=your_email_password
EMAIL_FROM=noreply@supportsense.com
```

---

## Development Commands

```bash
# Start the development server with Nodemon
npm run dev

# Run ESLint to find issues
npm run lint

# Run ESLint to automatically fix issues
npm run lint:fix

# Format code with Prettier
npm run format
```

---

## Production Commands

```bash
# Start the production server
npm start
```

*Note: Ensure `NODE_ENV` is set to `production` and all required environment variables are configured securely on your host.*

---

## API Versioning

All endpoints are versioned under `/api/v1/`. As the application grows, future breaking changes can be introduced under `/api/v2/` without affecting older clients.

---

## Health Check

To verify the backend is running correctly, use the built-in health check route.

**Endpoint:** `GET /api/v1/health`

**Sample Response:**
```json
{
  "success": true,
  "statusCode": 200,
  "message": "SupportSense Backend Running",
  "data": {
    "environment": "development",
    "uptime": 12.34,
    "memoryUsage": { ... },
    "timestamp": "2023-10-25T12:00:00.000Z"
  },
  "timestamp": "2023-10-25T12:00:00.000Z"
}
```

---

## Contributing

1. Create a feature branch from `main`.
2. Ensure you follow the Clean Architecture structure.
3. Run `npm run lint` and `npm run format` before committing.
4. Ensure no business logic leaks into Controllers or Routes.
5. Create a Pull Request outlining your changes.
