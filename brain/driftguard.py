from collections import deque

class DriftGuard:
    """
    Detects slow drift from normal behavior using rolling statistics.
    """

    def __init__(self, window_size=10, drift_threshold=1.5):
        self.window = deque(maxlen=window_size)
        self.drift_threshold = drift_threshold

    def update(self, value: float) -> dict:
        self.window.append(value)

        if len(self.window) < self.window.maxlen:
            return {
                "drift_detected": False,
                "reason": "Insufficient data for baseline"
            }

        avg = sum(self.window) / len(self.window)
        deviation = abs(value - avg)

        drift = deviation > self.drift_threshold * (avg * 0.1)

        return {
            "drift_detected": drift,
            "current_value": value,
            "baseline": round(avg, 2),
            "deviation": round(deviation, 2)
        }
