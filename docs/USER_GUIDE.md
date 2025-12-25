# User Guide - AI-Driven Cybersecurity Platform

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Dashboard Guide](#dashboard-guide)
4. [API Usage](#api-usage)
5. [AI Summarization](#ai-summarization)
6. [NATEM Agent](#natem-agent)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Introduction

The AI-Driven Cybersecurity Platform is a comprehensive threat detection and prediction system that uses machine learning to identify and analyze security threats in real-time.

### Key Components

- **ML Models**: Random Forest, Gradient Boosting, Neural Networks
- **AI Summarizer**: Natural language threat explanations
- **Real-time Dashboard**: Live monitoring and visualization
- **NATEM Agent**: Network Attack Threat Event Monitor
- **REST API**: Integration endpoints for external systems

## Getting Started

### Quick Start with Docker (Recommended)

1. **Prerequisites**
   - Docker Desktop or Docker Engine 20.10+
   - Docker Compose 1.29+
   - 4GB RAM available

2. **Installation**
   ```bash
   # Clone repository
   git clone https://github.com/aniket2040/AI-driven-cybersecurity-.git
   cd AI-driven-cybersecurity-
   
   # Set up environment
   cp .env.example .env
   
   # Start all services
   docker-compose up -d
   ```

3. **Verify Installation**
   ```bash
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

4. **Access Services**
   - Dashboard: http://localhost:8080
   - API: http://localhost:5000
   - API Health: http://localhost:5000/health

### Manual Installation

1. **Prerequisites**
   - Python 3.8+
   - PostgreSQL 12+ (optional)
   - pip package manager

2. **Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Train models
   python scripts/train_models.py
   ```

3. **Start Services**
   ```bash
   # Terminal 1: API Server
   python api/app.py --model models/trained/RandomForest_*.pkl
   
   # Terminal 2: Dashboard
   python dashboard/app.py
   
   # Terminal 3: NATEM Agent
   python scripts/natem_agent.py
   ```

## Dashboard Guide

### Overview

The dashboard provides real-time visualization of security events and threats.

### Dashboard Sections

#### 1. Summary Cards

**Total Events**: Number of network events analyzed in the last 24 hours

**Threats Detected**: Count and percentage of malicious traffic detected

**High Severity**: Number of critical threats requiring immediate action

**Detection Accuracy**: Current ML model performance metric

#### 2. Threat Activity Timeline

Real-time line chart showing:
- Threat count over time (red line)
- Benign traffic count (green line)
- Time-series trend analysis

**Usage**: Identify traffic patterns and threat spikes

#### 3. Severity Distribution

Doughnut chart showing distribution of threat severity levels:
- 🔴 High: Critical threats (immediate action)
- 🟡 Medium: Important threats (address soon)
- 🔵 Low: Minor threats (monitor)
- 🟢 Info: Informational only

#### 4. Active Alerts

Real-time feed of security alerts including:
- Severity level
- Alert message
- Source and destination IPs
- Timestamp

**Actions**:
- Click on alert for details
- Monitor high-severity alerts
- Review recommended actions

#### 5. AI Security Analysis

AI-generated summaries of security events with:
- Plain language threat descriptions
- Confidence scores
- Actionable recommendations
- Technical details

**Example**:
```
🚨 THREAT DETECTED: Port scanning activity detected originating from 
192.168.1.100 targeting 10.0.0.50 on SSH. Severity level is HIGH with 
95.3% confidence.

Recommendations:
→ IMMEDIATE: Block IP address at firewall
→ IMMEDIATE: Investigate all recent traffic from this source
→ Enable multi-factor authentication
```

#### 6. Protocol Distribution

Bar chart showing network traffic by protocol:
- TCP
- UDP
- ICMP
- HTTP/HTTPS

#### 7. Top Threat Sources & Targets

Lists of:
- Most active threat source IPs
- Most targeted destination IPs
- Connection counts

### Dashboard Features

#### Auto-Refresh

Dashboard updates automatically every 5 seconds with latest data.

#### Interactive Charts

- Hover over data points for details
- Click legend items to show/hide data
- Zoom and pan on charts

#### Alert Banner

Critical alerts appear at the top of the dashboard with:
- Red banner for HIGH severity
- Auto-dismiss after 10 seconds
- Manual dismiss option

## API Usage

### Authentication

Currently no authentication required (add for production).

### Endpoints

#### 1. Predict Single Threat

**Endpoint**: `POST /api/v1/predict`

**Request**:
```json
{
  "source_ip": "192.168.1.100",
  "destination_ip": "10.0.0.50",
  "source_port": 54321,
  "destination_port": 22,
  "protocol": "TCP",
  "packet_size": 64,
  "payload_size": 24,
  "tcp_flags": "SYN"
}
```

**Response**:
```json
{
  "is_threat": true,
  "confidence": 0.953,
  "severity": "HIGH",
  "timestamp": "2024-12-25T10:30:15.123456",
  "input_data": {...}
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"source_ip":"192.168.1.100","destination_ip":"10.0.0.50","source_port":54321,"destination_port":22,"protocol":"TCP","packet_size":64,"payload_size":24,"tcp_flags":"SYN"}'
```

#### 2. AI Summarization

**Endpoint**: `POST /api/v1/summarize`

**Request**: Same as predict endpoint

**Response**:
```json
{
  "summary": "🚨 THREAT DETECTED: Port scanning activity...",
  "severity_description": "CRITICAL - Immediate action required",
  "confidence_percentage": "95.3%",
  "recommendations": [
    "🔴 IMMEDIATE: Block IP address...",
    "🔴 IMMEDIATE: Investigate all recent traffic..."
  ],
  "threat_detected": true,
  "technical_details": {...}
}
```

#### 3. Batch Predictions

**Endpoint**: `POST /api/v1/predict/batch`

**Request**:
```json
{
  "data": [
    {"source_ip": "192.168.1.100", ...},
    {"source_ip": "192.168.1.101", ...}
  ]
}
```

**Response**:
```json
{
  "predictions": [...],
  "summary": {
    "total_analyzed": 2,
    "threat_count": 1,
    "threat_rate": 0.5
  }
}
```

#### 4. Get Alerts

**Endpoint**: `GET /api/v1/alerts?limit=10`

**Response**:
```json
{
  "alerts": [
    {
      "alert_id": 1,
      "severity": "HIGH",
      "confidence": 0.95,
      "source_ip": "192.168.1.100",
      "destination_ip": "10.0.0.50",
      "timestamp": "2024-12-25T10:30:15.123456",
      "message": "HIGH severity threat detected..."
    }
  ],
  "count": 1
}
```

#### 5. Get Statistics

**Endpoint**: `GET /api/v1/statistics`

**Response**:
```json
{
  "total_analyzed": 1000,
  "threat_count": 150,
  "benign_count": 850,
  "threat_rate": 0.15,
  "average_confidence": 0.87,
  "severity_distribution": {
    "HIGH": 20,
    "MEDIUM": 50,
    "LOW": 80,
    "INFO": 0
  }
}
```

## AI Summarization

### How It Works

The AI Summarization engine:

1. **Analyzes** threat prediction results
2. **Classifies** attack types based on patterns
3. **Generates** human-readable descriptions
4. **Provides** actionable recommendations

### Attack Type Detection

The system automatically identifies:

- **DDoS Attacks**: High volume, small packets
- **Port Scanning**: SYN/FIN flags on multiple ports
- **SQL Injection**: Database port targeting
- **Brute Force**: Repeated auth attempts
- **Malware**: Suspicious patterns
- **XSS/Web Attacks**: Large HTTP payloads

### Recommendation Engine

Recommendations are based on:

1. **Severity Level**: Urgency of response
2. **Attack Type**: Specific mitigation steps
3. **Confidence Score**: Verification needs
4. **Target Port**: Service-specific actions

### Example Summaries

**High Severity - Port Scan**:
```
🚨 THREAT DETECTED: Port scanning activity - attacker probing 
for open ports and services originating from 192.168.1.100 
targeting 10.0.0.50 on SSH. Severity level is HIGH with 95.3% 
confidence. Protocol: TCP.

Recommendations:
→ 🔴 IMMEDIATE: Block IP address 192.168.1.100 at firewall
→ 🔴 IMMEDIATE: Investigate all recent traffic from this source
→ 🔴 IMMEDIATE: Alert security team and escalate to SOC
→ Enable multi-factor authentication if not already active
```

**Low Severity - Benign Traffic**:
```
✅ NORMAL TRAFFIC: Connection from 192.168.1.50 to 10.0.0.20 
on HTTPS (Secure Web) using TCP protocol appears legitimate. 
The AI model classified this as benign traffic with 92.5% 
confidence.

Recommendations:
→ No immediate action required
→ Continue monitoring normal traffic patterns
```

## NATEM Agent

### Overview

NATEM (Network Attack Threat Event Monitor) is an agent that monitors network traffic and sends events to the API for analysis.

### Features

- Continuous network monitoring
- Real-time threat detection
- AI summary logging
- Statistical reporting

### Usage

#### Basic Usage

```bash
python scripts/natem_agent.py
```

#### With Options

```bash
python scripts/natem_agent.py \
  --api-url http://localhost:5000/api/v1 \
  --interval 2 \
  --duration 300
```

**Options**:
- `--api-url`: API endpoint URL (default: http://localhost:5000/api/v1)
- `--interval`: Monitoring interval in seconds (default: 2)
- `--duration`: Total duration in seconds (default: indefinite)

#### Docker Usage

```bash
docker-compose logs -f natem_agent
```

### Output

The agent logs:

**Normal Traffic**:
```
✅ Normal traffic from 192.168.1.50
```

**Threat Detected**:
```
🚨 THREAT DETECTED: Port scanning activity detected originating 
from 192.168.1.100 targeting 10.0.0.50 on SSH. Severity level 
is HIGH with 95.3% confidence.

Confidence: 95.3%
Recommendations:
  - IMMEDIATE: Block IP address at firewall
  - IMMEDIATE: Investigate all recent traffic
  - Enable multi-factor authentication
```

**Periodic Statistics**:
```
📊 Stats: 100 events analyzed, 15 threats detected (15.0%)
```

## Troubleshooting

### Common Issues

#### Dashboard Shows No Data

**Problem**: Dashboard displays "No data available"

**Solutions**:
1. Verify API is running: `curl http://localhost:5000/health`
2. Check NATEM agent is sending data: `docker logs natem_agent`
3. Review dashboard logs: `docker logs cyber_dashboard`
4. Check browser console for JavaScript errors

#### API Returns 503 Error

**Problem**: API returns "Model not loaded"

**Solutions**:
1. Train a model: `python scripts/train_models.py`
2. Verify model file exists: `ls models/trained/`
3. Specify model path: `python api/app.py --model models/trained/RandomForest_*.pkl`

#### Database Connection Failed

**Problem**: Cannot connect to PostgreSQL

**Solutions**:
1. Verify PostgreSQL is running: `docker ps | grep postgres`
2. Check database credentials in `.env`
3. Wait for database initialization: `docker logs cyber_threat_db`
4. Test connection: `docker exec cyber_threat_db pg_isready -U cyberuser`

#### Docker Compose Fails

**Problem**: Services won't start

**Solutions**:
1. Check port availability: `lsof -i :5000,8080,5432`
2. Review logs: `docker-compose logs`
3. Rebuild containers: `docker-compose build --no-cache`
4. Check disk space: `docker system df`

## Best Practices

### Security

1. **Change Default Passwords**: Update database passwords in `.env`
2. **Use HTTPS**: Deploy behind reverse proxy with SSL/TLS
3. **Enable Authentication**: Add API authentication for production
4. **Regular Updates**: Keep dependencies up to date
5. **Monitor Logs**: Review logs regularly for anomalies

### Performance

1. **Resource Allocation**: Ensure adequate RAM (4GB+)
2. **Model Selection**: Use Random Forest for best balance
3. **Database Optimization**: Regular VACUUM and index maintenance
4. **Caching**: Implement Redis for frequently accessed data
5. **Load Balancing**: Use multiple API instances for high traffic

### Monitoring

1. **Health Checks**: Monitor `/health` endpoints
2. **Alert Thresholds**: Configure appropriate severity levels
3. **Log Aggregation**: Use ELK stack or similar
4. **Metrics Collection**: Track prediction latency and accuracy
5. **Regular Testing**: Verify detection capabilities

### Model Maintenance

1. **Regular Retraining**: Weekly or monthly with new data
2. **Performance Monitoring**: Track accuracy drift
3. **A/B Testing**: Test new models on subset of traffic
4. **Backup Models**: Keep previous versions for rollback
5. **Data Quality**: Ensure training data is clean and labeled

### Dashboard Usage

1. **Monitor High Severity**: Prioritize RED alerts
2. **Investigate Patterns**: Look for unusual spikes
3. **Review AI Summaries**: Understand threat context
4. **Track Trends**: Use timeline for pattern analysis
5. **Regular Reviews**: Check dashboard daily

## Support

### Resources

- **Documentation**: `/docs` directory
- **API Reference**: http://localhost:5000/docs (if enabled)
- **GitHub Issues**: https://github.com/aniket2040/AI-driven-cybersecurity-/issues

### Getting Help

1. Check this guide first
2. Review documentation in `/docs`
3. Check existing GitHub issues
4. Open new issue with:
   - Problem description
   - Steps to reproduce
   - Error messages/logs
   - Environment details

## Glossary

**NATEM**: Network Attack Threat Event Monitor

**Threat**: Potentially malicious network activity

**Confidence Score**: Model's certainty in prediction (0-100%)

**Severity Level**: Priority classification (HIGH/MEDIUM/LOW/INFO)

**False Positive**: Benign traffic classified as threat

**False Negative**: Threat classified as benign

**ROC-AUC**: Model performance metric (0-1)

**F1-Score**: Harmonic mean of precision and recall

---

**Version**: 1.0  
**Last Updated**: December 2024
