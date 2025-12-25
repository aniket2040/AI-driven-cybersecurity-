"""
Security Event Summarizer - AI Agent for analyzing and summarizing complex security events.

This module uses natural language processing and pattern analysis to convert complex
security events into simple, actionable summaries for security teams.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityEventSummarizer:
    """
    AI Agent that analyzes security events and generates human-readable summaries.
    
    This agent takes complex security event data and converts it into simple,
    actionable language that security teams can quickly understand and act upon.
    """
    
    # Attack type descriptions
    ATTACK_DESCRIPTIONS = {
        'ddos': 'Distributed Denial of Service (DDoS) attack attempting to overwhelm the system',
        'port_scan': 'Port scanning activity - attacker probing for open ports and services',
        'brute_force': 'Brute force attack - repeated login attempts to guess credentials',
        'sql_injection': 'SQL Injection attempt - trying to manipulate database queries',
        'malware': 'Malware detected - malicious software attempting to infect the system',
        'phishing': 'Phishing attempt - fraudulent attempt to obtain sensitive information',
        'ransomware': 'Ransomware attack - malware attempting to encrypt files for ransom',
        'mitm': 'Man-in-the-Middle attack - intercepting communications between parties',
        'xss': 'Cross-Site Scripting (XSS) attack - injecting malicious scripts',
        'zero_day': 'Potential zero-day exploit - unknown or unpatched vulnerability',
        'dos': 'Denial of Service attack - attempting to make service unavailable',
        'backdoor': 'Backdoor detected - unauthorized access mechanism',
        'trojan': 'Trojan detected - malicious software disguised as legitimate',
        'worm': 'Worm activity - self-replicating malware spreading across network',
        'unknown': 'Unknown or unclassified threat pattern'
    }
    
    # Severity level descriptions
    SEVERITY_DESCRIPTIONS = {
        'HIGH': 'CRITICAL - Immediate action required',
        'MEDIUM': 'WARNING - Investigate and address soon',
        'LOW': 'NOTICE - Monitor and log for analysis',
        'INFO': 'INFORMATIONAL - For awareness only'
    }
    
    # Common port descriptions
    PORT_DESCRIPTIONS = {
        20: 'FTP Data',
        21: 'FTP Control',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP (Email)',
        53: 'DNS',
        80: 'HTTP (Web)',
        110: 'POP3 (Email)',
        143: 'IMAP (Email)',
        443: 'HTTPS (Secure Web)',
        445: 'SMB (File Sharing)',
        3306: 'MySQL Database',
        3389: 'RDP (Remote Desktop)',
        5432: 'PostgreSQL Database',
        8080: 'HTTP Alternative',
        8443: 'HTTPS Alternative'
    }
    
    def __init__(self):
        """Initialize the Security Event Summarizer."""
        self.summary_cache = []
        logger.info("Security Event Summarizer initialized")
    
    def summarize_threat(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a human-readable summary of a security threat.
        
        Args:
            threat_data: Dictionary containing threat information including:
                - is_threat: Boolean indicating if it's a threat
                - confidence: Confidence score (0-1)
                - severity: Severity level (HIGH, MEDIUM, LOW, INFO)
                - timestamp: When the threat was detected
                - input_data: Original network traffic data
                
        Returns:
            Dictionary containing the summary and analysis
        """
        try:
            # Extract key information
            is_threat = threat_data.get('is_threat', False)
            confidence = threat_data.get('confidence', 0.0)
            severity = threat_data.get('severity', 'INFO')
            input_data = threat_data.get('input_data', {})
            timestamp = threat_data.get('timestamp', datetime.now().isoformat())
            
            # Build the summary
            if not is_threat:
                summary = self._summarize_benign(input_data, confidence)
            else:
                summary = self._summarize_malicious(input_data, confidence, severity)
            
            # Add recommendations
            recommendations = self._generate_recommendations(
                is_threat, severity, input_data, confidence
            )
            
            # Build the complete summary object
            result = {
                'summary': summary,
                'severity_description': self.SEVERITY_DESCRIPTIONS.get(severity, 'Unknown'),
                'confidence_percentage': f"{confidence * 100:.1f}%",
                'recommendations': recommendations,
                'timestamp': timestamp,
                'threat_detected': is_threat,
                'technical_details': self._extract_technical_details(input_data)
            }
            
            # Cache for later retrieval
            self.summary_cache.append(result)
            
            logger.info(f"Generated summary for {'threat' if is_threat else 'benign'} event")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                'summary': 'Error generating summary',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _summarize_benign(self, input_data: Dict[str, Any], confidence: float) -> str:
        """Generate summary for benign traffic."""
        source_ip = input_data.get('source_ip', 'unknown')
        dest_ip = input_data.get('destination_ip', 'unknown')
        dest_port = input_data.get('destination_port', 'unknown')
        protocol = input_data.get('protocol', 'unknown')
        
        port_desc = self.PORT_DESCRIPTIONS.get(dest_port, f'port {dest_port}')
        
        summary = (
            f"✅ NORMAL TRAFFIC: Connection from {source_ip} to {dest_ip} "
            f"on {port_desc} using {protocol} protocol appears legitimate. "
            f"The AI model classified this as benign traffic with "
            f"{(1 - confidence) * 100:.1f}% confidence."
        )
        
        return summary
    
    def _summarize_malicious(self, input_data: Dict[str, Any], 
                            confidence: float, severity: str) -> str:
        """Generate summary for malicious traffic."""
        source_ip = input_data.get('source_ip', 'unknown')
        dest_ip = input_data.get('destination_ip', 'unknown')
        dest_port = input_data.get('destination_port', 'unknown')
        protocol = input_data.get('protocol', 'unknown')
        
        # Infer attack type based on patterns
        attack_type = self._infer_attack_type(input_data)
        attack_desc = self.ATTACK_DESCRIPTIONS.get(attack_type, 'Unknown threat pattern')
        
        port_desc = self.PORT_DESCRIPTIONS.get(dest_port, f'port {dest_port}')
        
        summary = (
            f"🚨 THREAT DETECTED: {attack_desc} originating from {source_ip} "
            f"targeting {dest_ip} on {port_desc}. "
            f"Severity level is {severity} with {confidence * 100:.1f}% confidence. "
            f"Protocol: {protocol}."
        )
        
        return summary
    
    def _infer_attack_type(self, input_data: Dict[str, Any]) -> str:
        """
        Infer the type of attack based on traffic patterns.
        
        This is a simplified heuristic-based approach. In production,
        this would use more sophisticated ML-based classification.
        """
        dest_port = input_data.get('destination_port', 0)
        protocol = input_data.get('protocol', '').upper()
        packet_size = input_data.get('packet_size', 0)
        tcp_flags = input_data.get('tcp_flags', '').upper()
        
        # Port scanning detection
        if tcp_flags in ['SYN', 'FIN', 'NULL', 'XMAS']:
            return 'port_scan'
        
        # Potential DDoS based on small packets
        if packet_size < 100 and protocol in ['UDP', 'ICMP']:
            return 'ddos'
        
        # Database attacks
        if dest_port in [3306, 5432, 1433, 27017]:
            return 'sql_injection'
        
        # Web attacks
        if dest_port in [80, 443, 8080, 8443]:
            if packet_size > 5000:
                return 'xss'
            return 'unknown'
        
        # SSH/RDP brute force
        if dest_port in [22, 3389]:
            return 'brute_force'
        
        # SMB attacks (WannaCry-like)
        if dest_port == 445:
            return 'ransomware'
        
        return 'unknown'
    
    def _generate_recommendations(self, is_threat: bool, severity: str,
                                 input_data: Dict[str, Any], 
                                 confidence: float) -> List[str]:
        """Generate actionable recommendations based on the threat."""
        recommendations = []
        
        if not is_threat:
            recommendations.append("No immediate action required")
            recommendations.append("Continue monitoring normal traffic patterns")
            return recommendations
        
        source_ip = input_data.get('source_ip', 'unknown')
        dest_port = input_data.get('destination_port', 0)
        
        # Severity-based recommendations
        if severity == 'HIGH':
            recommendations.append(f"🔴 IMMEDIATE: Block IP address {source_ip} at firewall")
            recommendations.append("🔴 IMMEDIATE: Investigate all recent traffic from this source")
            recommendations.append("🔴 IMMEDIATE: Alert security team and escalate to SOC")
            recommendations.append("Review system logs for any signs of compromise")
        elif severity == 'MEDIUM':
            recommendations.append(f"🟡 URGENT: Add {source_ip} to monitoring watchlist")
            recommendations.append("🟡 URGENT: Review firewall rules for affected services")
            recommendations.append("Increase logging for this source")
            recommendations.append("Consider temporary rate limiting")
        elif severity == 'LOW':
            recommendations.append("Monitor the source IP for repeated attempts")
            recommendations.append("Log the event for future analysis")
            recommendations.append("No immediate blocking required")
        
        # Port-specific recommendations
        if dest_port in [22, 3389]:
            recommendations.append("Enable multi-factor authentication if not already active")
            recommendations.append("Review failed login attempts")
        elif dest_port in [3306, 5432, 1433]:
            recommendations.append("Review database query logs for anomalies")
            recommendations.append("Ensure database is not directly exposed to internet")
        elif dest_port in [80, 443, 8080, 8443]:
            recommendations.append("Check web application firewall (WAF) logs")
            recommendations.append("Review application logs for injection attempts")
        
        # Confidence-based recommendations
        if confidence < 0.7:
            recommendations.append("⚠️  Note: Lower confidence - manual review recommended")
        
        return recommendations
    
    def _extract_technical_details(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and format technical details for advanced users."""
        return {
            'source_ip': input_data.get('source_ip', 'N/A'),
            'source_port': input_data.get('source_port', 'N/A'),
            'destination_ip': input_data.get('destination_ip', 'N/A'),
            'destination_port': input_data.get('destination_port', 'N/A'),
            'protocol': input_data.get('protocol', 'N/A'),
            'packet_size': input_data.get('packet_size', 'N/A'),
            'payload_size': input_data.get('payload_size', 'N/A'),
            'tcp_flags': input_data.get('tcp_flags', 'N/A')
        }
    
    def summarize_batch(self, threat_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary report for multiple security events.
        
        Args:
            threat_list: List of threat data dictionaries
            
        Returns:
            Dictionary containing batch summary and statistics
        """
        if not threat_list:
            return {'error': 'No threats to summarize'}
        
        # Count threats by severity
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        threat_count = 0
        benign_count = 0
        unique_sources = set()
        unique_targets = set()
        
        summaries = []
        
        for threat in threat_list:
            # Get individual summary
            summary = self.summarize_threat(threat)
            summaries.append(summary)
            
            # Update statistics
            if threat.get('is_threat', False):
                threat_count += 1
                severity = threat.get('severity', 'INFO')
                severity_counts[severity] += 1
            else:
                benign_count += 1
            
            # Track IPs
            input_data = threat.get('input_data', {})
            if 'source_ip' in input_data:
                unique_sources.add(input_data['source_ip'])
            if 'destination_ip' in input_data:
                unique_targets.add(input_data['destination_ip'])
        
        # Generate executive summary
        total = len(threat_list)
        threat_percentage = (threat_count / total * 100) if total > 0 else 0
        
        executive_summary = (
            f"📊 SECURITY ANALYSIS SUMMARY:\n"
            f"Analyzed {total} network events. "
            f"Detected {threat_count} potential threats ({threat_percentage:.1f}%) "
            f"and {benign_count} benign connections.\n\n"
            f"Severity Breakdown:\n"
            f"  🔴 HIGH: {severity_counts['HIGH']} events\n"
            f"  🟡 MEDIUM: {severity_counts['MEDIUM']} events\n"
            f"  🟢 LOW: {severity_counts['LOW']} events\n"
            f"  ℹ️  INFO: {severity_counts['INFO']} events\n\n"
            f"Unique source IPs: {len(unique_sources)}\n"
            f"Unique target IPs: {len(unique_targets)}"
        )
        
        # Priority recommendations
        priority_recommendations = []
        if severity_counts['HIGH'] > 0:
            priority_recommendations.append(
                f"🔴 CRITICAL: {severity_counts['HIGH']} high-severity threats require immediate attention"
            )
        if severity_counts['MEDIUM'] > 5:
            priority_recommendations.append(
                f"🟡 WARNING: {severity_counts['MEDIUM']} medium-severity threats detected"
            )
        if threat_count > total * 0.3:
            priority_recommendations.append(
                "⚠️  High threat rate detected - consider network-wide security review"
            )
        if not priority_recommendations:
            priority_recommendations.append("✅ No critical issues detected")
        
        return {
            'executive_summary': executive_summary,
            'total_analyzed': total,
            'threat_count': threat_count,
            'benign_count': benign_count,
            'severity_distribution': severity_counts,
            'unique_source_ips': len(unique_sources),
            'unique_target_ips': len(unique_targets),
            'threat_percentage': threat_percentage,
            'priority_recommendations': priority_recommendations,
            'individual_summaries': summaries,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_summary_cache(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve cached summaries.
        
        Args:
            limit: Maximum number of summaries to return
            
        Returns:
            List of cached summaries
        """
        return self.summary_cache[-limit:]
    
    def clear_cache(self):
        """Clear the summary cache."""
        self.summary_cache = []
        logger.info("Summary cache cleared")
    
    def export_summaries(self, filepath: str):
        """
        Export summaries to a JSON file.
        
        Args:
            filepath: Path to output JSON file
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.summary_cache, f, indent=2)
            logger.info(f"Exported {len(self.summary_cache)} summaries to {filepath}")
        except Exception as e:
            logger.error(f"Error exporting summaries: {e}")
            raise
