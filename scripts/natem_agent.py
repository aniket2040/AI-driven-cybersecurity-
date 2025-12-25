"""
NATEM Agent (Network Attack Threat Event Monitor)
Monitors network traffic and security events, feeding them to the prediction system.
"""
import sys
import os
import time
import logging
import requests
import json
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NATEMAgent:
    """
    Network Attack Threat Event Monitor Agent.
    
    This agent simulates network traffic monitoring and feeds events
    to the threat prediction API for analysis.
    """
    
    def __init__(self, api_url: str = 'http://localhost:5000/api/v1'):
        """
        Initialize NATEM agent.
        
        Args:
            api_url: Base URL of the threat prediction API
        """
        self.api_url = api_url
        self.running = False
        logger.info(f"NATEM Agent initialized with API URL: {api_url}")
    
    def generate_sample_traffic(self) -> Dict[str, Any]:
        """
        Generate sample network traffic data for monitoring.
        
        In production, this would capture real network packets using tools like Scapy.
        For demonstration, we generate synthetic traffic patterns.
        """
        import random
        
        # Define common patterns
        protocols = ['TCP', 'UDP', 'ICMP']
        
        # Benign traffic patterns (70% of traffic)
        benign_patterns = [
            {'source_port': 443, 'destination_port': random.randint(49152, 65535), 'protocol': 'TCP', 'packet_size': random.randint(500, 1500)},
            {'source_port': 80, 'destination_port': random.randint(49152, 65535), 'protocol': 'TCP', 'packet_size': random.randint(400, 1200)},
            {'source_port': 53, 'destination_port': random.randint(49152, 65535), 'protocol': 'UDP', 'packet_size': random.randint(50, 512)},
        ]
        
        # Malicious traffic patterns (30% of traffic)
        malicious_patterns = [
            {'source_port': random.randint(1024, 49151), 'destination_port': 22, 'protocol': 'TCP', 'packet_size': 64, 'tcp_flags': 'SYN'},  # Port scan
            {'source_port': random.randint(1024, 49151), 'destination_port': 3306, 'protocol': 'TCP', 'packet_size': 2048},  # SQL injection
            {'source_port': random.randint(1024, 49151), 'destination_port': 445, 'protocol': 'TCP', 'packet_size': 512},  # SMB exploit
            {'source_port': random.randint(1024, 49151), 'destination_port': 80, 'protocol': 'TCP', 'packet_size': 8192},  # Large HTTP (possible XSS)
        ]
        
        # 70% benign, 30% malicious
        if random.random() < 0.7:
            pattern = random.choice(benign_patterns)
        else:
            pattern = random.choice(malicious_patterns)
        
        # Generate complete traffic record
        traffic = {
            'source_ip': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'destination_ip': f"10.0.{random.randint(0, 255)}.{random.randint(1, 255)}",
            'source_port': pattern.get('source_port', random.randint(1024, 65535)),
            'destination_port': pattern.get('destination_port', 80),
            'protocol': pattern.get('protocol', random.choice(protocols)),
            'packet_size': pattern.get('packet_size', random.randint(64, 1500)),
            'payload_size': pattern.get('packet_size', random.randint(64, 1500)) - 40,  # Subtract header size
            'tcp_flags': pattern.get('tcp_flags', random.choice(['ACK', 'SYN', 'FIN', 'PSH']))
        }
        
        return traffic
    
    def send_to_api(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send traffic data to the API for analysis with AI summary.
        
        Args:
            traffic_data: Network traffic data
            
        Returns:
            API response with prediction and summary
        """
        try:
            # Use the summarize endpoint to get both prediction and AI summary
            response = requests.post(
                f"{self.api_url}/summarize",
                json=traffic_data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API returned status code: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending data to API: {e}")
            return None
    
    def monitor(self, interval: int = 2, duration: int = None):
        """
        Start monitoring network traffic.
        
        Args:
            interval: Seconds between each monitoring cycle
            duration: Total duration in seconds (None for indefinite)
        """
        self.running = True
        logger.info(f"Starting NATEM monitoring (interval: {interval}s)")
        
        start_time = time.time()
        event_count = 0
        threat_count = 0
        
        try:
            while self.running:
                # Generate traffic data
                traffic = self.generate_sample_traffic()
                
                # Send to API for analysis
                result = self.send_to_api(traffic)
                
                if result:
                    event_count += 1
                    
                    # Log the AI summary
                    if result.get('threat_detected'):
                        threat_count += 1
                        logger.warning(f"🚨 THREAT DETECTED: {result.get('summary', 'No summary available')}")
                        logger.info(f"Confidence: {result.get('confidence_percentage', 'N/A')}")
                        
                        # Log recommendations
                        recommendations = result.get('recommendations', [])
                        if recommendations:
                            logger.info("Recommendations:")
                            for rec in recommendations[:3]:  # Show top 3
                                logger.info(f"  - {rec}")
                    else:
                        logger.info(f"✅ Normal traffic from {traffic['source_ip']}")
                    
                    # Periodic summary
                    if event_count % 10 == 0:
                        threat_rate = (threat_count / event_count) * 100
                        logger.info(f"📊 Stats: {event_count} events analyzed, "
                                  f"{threat_count} threats detected ({threat_rate:.1f}%)")
                
                # Sleep until next cycle
                time.sleep(interval)
                
                # Check duration limit
                if duration and (time.time() - start_time) >= duration:
                    logger.info(f"Duration limit reached ({duration}s)")
                    break
                    
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        finally:
            self.stop()
    
    def stop(self):
        """Stop monitoring."""
        self.running = False
        logger.info("NATEM Agent stopped")


def main():
    """Main entry point for NATEM agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description='NATEM Agent - Network Attack Threat Event Monitor')
    parser.add_argument('--api-url', type=str, default='http://localhost:5000/api/v1',
                       help='Threat prediction API URL')
    parser.add_argument('--interval', type=int, default=2,
                       help='Monitoring interval in seconds (default: 2)')
    parser.add_argument('--duration', type=int, default=None,
                       help='Monitoring duration in seconds (default: indefinite)')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("NATEM Agent - Network Attack Threat Event Monitor")
    logger.info("=" * 60)
    
    # Create and start agent
    agent = NATEMAgent(api_url=args.api_url)
    
    # Check API health
    try:
        health_url = args.api_url.replace('/api/v1', '/health')
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            logger.info("✅ API health check passed")
        else:
            logger.warning("⚠️  API health check failed, but continuing...")
    except Exception as e:
        logger.warning(f"⚠️  Could not reach API ({e}), but continuing...")
    
    # Start monitoring
    agent.monitor(interval=args.interval, duration=args.duration)


if __name__ == '__main__':
    main()
