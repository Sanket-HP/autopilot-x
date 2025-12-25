from typing import Dict

class RuleWeave:
    """
    RuleWeave Engine
    ----------------
    Combines multiple logical conditions into a single
    explainable decision.
    """

    def decide(self, score: float, time_valid: bool) -> Dict:
        """
        Evaluate decision rules.

        Args:
            score (float): SignalScore value
            time_valid (bool): ChronoSense validation result

        Returns:
            dict: Decision result with explanation
        """

        # Rule 1: Severity check
        severity_ok = score >= 70

        # Rule 2: Time persistence check
        time_ok = time_valid

        # Final decision
        decision = severity_ok and time_ok

        return {
            "decision": decision,
            "rules_evaluated": {
                "severity_threshold_met": severity_ok,
                "time_persistence_met": time_ok
            },
            "decision_method": "RuleWeave"
        }
