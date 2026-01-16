from typing import Dict


class SignalScore:
    """
    SignalScore Matrix
    ------------------
    Converts raw system signals into a normalized, explainable
    severity score for decision making.
    """

    def calculate(
        self,
        severity: int,
        frequency: int,
        duration: int,
        max_severity: int = 100
    ) -> Dict:
        """
        Calculate signal score using weighted factors.

        Args:
            severity (int): Current severity value (e.g., CPU usage)
            frequency (int): How often the event occurs
            duration (int): How long the event lasts
            max_severity (int): Upper bound for normalization

        Returns:
            dict: Score details with explanation
        """

        # Normalize severity to 0–1 range
        normalized_severity = min(severity / max_severity, 1.0)

        # Weighted scoring logic
        score = (
            (normalized_severity * 100) * 0.5 +
            (frequency * 10) * 0.3 +
            (duration * 10) * 0.2
        )

        final_score = round(score, 2)

        return {
            "score": final_score,
            "components": {
                "normalized_severity": round(normalized_severity, 2),
                "frequency_factor": frequency,
                "duration_factor": duration
            },
            "scoring_method": "SignalScore"
        }
