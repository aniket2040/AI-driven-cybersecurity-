"""
AI Agent for summarizing complex security events in simple, actionable language.
Provides human-readable interpretations of threat predictions and security alerts.
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
PERCENTAGE_MULTIPLIER = 100  # For converting decimal to percentage


class SecurityEventSummarizer:
    """
    AI agent that converts complex security events into simple, actionable summaries.
    """
    
    def __init__(self):
        """Initialize the security event summarizer."""
        self.attack_types = {
            'DDoS': 'Distributed Denial of Service',
            'SQL Injection': 'Database Attack',
            'XSS': 'Cross-Site Scripting',
            'Port Scan': 'Network Reconnaissance',
            'Brute Force': 'Password Attack',
            'Malware': 'Malicious Software',
            'Phishing': 'Social Engineering Attack',
            'MITM': 'Man-in-the-Middle Attack',
            'Ransomware': 'Data Encryption Attack',
            'Zero-Day': 'Unknown Vulnerability Exploit'
        }
        
        self.severity_descriptions = {
            'HIGH': {
                'urgency': 'CRITICAL - Immediate action required',
                'impact': 'High risk to system security',
                'recommendation': 'Block source and investigate immediately'
            },
            'MEDIUM': {
                'urgency': 'WARNING - Action required soon',
                'impact': 'Moderate risk to system security',
                'recommendation': 'Monitor closely and prepare response'
            },
            'LOW': {
                'urgency': 'ADVISORY - Monitor situation',
                'impact': 'Low risk to system security',
                'recommendation': 'Log for analysis and watch for patterns'
            },
            'INFO': {
                'urgency': 'INFORMATIONAL - No immediate action needed',
                'impact': 'Minimal or no security impact',
                'recommendation': 'Keep for historical analysis'
            }
        }
    
    def summarize_single_event(self, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a human-readable summary of a single security event.
        
        Args:
            prediction: Prediction result dictionary containing threat details
            
        Returns:
            Dictionary with summarized information
        """
        is_threat = prediction.get('is_threat', False)
        confidence = prediction.get('confidence', 0.0)
        severity = prediction.get('severity', 'INFO')
        input_data = prediction.get('input_data', {})
        
        # Generate summary
        if is_threat:
            summary = self._generate_threat_summary(
                input_data, confidence, severity
            )
        else:
            summary = self._generate_benign_summary(input_data, confidence)
        
        # Add actionable recommendations
        summary['recommendations'] = self._generate_recommendations(
            is_threat, severity, input_data
        )
        
        # Add explanation
        summary['explanation'] = self._generate_explanation(
            is_threat, confidence, severity
        )
        
        return summary
    
    def _generate_threat_summary(
        self, 
        data: Dict[str, Any], 
        confidence: float, 
        severity: str
    ) -> Dict[str, str]:
        """Generate summary for detected threats."""
        source_ip = data.get('source_ip', 'unknown')
        dest_ip = data.get('destination_ip', 'unknown')
        protocol = data.get('protocol', 'unknown')
        dest_port = data.get('destination_port', 'unknown')
        
        # Infer attack type based on characteristics
        attack_type = self._infer_attack_type(data)
        
        severity_info = self.severity_descriptions.get(severity, {})
        
        title = f"🚨 Security Threat Detected - {severity} Severity"
        
        description = (
            f"A potential cyber threat has been detected with {confidence:.1%} confidence. "
            f"The system identified suspicious network activity from {source_ip} "
            f"attempting to connect to {dest_ip} on port {dest_port} using {protocol} protocol."
        )
        
        if attack_type:
            description += f" This pattern is consistent with a {attack_type} attack."
        
        return {
            'title': title,
            'description': description,
            'urgency': severity_info.get('urgency', 'Unknown urgency'),
            'impact': severity_info.get('impact', 'Unknown impact'),
            'source': source_ip,
            'target': dest_ip,
            'attack_type': attack_type or 'Unknown',
            'confidence_level': f"{confidence:.1%}"
        }
    
    def _generate_benign_summary(
        self, 
        data: Dict[str, Any], 
        confidence: float
    ) -> Dict[str, str]:
        """Generate summary for benign traffic."""
        source_ip = data.get('source_ip', 'unknown')
        dest_ip = data.get('destination_ip', 'unknown')
        protocol = data.get('protocol', 'unknown')
        
        title = "✅ Normal Network Activity"
        
        description = (
            f"The network traffic from {source_ip} to {dest_ip} "
            f"using {protocol} protocol appears to be legitimate. "
            f"The system is {(1-confidence):.1%} confident this is normal activity."
        )
        
        return {
            'title': title,
            'description': description,
            'urgency': 'NONE - Normal traffic',
            'impact': 'No security impact',
            'source': source_ip,
            'target': dest_ip,
            'attack_type': 'N/A - Benign Traffic',
            'confidence_level': f"{(1-confidence):.1%} (benign)"
        }
    
    def _infer_attack_type(self, data: Dict[str, Any]) -> str:
        """
        Infer attack type based on traffic characteristics.
        
        Args:
            data: Network traffic data
            
        Returns:
            Inferred attack type string
        """
        dest_port = data.get('destination_port', 0)
        protocol = data.get('protocol', '').upper()
        packet_size = data.get('packet_size', 0)
        tcp_flags = data.get('tcp_flags', '')
        
        # Port scan detection
        if isinstance(tcp_flags, str) and 'SYN' in tcp_flags and dest_port > 1024:
            return 'Port Scan'
        
        # SQL injection indicators (port 3306 MySQL, 5432 PostgreSQL)
        if dest_port in [3306, 5432, 1433]:
            return 'Potential SQL Injection'
        
        # Web attack indicators
        if dest_port in [80, 443, 8080, 8443]:
            return 'Potential Web Attack (XSS/Injection)'
        
        # SSH brute force
        if dest_port == 22:
            return 'Potential SSH Brute Force'
        
        # RDP attack
        if dest_port == 3389:
            return 'Potential RDP Attack'
        
        # Large packets (DDoS indicator)
        if packet_size > 1400:
            return 'Potential DDoS/Flooding'
        
        # Default
        return 'Suspicious Network Activity'
    
    def _generate_recommendations(
        self, 
        is_threat: bool, 
        severity: str, 
        data: Dict[str, Any]
    ) -> List[str]:
        """
        Generate actionable recommendations.
        
        Args:
            is_threat: Whether this is a threat
            severity: Threat severity level
            data: Traffic data
            
        Returns:
            List of recommendation strings
        """
        if not is_threat:
            return [
                "✓ Continue normal monitoring",
                "✓ No action required at this time",
                "✓ Log event for historical analysis"
            ]
        
        recommendations = []
        source_ip = data.get('source_ip', 'unknown')
        dest_port = data.get('destination_port', 'unknown')
        
        if severity == 'HIGH':
            recommendations.extend([
                f"🔴 IMMEDIATELY block traffic from {source_ip}",
                f"🔴 Isolate affected system at {data.get('destination_ip', 'target')}",
                "🔴 Alert security team for incident response",
                "🔴 Capture network traffic for forensic analysis",
                "🔴 Check for signs of compromise on target system"
            ])
        elif severity == 'MEDIUM':
            recommendations.extend([
                f"🟡 Monitor traffic from {source_ip} closely",
                f"🟡 Consider rate-limiting or temporary block",
                "🟡 Review firewall rules for port {dest_port}",
                "🟡 Check system logs for related activity",
                "🟡 Prepare incident response team"
            ])
        elif severity == 'LOW':
            recommendations.extend([
                f"🟢 Log and monitor {source_ip} for pattern analysis",
                "🟢 Review security policies",
                "🟢 Update threat intelligence database",
                "🟢 Schedule routine security audit"
            ])
        else:
            recommendations.extend([
                "ℹ️ Record event for trend analysis",
                "ℹ️ No immediate action required"
            ])
        
        return recommendations
    
    def _generate_explanation(
        self, 
        is_threat: bool, 
        confidence: float, 
        severity: str
    ) -> str:
        """
        Generate a plain-language explanation of the detection.
        
        Args:
            is_threat: Whether this is a threat
            confidence: Confidence score
            severity: Severity level
            
        Returns:
            Explanation string
        """
        if not is_threat:
            return (
                "Our AI model analyzed the network traffic patterns and determined "
                "this activity is consistent with normal, legitimate network behavior. "
                "The traffic exhibits characteristics typical of authorized applications "
                "and users."
            )
        
        severity_info = self.severity_descriptions.get(severity, {})
        
        explanation = (
            f"Our machine learning model detected unusual patterns in this network traffic "
            f"with {confidence:.1%} confidence. The activity shows characteristics "
            f"commonly associated with cyber attacks. "
        )
        
        if confidence >= 0.9:
            explanation += (
                "The extremely high confidence score indicates the model is very certain "
                "this is malicious activity based on learned attack patterns."
            )
        elif confidence >= 0.7:
            explanation += (
                "The high confidence score suggests strong indicators of malicious intent "
                "based on multiple suspicious characteristics."
            )
        elif confidence >= 0.5:
            explanation += (
                "The moderate confidence score indicates some suspicious characteristics, "
                "but the activity could potentially be legitimate. Further investigation recommended."
            )
        else:
            explanation += (
                "The lower confidence score suggests only mild suspicion. "
                "This could be a false positive, but should be monitored."
            )
        
        return explanation
    
    def summarize_batch_events(
        self, 
        predictions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a comprehensive summary of multiple security events.
        
        Args:
            predictions: List of prediction results
            
        Returns:
            Batch summary dictionary
        """
        total = len(predictions)
        threats = [p for p in predictions if p.get('is_threat', False)]
        threat_count = len(threats)
        
        # Categorize by severity
        severity_counts = {
            'HIGH': sum(1 for p in predictions if p.get('severity') == 'HIGH'),
            'MEDIUM': sum(1 for p in predictions if p.get('severity') == 'MEDIUM'),
            'LOW': sum(1 for p in predictions if p.get('severity') == 'LOW'),
            'INFO': sum(1 for p in predictions if p.get('severity') == 'INFO')
        }
        
        # Generate executive summary
        exec_summary = self._generate_executive_summary(
            total, threat_count, severity_counts
        )
        
        # Generate critical alerts
        critical_alerts = [
            self.summarize_single_event(p)
            for p in predictions
            if p.get('severity') == 'HIGH'
        ]
        
        return {
            'executive_summary': exec_summary,
            'total_events': total,
            'threat_count': threat_count,
            'benign_count': total - threat_count,
            'severity_breakdown': severity_counts,
            'critical_alerts': critical_alerts,
            'threat_rate': f"{(threat_count/total*100):.1f}%" if total > 0 else "0%",
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_executive_summary(
        self, 
        total: int, 
        threat_count: int, 
        severity_counts: Dict[str, int]
    ) -> str:
        """
        Generate executive-level summary.
        
        Args:
            total: Total events analyzed
            threat_count: Number of threats detected
            severity_counts: Breakdown by severity
            
        Returns:
            Executive summary string
        """
        threat_rate = (threat_count / total * PERCENTAGE_MULTIPLIER) if total > 0 else 0
        
        if severity_counts['HIGH'] > 0:
            status = "🚨 CRITICAL ALERT"
            message = (
                f"URGENT: {severity_counts['HIGH']} high-severity threats detected! "
                f"Immediate action required. "
            )
        elif severity_counts['MEDIUM'] > 0:
            status = "⚠️ WARNING"
            message = (
                f"WARNING: {severity_counts['MEDIUM']} medium-severity threats detected. "
                f"Action recommended. "
            )
        elif threat_count > 0:
            status = "ℹ️ ADVISORY"
            message = (
                f"ADVISORY: {threat_count} low-severity threats detected. "
                f"Monitoring recommended. "
            )
        else:
            status = "✅ ALL CLEAR"
            message = "All analyzed traffic appears legitimate. No threats detected. "
        
        summary = (
            f"{status}\n\n"
            f"{message}"
            f"Analysis Summary: {total} network events analyzed, "
            f"{threat_count} threats identified ({threat_rate:.1f}% threat rate).\n\n"
            f"Severity Distribution:\n"
            f"  • Critical (HIGH): {severity_counts['HIGH']}\n"
            f"  • Warning (MEDIUM): {severity_counts['MEDIUM']}\n"
            f"  • Advisory (LOW): {severity_counts['LOW']}\n"
            f"  • Info: {severity_counts['INFO']}"
        )
        
        return summary


class ThreatSummaryAgent:
    """
    High-level agent interface for generating threat intelligence reports.
    """
    
    def __init__(self):
        """Initialize the threat summary agent."""
        self.summarizer = SecurityEventSummarizer()
        self.event_history = []
    
    def analyze_and_summarize(
        self, 
        prediction: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a prediction and generate a complete summary.
        
        Args:
            prediction: Prediction result from threat predictor
            
        Returns:
            Complete analysis with summary
        """
        # Store in history
        self.event_history.append(prediction)
        
        # Generate summary
        summary = self.summarizer.summarize_single_event(prediction)
        
        # Combine with original prediction
        result = {
            'original_prediction': prediction,
            'ai_summary': summary,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Generated AI summary: {summary['title']}")
        
        return result
    
    def generate_report(
        self, 
        predictions: List[Dict[str, Any]] = None,
        include_history: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive threat intelligence report.
        
        Args:
            predictions: List of predictions to analyze (if None, uses history)
            include_history: Whether to include historical context
            
        Returns:
            Complete threat intelligence report
        """
        data_to_analyze = predictions if predictions else self.event_history
        
        if not data_to_analyze:
            return {
                'status': 'NO_DATA',
                'message': 'No security events to analyze',
                'timestamp': datetime.now().isoformat()
            }
        
        # Generate batch summary
        batch_summary = self.summarizer.summarize_batch_events(data_to_analyze)
        
        # Create full report
        report = {
            'report_type': 'Threat Intelligence Summary',
            'generated_at': datetime.now().isoformat(),
            'analysis_period': {
                'events_analyzed': len(data_to_analyze),
                'time_range': 'Real-time snapshot'
            },
            'summary': batch_summary,
            'recommendations': self._generate_report_recommendations(batch_summary)
        }
        
        if include_history and self.event_history:
            report['historical_context'] = {
                'total_historical_events': len(self.event_history),
                'historical_threat_rate': self._calculate_historical_threat_rate()
            }
        
        logger.info(f"Generated threat intelligence report: {report['summary']['threat_count']} threats")
        
        return report
    
    def _generate_report_recommendations(
        self, 
        batch_summary: Dict[str, Any]
    ) -> List[str]:
        """Generate high-level recommendations for the report."""
        recommendations = []
        severity_counts = batch_summary['severity_breakdown']
        
        if severity_counts['HIGH'] > 0:
            recommendations.append(
                "🔴 CRITICAL: Execute incident response plan immediately"
            )
            recommendations.append(
                "🔴 Engage security operations center (SOC) for threat hunting"
            )
        
        if severity_counts['MEDIUM'] > 5:
            recommendations.append(
                "🟡 Consider increasing security monitoring level"
            )
        
        if batch_summary['threat_count'] > batch_summary['total_events'] * 0.2:
            recommendations.append(
                "⚠️ High threat rate detected - review network security posture"
            )
        
        recommendations.extend([
            "📊 Archive this report for compliance and audit purposes",
            "🔄 Schedule regular security posture reviews",
            "📚 Update threat intelligence database with new indicators"
        ])
        
        return recommendations
    
    def _calculate_historical_threat_rate(self) -> str:
        """Calculate threat rate from historical events."""
        if not self.event_history:
            return "0%"
        
        threat_count = sum(
            1 for e in self.event_history 
            if e.get('is_threat', False)
        )
        
        return f"{(threat_count / len(self.event_history) * PERCENTAGE_MULTIPLIER):.1f}%"
    
    def clear_history(self):
        """Clear event history."""
        self.event_history = []
        logger.info("Event history cleared")
