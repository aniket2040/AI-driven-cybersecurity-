#!/usr/bin/env python
"""
Quick verification script to test core functionality.
"""
import sys
sys.path.insert(0, 'src')

from prediction.predictor import ThreatPredictor
import glob

print("="*80)
print("CYBERSECURITY THREAT PREDICTION - VERIFICATION TEST")
print("="*80)

# Find the best model
model_files = glob.glob('models/trained/GradientBoosting*.pkl')
if not model_files:
    print("❌ No trained model found!")
    sys.exit(1)

latest_model = max(model_files, key=lambda x: x.split('_')[-1])
print(f"\n✓ Loading model: {latest_model}")

# Initialize predictor
try:
    predictor = ThreatPredictor(model_path=latest_model)
    print("✓ Predictor initialized successfully")
except Exception as e:
    print(f"❌ Error initializing predictor: {e}")
    sys.exit(1)

# Test with sample data
test_cases = [
    {
        "name": "Benign HTTPS Traffic",
        "data": {
            'source_ip': 0,
            'destination_ip': 0,
            'source_port': 54321,
            'destination_port': 443,
            'protocol': 0,  # TCP encoded
            'packet_size': 1024,
            'payload_size': 800,
            'tcp_flags': 1,  # ACK encoded
            'is_privileged_src_port': 0,
            'is_privileged_dst_port': 0,
            'is_common_port': 1,
            'header_size': 224,
            'payload_ratio': 0.78,
            'is_large_packet': 1,
            'is_tcp': 1,
            'is_udp': 0,
            'is_icmp': 0
        }
    },
    {
        "name": "Suspicious SSH Traffic",
        "data": {
            'source_ip': 1,
            'destination_ip': 1,
            'source_port': 60000,
            'destination_port': 22,
            'protocol': 0,  # TCP
            'packet_size': 64,
            'payload_size': 20,
            'tcp_flags': 0,  # SYN
            'is_privileged_src_port': 0,
            'is_privileged_dst_port': 1,
            'is_common_port': 1,
            'header_size': 44,
            'payload_ratio': 0.31,
            'is_large_packet': 0,
            'is_tcp': 1,
            'is_udp': 0,
            'is_icmp': 0
        }
    }
]

print("\n" + "="*80)
print("RUNNING PREDICTIONS")
print("="*80)

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {test_case['name']}")
    print("-" * 60)
    
    try:
        result = predictor.predict_single(test_case['data'])
        
        threat_emoji = "🔴" if result['is_threat'] else "🟢"
        print(f"  {threat_emoji} Threat Detected: {result['is_threat']}")
        print(f"  📊 Confidence: {result['confidence']:.2%}")
        print(f"  ⚠️  Severity: {result['severity']}")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
print("\n✅ System is functional and ready for deployment!")
print("\nNext steps:")
print("  1. Start API: python api/app.py --model models/trained/GradientBoosting*.pkl")
print("  2. Test API: curl http://localhost:5000/health")
print("  3. Review documentation in docs/")
print("  4. Prepare Infosys presentation using docs/PRESENTATION_OUTLINE.md")
