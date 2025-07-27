import json
from typing import Optional

def parse_openrouter_log(line: str) -> Optional[dict]:
    """
    Extracts JSON part from a log line and parses relevant request metadata.
    """
    try:
        json_start = line.find("{")
        if json_start == -1:
            return None  # No JSON found in line

        json_part = line[json_start:]
        data = json.loads(json_part)

        return {
            "model": data.get("model", "unknown"),
            "latency": data.get("latency", -1),
            "prompt": data.get("prompt", "") or data.get("input", ""),
            "status": data.get("status", "unknown"),
        }
    except (json.JSONDecodeError, TypeError):
        return None
