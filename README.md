# mini-task-manager-API-secure-CI-CD
# mini-task-manager-API-secure-CI-CD
# Task Manager API 🚀

A minimal **Task Manager REST API** built with [Python Flask] (or Node.js Express).  
This project is designed as a **learning playground** for:
- Building web APIs (auth, CRUD, DB).
- Containerization & deployment.
- Secure CI/CD pipelines with Trivy, Snyk, CodeQL.
- Observability (Prometheus, Loki, Grafana).
- Security monitoring (SIEM concepts).

---

## ✨ Features
- User registration & login (with hashed passwords).
- Create, list, and delete tasks.
- Simple database (SQLite for now).
- Unit tests.
- Dockerized application.

---

## 🛠️ Tech Stack
- **Backend:** Python Flask 
- **Database:** SQLite (swap later for Postgres)
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Security Scans:**
  - [Snyk](https://snyk.io) → dependency scanning
  - [Trivy](https://aquasecurity.github.io/trivy/) → container & IaC scanning
  - [CodeQL](https://codeql.github.com/) → static code analysis
- **Observability (stretch goals):**
  - Prometheus → metrics
  - Loki → log aggregation
  - Grafana → dashboards
- **Security Monitoring (stretch goals):**
  - Elastic Stack (ELK) or OpenSearch → SIEM

---

## 📂 Project Structure
