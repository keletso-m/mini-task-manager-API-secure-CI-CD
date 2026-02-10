# 🔐 Task Manager API

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/task-manager-api/workflows/CI/CD%20Pipeline/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A secure, production-ready REST API for task management built with Flask. This project demonstrates modern DevOps practices including containerization, automated testing, security scanning, and CI/CD pipelines.

## ✨ Features

- **Authentication & Authorization**
  - User registration with password hashing (Werkzeug)
  - JWT-based authentication
  - Protected endpoints with token validation

- **Task Management**
  - Create, read, update, and delete tasks (CRUD)
  - User-specific task isolation
  - Task completion tracking

- **Security First**
  - Dependency scanning with Snyk
  - Container vulnerability scanning with Trivy
  - Static code analysis with CodeQL
  - Secure password storage
  - JWT token expiration

- **DevOps & CI/CD**
  - Automated testing with pytest
  - Code coverage reporting
  - Docker containerization
  - GitHub Actions workflows
  - Multi-stage security gates

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/task-manager-api.git
   cd task-manager-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app/app.py
   ```

   The API will be available at `http://localhost:5000`

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t task-manager-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 task-manager-api
   ```

## 📖 API Documentation

### Authentication Endpoints

#### Register a new user
```http
POST /api/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "username": "john_doe"
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "john_doe"
}
```

### Task Endpoints

> **Note:** All task endpoints require authentication. Include the JWT token in the Authorization header:
> ```
> Authorization: Bearer YOUR_JWT_TOKEN
> ```

#### Get all tasks
```http
GET /api/tasks
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write README and API docs",
      "completed": false,
      "created_at": "2024-01-15 10:30:00"
    }
  ]
}
```

#### Create a task
```http
POST /api/tasks
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description (optional)"
}
```

**Response (201 Created):**
```json
{
  "message": "Task created successfully",
  "task_id": 1,
  "title": "New task"
}
```

#### Update a task
```http
PUT /api/tasks/{task_id}
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "message": "Task updated successfully"
}
```

#### Delete a task
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

### Health Check

```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

## 🧪 Testing

The project includes comprehensive unit tests covering:
- User registration and authentication
- JWT token handling
- Task CRUD operations
- Error handling and edge cases

**Run all tests:**
```bash
pytest tests/ -v
```

**Run with coverage:**
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔒 Security

This project implements multiple security layers:

1. **Dependency Scanning** - Snyk monitors for vulnerable dependencies
2. **Container Scanning** - Trivy scans Docker images for CVEs
3. **Static Analysis** - CodeQL analyzes code for security issues
4. **Secure Authentication** - Password hashing with Werkzeug, JWT tokens
5. **Security Headers** - CORS and other protective headers (to be added)

### Security Scan Results

Security scans run automatically on every push via GitHub Actions. Check the Actions tab for results.

## 🏗️ Project Structure

```
task-manager-api/
├── app/
│   └── app.py              # Main Flask application
├── tests/
│   └── test_app.py         # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions workflow
├── Dockerfile              # Container definition
├── .dockerignore           # Docker ignore rules
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Backend Framework:** Flask 3.0
- **Authentication:** PyJWT 2.8
- **Database:** SQLite (easily replaceable with PostgreSQL)
- **Testing:** pytest, pytest-cov
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Security Scanning:** Snyk, Trivy, CodeQL

## 🚧 Future Enhancements

- [ ] Migrate to PostgreSQL for production
- [ ] Add Prometheus metrics endpoint
- [ ] Implement Loki for log aggregation
- [ ] Create Grafana dashboards
- [ ] Set up ELK/OpenSearch for SIEM
- [ ] Add API rate limiting
- [ ] Implement refresh tokens
- [ ] Add task categories and tags
- [ ] Email notifications
- [ ] Swagger/OpenAPI documentation

## 📝 Environment Variables

Create a `.env` file for production:

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///tasks.db  # or postgresql://...
FLASK_ENV=production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile](https://linkedin.com/in/YOUR_PROFILE)

## 🙏 Acknowledgments

- Built as a learning project for DevOps and security best practices
- Inspired by modern cloud-native application patterns

---

⭐ **Star this repo if you find it useful!**
