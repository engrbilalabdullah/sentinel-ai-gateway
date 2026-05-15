class PolicyEngine:
    def __init__(self):
        self.block_threshold = 0.6
        self.mask_threshold = 0.3

    def evaluate(self, rule_score, semantic_score, pii_entities, composite_risk=False):
        reasons = []
        # Base risk calculate karna
        final_risk = max(rule_score, semantic_score)

        # 1. Check for Injection (BLOCK ki conditions)
        if rule_score >= self.block_threshold:
            reasons.append("RULE_BASED_INJECTION")
        if semantic_score >= self.block_threshold:
            reasons.append("SEMANTIC_INJECTION")
        if composite_risk:
            reasons.append("COMPOSITE_ATTACK")
            
        # 2. Check for PII (MASK ki conditions)
        if len(pii_entities) > 0:
            reasons.append("PII_DETECTED")
            # Risk ko thora barhayen lekin Block threshold se neechay rakhein
            if final_risk < self.block_threshold:
                final_risk = max(final_risk, self.mask_threshold + 0.1)
        
        # 3. Final Decision Logic
        if "RULE_BASED_INJECTION" in reasons or "SEMANTIC_INJECTION" in reasons or "COMPOSITE_ATTACK" in reasons:
            decision = "BLOCK"
        elif "PII_DETECTED" in reasons:
            decision = "MASK"
        else:
            decision = "ALLOW"
            reasons.append("SAFE_PROMPT")

        return {
            "final_risk": round(final_risk, 2),
            "decision": decision,
            "reason_codes": reasons
        }