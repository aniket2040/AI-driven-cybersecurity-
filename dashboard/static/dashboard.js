// Dashboard JavaScript - Real-time Updates and Visualizations

// Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1';
const UPDATE_INTERVAL = 5000; // Update every 5 seconds

// Chart instances
let threatTimelineChart = null;
let severityChart = null;
let protocolChart = null;

// Data storage
let threatHistory = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    initializeCharts();
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    // Start periodic updates
    updateDashboard();
    setInterval(updateDashboard, UPDATE_INTERVAL);
});

// Update current time display
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleString();
    document.getElementById('current-time').textContent = timeString;
}

// Initialize all charts
function initializeCharts() {
    // Threat Timeline Chart
    const timelineCtx = document.getElementById('threat-timeline-chart').getContext('2d');
    threatTimelineChart = new Chart(timelineCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Threats',
                data: [],
                borderColor: '#dc2626',
                backgroundColor: 'rgba(220, 38, 38, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Benign',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#f1f5f9'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#334155'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#334155'
                    }
                }
            }
        }
    });

    // Severity Distribution Chart
    const severityCtx = document.getElementById('severity-chart').getContext('2d');
    severityChart = new Chart(severityCtx, {
        type: 'doughnut',
        data: {
            labels: ['High', 'Medium', 'Low', 'Info'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: [
                    '#dc2626',
                    '#f59e0b',
                    '#06b6d4',
                    '#10b981'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#f1f5f9'
                    }
                }
            }
        }
    });

    // Protocol Distribution Chart
    const protocolCtx = document.getElementById('protocol-chart').getContext('2d');
    protocolChart = new Chart(protocolCtx, {
        type: 'bar',
        data: {
            labels: ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS'],
            datasets: [{
                label: 'Protocol Usage',
                data: [0, 0, 0, 0, 0],
                backgroundColor: '#2563eb'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#334155'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#334155'
                    }
                }
            }
        }
    });
}

// Main dashboard update function
async function updateDashboard() {
    try {
        // Update statistics
        await updateStatistics();
        
        // Update alerts
        await updateAlerts();
        
        // Update AI summaries
        await updateAISummaries();
        
        // Update last update time
        document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
        showAlert('Connection error. Retrying...', 'warning');
    }
}

// Update statistics cards and charts
async function updateStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        if (!response.ok) {
            throw new Error('Failed to fetch statistics');
        }
        
        const data = await response.json();
        
        // Update summary cards
        document.getElementById('total-events').textContent = data.total_analyzed || 0;
        document.getElementById('threat-count').textContent = data.threat_count || 0;
        
        const threatPercentage = data.threat_rate ? (data.threat_rate * 100).toFixed(1) : 0;
        document.getElementById('threat-percentage').textContent = `${threatPercentage}% of traffic`;
        
        document.getElementById('high-severity').textContent = 
            data.severity_distribution?.HIGH || 0;
        
        // Update severity chart
        if (data.severity_distribution) {
            severityChart.data.datasets[0].data = [
                data.severity_distribution.HIGH || 0,
                data.severity_distribution.MEDIUM || 0,
                data.severity_distribution.LOW || 0,
                data.severity_distribution.INFO || 0
            ];
            severityChart.update();
        }
        
        // Update timeline chart (simulated data for demo)
        updateTimelineChart(data);
        
    } catch (error) {
        console.error('Error updating statistics:', error);
    }
}

// Update timeline chart
function updateTimelineChart(data) {
    const now = new Date();
    const timeLabel = now.toLocaleTimeString();
    
    // Add new data point
    if (threatTimelineChart.data.labels.length > 20) {
        threatTimelineChart.data.labels.shift();
        threatTimelineChart.data.datasets[0].data.shift();
        threatTimelineChart.data.datasets[1].data.shift();
    }
    
    threatTimelineChart.data.labels.push(timeLabel);
    threatTimelineChart.data.datasets[0].data.push(data.threat_count || 0);
    threatTimelineChart.data.datasets[1].data.push(data.benign_count || 0);
    threatTimelineChart.update();
}

