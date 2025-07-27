import argparse
import time
import os
from pathlib import Path
from openrouter_observer.observer.tracker import monitor_llm_requests
from openrouter_observer.utils.parser import parse_openrouter_log
from openrouter_observer.config_loader import load_config
from collections import defaultdict
import statistics

config = load_config()
print(f"🧪 Loaded config for {config.app.name} (mode={config.app.mode})")

def ingest_log(log_path: Path):
    if not log_path.exists():
        print(f"❌ Log file not found: {log_path}")
        return

    with log_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    parsed_entries = []
    for line in lines:
        parsed = parse_openrouter_log(line)
        if parsed:
            parsed_entries.append(parsed)

    if not parsed_entries:
        print("⚠️ No valid entries found in the log.")
        return

    total = len(parsed_entries)
    success = sum(1 for e in parsed_entries if e["status"] == "success")
    failure = total - success

    model_counts = defaultdict(int)
    latencies = defaultdict(list)
    longest_prompt = ("", 0)  # (text, length)

    for entry in parsed_entries:
        model_counts[entry["model"]] += 1
        latencies[entry["model"]].append(entry["latency"])
        if len(entry["prompt"]) > longest_prompt[1]:
            longest_prompt = (entry["prompt"], len(entry["prompt"]))

    print(f"\n📊 Ingest Summary from {log_path.name}")
    print(f"-------------------------------")
    print(f"🔢 Total Requests     : {total}")
    print(f"✅ Successes          : {success}")
    print(f"❌ Failures           : {failure}")
    print(f"🤖 Models Used        : {len(model_counts)}")
    print(f"✍️ Longest Prompt     : {longest_prompt[1]} characters")
    print(f"   → {longest_prompt[0][:60]}...")

    print("\n📈 Model Breakdown:")
    for model, count in sorted(model_counts.items(), key=lambda x: x[1], reverse=True):
        avg_latency = statistics.mean(latencies[model])
        print(f"  - {model}: {count} reqs | ⏱️ Avg Latency: {avg_latency:.2f}s")


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
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest entire log file and print aggregated statistics"
    )


    args = parser.parse_args()

    if args.hello:
        print("👋 Hello from OpenRouter Observer CLI!")
    elif args.run:
        print("🚀 Starting OpenRouter Observer")
        monitor_llm_requests()
    elif args.tail:
        tail_log(Path(config.app.log_path), config.app.poll_interval)
    elif args.ingest:
        ingest_log(Path(config.app.log_path))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
