from flask import Flask, request, jsonify
from flask_cors import CORS 
import time
from langdetect import detect

# Humari banai hui 4 core files ko import karna
from detectors.rule_detector import RuleDetector
from detectors.semantic_detector import SemanticDetector
from pii.presidio_custom import PIIHandler
from policy.policy_engine import PolicyEngine

app = Flask(__name__)
CORS(app) # Frontend ko connect karne ke liye

# System start hote hi guards ko duty par lagana
print("Initializing AI Models... Please wait (10-15 seconds).")
rule_detector = RuleDetector()
semantic_detector = SemanticDetector()
pii_handler = PIIHandler()
policy_engine = PolicyEngine()
print("Gateway API is Live and Ready!")

@app.route("/analyze", methods=['POST'])
def analyze_prompt():
    # Latency check karne ke liye timer start
    start_time = time.time() 
    
    data = request.get_json()
    input_text = data.get("text", "")
    input_id = data.get("id", "case_001")
    
    # Frontend se aane wale sliders ki values catch karna
    block_thresh = float(data.get("block_threshold", 0.6))
    mask_thresh = float(data.get("mask_threshold", 0.3))
    
    # Engine ke thresholds update karna
    policy_engine.block_threshold = block_thresh
    policy_engine.mask_threshold = mask_thresh
    
    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # 1. Language Detect karna
    try:
        lang = detect(input_text)
    except:
        lang = "unknown"

    # 2. Rule-Based Guard check karega
    rule_score = rule_detector.analyze(input_text)
    
    # 3. Semantic (AI) Guard check karega
    semantic_score = semantic_detector.analyze(input_text)
    
    # 4. Privacy Officer (Presidio) check karega
    pii_result = pii_handler.analyze_and_anonymize(input_text)
    
    # 5. Policy Engine Faisla (Decision) karega
    policy_result = policy_engine.evaluate(
        rule_score=rule_score,
        semantic_score=semantic_score,
        pii_entities=pii_result["entities_detected"],
        composite_risk=pii_result["composite_risk"]
    )
    
    # Latency calculate karna (milliseconds mein)
    latency_ms = int((time.time() - start_time) * 1000)

    # Final JSON Response
    response = {
        "input_id": input_id,
        "language": lang,
        "rule_score": rule_score,
        "semantic_score": semantic_score,
        "pii_entities": pii_result["entities_detected"],
        "final_risk": policy_result["final_risk"],
        "decision": policy_result["decision"],
        "safe_text": pii_result["safe_text"] if policy_result["decision"] != "BLOCK" else None,
        "reason_codes": policy_result["reason_codes"],
        "latency_ms": latency_ms
    }
    
    return jsonify(response)

if __name__ == "__main__":
    # Server ko port 5000 par run karna
    app.run(debug=True, port=5000)