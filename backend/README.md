# SupportSense Backend

> **AI-Powered Customer Churn Prediction & Support Intelligence Platform**

SupportSense is an enterprise SaaS platform that helps businesses predict customer churn before customers leave. The platform combines customer profiles, support tickets, escalations, feedback, subscription history, and resolution metrics to generate churn probabilities, health scores, and AI retention recommendations.

---

## 🏗️ Architecture

The backend follows **Clean Architecture** and **SOLID Principles**, enforcing strict separation of concerns for maximum scalability, testability, and maintainability.

### Request Flow
\`\`\`
Request -> Route -> Controller -> Service -> Repository -> Database
\`\`\`

- **Routes**: Define endpoints and apply middleware. Zero business logic.
- **Controllers**: Handle HTTP requests and responses. Map data to DTOs.
- **Services**: Contain pure business and application logic.
- **Repositories**: Handle all database operations (Mongoose/MongoDB).

---

## 📁 Folder Structure

\`\`\`
backend/
├── src/
│   ├── config/        # Environment, DB, external services configuration
│   ├── constants/     # Application constants (HTTP status, messages)
│   ├── controllers/   # Request/Response handling
│   ├── database/      # Database connection and seeding
│   ├── docs/          # API documentation (Swagger/OpenAPI)
│   ├── errors/        # Custom error classes
│   ├── events/        # Event emitters and listeners
│   ├── helpers/       # Helper functions
│   ├── jobs/          # Background jobs and cron tasks
│   ├── middleware/    # Express middlewares (auth, validation, etc.)
│   ├── models/        # Mongoose schemas
│   ├── repositories/  # Database access layer
│   ├── responses/     # Standardized response formatters
│   ├── routes/        # API route definitions
│   ├── services/      # Business logic
│   ├── sockets/       # WebSocket handlers
│   ├── types/         # TypeScript-like type definitions/JSDoc
│   ├── utils/         # Reusable utilities (logger, etc.)
│   ├── validators/    # Request validation logic
│   ├── app.js         # Express app initialization
│   └── server.js      # Application entry point
├── logs/              # Application logs
├── tests/             # Unit and integration tests
├── uploads/           # File uploads directory
├── .env.example       # Example environment variables
├── .eslintrc.json     # ESLint configuration
├── .prettierrc        # Prettier configuration
└── package.json       # Project metadata and dependencies
\`\`\`

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher (LTS recommended)
- **MongoDB**: Local or Atlas instance

### Installation
1. Clone the repository and navigate to the backend folder:
   \`\`\`bash
   cd backend
   \`\`\`
2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

### Environment Variables
Copy the example environment file and fill in your values:
\`\`\`bash
cp .env.example .env
\`\`\`

#### Required Variables
- \`PORT\`: API port (default: 5000)
- \`NODE_ENV\`: \`development\` or \`production\`
- \`CLIENT_URL\`: Frontend URL for CORS
- \`MONGO_URI\`: MongoDB connection string
- \`JWT_SECRET\`, \`JWT_EXPIRE\`: JWT authentication
- \`CLOUDINARY_*\`: Image upload credentials
- \`EMAIL_*\`: SMTP credentials for Nodemailer

---

## 💻 Development Commands

- **Start Development Server**: \`npm run dev\` (uses Nodemon)
- **Start Production Server**: \`npm start\`
- **Run Linter**: \`npm run lint\`
- **Fix Lint Issues**: \`npm run lint:fix\`
- **Format Code**: \`npm run format\`
- **Run Tests**: \`npm test\`

---

## 🌐 API Versioning

All API endpoints are versioned. Current active version: **v1**
Base URL: \`/api/v1\`

### Health Endpoint
Check if the API is running correctly:

**GET** \`/api/v1/health\`

**Response:**
\`\`\`json
{
    "success": true,
    "message": "SupportSense Backend Running",
    "environment": "development",
    "timestamp": "2023-10-25T12:00:00.000Z"
}
\`\`\`

---

## 🤝 Contributing Guidelines

1. **Architecture Rules**: Never import Express into Services. Keep Controllers thin. Place DB queries exclusively in Repositories.
2. **Error Handling**: Use the built-in \`ApiError\` class for operational errors. Do not use \`console.log\`; use the provided \`logger\`.
3. **Async Code**: Wrap all async controller functions with the \`asyncHandler\` utility to catch promise rejections automatically.
4. **Code Quality**: Ensure \`npm run lint\` passes without warnings before submitting a PR.
5. **No Secrets**: Never commit passwords, keys, or secrets to version control. Always use environment variables.
