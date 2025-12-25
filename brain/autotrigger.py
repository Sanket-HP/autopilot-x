from datetime import datetime

class AutoTrigger:
    """
    AutoTrigger Orchestrator
    ------------------------
    Responsible for executing automation actions in a controlled,
    traceable, and repeat-safe manner.
    """

    def __init__(self):
        # Keeps track of last executed action to avoid loops (demo-safe)
        self.last_action = None

    def execute(self, action_name: str) -> dict:
        """
        Execute an automation action.

        Args:
            action_name (str): Name of the action to execute

        Returns:
            dict: Execution result with metadata
        """

        # Prevent repeated execution of the same action
        if self.last_action == action_name:
            return {
                "action": action_name,
                "status": "SKIPPED",
                "reason": "Action already executed recently",
                "timestamp": datetime.utcnow().isoformat()
            }

        # Simulated execution (real systems would call APIs here)
        self.last_action = action_name

        return {
            "action": action_name,
            "status": "EXECUTED",
            "executed_at": datetime.utcnow().isoformat(),
            "executor": "AutoPilot-X AutoTrigger"
        }
