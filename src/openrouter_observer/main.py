import argparse
import time
import os
from pathlib import Path
from openrouter_observer.observer.tracker import monitor_llm_requests
from openrouter_observer.utils.parser import parse_openrouter_log
from openrouter_observer.config_loader import load_config

config = load_config()
print(f"🧪 Loaded config for {config.app.name} (mode={config.app.mode})")

def tail_log(log_path: Path, poll_interval: float = 1.0):
    if not log_path.exists():
        print(f"❌ Log file not found: {log_path}")
        return

    print(f"📄 Tailing log file: {log_path}")
    with log_path.open("r", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)  # Seek to end of file

        while True:
            line = file.readline()
            if not line:
                time.sleep(poll_interval)
                continue

            parsed = parse_openrouter_log(line)
            if parsed:           
                status_icon = "✅" if parsed["status"] == "success" else "❌"
                print(f"{status_icon} Model: {parsed['model']} | ⏱️ {parsed['latency']}s | 📄 Prompt: {parsed['prompt'][:40]}...")

def main():
    parser = argparse.ArgumentParser(description="🧠 OpenRouter Observer CLI")
    parser.add_argument("--run", action="store_true", help="Start the Observer pipeline")
    parser.add_argument("--hello", action="store_true", help="Say Hello and exit")
    parser.add_argument(
        "--tail",
        action="store_true",
        help="Tail the log file in real-time and print request summaries"
    )

    args = parser.parse_args()

    if args.hello:
        print("👋 Hello from OpenRouter Observer CLI!")
    elif args.run:
        print("🚀 Starting OpenRouter Observer")
        monitor_llm_requests()
    elif args.tail:
        tail_log(Path(config.app.log_path), config.app.poll_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
