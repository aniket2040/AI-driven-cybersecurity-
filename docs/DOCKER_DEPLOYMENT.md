# Docker Deployment Guide for AI-Driven Cybersecurity Platform

## Overview

This guide explains how to deploy the AI-driven cybersecurity threat detection platform using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- At least 4GB RAM
- 10GB free disk space

## Quick Start

### 1. Build and Start All Services

```bash
# Start all services (API, Dashboard, Database)
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 2. Train Models (First Time Setup)

```bash
# Train ML models inside the container
docker-compose exec api python scripts/train_models.py

# Or build models locally and mount the volume
python scripts/train_models.py
```

### 3. Access Services

- **API**: http://localhost:5000
- **Dashboard**: http://localhost:8000
- **Database**: localhost:5432

### 4. Test the System

```bash
# Health check
curl http://localhost:5000/health

# Make a prediction
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "source_port": 12345,
    "destination_port": 443,
    "protocol": "TCP",
    "packet_size": 1024,
    "payload_size": 800,
    "tcp_flags": "SYN"
  }'
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ PostgreSQL │  │  API Server │  │   Dashboard     │  │
│  │  Port:5432 │◄─┤  Port:5000  │◄─┤   Port:8000     │  │
│  │            │  │             │  │                 │  │
│  └────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
         ▲                ▲                    ▲
         │                │                    │
      Database       REST API            Web Interface
```

## Services

### 1. PostgreSQL Database (`postgres`)
- **Image**: postgres:15-alpine
- **Port**: 5432
- **Purpose**: Stores threat data, predictions, and metrics
- **Credentials**: 
  - User: cybersec_user
  - Password: Set via `DB_PASSWORD` env var (default: changeme123)
  - Database: cyber_threat_db

### 2. API Service (`api`)
- **Port**: 5000
- **Purpose**: REST API for threat prediction
- **Endpoints**:
  - `/health` - Health check
  - `/api/v1/predict` - Single prediction
  - `/api/v1/predict/batch` - Batch predictions
  - `/api/v1/alerts` - Get alerts
  - `/api/v1/statistics` - Get statistics

### 3. Dashboard Service (`dashboard`)
- **Port**: 8000
- **Purpose**: Real-time monitoring dashboard
- **Features**:
  - Live threat feed
  - Active alerts
  - Statistics visualization
  - AI-generated summaries

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DB_PASSWORD=your_secure_password

# Model path (optional)
MODEL_PATH=/app/models/trained/RandomForest_*.pkl
```

### Custom Configuration

Edit `docker-compose.yml` to customize:
- Port mappings
- Resource limits
- Volume mounts
- Environment variables

## Advanced Usage

### Scale Services

```bash
# Scale API service to 3 instances
docker-compose up -d --scale api=3
```

### Use Custom Model

```bash
# Mount custom model directory
docker-compose run -v /path/to/models:/app/models api python api/app.py --model /app/models/my_model.pkl
```

### Database Management

```bash
# Access database
docker-compose exec postgres psql -U cybersec_user -d cyber_threat_db

# Backup database
docker-compose exec postgres pg_dump -U cybersec_user cyber_threat_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U cybersec_user cyber_threat_db < backup.sql
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f dashboard
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 api
```

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Stop specific service
docker-compose stop api
```

## Production Deployment

### Security Hardening

1. **Change default passwords**
```bash
export DB_PASSWORD=$(openssl rand -base64 32)
```

2. **Use secrets management**
```yaml
# docker-compose.yml
secrets:
  db_password:
    external: true
```

3. **Enable TLS/SSL**
```yaml
# Add nginx reverse proxy with SSL
nginx:
  image: nginx:alpine
  ports:
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./certs:/etc/nginx/certs
```

### Resource Limits

```yaml
# docker-compose.yml
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

### Health Monitoring

```bash
# Check health status
docker-compose ps

# Restart unhealthy services
docker-compose restart api
```

### Logging

```yaml
# docker-compose.yml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs api

# Inspect container
docker inspect cybersec_api

# Check network
docker network inspect cyber_threat_network
```

### Database connection issues

```bash
# Test database connectivity
docker-compose exec api python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://cybersec_user:changeme123@postgres:5432/cyber_threat_db'); print(engine.connect())"
```

### Model not loading

```bash
# Check model files exist
docker-compose exec api ls -la /app/models/trained/

# Train models if missing
docker-compose exec api python scripts/train_models.py
```

### Port already in use

```bash
# Find process using port
lsof -i :5000

# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Map host 5001 to container 5000
```

## Monitoring

### Prometheus Integration

```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### Grafana Dashboard

```yaml
grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  depends_on:
    - prometheus
```

## Backup and Recovery

### Automated Backups

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U cybersec_user cyber_threat_db > backup_$DATE.sql
```

### Model Version Control

```bash
# Tag and save model versions
docker-compose exec api python -c "
from datetime import datetime
import shutil
shutil.copy('models/trained/best_model.pkl', f'models/trained/model_{datetime.now().strftime(\"%Y%m%d\")}.pkl')
"
```

## Updates and Maintenance

### Update Services

```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build

# Verify update
docker-compose ps
```

### Cleanup

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Complete cleanup
docker system prune -a --volumes
```

## Performance Optimization

### Database Tuning

```yaml
# docker-compose.yml
postgres:
  environment:
    POSTGRES_SHARED_BUFFERS: 256MB
    POSTGRES_MAX_CONNECTIONS: 100
```

### API Performance

```yaml
# Use gunicorn for production
api:
  command: gunicorn -w 4 -b 0.0.0.0:5000 api.app:app
```

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review documentation in `docs/`
- Open issue on GitHub

## License

MIT License - see LICENSE file
