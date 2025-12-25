from datetime import datetime
from typing import List, Dict, Optional

def generate_log(
    reason: str,
    algorithms_used: Optional[List[str]] = None,
    input_snapshot: Optional[Dict] = None,
    decision: Optional[str] = None
) -> dict:
    """
    ExplainLog Framework
    --------------------
    Generates explainable, auditable logs for every AI decision.
    """

    return {
        "reason": reason,
        "decision": decision,
        "algorithms_used": algorithms_used or [],
        "input_snapshot": input_snapshot or {},
        "timestamp": datetime.utcnow().isoformat(),
        "explainable": True
    }
