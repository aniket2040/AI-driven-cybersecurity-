# AI-Driven Cybersecurity Threat Prediction System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive AI/ML-based cybersecurity threat detection and prediction system that analyzes network traffic patterns to identify potential security threats in real-time. This project leverages multiple machine learning algorithms to detect and predict cyber threats from both static and live data sources.

## 🎯 Project Overview

This system is designed to:
- **Detect cyber threats** using advanced machine learning models
- **Analyze network traffic** patterns from both static datasets and live data streams
- **Predict security threats** before they materialize
- **Provide real-time monitoring** and alerting capabilities
- **Support multiple ML algorithms** for comparison and ensemble approaches

## 🏗️ Architecture

The system follows a modular architecture with the following components:

```
AI-driven-cybersecurity/
├── data/                      # Data storage
│   ├── raw/                   # Raw input data
│   ├── processed/             # Processed datasets
│   └── live/                  # Live data captures
├── database/                  # Database schemas and scripts
│   └── schema.sql             # PostgreSQL schema
├── src/                       # Source code
│   ├── data_collection/       # Data collection modules
│   ├── preprocessing/         # Data preprocessing
│   ├── feature_engineering/   # Feature engineering
│   ├── model_training/        # ML model training
│   ├── prediction/            # Prediction service
│   └── utils/                 # Utility functions
├── models/                    # Trained models
│   ├── trained/               # Saved model files
│   └── evaluation/            # Model evaluation results
├── api/                       # REST API
│   └── app.py                 # Flask API server
├── config/                    # Configuration files
├── scripts/                   # Training and utility scripts
├── notebooks/                 # Jupyter notebooks
├── tests/                     # Unit tests
└── docs/                      # Documentation

```

## 🚀 Features

### Data Processing
- **Static Data Loading**: Support for CSV, JSON, and other formats
- **Live Data Capture**: Real-time network traffic monitoring
- **Data Preprocessing**: Cleaning, normalization, and transformation
- **Feature Engineering**: Automated feature creation and selection

### Machine Learning Models
- **Random Forest**: Ensemble learning for robust predictions
- **Gradient Boosting**: Sequential model improvement
- **Neural Networks**: Deep learning for complex patterns
- **Support Vector Machines**: Effective for high-dimensional data

### Threat Detection
- **Multi-level Severity Classification**: HIGH, MEDIUM, LOW, INFO
- **Real-time Prediction**: Instant threat assessment
- **Batch Processing**: Efficient bulk analysis
- **Confidence Scoring**: Probability-based predictions

### API & Monitoring
- **RESTful API**: Easy integration with existing systems
- **Real-time Alerts**: Immediate notification of threats
- **Statistics Dashboard**: Comprehensive threat analytics
- **Configurable Thresholds**: Customizable severity levels

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12+ (optional, for database features)
- 4GB+ RAM recommended
- Linux/macOS/Windows

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aniket2040/AI-driven-cybersecurity-.git
   cd AI-driven-cybersecurity-
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database (optional)**
   ```bash
   # Create PostgreSQL database
   createdb cyber_threat_db
   
   # Initialize schema
   psql cyber_threat_db < database/schema.sql
   ```

5. **Configure environment variables**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/cyber_threat_db"
   ```

## 📚 Usage

### Training Models

Train all models using the sample dataset:

```bash
python scripts/train_models.py
```

This will:
- Load and preprocess data
- Engineer features
- Train multiple ML models
- Evaluate and compare models
- Save the best models to `models/trained/`

### Running the API Server

Start the threat detection API:

```bash
python api/app.py --model models/trained/RandomForest_XXXXXX.pkl --host 0.0.0.0 --port 5000
```

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Single Prediction
```bash
POST /api/v1/predict
Content-Type: application/json

{
  "source_ip": "192.168.1.100",
  "destination_ip": "10.0.0.50",
  "source_port": 12345,
  "destination_port": 443,
  "protocol": "TCP",
  "packet_size": 1024,
  "payload_size": 800,
  "tcp_flags": "SYN"
}
```

#### Batch Predictions
```bash
POST /api/v1/predict/batch
Content-Type: application/json

{
  "data": [
    {"source_ip": "...", "destination_ip": "...", ...},
    {"source_ip": "...", "destination_ip": "...", ...}
  ]
}
```

#### Get Alerts
```bash
GET /api/v1/alerts?limit=10
```

#### Get Statistics
```bash
GET /api/v1/statistics
```

## 🔬 Model Performance

The system trains and compares multiple models:

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Random Forest | ~0.95 | ~0.94 | ~0.96 | ~0.95 |
| Gradient Boosting | ~0.93 | ~0.92 | ~0.95 | ~0.93 |
| Neural Network | ~0.91 | ~0.90 | ~0.92 | ~0.91 |

*Note: Performance metrics may vary based on the dataset*

## 📊 Database Schema

The system uses a comprehensive PostgreSQL schema with the following main tables:

- **threats**: Detected and classified threats
- **network_traffic**: Raw network traffic logs
- **predictions**: Model predictions with confidence scores
- **model_metrics**: Model performance tracking
- **attack_signatures**: Known attack patterns
- **alerts**: Security alerts and notifications

## 🛠️ Development

### Project Structure

- **src/data_collection**: Data ingestion from various sources
- **src/preprocessing**: Data cleaning and transformation
- **src/feature_engineering**: Feature creation and selection
- **src/model_training**: ML model training and evaluation
- **src/prediction**: Real-time prediction service
- **src/utils**: Database and utility functions

### Running Tests

```bash
pytest tests/ -v
```

## 📈 Model Research

The project explores various ML algorithms:

1. **Random Forest**: Best for interpretability and feature importance
2. **Gradient Boosting**: Excellent for imbalanced datasets
3. **Neural Networks**: Captures complex non-linear patterns
4. **SVM**: Effective for high-dimensional feature spaces

## 🔐 Security Considerations

- All database connections use parameterized queries
- API includes CORS protection
- Sensitive data should be encrypted at rest
- Rate limiting recommended for production deployment

## 📝 Configuration

Edit `config/config.yaml` to customize:
- Model hyperparameters
- Feature engineering settings
- Severity thresholds
- Database connections
- API settings

## 🤝 Contributing

This project was developed as part of an Infosys presentation on AI-driven cybersecurity.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Educational Use

This project is designed for educational and research purposes. It demonstrates:
- End-to-end ML pipeline development
- Real-time threat detection systems
- API design for ML services
- Database design for security applications
- Model comparison and selection

## 📞 Support

For questions or issues, please open an issue on the GitHub repository.

## 🙏 Acknowledgments

- Infosys for the project opportunity
- Open-source ML community
- Cybersecurity research community

---

**Note**: This is a demonstration project. For production use, additional security hardening, testing, and optimization are required. 
