import time
from datetime import datetime

class ChronoSense:
    """
    ChronoSense Algorithm
    --------------------
    Adds time-awareness to decision making.
    Ensures conditions persist before triggering actions,
    preventing false positives.
    """

    def __init__(self, threshold_seconds: int = 10):
        self.threshold_seconds = threshold_seconds
        self.start_time = None
        self.last_triggered_at = None

    def evaluate(self, condition: bool) -> dict:
        """
        Evaluate whether a condition has remained true
        for the required duration.

        Args:
            condition (bool): Current condition state

        Returns:
            dict: Evaluation result with metadata
        """

        current_time = time.time()

        if condition:
            if self.start_time is None:
                self.start_time = current_time

            elapsed = current_time - self.start_time

            if elapsed >= self.threshold_seconds:
                self.last_triggered_at = datetime.utcnow().isoformat()
                return {
                    "valid": True,
                    "elapsed_seconds": round(elapsed, 2),
                    "triggered_at": self.last_triggered_at
                }

            return {
                "valid": False,
                "elapsed_seconds": round(elapsed, 2),
                "message": "Condition observed, waiting for persistence"
            }

        # Reset when condition breaks
        self.start_time = None

        return {
            "valid": False,
            "elapsed_seconds": 0,
            "message": "Condition not active"
        }
