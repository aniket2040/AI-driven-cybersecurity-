# Quick Start Guide

This guide will help you get started with the AI-Driven Cybersecurity Threat Prediction System in just a few minutes.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip package manager
- ✅ At least 4GB RAM
- ✅ 1GB free disk space

Check your Python version:
```bash
python --version
```

## Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/aniket2040/AI-driven-cybersecurity-.git
cd AI-driven-cybersecurity-

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Train Your First Model (5 minutes)

The training script will automatically:
- Generate sample threat data
- Engineer features
- Train multiple ML models
- Evaluate and compare models
- Save the best models

```bash
python scripts/train_models.py
```

Expected output:
```
[1/6] Loading data...
Loaded dataset with shape: (1000, 10)

[2/6] Engineering features...
Feature engineering complete. Shape: (1000, 25)

[3/6] Preprocessing data...
Train set: (800, 24), Test set: (200, 24)

[4/6] Training models...
Training RandomForest model...
Training GradientBoosting model...
Training NeuralNetwork model...

[5/6] Evaluating models...
RandomForest Accuracy: 0.9500
GradientBoosting Accuracy: 0.9300
NeuralNetwork Accuracy: 0.9100

[6/6] Saving models...
Best model: RandomForest with F1-score: 0.9500
```

## Step 3: Test Predictions (2 minutes)

Create a test script `test_prediction.py`:

```python
import sys
sys.path.insert(0, 'src')

from prediction.predictor import ThreatPredictor
import glob

# Load the most recent model
model_files = glob.glob('models/trained/RandomForest*.pkl')
if not model_files:
    print("No trained model found! Run training first.")
    sys.exit(1)

latest_model = max(model_files, key=lambda x: x.split('_')[-1])
print(f"Loading model: {latest_model}")

# Initialize predictor
predictor = ThreatPredictor(model_path=latest_model)

# Test with sample data
test_data = {
    'source_ip': '192.168.1.100',
    'destination_ip': '10.0.0.50',
    'source_port': 54321,
    'destination_port': 443,
    'protocol': 'TCP',
    'packet_size': 1024,
    'payload_size': 800,
    'tcp_flags': 'SYN',
    'is_privileged_src_port': 0,
    'is_privileged_dst_port': 0,
    'is_common_port': 1,
    'header_size': 224,
    'payload_ratio': 0.78,
    'is_large_packet': 1,
    'is_tcp': 1,
    'is_udp': 0,
    'is_icmp': 0
}

# Make prediction
result = predictor.predict_single(test_data)

print("\n" + "="*50)
print("PREDICTION RESULT")
print("="*50)
print(f"Is Threat: {result['is_threat']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Severity: {result['severity']}")
print("="*50)
```

Run it:
```bash
python test_prediction.py
```

## Step 4: Start the API Server (1 minute)

Find your trained model and start the API:

```bash
# List available models
ls -lh models/trained/

# Start API with your model
python api/app.py --model models/trained/RandomForest_*.pkl --port 5000
```

The API will be available at `http://localhost:5000`

## Step 5: Test the API (2 minutes)

### Health Check
```bash
curl http://localhost:5000/health
```

### Make a Prediction
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50",
    "source_port": 54321,
    "destination_port": 443,
    "protocol": "TCP",
    "packet_size": 1024,
    "payload_size": 800,
    "tcp_flags": "SYN",
    "is_privileged_src_port": 0,
    "is_privileged_dst_port": 0,
    "is_common_port": 1,
    "header_size": 224,
    "payload_ratio": 0.78,
    "is_large_packet": 1,
    "is_tcp": 1,
    "is_udp": 0,
    "is_icmp": 0
  }'
```

Expected response:
```json
{
  "is_threat": true,
  "confidence": 0.85,
  "severity": "HIGH",
  "timestamp": "2024-01-01T12:00:00",
  "input_data": {...}
}
```

## Common Tasks

### View Model Performance

After training, check the comparison:
```bash
grep "MODEL COMPARISON" -A 10 <training_output>
```

### Update Severity Thresholds

```bash
curl -X POST http://localhost:5000/api/v1/config/thresholds \
  -H "Content-Type: application/json" \
  -d '{"high": 0.9, "medium": 0.6, "low": 0.3}'
```

### Get Statistics

```bash
curl http://localhost:5000/api/v1/statistics
```

## Understanding the Output

### Threat Severity Levels

| Level | Confidence Range | Action Required |
|-------|-----------------|-----------------|
| HIGH | ≥ 80% | Immediate investigation |
| MEDIUM | 50-79% | Monitor closely |
| LOW | 30-49% | Log for analysis |
| INFO | < 30% | Informational only |

### Model Metrics

- **Accuracy**: Overall correctness of predictions
- **Precision**: Accuracy of threat predictions (fewer false positives)
- **Recall**: Ability to detect all threats (fewer false negatives)
- **F1-Score**: Balance between precision and recall
- **ROC-AUC**: Overall model discrimination ability

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Make sure you're in the virtual environment
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: No trained model found
**Solution**: Run the training script first
```bash
python scripts/train_models.py
```

### Issue: API not starting
**Solution**: Check if port is already in use
```bash
# Try a different port
python api/app.py --model <model_path> --port 5001
```

### Issue: Low model accuracy
**Solution**: 
- Use real cybersecurity datasets (e.g., NSL-KDD, CICIDS)
- Increase training data size
- Tune hyperparameters in `config/config.yaml`

## Next Steps

Now that you have the system running, you can:

1. **Use Real Data**: Replace sample data with actual network traffic
2. **Customize Features**: Modify feature engineering for your use case
3. **Tune Models**: Adjust hyperparameters in `config/config.yaml`
4. **Add Models**: Implement additional ML algorithms
5. **Deploy**: Set up production environment with database
6. **Monitor**: Track model performance over time

## Useful Commands

```bash
# Activate environment
source venv/bin/activate

# Train models
python scripts/train_models.py

# Run API
python api/app.py --model models/trained/<model>.pkl

# Run tests (if available)
pytest tests/ -v

# Check code style
flake8 src/

# View logs
tail -f logs/cybersecurity.log
```

## Getting Help

- Check the [Architecture Documentation](docs/ARCHITECTURE.md)
- Review the main [README](README.md)
- Open an issue on GitHub

## Example Project Timeline

For a team presentation (e.g., to Infosys):

**Week 1**: Setup and familiarization
- Day 1-2: Environment setup and dependency installation
- Day 3-4: Understanding the codebase and architecture
- Day 5: Training models with sample data

**Week 2**: Customization and improvement
- Day 1-2: Integrate real cybersecurity datasets
- Day 3-4: Feature engineering and model tuning
- Day 5: API testing and integration

**Week 3**: Analysis and presentation
- Day 1-2: Model evaluation and comparison
- Day 3-4: Prepare presentation materials
- Day 5: Practice and final presentation

## Quick Reference

### File Structure
```
├── src/               # Source code
├── models/trained/    # Saved models
├── scripts/           # Training scripts
├── api/              # REST API
├── config/           # Configuration
└── docs/             # Documentation
```

### Key Files
- `scripts/train_models.py` - Main training script
- `api/app.py` - REST API server
- `config/config.yaml` - Configuration
- `requirements.txt` - Dependencies

Happy threat hunting! 🔒🛡️
