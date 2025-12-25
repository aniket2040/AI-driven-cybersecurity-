"""
Unit tests for AI agent and summarization functionality.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ai_agent.summarizer import SecurityEventSummarizer


class TestSecurityEventSummarizer:
    """Test AI security event summarization."""
    
    def test_summarizer_initialization(self):
        """Test summarizer initialization."""
        summarizer = SecurityEventSummarizer()
        
        assert isinstance(summarizer.summary_cache, list)
        assert len(summarizer.summary_cache) == 0
        assert isinstance(summarizer.ATTACK_DESCRIPTIONS, dict)
        assert isinstance(summarizer.SEVERITY_DESCRIPTIONS, dict)
    
    def test_summarize_threat(self):
        """Test threat summarization."""
        summarizer = SecurityEventSummarizer()
        
        threat_data = {
            'is_threat': True,
            'confidence': 0.95,
            'severity': 'HIGH',
            'timestamp': '2024-12-25T10:00:00',
            'input_data': {
                'source_ip': '192.168.1.100',
                'destination_ip': '10.0.0.50',
                'source_port': 54321,
                'destination_port': 22,
                'protocol': 'TCP',
                'packet_size': 64,
                'payload_size': 24,
                'tcp_flags': 'SYN'
            }
        }
        
        result = summarizer.summarize_threat(threat_data)
        
        assert 'summary' in result
        assert 'severity_description' in result
        assert 'confidence_percentage' in result
        assert 'recommendations' in result
        assert 'threat_detected' in result
        assert result['threat_detected'] is True
        assert isinstance(result['recommendations'], list)
        assert len(result['recommendations']) > 0
    
    def test_summarize_benign(self):
        """Test benign traffic summarization."""
        summarizer = SecurityEventSummarizer()
        
        benign_data = {
            'is_threat': False,
            'confidence': 0.15,
            'severity': 'INFO',
            'timestamp': '2024-12-25T10:01:00',
            'input_data': {
                'source_ip': '192.168.1.50',
                'destination_ip': '10.0.0.100',
                'source_port': 49152,
                'destination_port': 443,
                'protocol': 'TCP',
                'packet_size': 1024,
                'payload_size': 984,
                'tcp_flags': 'ACK'
            }
        }
        
        result = summarizer.summarize_threat(benign_data)
        
        assert 'summary' in result
        assert result['threat_detected'] is False
        assert '✅' in result['summary'] or 'NORMAL' in result['summary']
    
    def test_summarize_batch(self):
        """Test batch summarization."""
        summarizer = SecurityEventSummarizer()
        
        threats = [
            {
                'is_threat': True,
                'confidence': 0.95,
                'severity': 'HIGH',
                'timestamp': '2024-12-25T10:00:00',
                'input_data': {
                    'source_ip': '192.168.1.100',
                    'destination_ip': '10.0.0.50',
                    'source_port': 54321,
                    'destination_port': 22,
                    'protocol': 'TCP',
                    'packet_size': 64,
                    'payload_size': 24,
                    'tcp_flags': 'SYN'
                }
            },
            {
                'is_threat': False,
                'confidence': 0.15,
                'severity': 'INFO',
                'timestamp': '2024-12-25T10:01:00',
                'input_data': {
                    'source_ip': '192.168.1.50',
                    'destination_ip': '10.0.0.100',
                    'source_port': 49152,
                    'destination_port': 443,
                    'protocol': 'TCP',
                    'packet_size': 1024,
                    'payload_size': 984,
                    'tcp_flags': 'ACK'
                }
            },
            {
                'is_threat': True,
                'confidence': 0.75,
                'severity': 'MEDIUM',
                'timestamp': '2024-12-25T10:02:00',
                'input_data': {
                    'source_ip': '192.168.1.101',
                    'destination_ip': '10.0.0.60',
                    'source_port': 12345,
                    'destination_port': 3306,
                    'protocol': 'TCP',
                    'packet_size': 2048,
                    'payload_size': 2008,
                    'tcp_flags': 'PSH'
                }
            }
        ]
        
        result = summarizer.summarize_batch(threats)
        
        assert 'executive_summary' in result
        assert 'total_analyzed' in result
        assert 'threat_count' in result
        assert 'benign_count' in result
        assert 'severity_distribution' in result
        assert 'individual_summaries' in result
        
        assert result['total_analyzed'] == 3
        assert result['threat_count'] == 2
        assert result['benign_count'] == 1
        assert result['severity_distribution']['HIGH'] == 1
        assert result['severity_distribution']['MEDIUM'] == 1
    
    def test_infer_attack_type(self):
        """Test attack type inference."""
        summarizer = SecurityEventSummarizer()
        
        # Port scan test
        port_scan_data = {
            'destination_port': 22,
            'protocol': 'TCP',
            'tcp_flags': 'SYN',
            'packet_size': 64
        }
        attack_type = summarizer._infer_attack_type(port_scan_data)
        assert attack_type == 'port_scan'
        
        # SQL injection test
        sql_injection_data = {
            'destination_port': 3306,
            'protocol': 'TCP',
            'tcp_flags': 'PSH',
            'packet_size': 2048
        }
        attack_type = summarizer._infer_attack_type(sql_injection_data)
        assert attack_type == 'sql_injection'
        
        # DDoS test
        ddos_data = {
            'destination_port': 80,
            'protocol': 'UDP',
            'tcp_flags': '',
            'packet_size': 50
        }
        attack_type = summarizer._infer_attack_type(ddos_data)
        assert attack_type == 'ddos'
    
    def test_generate_recommendations(self):
        """Test recommendation generation."""
        summarizer = SecurityEventSummarizer()
        
        # High severity recommendations
        high_rec = summarizer._generate_recommendations(
            is_threat=True,
            severity='HIGH',
            input_data={'source_ip': '192.168.1.100', 'destination_port': 22},
            confidence=0.95
        )
        
        assert isinstance(high_rec, list)
        assert len(high_rec) > 0
        assert any('IMMEDIATE' in rec or '🔴' in rec for rec in high_rec)
        
        # Benign recommendations
        benign_rec = summarizer._generate_recommendations(
            is_threat=False,
            severity='INFO',
            input_data={'source_ip': '192.168.1.50', 'destination_port': 443},
            confidence=0.10
        )
        
        assert isinstance(benign_rec, list)
        assert any('No immediate action' in rec for rec in benign_rec)
    
    def test_cache_functionality(self):
        """Test summary caching."""
        summarizer = SecurityEventSummarizer()
        
        threat_data = {
            'is_threat': True,
            'confidence': 0.95,
            'severity': 'HIGH',
            'timestamp': '2024-12-25T10:00:00',
            'input_data': {
                'source_ip': '192.168.1.100',
                'destination_ip': '10.0.0.50',
                'source_port': 54321,
                'destination_port': 22,
                'protocol': 'TCP',
                'packet_size': 64,
                'payload_size': 24,
                'tcp_flags': 'SYN'
            }
        }
        
        # Generate summary
        summarizer.summarize_threat(threat_data)
        summarizer.summarize_threat(threat_data)
        
        # Check cache
        cache = summarizer.get_summary_cache()
        assert len(cache) == 2
        
        # Clear cache
        summarizer.clear_cache()
        cache = summarizer.get_summary_cache()
        assert len(cache) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
