"""
Feature engineering module for cybersecurity threat detection.
Creates derived features and performs feature selection.
"""
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Engineer features for threat detection models."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.selected_features = None
    
    def create_network_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived network-based features.
        
        Args:
            df: Input DataFrame with network traffic data
            
        Returns:
            DataFrame with additional features
        """
        logger.info("Creating network-based features")
        
        df = df.copy()
        
        # Port-based features
        if 'source_port' in df.columns:
            df['is_privileged_src_port'] = (df['source_port'] < 1024).astype(int)
        
        if 'destination_port' in df.columns:
            df['is_privileged_dst_port'] = (df['destination_port'] < 1024).astype(int)
            df['is_common_port'] = df['destination_port'].isin([80, 443, 22, 21, 23, 25]).astype(int)
        
        # Packet size features
        if 'packet_size' in df.columns and 'payload_size' in df.columns:
            df['header_size'] = df['packet_size'] - df['payload_size']
            df['payload_ratio'] = df['payload_size'] / (df['packet_size'] + 1)
            df['is_large_packet'] = (df['packet_size'] > 1000).astype(int)
        
        # Protocol-based features
        if 'protocol' in df.columns:
            df['is_tcp'] = (df['protocol'] == 'TCP').astype(int)
            df['is_udp'] = (df['protocol'] == 'UDP').astype(int)
            df['is_icmp'] = (df['protocol'] == 'ICMP').astype(int)
        
        logger.info(f"Created network features. New shape: {df.shape}")
        
        return df
    
    def create_statistical_features(self, df: pd.DataFrame, 
                                    group_by: str = 'source_ip',
                                    window: int = 10) -> pd.DataFrame:
        """
        Create statistical features based on grouped data.
        
        Args:
            df: Input DataFrame
            group_by: Column to group by
            window: Window size for rolling statistics
            
        Returns:
            DataFrame with statistical features
        """
        logger.info(f"Creating statistical features grouped by {group_by}")
        
        df = df.copy()
        
        # Ensure we have a sortable index
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp')
        
        # Count-based features
        if group_by in df.columns:
            df[f'{group_by}_count'] = df.groupby(group_by).cumcount() + 1
        
        # Numeric columns for statistics
        numeric_cols = ['packet_size', 'payload_size', 'source_port', 'destination_port']
        available_cols = [col for col in numeric_cols if col in df.columns]
        
        for col in available_cols:
            if group_by in df.columns:
                # Rolling mean
                df[f'{col}_rolling_mean'] = df.groupby(group_by)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
                
                # Rolling std
                df[f'{col}_rolling_std'] = df.groupby(group_by)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).std()
                )
        
        # Fill NaN values that might result from rolling calculations
        df = df.fillna(0)
        
        logger.info(f"Created statistical features. New shape: {df.shape}")
        
        return df
    
    def create_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create time-based features from timestamp.
        
        Args:
            df: Input DataFrame with timestamp column
            
        Returns:
            DataFrame with temporal features
        """
        if 'timestamp' not in df.columns:
            logger.warning("No timestamp column found, skipping temporal features")
            return df
        
        logger.info("Creating temporal features")
        
        df = df.copy()
        
        # Convert timestamp to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract time components
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 17)).astype(int)
        df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
        
        logger.info(f"Created temporal features. New shape: {df.shape}")
        
        return df
    
    def select_features(self, X, y, k: int = 20, method: str = 'mutual_info') -> np.ndarray:
        """
        Select top k features based on statistical tests.
        
        Args:
            X: Feature matrix
            y: Target variable
            k: Number of features to select
            method: Selection method ('chi2' or 'mutual_info')
            
        Returns:
            Selected feature matrix
        """
        logger.info(f"Selecting top {k} features using {method}")
        
        # Ensure k doesn't exceed number of features
        k = min(k, X.shape[1])
        
        if method == 'chi2':
            # Chi2 requires non-negative features
            X_positive = X - X.min() + 1
            selector = SelectKBest(chi2, k=k)
        elif method == 'mutual_info':
            selector = SelectKBest(mutual_info_classif, k=k)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        X_selected = selector.fit_transform(X, y)
        self.selected_features = selector.get_support(indices=True)
        
        logger.info(f"Selected {X_selected.shape[1]} features")
        
        return X_selected
    
    def get_feature_importance_scores(self, X, y, method: str = 'mutual_info') -> pd.DataFrame:
        """
        Get feature importance scores.
        
        Args:
            X: Feature matrix
            y: Target variable
            method: Scoring method
            
        Returns:
            DataFrame with feature scores
        """
        if method == 'mutual_info':
            scores = mutual_info_classif(X, y)
        elif method == 'chi2':
            X_positive = X - X.min() + 1
            scores = chi2(X_positive, y)[0]
        else:
            raise ValueError(f"Unknown method: {method}")
        
        feature_scores = pd.DataFrame({
            'feature_idx': range(len(scores)),
            'importance_score': scores
        }).sort_values('importance_score', ascending=False)
        
        return feature_scores
    
    def engineer_features_pipeline(self, df: pd.DataFrame, 
                                  include_statistical: bool = True,
                                  include_temporal: bool = True) -> pd.DataFrame:
        """
        Complete feature engineering pipeline.
        
        Args:
            df: Input DataFrame
            include_statistical: Whether to include statistical features
            include_temporal: Whether to include temporal features
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Starting feature engineering pipeline")
        
        # Create network features
        df = self.create_network_features(df)
        
        # Create temporal features
        if include_temporal and 'timestamp' in df.columns:
            df = self.create_temporal_features(df)
        
        # Create statistical features
        if include_statistical and 'source_ip' in df.columns:
            df = self.create_statistical_features(df)
        
        logger.info(f"Feature engineering complete. Final shape: {df.shape}")
        
        return df
