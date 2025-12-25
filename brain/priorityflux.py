from datetime import datetime
from typing import List, Dict, Optional

class PriorityFlux:
    """
    PriorityFlux Algorithm
    ----------------------
    Resolves conflicts when multiple automation actions
    are eligible for execution.
    """

    def resolve(self, actions: List[Dict]) -> Optional[Dict]:
        """
        Selects the highest-priority action.

        Args:
            actions (list): List of possible actions with priority

        Returns:
            dict | None: Selected action
        """

        if not actions:
            return None

        # Validate input structure
        valid_actions = [
            action for action in actions
            if "priority" in action and "name" in action
        ]

        if not valid_actions:
            return None

        # Sort by priority (highest first)
        valid_actions.sort(
            key=lambda action: action["priority"],
            reverse=True
        )

        chosen_action = valid_actions[0]

        # Add resolution metadata (explainable AI)
        chosen_action["resolved_at"] = datetime.utcnow().isoformat()
        chosen_action["resolution_method"] = "PriorityFlux"

        return chosen_action
