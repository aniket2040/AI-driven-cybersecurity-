"""
REST API for cybersecurity threat prediction service.
Provides endpoints for real-time threat detection and model management.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prediction.predictor import ThreatPredictor, RealTimeThreatMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize predictor and monitor
predictor = None
monitor = None


def initialize_service(model_path: str = None):
    """
    Initialize the prediction service.
    
    Args:
        model_path: Path to trained model
    """
    global predictor, monitor
    
    try:
        predictor = ThreatPredictor(model_path=model_path)
        monitor = RealTimeThreatMonitor(predictor)
        logger.info("Threat prediction service initialized")
    except Exception as e:
        logger.error(f"Error initializing service: {e}")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'cybersecurity-threat-detection',
        'model_loaded': predictor is not None and predictor.model is not None
    }), 200


@app.route('/api/v1/predict', methods=['POST'])
def predict_threat():
    """
    Predict if network traffic is a threat.
    
    Expected JSON payload:
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
    """
    if predictor is None or predictor.model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Make prediction
        result = predictor.predict_single(data)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict threats for multiple traffic entries.
    
    Expected JSON payload:
    {
        "data": [
            {"source_ip": "...", "destination_ip": "...", ...},
            {"source_ip": "...", "destination_ip": "...", ...}
        ]
    }
    """
    if predictor is None or predictor.model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    try:
        payload = request.get_json()
        
        if not payload or 'data' not in payload:
            return jsonify({'error': 'Invalid payload format'}), 400
        
        data_list = payload['data']
        
        if not isinstance(data_list, list):
            return jsonify({'error': 'Data must be a list'}), 400
        
        # Make batch predictions
        results = predictor.predict_batch(data_list)
        
        # Analyze results
        summary = predictor.analyze_threats(results)
        
        return jsonify({
            'predictions': results,
            'summary': summary
        }), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/monitor/traffic', methods=['POST'])
def monitor_traffic():
    """
    Monitor incoming traffic and generate alerts if needed.
    
    Expected JSON payload: same as /predict endpoint
    """
    if monitor is None:
        return jsonify({'error': 'Monitor not initialized'}), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process traffic through monitor
        result = monitor.process_traffic(data)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Monitor error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts."""
    if monitor is None:
        return jsonify({'error': 'Monitor not initialized'}), 503
    
    try:
        limit = request.args.get('limit', 10, type=int)
        alerts = monitor.get_active_alerts(limit)
        
        return jsonify({
            'alerts': alerts,
            'count': len(alerts)
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/alerts/clear', methods=['POST'])
def clear_alerts():
    """Clear all alerts."""
    if monitor is None:
        return jsonify({'error': 'Monitor not initialized'}), 503
    
    try:
        monitor.clear_alerts()
        return jsonify({'message': 'Alerts cleared successfully'}), 200
    
    except Exception as e:
        logger.error(f"Error clearing alerts: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/statistics', methods=['GET'])
def get_statistics():
    """Get threat detection statistics."""
    if monitor is None:
        return jsonify({'error': 'Monitor not initialized'}), 503
    
    try:
        stats = monitor.get_threat_statistics()
        return jsonify(stats), 200
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/config/thresholds', methods=['POST'])
def update_thresholds():
    """
    Update severity thresholds.
    
    Expected JSON payload:
    {
        "high": 0.8,
        "medium": 0.5,
        "low": 0.3
    }
    """
    if predictor is None:
        return jsonify({'error': 'Predictor not initialized'}), 503
    
    try:
        data = request.get_json()
        
        high = data.get('high', 0.8)
        medium = data.get('medium', 0.5)
        low = data.get('low', 0.3)
        
        predictor.set_thresholds(high, medium, low)
        
        return jsonify({
            'message': 'Thresholds updated successfully',
            'thresholds': {'high': high, 'medium': medium, 'low': low}
        }), 200
    
    except Exception as e:
        logger.error(f"Error updating thresholds: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Cybersecurity Threat Detection API')
    parser.add_argument('--model', type=str, help='Path to trained model')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Initialize service
    if args.model:
        initialize_service(args.model)
    else:
        logger.warning("No model specified. Service started without loaded model.")
    
    # Run app
    app.run(host=args.host, port=args.port, debug=args.debug)
