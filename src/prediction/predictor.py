"""
Prediction service for real-time threat detection.
"""
import numpy as np
import pandas as pd
import joblib
import logging
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThreatPredictor:
    """Service for making threat predictions on new data."""
    
    def __init__(self, model_path: str = None, preprocessor_path: str = None):
        """
        Initialize threat predictor.
        
        Args:
            model_path: Path to trained model file
            preprocessor_path: Path to preprocessor file
        """
        self.model = None
        self.preprocessor = None
        self.threshold_high = 0.8
        self.threshold_medium = 0.5
        self.threshold_low = 0.3
        
        if model_path:
            self.load_model(model_path)
        if preprocessor_path:
            self.load_preprocessor(preprocessor_path)
    
    def load_model(self, model_path: str):
        """
        Load a trained model.
        
        Args:
            model_path: Path to the model file
        """
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def load_preprocessor(self, preprocessor_path: str):
        """
        Load a preprocessor.
        
        Args:
            preprocessor_path: Path to preprocessor file
        """
        try:
            self.preprocessor = joblib.load(preprocessor_path)
            logger.info(f"Preprocessor loaded from {preprocessor_path}")
        except Exception as e:
            logger.error(f"Error loading preprocessor: {e}")
            raise
    
    def set_thresholds(self, high: float = 0.8, medium: float = 0.5, low: float = 0.3):
        """
        Set severity thresholds.
        
        Args:
            high: Threshold for high severity
            medium: Threshold for medium severity
            low: Threshold for low severity
        """
        self.threshold_high = high
        self.threshold_medium = medium
        self.threshold_low = low
        logger.info(f"Thresholds set - High: {high}, Medium: {medium}, Low: {low}")
    
    def determine_severity(self, confidence: float) -> str:
        """
        Determine threat severity based on confidence score.
        
        Args:
            confidence: Prediction confidence score
            
        Returns:
            Severity level string
        """
        if confidence >= self.threshold_high:
            return "HIGH"
        elif confidence >= self.threshold_medium:
            return "MEDIUM"
        elif confidence >= self.threshold_low:
            return "LOW"
        else:
            return "INFO"
    
    def predict_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction for a single data point.
        
        Args:
            data: Dictionary containing traffic data
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Make prediction
        prediction = self.model.predict(df)[0]
        confidence = self.model.predict_proba(df)[0][1]
        
        # Determine severity
        severity = self.determine_severity(confidence)
        
        result = {
            'is_threat': bool(prediction),
            'confidence': float(confidence),
            'severity': severity,
            'timestamp': datetime.now().isoformat(),
            'input_data': data
        }
        
        logger.info(f"Prediction: {'THREAT' if prediction else 'BENIGN'}, "
                   f"Confidence: {confidence:.4f}, Severity: {severity}")
        
        return result
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Make predictions for multiple data points.
        
        Args:
            data_list: List of dictionaries containing traffic data
            
        Returns:
            List of prediction results
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Convert to DataFrame
        df = pd.DataFrame(data_list)
        
        # Make predictions
        predictions = self.model.predict(df)
        confidences = self.model.predict_proba(df)[:, 1]
        
        results = []
        for i, (pred, conf) in enumerate(zip(predictions, confidences)):
            severity = self.determine_severity(conf)
            result = {
                'is_threat': bool(pred),
                'confidence': float(conf),
                'severity': severity,
                'timestamp': datetime.now().isoformat(),
                'input_data': data_list[i]
            }
            results.append(result)
        
        threat_count = sum(1 for r in results if r['is_threat'])
        logger.info(f"Batch prediction completed: {threat_count}/{len(results)} threats detected")
        
        return results
    
    def predict_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on a DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with predictions added
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        df = df.copy()
        
        # Make predictions
        df['prediction'] = self.model.predict(df)
        df['confidence'] = self.model.predict_proba(df)[:, 1]
        df['severity'] = df['confidence'].apply(self.determine_severity)
        df['prediction_timestamp'] = datetime.now()
        
        threat_count = df['prediction'].sum()
        logger.info(f"DataFrame prediction completed: {threat_count}/{len(df)} threats detected")
        
        return df
    
    def analyze_threats(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze threat predictions and generate summary.
        
        Args:
            predictions: List of prediction results
            
        Returns:
            Analysis summary dictionary
        """
        total = len(predictions)
        threats = [p for p in predictions if p['is_threat']]
        threat_count = len(threats)
        
        # Count by severity
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        for pred in predictions:
            severity_counts[pred['severity']] += 1
        
        # Calculate average confidence
        avg_confidence = np.mean([p['confidence'] for p in predictions])
        
        # Calculate threat rate
        threat_rate = threat_count / total if total > 0 else 0
        
        summary = {
            'total_analyzed': total,
            'threat_count': threat_count,
            'benign_count': total - threat_count,
            'threat_rate': threat_rate,
            'average_confidence': avg_confidence,
            'severity_distribution': severity_counts,
            'high_severity_threats': severity_counts['HIGH'],
            'timestamp': datetime.now().isoformat()
        }
        
        return summary


class RealTimeThreatMonitor:
    """Monitor for real-time threat detection."""
    
    def __init__(self, predictor: ThreatPredictor):
        """
        Initialize real-time monitor.
        
        Args:
            predictor: ThreatPredictor instance
        """
        self.predictor = predictor
        self.alert_queue = []
        self.threat_history = []
    
    def process_traffic(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming traffic and detect threats.
        
        Args:
            traffic_data: Network traffic data
            
        Returns:
            Processing result with alert if threat detected
        """
        result = self.predictor.predict_single(traffic_data)
        
        # Add to history
        self.threat_history.append(result)
        
        # Generate alert if threat detected
        if result['is_threat'] and result['severity'] in ['HIGH', 'MEDIUM']:
            alert = {
                'alert_id': len(self.alert_queue) + 1,
                'severity': result['severity'],
                'confidence': result['confidence'],
                'source_ip': traffic_data.get('source_ip', 'unknown'),
                'destination_ip': traffic_data.get('destination_ip', 'unknown'),
                'timestamp': result['timestamp'],
                'message': f"{result['severity']} severity threat detected with {result['confidence']:.2%} confidence"
            }
            self.alert_queue.append(alert)
            logger.warning(f"ALERT: {alert['message']}")
        
        return result
    
    def get_active_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent active alerts.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        return self.alert_queue[-limit:]
    
    def clear_alerts(self):
        """Clear all alerts."""
        self.alert_queue = []
        logger.info("Alerts cleared")
    
    def get_threat_statistics(self) -> Dict[str, Any]:
        """
        Get statistics on detected threats.
        
        Returns:
            Dictionary of threat statistics
        """
        return self.predictor.analyze_threats(self.threat_history)
