import json
import re
from pathlib import Path
from datetime import datetime

from openrouter_observer.config_loader import load_config

def parse_log_line(line: str):
    try:
        # Regex to extract timestamp and JSON payload
        match = re.match(r"^(.*?) (INFO|ERROR).*?({.*})", line)
        if not match:
            return None

        timestamp_str, level, json_str = match.groups()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        data = json.loads(json_str)

        return {
            "timestamp": timestamp,
            "level": level,
            "model": data.get("model"),
            "prompt": data.get("prompt", "")[:50] + "...",
            "latency": data.get("latency"),
            "status": data.get("status")
        }
    except Exception as e:
        print(f"❌ Failed to parse line: {line.strip()} — {e}")
        return None

def monitor_llm_requests():
    config = load_config()
    log_path = Path(config["observer"]["source"])
    print(f"📄 Reading log file: {log_path.resolve()}")

    if not log_path.exists():
        print(f"⚠️  Log file does not exist: {log_path}")
        return

    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            result = parse_log_line(line)
            if result:
                print(f"🧠 Model: {result['model']} | ⏱️ {result['latency']}s | 📄 Prompt: {result['prompt']}")
