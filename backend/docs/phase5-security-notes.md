# Phase 5 Security Notes

## HTTPS Requirement

MindMirror uses JWT-based authentication to protect authenticated API requests.

### Local Development

Local development may use HTTP:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

This is acceptable because the application is running locally during development.

### Production Deployment

Production deployment must use HTTPS.

HTTPS is required because authenticated requests contain a JWT access token in the `Authorization` header. HTTPS protects the token and other application data while they are transmitted between the browser and backend.

Production requirements:

- Serve the frontend over HTTPS.
- Serve the backend API over HTTPS.
- Do not deploy authenticated production traffic over plain HTTP.
- Configure the production frontend URL using the `FRONTEND_URL` environment variable.
- Keep `JWT_SECRET` in environment configuration and never commit it to Git.
- Do not expose passwords, JWTs, password hashes, or raw journal content in application logs.

## Authentication Security

MindMirror uses:

- Argon2-based password hashing.
- JWT access tokens with expiration.
- Protected API endpoints requiring authentication.
- User-level authorization and data isolation.
- Rate limiting on login and registration endpoints.
- Restricted CORS using the configured frontend origin.

## Development vs Production

The current local configuration is intended for development and testing.

Before production deployment, HTTPS, production environment variables, secure secret management, and the production frontend origin must be configured appropriately.