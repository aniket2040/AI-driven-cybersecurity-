"""
Demo script to showcase the new AI-driven features:
- AI agent for security event summarization
- Real-time threat intelligence reports
- Dashboard integration
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ai_agent.summarizer import SecurityEventSummarizer, ThreatSummaryAgent


def print_section(title):
    """Print a section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def demo_security_event_summarizer():
    """Demonstrate the SecurityEventSummarizer functionality."""
    print_section("DEMO: Security Event Summarizer")
    
    summarizer = SecurityEventSummarizer()
    
    # Example 1: High-severity threat
    print("Example 1: HIGH Severity Threat (SSH Brute Force)")
    print("-" * 80)
    
    high_threat = {
        'is_threat': True,
        'confidence': 0.92,
        'severity': 'HIGH',
        'timestamp': '2024-12-25T10:30:00',
        'input_data': {
            'source_ip': '203.0.113.45',
            'destination_ip': '10.0.0.15',
            'source_port': 54321,
            'destination_port': 22,
            'protocol': 'TCP',
            'packet_size': 512,
            'tcp_flags': 'SYN'
        }
    }
    
    summary = summarizer.summarize_single_event(high_threat)
    
    print(f"Title: {summary['title']}")
    print(f"\nDescription: {summary['description']}")
    print(f"\nUrgency: {summary['urgency']}")
    print(f"Impact: {summary['impact']}")
    print(f"Attack Type: {summary['attack_type']}")
    print(f"Confidence: {summary['confidence_level']}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(summary['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print(f"\nExplanation:\n{summary['explanation']}")
    
    # Example 2: Medium-severity threat
    print("\n\nExample 2: MEDIUM Severity Threat (Web Attack)")
    print("-" * 80)
    
    medium_threat = {
        'is_threat': True,
        'confidence': 0.65,
        'severity': 'MEDIUM',
        'timestamp': '2024-12-25T10:35:00',
        'input_data': {
            'source_ip': '198.51.100.23',
            'destination_ip': '10.0.0.25',
            'source_port': 49152,
            'destination_port': 443,
            'protocol': 'TCP',
            'packet_size': 1200
        }
    }
    
    summary = summarizer.summarize_single_event(medium_threat)
    
    print(f"Title: {summary['title']}")
    print(f"\nDescription: {summary['description']}")
    print(f"Attack Type: {summary['attack_type']}")
    print("\nTop 3 Recommendations:")
    for i, rec in enumerate(summary['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    # Example 3: Benign traffic
    print("\n\nExample 3: Benign Traffic (Normal Activity)")
    print("-" * 80)
    
    benign = {
        'is_threat': False,
        'confidence': 0.15,
        'severity': 'INFO',
        'timestamp': '2024-12-25T10:40:00',
        'input_data': {
            'source_ip': '192.168.1.100',
            'destination_ip': '93.184.216.34',
            'source_port': 54000,
            'destination_port': 443,
            'protocol': 'TCP',
            'packet_size': 800
        }
    }
    
    summary = summarizer.summarize_single_event(benign)
    
    print(f"Title: {summary['title']}")
    print(f"\nDescription: {summary['description']}")
    print(f"Attack Type: {summary['attack_type']}")


def demo_batch_summarization():
    """Demonstrate batch event summarization."""
    print_section("DEMO: Batch Event Summarization")
    
    summarizer = SecurityEventSummarizer()
    
    # Simulate multiple events
    events = [
        {
            'is_threat': True,
            'confidence': 0.95,
            'severity': 'HIGH',
            'input_data': {'source_ip': '1.1.1.1', 'destination_ip': '10.0.0.1'}
        },
        {
            'is_threat': True,
            'confidence': 0.88,
            'severity': 'HIGH',
            'input_data': {'source_ip': '2.2.2.2', 'destination_ip': '10.0.0.2'}
        },
        {
            'is_threat': True,
            'confidence': 0.62,
            'severity': 'MEDIUM',
            'input_data': {'source_ip': '3.3.3.3', 'destination_ip': '10.0.0.3'}
        },
        {
            'is_threat': True,
            'confidence': 0.45,
            'severity': 'LOW',
            'input_data': {'source_ip': '4.4.4.4', 'destination_ip': '10.0.0.4'}
        },
        {
            'is_threat': False,
            'confidence': 0.10,
            'severity': 'INFO',
            'input_data': {'source_ip': '5.5.5.5', 'destination_ip': '10.0.0.5'}
        },
        {
            'is_threat': False,
            'confidence': 0.05,
            'severity': 'INFO',
            'input_data': {'source_ip': '6.6.6.6', 'destination_ip': '10.0.0.6'}
        }
    ]
    
    batch_summary = summarizer.summarize_batch_events(events)
    
    print("Executive Summary:")
    print("-" * 80)
    print(batch_summary['executive_summary'])
    
    print(f"\n\nStatistics:")
    print(f"  Total Events: {batch_summary['total_events']}")
    print(f"  Threats Detected: {batch_summary['threat_count']}")
    print(f"  Benign Traffic: {batch_summary['benign_count']}")
    print(f"  Threat Rate: {batch_summary['threat_rate']}")
    
    print(f"\n  Severity Breakdown:")
    for severity, count in batch_summary['severity_breakdown'].items():
        print(f"    {severity}: {count}")


def demo_threat_intelligence_agent():
    """Demonstrate the ThreatSummaryAgent."""
    print_section("DEMO: Threat Intelligence Agent")
    
    agent = ThreatSummaryAgent()
    
    print("Processing multiple security events...")
    print("-" * 80)
    
    # Simulate events being processed
    events = [
        {
            'is_threat': True,
            'confidence': 0.93,
            'severity': 'HIGH',
            'timestamp': '2024-12-25T11:00:00',
            'input_data': {
                'source_ip': '198.18.0.100',
                'destination_ip': '10.0.0.50',
                'destination_port': 3306,
                'protocol': 'TCP'
            }
        },
        {
            'is_threat': True,
            'confidence': 0.78,
            'severity': 'MEDIUM',
            'timestamp': '2024-12-25T11:05:00',
            'input_data': {
                'source_ip': '198.18.0.101',
                'destination_ip': '10.0.0.51',
                'destination_port': 3389,
                'protocol': 'TCP'
            }
        },
        {
            'is_threat': False,
            'confidence': 0.08,
            'severity': 'INFO',
            'timestamp': '2024-12-25T11:10:00',
            'input_data': {
                'source_ip': '192.168.1.25',
                'destination_ip': '8.8.8.8',
                'destination_port': 53,
                'protocol': 'UDP'
            }
        }
    ]
    
    for i, event in enumerate(events, 1):
        print(f"\nProcessing Event {i}...")
        analysis = agent.analyze_and_summarize(event)
        summary = analysis['ai_summary']
        print(f"  {summary['title']}")
        print(f"  Source: {summary.get('source', 'N/A')}")
        print(f"  Target: {summary.get('target', 'N/A')}")
        print(f"  Attack Type: {summary.get('attack_type', 'N/A')}")
    
    print("\n\nGenerating Comprehensive Threat Intelligence Report...")
    print("="*80)
    
    report = agent.generate_report(include_history=True)
    
    print(f"\nReport Type: {report['report_type']}")
    print(f"Generated At: {report['generated_at']}")
    
    print("\nExecutive Summary:")
    print("-" * 80)
    print(report['summary']['executive_summary'])
    
    print("\n\nKey Recommendations:")
    print("-" * 80)
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"{i}. {rec}")
    
    if 'historical_context' in report:
        print("\n\nHistorical Context:")
        print("-" * 80)
        hc = report['historical_context']
        print(f"  Total Historical Events: {hc['total_historical_events']}")
        print(f"  Historical Threat Rate: {hc['historical_threat_rate']}")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  AI-DRIVEN CYBERSECURITY THREAT DETECTION SYSTEM".center(78) + "║")
    print("║" + "  Feature Demonstration".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        demo_security_event_summarizer()
        demo_batch_summarization()
        demo_threat_intelligence_agent()
        
        print("\n\n" + "="*80)
        print("  DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nKey Features Demonstrated:")
        print("  ✓ Single event AI summarization with human-readable explanations")
        print("  ✓ Batch event analysis with executive summaries")
        print("  ✓ Threat intelligence report generation")
        print("  ✓ Actionable security recommendations")
        print("  ✓ Attack type inference and classification")
        print("\nNext Steps:")
        print("  1. Run the API server: python api/app.py --model <model_path>")
        print("  2. Run the dashboard: python dashboard/app.py --model <model_path>")
        print("  3. Or use Docker: docker-compose up -d")
        print("  4. Access dashboard at: http://localhost:8000")
        print("\n")
        
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
