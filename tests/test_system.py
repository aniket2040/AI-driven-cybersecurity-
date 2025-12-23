"""
Unit tests for the cybersecurity threat detection system.
"""
import pytest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_collection.collector import load_sample_threat_data, StaticDataLoader, LiveDataCollector
from preprocessing.preprocessor import DataPreprocessor
from feature_engineering.engineer import FeatureEngineer


class TestDataCollection:
    """Test data collection functionality."""
    
    def test_load_sample_data(self):
        """Test sample data generation."""
        df = load_sample_threat_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1000
        assert 'source_ip' in df.columns
        assert 'is_malicious' in df.columns
        assert df['is_malicious'].dtype in [np.int64, np.int32, int]
    
    def test_live_data_collector_initialization(self):
        """Test live data collector initialization."""
        collector = LiveDataCollector(interface='eth0')
        
        assert collector.interface == 'eth0'
        assert isinstance(collector.captured_packets, list)
        assert len(collector.captured_packets) == 0
    
    def test_live_data_collector_capture(self):
        """Test packet capture simulation."""
        collector = LiveDataCollector()
        collector.start_capture(packet_count=10)
        
        df = collector.get_captured_data()
        assert len(df) == 10
        assert 'source_ip' in df.columns
        assert 'protocol' in df.columns


class TestPreprocessing:
    """Test data preprocessing functionality."""
    
    def test_preprocessor_initialization(self):
        """Test preprocessor initialization."""
        preprocessor = DataPreprocessor()
        
        assert preprocessor.scaler is None
        assert isinstance(preprocessor.label_encoders, dict)
        assert isinstance(preprocessor.feature_names, list)
    
    def test_clean_data(self):
        """Test data cleaning."""
        preprocessor = DataPreprocessor()
        
        # Create sample data with issues
        df = pd.DataFrame({
            'col1': [1, 2, 2, 3, np.nan],
            'col2': ['a', 'b', 'b', 'c', None]
        })
        
        cleaned = preprocessor.clean_data(df)
        
        assert cleaned['col1'].isnull().sum() == 0
        assert cleaned['col2'].isnull().sum() == 0
        assert len(cleaned) <= len(df)  # Duplicates removed
    
    def test_encode_categorical(self):
        """Test categorical encoding."""
        preprocessor = DataPreprocessor()
        
        df = pd.DataFrame({
            'protocol': ['TCP', 'UDP', 'TCP', 'ICMP'],
            'value': [1, 2, 3, 4]
        })
        
        encoded = preprocessor.encode_categorical_features(df, ['protocol'])
        
        assert encoded['protocol'].dtype in [np.int64, np.int32, int]
        assert 'protocol' in preprocessor.label_encoders


class TestFeatureEngineering:
    """Test feature engineering functionality."""
    
    def test_feature_engineer_initialization(self):
        """Test feature engineer initialization."""
        engineer = FeatureEngineer()
        
        assert engineer.selected_features is None
    
    def test_create_network_features(self):
        """Test network feature creation."""
        engineer = FeatureEngineer()
        
        df = pd.DataFrame({
            'source_port': [80, 443, 8080],
            'destination_port': [12345, 443, 22],
            'packet_size': [1000, 500, 1500],
            'payload_size': [800, 300, 1200],
            'protocol': ['TCP', 'UDP', 'TCP']
        })
        
        result = engineer.create_network_features(df)
        
        assert 'is_privileged_src_port' in result.columns
        assert 'is_common_port' in result.columns
        assert 'payload_ratio' in result.columns
        assert len(result.columns) > len(df.columns)
    
    def test_create_temporal_features(self):
        """Test temporal feature creation."""
        engineer = FeatureEngineer()
        
        df = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=5, freq='H'),
            'value': [1, 2, 3, 4, 5]
        })
        
        result = engineer.create_temporal_features(df)
        
        assert 'hour' in result.columns
        assert 'day_of_week' in result.columns
        assert 'is_weekend' in result.columns


class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_full_preprocessing_pipeline(self):
        """Test complete preprocessing pipeline."""
        # Generate sample data
        df = load_sample_threat_data()
        
        # Preprocess
        preprocessor = DataPreprocessor()
        result = preprocessor.preprocess_pipeline(
            df,
            target_col='is_malicious',
            test_size=0.2
        )
        
        # Verify results
        assert 'X_train' in result
        assert 'X_test' in result
        assert 'y_train' in result
        assert 'y_test' in result
        assert result['X_train'].shape[0] == 800  # 80% of 1000
        assert result['X_test'].shape[0] == 200   # 20% of 1000
    
    def test_feature_engineering_pipeline(self):
        """Test feature engineering pipeline."""
        # Generate sample data
        df = load_sample_threat_data()
        
        # Engineer features
        engineer = FeatureEngineer()
        result = engineer.engineer_features_pipeline(
            df,
            include_statistical=False,
            include_temporal=False
        )
        
        # Verify features added
        assert result.shape[1] > df.shape[1]
        assert 'is_privileged_src_port' in result.columns or result.shape[1] > df.shape[1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
