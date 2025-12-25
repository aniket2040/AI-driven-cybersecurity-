"""
Dashboard server for AI-Driven Cybersecurity Platform.
Provides a real-time web interface for monitoring security events.
"""
from flask import Flask, render_template
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')


@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy', 'service': 'dashboard'}, 200


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Cybersecurity Dashboard Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=8080, help='Port number')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"Starting dashboard server on http://{args.host}:{args.port}")
    print("Make sure the API server is running on http://localhost:5000")
    
    app.run(host=args.host, port=args.port, debug=args.debug)
