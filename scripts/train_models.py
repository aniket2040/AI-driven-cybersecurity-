"""
Main training script for cybersecurity threat detection models.
Orchestrates the complete ML pipeline from data loading to model evaluation.
"""
import sys
import os
import logging
from datetime import datetime

# Add src to path for development
# Note: In production, install as a package or use PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collection.collector import load_sample_threat_data
from src.preprocessing.preprocessor import DataPreprocessor
from src.feature_engineering.engineer import FeatureEngineer
from src.model_training.trainer import (
    ModelTrainer, RandomForestModel, GradientBoostingModel,
    NeuralNetworkModel, SVMModel
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main training pipeline."""
    logger.info("="*80)
    logger.info("Starting Cybersecurity Threat Detection Training Pipeline")
    logger.info("="*80)
    
    # Step 1: Load data
    logger.info("\n[1/6] Loading data...")
    df = load_sample_threat_data()
    logger.info(f"Loaded dataset with shape: {df.shape}")
    
    # Step 2: Feature Engineering
    logger.info("\n[2/6] Engineering features...")
    feature_engineer = FeatureEngineer()
    df_engineered = feature_engineer.engineer_features_pipeline(
        df, 
        include_statistical=False,  # Disable for sample data
        include_temporal=False       # Disable for sample data
    )
    logger.info(f"Feature engineering complete. Shape: {df_engineered.shape}")
    
    # Step 3: Preprocessing
    logger.info("\n[3/6] Preprocessing data...")
    preprocessor = DataPreprocessor()
    data = preprocessor.preprocess_pipeline(
        df_engineered,
        target_col='is_malicious',
        test_size=0.2,
        scaling_method='standard'
    )
    
    X_train = data['X_train']
    X_test = data['X_test']
    y_train = data['y_train']
    y_test = data['y_test']
    
    logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
    
    # Step 4: Model Training
    logger.info("\n[4/6] Training models...")
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Add models to trainer
    logger.info("Adding models to trainer...")
    trainer.add_model(RandomForestModel(n_estimators=100, max_depth=20, random_state=42))
    trainer.add_model(GradientBoostingModel(n_estimators=100, learning_rate=0.1, random_state=42))
    trainer.add_model(NeuralNetworkModel(hidden_layers=(64, 32), max_iter=100, random_state=42))
    # Note: SVM can be slow on large datasets, uncomment if needed
    # trainer.add_model(SVMModel(kernel='rbf', C=1.0, random_state=42))
    
    # Train all models
    trainer.train_all(X_train, y_train)
    
    # Step 5: Model Evaluation
    logger.info("\n[5/6] Evaluating models...")
    results = trainer.evaluate_all(X_test, y_test)
    
    # Display comparison
    logger.info("\n" + "="*80)
    logger.info("MODEL COMPARISON")
    logger.info("="*80)
    comparison_df = trainer.get_comparison_dataframe()
    logger.info("\n" + comparison_df.to_string(index=False))
    
    # Display best model
    logger.info("\n" + "="*80)
    logger.info(f"BEST MODEL: {trainer.best_model_name}")
    logger.info(f"Best F1-Score: {trainer.best_score:.4f}")
    logger.info("="*80)
    
    # Step 6: Save models
    logger.info("\n[6/6] Saving models...")
    saved_paths = trainer.save_all_models('models/trained')
    for model_name, path in saved_paths.items():
        logger.info(f"  {model_name}: {path}")
    
    # Display detailed metrics for best model
    if trainer.best_model:
        logger.info("\n" + "="*80)
        logger.info(f"DETAILED METRICS FOR {trainer.best_model_name}")
        logger.info("="*80)
        best_metrics = trainer.best_model.metrics
        logger.info(f"Accuracy:  {best_metrics['accuracy']:.4f}")
        logger.info(f"Precision: {best_metrics['precision']:.4f}")
        logger.info(f"Recall:    {best_metrics['recall']:.4f}")
        logger.info(f"F1-Score:  {best_metrics['f1_score']:.4f}")
        logger.info(f"ROC-AUC:   {best_metrics['roc_auc']:.4f}")
        logger.info(f"\nConfusion Matrix:\n{best_metrics['confusion_matrix']}")
        logger.info(f"\nClassification Report:\n{best_metrics['classification_report']}")
    
    logger.info("\n" + "="*80)
    logger.info("Training pipeline completed successfully!")
    logger.info("="*80)
    
    return trainer


if __name__ == '__main__':
    try:
        trainer = main()
        logger.info("\nTraining completed. Models are ready for deployment.")
    except Exception as e:
        logger.error(f"Training pipeline failed: {e}", exc_info=True)
        sys.exit(1)
