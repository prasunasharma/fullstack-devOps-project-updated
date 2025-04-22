# 🚀 Fullstack DevOps Project: FastAPI Application Deployment

This project demonstrates a full DevOps pipeline using FastAPI, Docker, Terraform, Ansible, and Monitoring tools like Prometheus and Grafana.

---

## 📦 Tech Stack

- **FastAPI** – Lightweight Python web framework
- **Docker & Docker Compose** – Containerization and orchestration
- **Terraform** – Infrastructure provisioning (Docker-based in this case)
- **Ansible** – Configuration management and deployment automation
- **Prometheus, Grafana, Loki, Promtail** – Monitoring and observability stack

---

## 🔧 Project Structure


---

## ✅ What It Does

1. Uses **Terraform** to pull and run a FastAPI Docker container
2. Uses **Ansible** to install Docker, copy the app, and run it on remote/local machine
3. Exposes metrics/logs to **Grafana** using Prometheus, Loki, and Promtail
4. Runs the full stack in a reproducible manner via automation

---

## 🧪 Reproduction Steps

### 🐳 Run with Docker Compose
```bash
docker-compose up --build


App available at: http://localhost:3000

Deploy with Terraform

cd terraform
terraform init
terraform apply

Deploys a container named fastapi-demo at http://localhost:8080

Run Monitoring Stack
docker-compose -f docker-compose.monitoring.yml up -d

Grafana: http://localhost:3001

Prometheus: http://localhost:9090

Ansible Deployment
cd ansible
ansible-playbook deploy.yml -i inventory
This playbook:

Installs Docker

Copies app files to /opt/fullstack-app

Runs docker-compose up -d from that path



