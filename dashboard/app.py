"""
Real-time dashboard for threat monitoring and visualization.
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prediction.predictor import ThreatPredictor, RealTimeThreatMonitor
from src.ai_agent.summarizer import ThreatSummaryAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize services
predictor = None
monitor = None
ai_agent = None


def initialize_dashboard(model_path: str = None):
    """
    Initialize the dashboard services.
    
    Args:
        model_path: Path to trained model
    """
    global predictor, monitor, ai_agent
    
    try:
        predictor = ThreatPredictor(model_path=model_path)
        monitor = RealTimeThreatMonitor(predictor)
        ai_agent = ThreatSummaryAgent()
        logger.info("Dashboard initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing dashboard: {e}")


@app.route('/')
def index():
    """Render main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/dashboard/status')
def get_dashboard_status():
    """Get overall system status."""
    if monitor is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    stats = monitor.get_threat_statistics()
    alerts = monitor.get_active_alerts(limit=5)
    
    # Calculate system health
    threat_rate = float(stats.get('threat_rate', 0))
    health_status = 'healthy'
    
    if threat_rate > 0.5:
        health_status = 'critical'
    elif threat_rate > 0.2:
        health_status = 'warning'
    
    return jsonify({
        'status': health_status,
        'timestamp': datetime.now().isoformat(),
        'statistics': stats,
        'recent_alerts': alerts,
        'model_loaded': predictor is not None and predictor.model is not None
    })


@app.route('/api/dashboard/threats/live')
def get_live_threats():
    """Get live threat feed."""
    if monitor is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    # Get recent threats from history
    recent_threats = [
        event for event in monitor.threat_history[-20:]
        if event.get('is_threat', False)
    ]
    
    return jsonify({
        'threats': recent_threats,
        'count': len(recent_threats),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/dashboard/alerts')
def get_dashboard_alerts():
    """Get active alerts with AI summaries."""
    if monitor is None or ai_agent is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    limit = request.args.get('limit', 10, type=int)
    alerts = monitor.get_active_alerts(limit)
    
    # Generate AI summaries for alerts
    enriched_alerts = []
    for alert in alerts:
        # Find corresponding threat in history
        threat_data = next(
            (t for t in monitor.threat_history if t.get('timestamp') == alert.get('timestamp')),
            None
        )
        
        if threat_data:
            summary = ai_agent.analyze_and_summarize(threat_data)
            enriched_alerts.append({
                'alert': alert,
                'ai_summary': summary.get('ai_summary', {})
            })
        else:
            enriched_alerts.append({'alert': alert, 'ai_summary': {}})
    
    return jsonify({
        'alerts': enriched_alerts,
        'count': len(enriched_alerts),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/dashboard/report')
def generate_dashboard_report():
    """Generate comprehensive threat intelligence report."""
    if ai_agent is None or monitor is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    # Generate report from recent history
    report = ai_agent.generate_report(
        predictions=monitor.threat_history,
        include_history=True
    )
    
    return jsonify(report)


@app.route('/api/dashboard/statistics')
def get_detailed_statistics():
    """Get detailed statistics with breakdown."""
    if monitor is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    stats = monitor.get_threat_statistics()
    
    # Add additional metrics
    threat_history = monitor.threat_history
    
    # Calculate hourly threat rate
    if threat_history:
        threats = [t for t in threat_history if t.get('is_threat', False)]
        hourly_threat_count = len([t for t in threats])
        
        stats['hourly_metrics'] = {
            'total_analyzed': len(threat_history),
            'threats_detected': len(threats),
            'benign_traffic': len(threat_history) - len(threats)
        }
    
    return jsonify(stats)


@app.route('/api/dashboard/predict', methods=['POST'])
def predict_and_display():
    """
    Make a prediction and return with AI summary.
    For testing the dashboard with manual input.
    """
    if predictor is None or ai_agent is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Make prediction
        result = predictor.predict_single(data)
        
        # Process through monitor
        monitor.process_traffic(data)
        
        # Generate AI summary
        analysis = ai_agent.analyze_and_summarize(result)
        
        return jsonify(analysis), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/clear', methods=['POST'])
def clear_dashboard_data():
    """Clear all dashboard data (alerts, history)."""
    if monitor is None or ai_agent is None:
        return jsonify({'error': 'System not initialized'}), 503
    
    try:
        monitor.clear_alerts()
        monitor.threat_history = []
        ai_agent.clear_history()
        
        return jsonify({'message': 'Dashboard data cleared successfully'}), 200
    
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'cybersecurity-dashboard',
        'model_loaded': predictor is not None and predictor.model is not None,
        'ai_agent_active': ai_agent is not None
    }), 200


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Cybersecurity Threat Dashboard')
    parser.add_argument('--model', type=str, help='Path to trained model')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=8000, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Initialize dashboard
    if args.model:
        initialize_dashboard(args.model)
    else:
        logger.warning("No model specified. Dashboard started without loaded model.")
    
    # Run app
    logger.info(f"Starting dashboard on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)
