class ConfidenceGate:
    """
    Validates how confident the system is before executing an action.
    """

    def __init__(self, min_confidence=0.7):
        self.min_confidence = min_confidence

    def evaluate(self, score: float, persistence: bool) -> dict:
        confidence = 0.0

        if score >= 70:
            confidence += 0.5
        elif score >= 50:
            confidence += 0.3

        if persistence:
            confidence += 0.4

        decision_allowed = confidence >= self.min_confidence

        return {
            "confidence": round(confidence, 2),
            "allowed": decision_allowed,
            "reason": "High confidence" if decision_allowed else "Low confidence"
        }