// Update alerts
async function updateAlerts() {
    try {
        const response = await fetch(`${API_BASE_URL}/alerts?limit=10`);
        if (!response.ok) {
            throw new Error('Failed to fetch alerts');
        }
        
        const data = await response.json();
        const alertsContainer = document.getElementById('alerts-container');
        
        if (!data.alerts || data.alerts.length === 0) {
            alertsContainer.innerHTML = '<p class="no-data">No active alerts</p>';
            return;
        }
        
        alertsContainer.innerHTML = data.alerts.map(alert => `
            <div class="alert-item ${alert.severity.toLowerCase()}">
                <div class="alert-item-header">
                    <span class="alert-severity ${alert.severity.toLowerCase()}">${alert.severity}</span>
                    <span class="alert-time">${new Date(alert.timestamp).toLocaleTimeString()}</span>
                </div>
                <div class="alert-message">
                    ${alert.message}
                    <br>
                    <small>${alert.source_ip} → ${alert.destination_ip}</small>
                </div>
            </div>
        `).join('');
        
        // Show critical alert banner if HIGH severity exists
        const highSeverityAlert = data.alerts.find(a => a.severity === 'HIGH');
        if (highSeverityAlert) {
            showAlert(`CRITICAL: ${highSeverityAlert.message}`, 'danger');
        }
        
    } catch (error) {
        console.error('Error updating alerts:', error);
    }
}

// Update AI summaries
async function updateAISummaries() {
    try {
        const response = await fetch(`${API_BASE_URL}/summaries?limit=5`);
        if (!response.ok) {
            throw new Error('Failed to fetch summaries');
        }
        
        const data = await response.json();
        const summariesContainer = document.getElementById('ai-summaries');
        
        if (!data.summaries || data.summaries.length === 0) {
            summariesContainer.innerHTML = '<p class="no-data">Waiting for security events...</p>';
            return;
        }
        
        summariesContainer.innerHTML = data.summaries.map(summary => {
            const severityClass = summary.threat_detected ? 'danger' : 'success';
            return `
                <div class="ai-summary-item">
                    <div class="ai-summary-header">
                        <span class="ai-summary-severity ${severityClass}">${summary.severity_description}</span>
                        <span class="alert-time">${new Date(summary.timestamp).toLocaleString()}</span>
                    </div>
                    <div class="ai-summary-text">
                        ${summary.summary}
                    </div>
                    <div class="ai-summary-confidence">
                        <strong>Confidence:</strong> ${summary.confidence_percentage}
                    </div>
                    ${summary.recommendations && summary.recommendations.length > 0 ? `
                        <div class="ai-recommendations">
                            <h4>Recommendations:</h4>
                            <ul>
                                ${summary.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Error updating AI summaries:', error);
    }
}

// Show alert banner
function showAlert(message, type = 'info') {
    const alertBanner = document.getElementById('alert-banner');
    const alertMessage = document.getElementById('alert-message');
    
    alertMessage.textContent = message;
    alertBanner.classList.remove('hidden');
    
    // Auto-dismiss after 10 seconds
    setTimeout(() => {
        alertBanner.classList.add('hidden');
    }, 10000);
}

// Dismiss alert banner
function dismissAlert() {
    document.getElementById('alert-banner').classList.add('hidden');
}

// Simulate real-time data for demo purposes
// In production, this would come from actual API calls
function simulateRecentThreats() {
    const threatsContainer = document.getElementById('recent-threats');
    const sampleThreats = [
        {
            ip: '192.168.1.100',
            confidence: 0.95,
            details: 'Port scanning attempt on port 22',
            time: new Date()
        },
        {
            ip: '10.0.0.50',
            confidence: 0.87,
            details: 'Suspicious SQL query pattern',
            time: new Date(Date.now() - 120000)
        }
    ];
    
    threatsContainer.innerHTML = sampleThreats.map(threat => `
        <div class="threat-item">
            <div class="threat-header">
                <span class="threat-ip">${threat.ip}</span>
                <span class="threat-confidence">${(threat.confidence * 100).toFixed(1)}%</span>
            </div>
            <div class="threat-details">
                ${threat.details}
                <br>
                <small>${threat.time.toLocaleTimeString()}</small>
            </div>
        </div>
    `).join('');
}

// Update protocol chart with simulated data
function updateProtocolChart() {
    // Simulate protocol distribution
    protocolChart.data.datasets[0].data = [
        Math.floor(Math.random() * 100) + 50,
        Math.floor(Math.random() * 50) + 20,
        Math.floor(Math.random() * 30) + 10,
        Math.floor(Math.random() * 80) + 40,
        Math.floor(Math.random() * 60) + 30
    ];
    protocolChart.update();
}

// Initial call for demo data
setTimeout(() => {
    simulateRecentThreats();
    updateProtocolChart();
}, 1000);
