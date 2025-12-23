"""
Model training module for cybersecurity threat detection.
Supports multiple ML algorithms including Random Forest, Gradient Boosting, 
Neural Networks, and SVM.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, classification_report, 
                             confusion_matrix)
import joblib
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThreatDetectionModel:
    """Base class for threat detection models."""
    
    def __init__(self, model_name: str):
        """
        Initialize threat detection model.
        
        Args:
            model_name: Name of the model
        """
        self.model_name = model_name
        self.model = None
        self.metrics = {}
        self.training_date = None
    
    def train(self, X_train, y_train):
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        logger.info(f"Training {self.model_name} model...")
        self.training_date = datetime.now()
        self.model.fit(X_train, y_train)
        logger.info(f"{self.model_name} training completed")
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predict probabilities.
        
        Args:
            X: Input features
            
        Returns:
            Prediction probabilities
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            # For models without predict_proba, return binary predictions
            predictions = self.model.predict(X)
            return np.column_stack([1 - predictions, predictions])
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance.
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info(f"Evaluating {self.model_name} model...")
        
        y_pred = self.predict(X_test)
        y_pred_proba = self.predict_proba(X_test)[:, 1]
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='binary'),
            'recall': recall_score(y_test, y_pred, average='binary'),
            'f1_score': f1_score(y_test, y_pred, average='binary'),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred)
        }
        
        logger.info(f"{self.model_name} Accuracy: {self.metrics['accuracy']:.4f}")
        logger.info(f"{self.model_name} F1-Score: {self.metrics['f1_score']:.4f}")
        logger.info(f"{self.model_name} ROC-AUC: {self.metrics['roc_auc']:.4f}")
        
        return self.metrics
    
    def save_model(self, output_dir: str = 'models/trained'):
        """
        Save trained model to disk.
        
        Args:
            output_dir: Directory to save the model
        """
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{self.model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        joblib.dump(self.model, filename)
        logger.info(f"Model saved to {filename}")
        return filename
    
    def load_model(self, filepath: str):
        """
        Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
        """
        self.model = joblib.load(filepath)
        logger.info(f"Model loaded from {filepath}")


class RandomForestModel(ThreatDetectionModel):
    """Random Forest classifier for threat detection."""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 20, 
                 min_samples_split: int = 5, random_state: int = 42):
        """
        Initialize Random Forest model.
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum depth of trees
            min_samples_split: Minimum samples to split a node
            random_state: Random seed
        """
        super().__init__("RandomForest")
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=random_state,
            n_jobs=-1
        )


class GradientBoostingModel(ThreatDetectionModel):
    """Gradient Boosting classifier for threat detection."""
    
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1,
                 max_depth: int = 5, random_state: int = 42):
        """
        Initialize Gradient Boosting model.
        
        Args:
            n_estimators: Number of boosting stages
            learning_rate: Learning rate
            max_depth: Maximum depth of trees
            random_state: Random seed
        """
        super().__init__("GradientBoosting")
        self.model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state
        )


class NeuralNetworkModel(ThreatDetectionModel):
    """Neural Network classifier for threat detection."""
    
    def __init__(self, hidden_layers: tuple = (128, 64, 32), 
                 learning_rate: float = 0.001, max_iter: int = 200,
                 random_state: int = 42):
        """
        Initialize Neural Network model.
        
        Args:
            hidden_layers: Tuple of hidden layer sizes
            learning_rate: Learning rate for optimization
            max_iter: Maximum number of iterations
            random_state: Random seed
        """
        super().__init__("NeuralNetwork")
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            learning_rate_init=learning_rate,
            max_iter=max_iter,
            random_state=random_state,
            early_stopping=True,
            validation_fraction=0.1
        )


class SVMModel(ThreatDetectionModel):
    """Support Vector Machine classifier for threat detection."""
    
    def __init__(self, kernel: str = 'rbf', C: float = 1.0, 
                 gamma: str = 'auto', random_state: int = 42):
        """
        Initialize SVM model.
        
        Args:
            kernel: Kernel type
            C: Regularization parameter
            gamma: Kernel coefficient
            random_state: Random seed
        """
        super().__init__("SVM")
        self.model = SVC(
            kernel=kernel,
            C=C,
            gamma=gamma,
            random_state=random_state,
            probability=True
        )


class ModelTrainer:
    """Manager for training and comparing multiple models."""
    
    def __init__(self):
        """Initialize model trainer."""
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.best_score = 0
    
    def add_model(self, model: ThreatDetectionModel):
        """
        Add a model to the trainer.
        
        Args:
            model: ThreatDetectionModel instance
        """
        self.models[model.model_name] = model
        logger.info(f"Added {model.model_name} to trainer")
    
    def train_all(self, X_train, y_train):
        """
        Train all models.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        logger.info(f"Training {len(self.models)} models...")
        
        for model_name, model in self.models.items():
            try:
                model.train(X_train, y_train)
            except Exception as e:
                logger.error(f"Error training {model_name}: {e}")
    
    def evaluate_all(self, X_test, y_test):
        """
        Evaluate all models and find the best one.
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of model metrics
        """
        logger.info(f"Evaluating {len(self.models)} models...")
        
        results = {}
        for model_name, model in self.models.items():
            try:
                metrics = model.evaluate(X_test, y_test)
                results[model_name] = metrics
                
                # Track best model based on F1-score
                if metrics['f1_score'] > self.best_score:
                    self.best_score = metrics['f1_score']
                    self.best_model = model
                    self.best_model_name = model_name
            except Exception as e:
                logger.error(f"Error evaluating {model_name}: {e}")
        
        logger.info(f"Best model: {self.best_model_name} with F1-score: {self.best_score:.4f}")
        
        return results
    
    def save_all_models(self, output_dir: str = 'models/trained'):
        """
        Save all trained models.
        
        Args:
            output_dir: Directory to save models
        """
        saved_paths = {}
        for model_name, model in self.models.items():
            try:
                path = model.save_model(output_dir)
                saved_paths[model_name] = path
            except Exception as e:
                logger.error(f"Error saving {model_name}: {e}")
        
        return saved_paths
    
    def get_comparison_dataframe(self):
        """
        Get a comparison DataFrame of all model metrics.
        
        Returns:
            DataFrame with model comparison
        """
        comparison_data = []
        
        for model_name, model in self.models.items():
            if model.metrics:
                comparison_data.append({
                    'Model': model_name,
                    'Accuracy': model.metrics['accuracy'],
                    'Precision': model.metrics['precision'],
                    'Recall': model.metrics['recall'],
                    'F1-Score': model.metrics['f1_score'],
                    'ROC-AUC': model.metrics['roc_auc']
                })
        
        return pd.DataFrame(comparison_data).sort_values('F1-Score', ascending=False)
