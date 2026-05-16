# 🛡️ Sentinel AI: Robust LLM Security Gateway

**Sentinel AI** is an advanced, hybrid pre-model security gateway designed to protect Large Language Models (LLMs) from prompt injections, jailbreaks, and PII data leaks. Developed as a Lab Final Project.

## ✨ Key Features
- **Hybrid Detection Engine:** Combines Rule-based filtering with a Semantic Machine Learning Classifier (TF-IDF + Logistic Regression).
- **Multilingual Defense:** Detects and blocks attacks in English, Urdu, and Korean.
- **PII Anonymization:** Uses customized Microsoft Presidio with regional Regex to mask Pakistani CNICs and Phone numbers.
- **Ultra-Low Latency:** Processes and sanitizes prompts in under 25 milliseconds.
- **Dynamic Dashboard:** Interactive HTML/JS frontend with live threshold calibration sliders.

## 📂 Project Structure

```text
sentinel-ai-gateway/
│
├── data/
│   └── final_eval.csv             # Custom dataset of 150 diverse prompts
│
├── detectors/
│   ├── rule_detector.py           # Fast Regex-based keyword filtering
│   └── semantic_detector.py       # ML Model (TF-IDF + Logistic Regression)
│
├── pii/
│   └── presidio_custom.py         # Customized Presidio engine for PK_CNIC/PHONE
│
├── policy/
│   └── policy_engine.py           # Core logic evaluating risks and thresholds
│
├── results/
│   └── evaluation_results.csv     # Output of the automated evaluation script
│
├── index.html                     # Dynamic Web Dashboard UI
├── main.py                        # Flask API Backend 
├── requirements.txt               # Project dependencies
└── run_evaluation.py              # Automated stress-testing script
