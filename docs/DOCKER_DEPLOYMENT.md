# Docker Deployment Guide

This guide explains how to deploy the AI-Driven Cybersecurity Platform using Docker containers.

## Architecture Overview

The platform consists of four main services:

1. **PostgreSQL Database** - Stores security events, threats, and analytics
2. **API Service** - REST API for threat prediction and management
3. **Dashboard Service** - Web-based real-time monitoring interface
4. **NATEM Agent** - Network Attack Threat Event Monitor

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB+ RAM available
- Port availability: 5000, 5432, 8080

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/aniket2040/AI-driven-cybersecurity-.git
cd AI-driven-cybersecurity-
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_PASSWORD=YourSecurePassword123

# Optional: API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Optional: Dashboard Configuration
DASHBOARD_PORT=8080
```

### 3. Build and Start Services

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Verify Deployment

```bash
# Check service health
docker-compose ps

# Test API
curl http://localhost:5000/health

# Test Dashboard
curl http://localhost:8080/health
```

### 5. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:8080
```

## Service Details

### PostgreSQL Database

- **Container Name**: `cyber_threat_db`
- **Port**: 5432
- **Default Database**: cyber_threat_db
- **Default User**: cyberuser
- **Volume**: postgres_data (persistent storage)

#### Connect to Database

```bash
docker exec -it cyber_threat_db psql -U cyberuser -d cyber_threat_db
```

### API Service

- **Container Name**: `cyber_api`
- **Port**: 5000
- **Endpoints**:
  - `GET /health` - Health check
  - `POST /api/v1/predict` - Single threat prediction
  - `POST /api/v1/predict/batch` - Batch predictions
  - `POST /api/v1/summarize` - Get AI summary of threat
  - `GET /api/v1/alerts` - Get active alerts
  - `GET /api/v1/statistics` - Get system statistics

#### Test API Prediction

```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "source_port": 12345,
    "destination_port": 22,
    "protocol": "TCP",
    "packet_size": 64,
    "payload_size": 24,
    "tcp_flags": "SYN"
  }'
```

#### Test AI Summarization

```bash
curl -X POST http://localhost:5000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "source_port": 54321,
    "destination_port": 3306,
    "protocol": "TCP",
    "packet_size": 2048,
    "payload_size": 2008,
    "tcp_flags": "PSH"
  }'
```

### Dashboard Service

- **Container Name**: `cyber_dashboard`
- **Port**: 8080
- **Features**:
  - Real-time threat monitoring
  - AI-generated security summaries
  - Interactive charts and graphs
  - Alert management
  - Historical analysis

### NATEM Agent

- **Container Name**: `natem_agent`
- **Purpose**: Monitors network traffic and feeds events to the API
- **Features**:
  - Simulates network traffic patterns
  - Generates both benign and malicious traffic
  - Logs AI summaries of detected threats
  - Provides real-time statistics

#### View NATEM Agent Logs

```bash
docker logs -f natem_agent
```

## Container Management

### Start Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api
```

### Scale Services

```bash
# Run multiple API instances (requires load balancer)
docker-compose up -d --scale api=3
```

## Model Training

Before the API can make predictions, you need to train a model:

### Option 1: Train Inside Container

```bash
# Access the API container
docker exec -it cyber_api bash

# Train models
python scripts/train_models.py

# Exit container
exit
```

### Option 2: Train on Host and Mount

```bash
# Train on host machine
python scripts/train_models.py

# Models are automatically available in container via volume mount
```

## Data Persistence

### Database Backups

```bash
# Create backup
docker exec cyber_threat_db pg_dump -U cyberuser cyber_threat_db > backup.sql

# Restore backup
cat backup.sql | docker exec -i cyber_threat_db psql -U cyberuser cyber_threat_db
```

### Model Persistence

Models are stored in the `./models` directory which is mounted as a volume. They persist across container restarts.

## Troubleshooting

### Issue: API service won't start

**Solution**: Check if port 5000 is available
```bash
lsof -i :5000
docker-compose logs api
```

### Issue: Database connection refused

**Solution**: Wait for database to be ready
```bash
docker-compose logs postgres
docker exec cyber_threat_db pg_isready -U cyberuser
```

### Issue: Dashboard shows no data

**Solution**: Ensure API is running and accessible
```bash
curl http://localhost:5000/health
docker-compose logs dashboard
```

### Issue: NATEM agent can't connect to API

**Solution**: Check network connectivity
```bash
docker network inspect ai-driven-cybersecurity-_cyber_network
docker exec natem_agent ping api
```

## Production Deployment Considerations

### 1. Security

- Change default database password
- Use secrets management (Docker Secrets)
- Enable HTTPS with reverse proxy (nginx/traefik)
- Implement authentication for API endpoints

```yaml
# Example with secrets
secrets:
  db_password:
    external: true

services:
  postgres:
    secrets:
      - db_password
```

### 2. Scalability

- Use load balancer for API services
- Implement Redis for caching
- Use managed database (AWS RDS, etc.)
- Add monitoring (Prometheus + Grafana)

### 3. High Availability

```yaml
services:
  api:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

### 4. Monitoring

```bash
# Add Prometheus
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### 5. Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Network Configuration

### Custom Network

```yaml
networks:
  cyber_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

### Expose to External Network

```yaml
services:
  api:
    networks:
      - cyber_network
      - external_network
```

## Environment Variables Reference

| Variable | Service | Description | Default |
|----------|---------|-------------|---------|
| DB_PASSWORD | postgres, api | Database password | SecurePassword123 |
| DATABASE_URL | api, natem_agent | Full database connection string | Auto-generated |
| API_BASE_URL | dashboard | API endpoint URL | http://api:5000/api/v1 |
| PYTHONPATH | All | Python module path | /app |

## Useful Commands

```bash
# View resource usage
docker stats

# Clean up unused resources
docker system prune -a

# Export database schema
docker exec cyber_threat_db pg_dump -U cyberuser -s cyber_threat_db > schema.sql

# Check disk usage
docker system df

# View container processes
docker-compose top

# Execute command in container
docker exec -it cyber_api python --version

# Copy files from container
docker cp cyber_api:/app/models/trained/model.pkl ./model.pkl
```

## Maintenance

### Update Images

```bash
# Pull latest images
docker-compose pull

# Rebuild services
docker-compose build --no-cache

# Restart with new images
docker-compose up -d
```

### Clean Logs

```bash
# Clear logs for service
docker-compose logs --no-log-prefix api > /dev/null

# Or restart service to clear in-memory logs
docker-compose restart api
```

## Support and Documentation

- **API Documentation**: http://localhost:5000/docs (if enabled)
- **Dashboard**: http://localhost:8080
- **GitHub Issues**: https://github.com/aniket2040/AI-driven-cybersecurity-/issues

## License

This project is licensed under the MIT License - see LICENSE file for details.
