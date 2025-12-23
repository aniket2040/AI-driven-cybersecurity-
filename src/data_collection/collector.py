"""
Data collection module for cybersecurity threat data.
Supports both static data loading and live network traffic capture.
"""
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StaticDataLoader:
    """Load and process static cybersecurity datasets."""
    
    def __init__(self, data_path: str):
        """
        Initialize static data loader.
        
        Args:
            data_path: Path to the static data file (CSV, JSON, etc.)
        """
        self.data_path = data_path
        self.data = None
    
    def load_csv(self, **kwargs) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
            DataFrame containing the loaded data
        """
        try:
            self.data = pd.read_csv(self.data_path, **kwargs)
            logger.info(f"Loaded {len(self.data)} records from {self.data_path}")
            return self.data
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
    
    def load_json(self, **kwargs) -> pd.DataFrame:
        """
        Load data from JSON file.
        
        Returns:
            DataFrame containing the loaded data
        """
        try:
            self.data = pd.read_json(self.data_path, **kwargs)
            logger.info(f"Loaded {len(self.data)} records from {self.data_path}")
            return self.data
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            raise
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded data.
        
        Returns:
            Dictionary containing data statistics
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        return {
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "dtypes": self.data.dtypes.to_dict(),
            "missing_values": self.data.isnull().sum().to_dict(),
            "sample": self.data.head().to_dict()
        }


class LiveDataCollector:
    """Collect live network traffic data for threat detection."""
    
    def __init__(self, interface: str = None):
        """
        Initialize live data collector.
        
        Args:
            interface: Network interface to capture from (e.g., 'eth0')
        """
        self.interface = interface
        self.captured_packets = []
        self.is_collecting = False
    
    def start_capture(self, packet_count: int = 100, timeout: int = 60):
        """
        Start capturing network packets.
        
        Args:
            packet_count: Number of packets to capture
            timeout: Timeout in seconds
        """
        logger.info(f"Starting packet capture on interface: {self.interface}")
        self.is_collecting = True
        
        # Simulated packet capture for demonstration
        # In production, this would use scapy or pcapy
        self._simulate_packet_capture(packet_count)
    
    def _simulate_packet_capture(self, count: int):
        """
        Simulate packet capture for demonstration purposes.
        In production, replace with actual packet capture using scapy.
        
        Args:
            count: Number of packets to simulate
        """
        for i in range(count):
            packet = {
                'timestamp': datetime.now(),
                'source_ip': f'192.168.1.{np.random.randint(1, 255)}',
                'destination_ip': f'10.0.0.{np.random.randint(1, 255)}',
                'source_port': np.random.randint(1024, 65535),
                'destination_port': np.random.choice([80, 443, 22, 3389, 8080]),
                'protocol': np.random.choice(['TCP', 'UDP', 'ICMP']),
                'packet_size': np.random.randint(64, 1500),
                'payload_size': np.random.randint(0, 1400),
                'tcp_flags': np.random.choice(['SYN', 'ACK', 'FIN', 'PSH', 'RST'])
            }
            self.captured_packets.append(packet)
        
        logger.info(f"Captured {len(self.captured_packets)} packets")
    
    def stop_capture(self):
        """Stop capturing packets."""
        self.is_collecting = False
        logger.info("Packet capture stopped")
    
    def get_captured_data(self) -> pd.DataFrame:
        """
        Get captured packets as a DataFrame.
        
        Returns:
            DataFrame containing captured packet data
        """
        if not self.captured_packets:
            logger.warning("No packets captured")
            return pd.DataFrame()
        
        return pd.DataFrame(self.captured_packets)
    
    def clear_buffer(self):
        """Clear the captured packets buffer."""
        self.captured_packets = []
        logger.info("Packet buffer cleared")


def load_sample_threat_data() -> pd.DataFrame:
    """
    Generate sample threat data for testing and demonstration.
    
    Returns:
        DataFrame containing sample threat data
    """
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'timestamp': [datetime.now() for _ in range(n_samples)],
        'source_ip': [f'192.168.{np.random.randint(0, 255)}.{np.random.randint(1, 255)}' 
                     for _ in range(n_samples)],
        'destination_ip': [f'10.0.{np.random.randint(0, 255)}.{np.random.randint(1, 255)}' 
                          for _ in range(n_samples)],
        'source_port': np.random.randint(1024, 65535, n_samples),
        'destination_port': np.random.choice([80, 443, 22, 3389, 21, 23, 25], n_samples),
        'protocol': np.random.choice(['TCP', 'UDP', 'ICMP'], n_samples),
        'packet_size': np.random.randint(64, 1500, n_samples),
        'payload_size': np.random.randint(0, 1400, n_samples),
        'tcp_flags': np.random.choice(['SYN', 'ACK', 'FIN', 'PSH', 'RST', 'SYN-ACK'], n_samples),
        'is_malicious': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    }
    
    df = pd.DataFrame(data)
    logger.info(f"Generated {len(df)} sample threat records")
    
    return df
