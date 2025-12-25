-- Cybersecurity Threat Database Schema
-- Database: cyber_threat_db

-- Table for storing threat data
CREATE TABLE IF NOT EXISTS threats (
    threat_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_ip VARCHAR(45),
    destination_ip VARCHAR(45),
    source_port INTEGER,
    destination_port INTEGER,
    protocol VARCHAR(10),
    attack_type VARCHAR(100),
    severity_level VARCHAR(20),
    threat_score DECIMAL(5,2),
    is_malicious BOOLEAN DEFAULT FALSE,
    detection_confidence DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for network traffic logs
CREATE TABLE IF NOT EXISTS network_traffic (
    traffic_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    source_ip VARCHAR(45) NOT NULL,
    destination_ip VARCHAR(45) NOT NULL,
    source_port INTEGER,
    destination_port INTEGER,
    protocol VARCHAR(10),
    packet_size INTEGER,
    flags VARCHAR(50),
    payload_size INTEGER,
    tcp_flags VARCHAR(20),
    http_method VARCHAR(10),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for threat predictions
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id SERIAL PRIMARY KEY,
    traffic_id INTEGER REFERENCES network_traffic(traffic_id),
    model_name VARCHAR(100),
    prediction_label VARCHAR(100),
    confidence_score DECIMAL(5,2),
    feature_importance JSONB,
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for model performance metrics
CREATE TABLE IF NOT EXISTS model_metrics (
    metric_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100),
    accuracy DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    auc_score DECIMAL(5,2),
    training_date TIMESTAMP,
    dataset_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for attack signatures
CREATE TABLE IF NOT EXISTS attack_signatures (
    signature_id SERIAL PRIMARY KEY,
    attack_name VARCHAR(100) NOT NULL,
    attack_category VARCHAR(50),
    pattern_description TEXT,
    indicators JSONB,
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for system alerts
CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    threat_id INTEGER REFERENCES threats(threat_id),
    alert_level VARCHAR(20),
    alert_message TEXT,
    is_acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_threats_timestamp ON threats(timestamp);
CREATE INDEX idx_threats_severity ON threats(severity_level);
CREATE INDEX idx_network_timestamp ON network_traffic(timestamp);
CREATE INDEX idx_network_source_ip ON network_traffic(source_ip);
CREATE INDEX idx_predictions_model ON predictions(model_name);
CREATE INDEX idx_alerts_level ON alerts(alert_level);

-- Create view for threat summary
CREATE VIEW threat_summary AS
SELECT 
    DATE(timestamp) as date,
    attack_type,
    severity_level,
    COUNT(*) as threat_count,
    AVG(threat_score) as avg_threat_score,
    SUM(CASE WHEN is_malicious = TRUE THEN 1 ELSE 0 END) as malicious_count
FROM threats
GROUP BY DATE(timestamp), attack_type, severity_level;

-- Create view for model performance comparison
CREATE VIEW model_performance_comparison AS
SELECT 
    model_name,
    MAX(accuracy) as best_accuracy,
    MAX(f1_score) as best_f1,
    MAX(auc_score) as best_auc,
    MAX(training_date) as latest_training
FROM model_metrics
GROUP BY model_name;

-- Table for AI-generated security event summaries
CREATE TABLE IF NOT EXISTS ai_summaries (
    summary_id SERIAL PRIMARY KEY,
    threat_id INTEGER REFERENCES threats(threat_id),
    summary_text TEXT NOT NULL,
    severity_description VARCHAR(100),
    confidence_percentage VARCHAR(10),
    recommendations JSONB,
    technical_details JSONB,
    threat_detected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for dashboard real-time data
CREATE TABLE IF NOT EXISTS dashboard_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metric_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Table for threat summaries by time period
CREATE TABLE IF NOT EXISTS threat_time_series (
    ts_id SERIAL PRIMARY KEY,
    time_bucket TIMESTAMP NOT NULL,
    threat_count INTEGER DEFAULT 0,
    high_severity_count INTEGER DEFAULT 0,
    medium_severity_count INTEGER DEFAULT 0,
    low_severity_count INTEGER DEFAULT 0,
    unique_source_ips INTEGER DEFAULT 0,
    avg_confidence DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for new tables
CREATE INDEX idx_ai_summaries_threat_id ON ai_summaries(threat_id);
CREATE INDEX idx_ai_summaries_created_at ON ai_summaries(created_at);
CREATE INDEX idx_dashboard_metrics_timestamp ON dashboard_metrics(timestamp);
CREATE INDEX idx_dashboard_metrics_name ON dashboard_metrics(metric_name);
CREATE INDEX idx_threat_time_series_bucket ON threat_time_series(time_bucket);

-- Create view for dashboard summary
CREATE VIEW dashboard_summary AS
SELECT 
    DATE(t.timestamp) as date,
    COUNT(*) as total_events,
    SUM(CASE WHEN t.is_malicious = TRUE THEN 1 ELSE 0 END) as threat_count,
    SUM(CASE WHEN t.severity_level = 'HIGH' THEN 1 ELSE 0 END) as high_severity,
    SUM(CASE WHEN t.severity_level = 'MEDIUM' THEN 1 ELSE 0 END) as medium_severity,
    SUM(CASE WHEN t.severity_level = 'LOW' THEN 1 ELSE 0 END) as low_severity,
    AVG(t.detection_confidence) as avg_confidence,
    COUNT(DISTINCT t.source_ip) as unique_sources
FROM threats t
GROUP BY DATE(t.timestamp)
ORDER BY date DESC;
