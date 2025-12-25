# AI Features Quick Start Guide

## Overview

This guide explains how to use the new AI-powered features for security event summarization and threat intelligence reporting.

## Features

### 1. AI Security Event Summarizer

Converts complex threat predictions into simple, actionable summaries.

#### Key Capabilities
- **Human-readable explanations** of threats
- **Attack type inference** (SQL injection, SSH brute force, DDoS, etc.)
- **Severity-based recommendations**
- **Confidence scoring interpretation**

#### Example Usage

```python
from src.ai_agent.summarizer import SecurityEventSummarizer

summarizer = SecurityEventSummarizer()

# Sample threat prediction
prediction = {
    'is_threat': True,
    'confidence': 0.85,
    'severity': 'HIGH',
    'timestamp': '2024-12-25T12:00:00',
    'input_data': {
        'source_ip': '192.168.1.100',
        'destination_ip': '10.0.0.50',
        'destination_port': 22,
        'protocol': 'TCP'
    }
}

# Generate summary
summary = summarizer.summarize_single_event(prediction)

print(summary['title'])           # "🚨 Security Threat Detected - HIGH Severity"
print(summary['description'])      # Human-readable description
print(summary['attack_type'])      # "Potential SSH Brute Force"
print(summary['recommendations'])  # List of action items
print(summary['explanation'])      # Why it's a threat
```

### 2. Threat Summary Agent

High-level interface for threat intelligence reporting.

#### Key Capabilities
- **Event history tracking**
- **Comprehensive report generation**
- **Executive summaries**
- **Historical trend analysis**

#### Example Usage

```python
from src.ai_agent.summarizer import ThreatSummaryAgent

agent = ThreatSummaryAgent()

# Analyze single event
result = agent.analyze_and_summarize(prediction)
print(result['ai_summary']['title'])

# Generate comprehensive report
report = agent.generate_report(include_history=True)
print(report['summary']['executive_summary'])
print(report['recommendations'])
```

## API Endpoints

### Predict with AI Summary

**Endpoint:** `POST /api/v1/predict/summarize`

Make a prediction and get an AI-generated summary:

```bash
curl -X POST http://localhost:5000/api/v1/predict/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "source_port": 12345,
    "destination_port": 22,
    "protocol": "TCP",
    "packet_size": 1024,
    "payload_size": 800
  }'
```

**Response:**
```json
{
  "original_prediction": {
    "is_threat": true,
    "confidence": 0.85,
    "severity": "HIGH"
  },
  "ai_summary": {
    "title": "🚨 Security Threat Detected - HIGH Severity",
    "description": "A potential cyber threat has been detected...",
    "attack_type": "Potential SSH Brute Force",
    "recommendations": [
      "🔴 IMMEDIATELY block traffic from 192.168.1.100",
      "🔴 Isolate affected system...",
      "..."
    ],
    "explanation": "Our machine learning model detected..."
  }
}
```

### Generate Threat Intelligence Report

**Endpoint:** `GET /api/v1/report/generate`

Generate a comprehensive threat intelligence report:

```bash
curl http://localhost:5000/api/v1/report/generate?include_history=true
```

**Response:**
```json
{
  "report_type": "Threat Intelligence Summary",
  "generated_at": "2024-12-25T12:00:00",
  "summary": {
    "executive_summary": "🚨 CRITICAL ALERT...",
    "total_events": 100,
    "threat_count": 15,
    "threat_rate": "15.0%",
    "severity_breakdown": {
      "HIGH": 3,
      "MEDIUM": 7,
      "LOW": 5,
      "INFO": 85
    }
  },
  "recommendations": [
    "🔴 CRITICAL: Execute incident response plan immediately",
    "..."
  ]
}
```

## Dashboard Integration

The real-time dashboard automatically uses the AI agent to:
- Display AI-summarized alerts
- Show attack type classifications
- Present actionable recommendations
- Generate executive reports

Access the dashboard at: `http://localhost:8000`

## Running the Demo

See the AI features in action:

```bash
python scripts/demo_ai_features.py
```

This will demonstrate:
- Single event summarization
- Batch analysis
- Report generation
- Attack type inference

## Attack Type Detection

The AI agent can automatically identify:

| Port | Attack Type |
|------|-------------|
| 22 | SSH Brute Force |
| 80, 443 | Web Attack (XSS/Injection) |
| 3306, 5432 | SQL Injection |
| 3389 | RDP Attack |
| Large packets | DDoS/Flooding |
| SYN flags + high ports | Port Scan |

## Severity Levels

### HIGH (Critical)
- **Confidence:** ≥80%
- **Urgency:** Immediate action required
- **Actions:** Block source, isolate system, alert team

### MEDIUM (Warning)
- **Confidence:** ≥50%
- **Urgency:** Action required soon
- **Actions:** Monitor closely, consider rate-limiting

### LOW (Advisory)
- **Confidence:** ≥30%
- **Urgency:** Monitor situation
- **Actions:** Log and analyze patterns

### INFO (Informational)
- **Confidence:** <30%
- **Urgency:** No immediate action needed
- **Actions:** Keep for historical analysis

## Customization

### Custom Attack Signatures

Extend the attack type detection:

```python
from src.ai_agent.summarizer import SecurityEventSummarizer

class CustomSummarizer(SecurityEventSummarizer):
    def _infer_attack_type(self, data):
        # Add custom logic
        if data.get('destination_port') == 8080:
            return 'Custom Web Service Attack'
        return super()._infer_attack_type(data)
```

### Custom Recommendations

Override recommendation generation:

```python
def custom_recommendations(self, is_threat, severity, data):
    if severity == 'HIGH':
        return [
            "Custom action 1",
            "Custom action 2"
        ]
    return super()._generate_recommendations(is_threat, severity, data)
```

## Best Practices

1. **Review AI Summaries:** Always verify AI-generated summaries with actual network logs
2. **Update Training Data:** Retrain models with new attack patterns regularly
3. **Monitor False Positives:** Track and adjust thresholds based on your environment
4. **Archive Reports:** Save threat intelligence reports for compliance
5. **Integrate with SIEM:** Export summaries to your security monitoring platform

## Testing

Run AI agent tests:

```bash
pytest tests/test_ai_agent.py -v
```

## Troubleshooting

### AI Agent Not Initialized

**Error:** `AI agent not initialized`

**Solution:** Ensure the agent is initialized in your application:

```python
from src.ai_agent.summarizer import ThreatSummaryAgent
ai_agent = ThreatSummaryAgent()
```

### Empty Reports

**Error:** Reports show "NO_DATA"

**Solution:** Process some events first:

```python
agent = ThreatSummaryAgent()
agent.analyze_and_summarize(prediction)
report = agent.generate_report()
```

## Support

For issues:
- Check logs: Look for AI agent errors in application logs
- Run demo: `python scripts/demo_ai_features.py`
- Run tests: `pytest tests/test_ai_agent.py -v`
- Review docs: `docs/ARCHITECTURE.md`

## Next Steps

1. ✅ Train ML models: `python scripts/train_models.py`
2. ✅ Start API with AI: `python api/app.py --model <path>`
3. ✅ Launch dashboard: `python dashboard/app.py --model <path>`
4. ✅ Test AI features: `python scripts/demo_ai_features.py`
5. ✅ Deploy with Docker: `docker-compose up -d`

---

**Version:** 1.0  
**Last Updated:** December 25, 2024
