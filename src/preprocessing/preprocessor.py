"""
Data preprocessing module for cybersecurity threat detection.
Handles data cleaning, transformation, and preparation for ML models.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess cybersecurity data for machine learning."""
    
    def __init__(self):
        """Initialize data preprocessor."""
        self.scaler = None
        self.label_encoders = {}
        self.feature_names = []
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the input data by handling missing values and duplicates.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info(f"Cleaning data with shape: {df.shape}")
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        # For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        logger.info(f"Cleaned data shape: {df.shape}")
        return df
    
    def encode_categorical_features(self, df: pd.DataFrame, 
                                    categorical_cols: list = None) -> pd.DataFrame:
        """
        Encode categorical features using label encoding.
        
        Args:
            df: Input DataFrame
            categorical_cols: List of categorical column names
            
        Returns:
            DataFrame with encoded categorical features
        """
        if categorical_cols is None:
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        logger.info(f"Encoding categorical features: {categorical_cols}")
        
        for col in categorical_cols:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def scale_features(self, X: pd.DataFrame, method: str = 'standard') -> np.ndarray:
        """
        Scale numeric features.
        
        Args:
            X: Input features DataFrame
            method: Scaling method ('standard' or 'minmax')
            
        Returns:
            Scaled feature array
        """
        logger.info(f"Scaling features using {method} method")
        
        if self.scaler is None:
            if method == 'standard':
                self.scaler = StandardScaler()
            elif method == 'minmax':
                self.scaler = MinMaxScaler()
            else:
                raise ValueError(f"Unknown scaling method: {method}")
            
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def prepare_features(self, df: pd.DataFrame, 
                        target_col: str = 'is_malicious',
                        drop_cols: list = None) -> tuple:
        """
        Prepare features and target variable for modeling.
        
        Args:
            df: Input DataFrame
            target_col: Name of the target column
            drop_cols: Columns to drop from features
            
        Returns:
            Tuple of (X, y) where X is features and y is target
        """
        logger.info("Preparing features for modeling")
        
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Drop specified columns and target
        if drop_cols is None:
            drop_cols = []
        
        # Add timestamp-like columns to drop list
        cols_to_drop = drop_cols + [target_col]
        cols_to_drop = [col for col in cols_to_drop if col in df.columns]
        
        # Drop timestamp if present
        if 'timestamp' in df.columns:
            cols_to_drop.append('timestamp')
        
        # Separate features and target
        y = df[target_col] if target_col in df.columns else None
        X = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        logger.info(f"Features shape: {X.shape}, Target shape: {y.shape if y is not None else 'None'}")
        
        return X, y
    
    def split_data(self, X, y, test_size: float = 0.2, random_state: int = 42):
        """
        Split data into training and testing sets.
        
        Args:
            X: Features
            y: Target variable
            test_size: Proportion of data for testing
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        logger.info(f"Splitting data with test_size={test_size}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def preprocess_pipeline(self, df: pd.DataFrame, 
                           target_col: str = 'is_malicious',
                           test_size: float = 0.2,
                           scaling_method: str = 'standard') -> dict:
        """
        Complete preprocessing pipeline.
        
        Args:
            df: Input DataFrame
            target_col: Name of target column
            test_size: Proportion of test data
            scaling_method: Method for feature scaling
            
        Returns:
            Dictionary containing processed data splits
        """
        logger.info("Starting preprocessing pipeline")
        
        # Clean data
        df = self.clean_data(df)
        
        # Encode categorical features
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if target_col in categorical_cols:
            categorical_cols.remove(target_col)
        if 'timestamp' in categorical_cols:
            categorical_cols.remove('timestamp')
        
        df = self.encode_categorical_features(df, categorical_cols)
        
        # Prepare features
        X, y = self.prepare_features(df, target_col)
        
        # Split data
        X_train, X_test, y_train, y_test = self.split_data(X, y, test_size)
        
        # Scale features
        X_train_scaled = self.scale_features(X_train, scaling_method)
        X_test_scaled = self.scale_features(X_test, scaling_method)
        
        logger.info("Preprocessing pipeline completed")
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train,
            'y_test': y_test,
            'feature_names': self.feature_names
        }
