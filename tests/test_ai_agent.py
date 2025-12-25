"""
Unit tests for AI agent summarization functionality.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ai_agent.summarizer import SecurityEventSummarizer, ThreatSummaryAgent


class TestSecurityEventSummarizer:
    """Test AI summarizer functionality."""
    
    def test_summarizer_initialization(self):
        """Test summarizer initialization."""
        summarizer = SecurityEventSummarizer()
        
        assert summarizer is not None
        assert len(summarizer.attack_types) > 0
        assert 'HIGH' in summarizer.severity_descriptions
        assert 'MEDIUM' in summarizer.severity_descriptions
        assert 'LOW' in summarizer.severity_descriptions
    
    def test_summarize_threat_event(self):
        """Test summarizing a threat event."""
        summarizer = SecurityEventSummarizer()
        
        prediction = {
            'is_threat': True,
            'confidence': 0.85,
            'severity': 'HIGH',
            'timestamp': '2024-01-01T12:00:00',
            'input_data': {
                'source_ip': '192.168.1.100',
                'destination_ip': '10.0.0.50',
                'destination_port': 22,
                'protocol': 'TCP',
                'packet_size': 1024
            }
        }
        
        summary = summarizer.summarize_single_event(prediction)
        
        assert 'title' in summary
        assert 'description' in summary
        assert 'recommendations' in summary
        assert 'explanation' in summary
        assert 'urgency' in summary
        assert 'HIGH' in summary['title']
        assert isinstance(summary['recommendations'], list)
        assert len(summary['recommendations']) > 0
    
    def test_summarize_benign_event(self):
        """Test summarizing a benign event."""
        summarizer = SecurityEventSummarizer()
        
        prediction = {
            'is_threat': False,
            'confidence': 0.15,
            'severity': 'INFO',
            'timestamp': '2024-01-01T12:00:00',
            'input_data': {
                'source_ip': '192.168.1.50',
                'destination_ip': '10.0.0.100',
                'destination_port': 443,
                'protocol': 'TCP'
            }
        }
        
        summary = summarizer.summarize_single_event(prediction)
        
        assert 'title' in summary
        assert 'Normal' in summary['title'] or '✅' in summary['title']
        assert summary['attack_type'] == 'N/A - Benign Traffic'
        assert len(summary['recommendations']) >= 3
    
    def test_infer_attack_type(self):
        """Test attack type inference."""
        summarizer = SecurityEventSummarizer()
        
        # SSH brute force
        data_ssh = {'destination_port': 22, 'protocol': 'TCP'}
        attack_type = summarizer._infer_attack_type(data_ssh)
        assert 'SSH' in attack_type
        
        # SQL injection
        data_sql = {'destination_port': 3306, 'protocol': 'TCP'}
        attack_type = summarizer._infer_attack_type(data_sql)
        assert 'SQL' in attack_type
        
        # Web attack
        data_web = {'destination_port': 80, 'protocol': 'TCP'}
        attack_type = summarizer._infer_attack_type(data_web)
        assert 'Web' in attack_type
    
    def test_summarize_batch_events(self):
        """Test batch event summarization."""
        summarizer = SecurityEventSummarizer()
        
        predictions = [
            {
                'is_threat': True,
                'confidence': 0.9,
                'severity': 'HIGH',
                'input_data': {'source_ip': '1.1.1.1', 'destination_ip': '2.2.2.2'}
            },
            {
                'is_threat': True,
                'confidence': 0.6,
                'severity': 'MEDIUM',
                'input_data': {'source_ip': '3.3.3.3', 'destination_ip': '4.4.4.4'}
            },
            {
                'is_threat': False,
                'confidence': 0.2,
                'severity': 'INFO',
                'input_data': {'source_ip': '5.5.5.5', 'destination_ip': '6.6.6.6'}
            }
        ]
        
        summary = summarizer.summarize_batch_events(predictions)
        
        assert summary['total_events'] == 3
        assert summary['threat_count'] == 2
        assert summary['benign_count'] == 1
        assert summary['severity_breakdown']['HIGH'] == 1
        assert summary['severity_breakdown']['MEDIUM'] == 1
        assert 'executive_summary' in summary
        assert 'CRITICAL' in summary['executive_summary'] or 'ALERT' in summary['executive_summary']


class TestThreatSummaryAgent:
    """Test threat summary agent."""
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = ThreatSummaryAgent()
        
        assert agent is not None
        assert agent.summarizer is not None
        assert isinstance(agent.event_history, list)
        assert len(agent.event_history) == 0
    
    def test_analyze_and_summarize(self):
        """Test analyze and summarize functionality."""
        agent = ThreatSummaryAgent()
        
        prediction = {
            'is_threat': True,
            'confidence': 0.8,
            'severity': 'MEDIUM',
            'timestamp': '2024-01-01T12:00:00',
            'input_data': {
                'source_ip': '192.168.1.100',
                'destination_ip': '10.0.0.50',
                'destination_port': 3389,
                'protocol': 'TCP'
            }
        }
        
        result = agent.analyze_and_summarize(prediction)
        
        assert 'original_prediction' in result
        assert 'ai_summary' in result
        assert 'analysis_timestamp' in result
        assert result['ai_summary']['title'] is not None
        assert len(agent.event_history) == 1
    
    def test_generate_report(self):
        """Test report generation."""
        agent = ThreatSummaryAgent()
        
        # Add some events to history
        predictions = [
            {
                'is_threat': True,
                'confidence': 0.9,
                'severity': 'HIGH',
                'input_data': {'source_ip': '1.1.1.1', 'destination_ip': '2.2.2.2'}
            },
            {
                'is_threat': False,
                'confidence': 0.1,
                'severity': 'INFO',
                'input_data': {'source_ip': '3.3.3.3', 'destination_ip': '4.4.4.4'}
            }
        ]
        
        for pred in predictions:
            agent.analyze_and_summarize(pred)
        
        report = agent.generate_report(include_history=True)
        
        assert report['report_type'] == 'Threat Intelligence Summary'
        assert 'generated_at' in report
        assert 'summary' in report
        assert 'recommendations' in report
        assert report['summary']['total_events'] == 2
        assert report['summary']['threat_count'] == 1
    
    def test_generate_report_no_data(self):
        """Test report generation with no data."""
        agent = ThreatSummaryAgent()
        
        report = agent.generate_report()
        
        assert report['status'] == 'NO_DATA'
        assert 'message' in report
    
    def test_clear_history(self):
        """Test clearing event history."""
        agent = ThreatSummaryAgent()
        
        # Add event
        prediction = {
            'is_threat': True,
            'confidence': 0.7,
            'severity': 'MEDIUM',
            'input_data': {}
        }
        agent.analyze_and_summarize(prediction)
        
        assert len(agent.event_history) == 1
        
        # Clear history
        agent.clear_history()
        
        assert len(agent.event_history) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
