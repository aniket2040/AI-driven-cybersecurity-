# Project Architecture

## System Overview

The AI-Driven Cybersecurity Threat Prediction System is built using a modular, scalable architecture that supports both batch and real-time threat detection.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Data Sources                                │
├─────────────────────────────────────────────────────────────────┤
│  Static Data (CSV/JSON)  │  Live Network Traffic  │  Databases  │
└──────────────┬───────────┴────────────┬───────────┴─────────────┘
               │                        │
               v                        v
┌─────────────────────────────────────────────────────────────────┐
│                   Data Collection Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  StaticDataLoader  │  LiveDataCollector  │  DatabaseConnector   │
└──────────────┬──────────────────────────┬──────────────────────┘
               │                          │
               v                          v
┌─────────────────────────────────────────────────────────────────┐
│                  Data Processing Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  Data Cleaning  │  Feature Engineering  │  Data Transformation  │
└──────────────┬──────────────────────────┬──────────────────────┘
               │                          │
               v                          v
┌─────────────────────────────────────────────────────────────────┐
│                    ML Model Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  Random Forest  │  Gradient Boost  │  Neural Net  │    SVM      │
└──────────────┬──────────────────────────┬──────────────────────┘
               │                          │
               v                          v
┌─────────────────────────────────────────────────────────────────┐
│                  Prediction Service                              │
├─────────────────────────────────────────────────────────────────┤
│  ThreatPredictor  │  RealTimeMonitor  │  AlertingSystem        │
└──────────────┬──────────────────────────┬──────────────────────┘
               │                          │
               v                          v
┌─────────────────────────────────────────────────────────────────┐
│                      API Layer                                   │
├─────────────────────────────────────────────────────────────────┤
│  REST API  │  WebSocket  │  Dashboard  │  Reporting             │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Collection Layer

**Purpose**: Ingests data from multiple sources
- **Static Data Loader**: Handles CSV, JSON, and other file formats
- **Live Data Collector**: Captures real-time network traffic
- **Database Connector**: Interfaces with PostgreSQL database

**Technologies**: Pandas, Scapy (for packet capture), SQLAlchemy

### 2. Data Processing Layer

**Purpose**: Prepares data for ML models

#### Preprocessing Module
- Data cleaning and validation
- Missing value imputation
- Duplicate removal
- Data type conversion

#### Feature Engineering Module
- Network-based features (port analysis, packet size ratios)
- Statistical features (rolling means, standard deviations)
- Temporal features (time of day, day of week)
- Categorical encoding

**Technologies**: Scikit-learn, NumPy, Pandas

### 3. ML Model Layer

**Purpose**: Trains and maintains multiple ML models

#### Supported Algorithms
1. **Random Forest**: Ensemble method for robust predictions
2. **Gradient Boosting**: Sequential improvement for accuracy
3. **Neural Networks**: Deep learning for complex patterns
4. **Support Vector Machines**: Effective for classification

#### Model Training Pipeline
```
Data → Split (Train/Test) → Scale → Train → Evaluate → Save
```

**Technologies**: Scikit-learn, TensorFlow/Keras, PyTorch

### 4. Prediction Service

**Purpose**: Provides real-time and batch predictions

#### Components
- **ThreatPredictor**: Core prediction logic
- **RealTimeMonitor**: Continuous monitoring service
- **AlertingSystem**: Generates and manages alerts

#### Severity Levels
- **HIGH**: Confidence ≥ 80%
- **MEDIUM**: Confidence ≥ 50%
- **LOW**: Confidence ≥ 30%
- **INFO**: Confidence < 30%

### 5. API Layer

**Purpose**: Exposes system functionality via REST API

#### Endpoints
- `/health`: Health check
- `/api/v1/predict`: Single prediction
- `/api/v1/predict/batch`: Batch predictions
- `/api/v1/monitor/traffic`: Real-time monitoring
- `/api/v1/alerts`: Alert management
- `/api/v1/statistics`: System statistics

**Technologies**: Flask, Flask-CORS

## Database Schema

### Key Tables

#### threats
Stores detected and classified threats
- Primary Key: threat_id
- Foreign Keys: None
- Indexes: timestamp, severity_level

#### network_traffic
Raw network traffic logs
- Primary Key: traffic_id
- Foreign Keys: None
- Indexes: timestamp, source_ip

#### predictions
Model predictions with confidence scores
- Primary Key: prediction_id
- Foreign Keys: traffic_id
- Indexes: model_name

#### model_metrics
Tracks model performance over time
- Primary Key: metric_id
- Foreign Keys: None
- Purpose: Model monitoring and comparison

## Data Flow

### Training Flow
```
1. Load data from sources
2. Engineer features
3. Preprocess and split data
4. Train multiple models
5. Evaluate and compare
6. Save best models
7. Log metrics to database
```

### Prediction Flow
```
1. Receive traffic data (API/Monitor)
2. Apply same preprocessing
3. Extract features
4. Run through trained model
5. Calculate confidence score
6. Determine severity level
7. Generate alert if needed
8. Return prediction result
```

## Scalability Considerations

### Horizontal Scaling
- API can be deployed behind load balancer
- Multiple prediction workers can process in parallel
- Database can be replicated for read operations

### Performance Optimization
- Model caching in memory
- Batch prediction for efficiency
- Feature pre-computation for common patterns
- Database indexing on frequently queried columns

## Security Architecture

### Data Security
- Parameterized SQL queries
- Input validation on all endpoints
- Rate limiting (recommended for production)

### Model Security
- Model versioning and audit trail
- Regular retraining with new data
- Anomaly detection on prediction patterns

### API Security
- CORS protection
- Authentication (to be implemented)
- HTTPS encryption (recommended)

## Deployment Architecture

### Development
```
Single machine with all components
├── Python application
├── PostgreSQL database
└── Local file storage
```

### Production (Recommended)
```
├── Load Balancer
├── API Servers (multiple instances)
├── Prediction Workers (multiple instances)
├── Database Cluster (primary + replicas)
├── Model Storage (S3/Azure Blob)
└── Monitoring & Logging (ELK/Prometheus)
```

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Language | Python 3.8+ |
| ML/AI | Scikit-learn, TensorFlow, Keras |
| API | Flask, Flask-CORS |
| Database | PostgreSQL, SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Network | Scapy (for packet capture) |
| Deployment | Docker (optional), Gunicorn |

## Extension Points

The architecture supports easy extension:
- **New Models**: Add to model_training module
- **New Features**: Extend feature_engineering module
- **New Data Sources**: Implement in data_collection
- **New API Endpoints**: Add to api/app.py

## Monitoring and Observability

### Metrics to Track
- Model prediction latency
- Prediction accuracy over time
- Alert generation rate
- API response times
- Database query performance

### Logging
- Structured logging with levels (INFO, WARNING, ERROR)
- Centralized log aggregation recommended
- Log rotation for production use

## Future Enhancements

1. **Real-time Learning**: Online learning capabilities
2. **Ensemble Models**: Combine multiple models for better accuracy
3. **Explainable AI**: Feature importance and SHAP values
4. **Auto-tuning**: Hyperparameter optimization
5. **Dashboard**: Web-based monitoring interface
6. **Integration**: SIEM system integration
