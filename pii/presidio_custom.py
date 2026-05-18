from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

class PIIHandler:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        cnic_pattern = Pattern(name="cnic_regex", regex=r"\d{5}-\d{7}-\d{1}", score=0.6)
        cnic_recognizer = PatternRecognizer(
            supported_entity="CNIC", 
            patterns=[cnic_pattern],
            context=["cnic", "id", "card", "شناختی"] 
        )
        self.analyzer.registry.add_recognizer(cnic_recognizer)

        id_pattern = Pattern(name="student_id_regex", regex=r"[A-Z]{2}\d{2}-[A-Z]{3}-\d{3}", score=0.8)
        id_recognizer = PatternRecognizer(
            supported_entity="STUDENT_ID", 
            patterns=[id_pattern],
            context=["student", "registration", "reg", "roll"]
        )
        self.analyzer.registry.add_recognizer(id_recognizer)

        phone_pattern = Pattern(name="pk_phone_regex", regex=r"(\+92|0)[3][0-9]{2}-?[0-9]{7}", score=0.7)
        phone_recognizer = PatternRecognizer(
            supported_entity="PK_PHONE", 
            patterns=[phone_pattern],
            context=["phone", "mobile", "contact", "call", "whatsapp"]
        )
        self.analyzer.registry.add_recognizer(phone_recognizer)

        api_pattern = Pattern(name="api_key_regex", regex=r"sk-[a-zA-Z0-9]{32,}", score=0.9)
        api_recognizer = PatternRecognizer(
            supported_entity="API_KEY", 
            patterns=[api_pattern],
            context=["api", "key", "secret", "token", "openai", "password"]
        )
        self.analyzer.registry.add_recognizer(api_recognizer)

        iban_pattern = Pattern(name="pk_iban_regex", regex=r"PK\d{2}[A-Z]{4}\d{16}", score=0.9)
        iban_recognizer = PatternRecognizer(
            supported_entity="PK_IBAN", 
            patterns=[iban_pattern],
            context=["iban", "bank", "account", "transfer", "payment"]
        )
        self.analyzer.registry.add_recognizer(iban_recognizer)

    def analyze_and_anonymize(self, text):
        results = self.analyzer.analyze(
            text=text, 
            entities=["PERSON", "EMAIL_ADDRESS", "CNIC", "STUDENT_ID", "PK_PHONE", "API_KEY", "PK_IBAN"], 
            language='en', 
            score_threshold=0.5
        )
        
        anonymized_result = self.anonymizer.anonymize(text=text, analyzer_results=results)
        
        detected_types = [res.entity_type for res in results]
        
        composite_risk = False
        if ("PERSON" in detected_types and "CNIC" in detected_types) or \
           ("STUDENT_ID" in detected_types and "EMAIL_ADDRESS" in detected_types) or \
           ("PERSON" in detected_types and "PK_PHONE" in detected_types): 
            composite_risk = True 
            
        return {
            "safe_text": anonymized_result.text,
            "entities_detected": detected_types,
            "composite_risk": composite_risk
        }

# Testing the custom recognizers
if __name__ == "__main__":
    handler = PIIHandler()
    
    print("\n--- Test: Comprehensive PII Detection ---")
    test_text = "My mobile is 0300-1234567, my bank IBAN is PK24MEZN00012345678901 and my secret OpenAI key is sk-1234567890abcdef1234567890abcdef12"
    print(handler.analyze_and_anonymize(test_text))
