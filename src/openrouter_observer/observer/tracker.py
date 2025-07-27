import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from openrouter_observer.config_loader import load_config
from colorama import Fore, Style, init as colorama_init
colorama_init(autoreset=True)


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

    stats = StatsTracker()

    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            result = parse_log_line(line)
            if result:
                print(f"{Fore.CYAN}🧠 Model: {Fore.YELLOW}{result['model']} {Fore.CYAN}| ⏱️ {result['latency']}s | 📄 Prompt: {Fore.WHITE}{result['prompt']}{Style.RESET_ALL}")
                stats.update(result)

    stats.print_summary()

class StatsTracker:
    def __init__(self):
        self.total_requests = 0
        self.success_count = 0
        self.failure_count = 0
        self.model_counts = defaultdict(int)
        self.latency_sum = defaultdict(float)
        self.latency_count = defaultdict(int)

    def update(self, parsed):
        self.total_requests += 1
        status = parsed["status"]
        model = parsed["model"]
        latency = parsed.get("latency", 0.0)

        if status == "success":
            self.success_count += 1
        elif status == "failure":
            self.failure_count += 1

        self.model_counts[model] += 1
        self.latency_sum[model] += latency
        self.latency_count[model] += 1

    def print_summary(self):
        print(f"\n{Fore.MAGENTA}📊 Request Summary{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}Total requests  : {self.total_requests}")
        print(f"   {Fore.GREEN}Successes       : {self.success_count}")
        print(f"   {Fore.RED}Failures        : {self.failure_count}")
        print(f"   {Fore.YELLOW}Requests per model:{Style.RESET_ALL}")
        for model, count in self.model_counts.items():
            avg_latency = self.latency_sum[model] / self.latency_count[model]
            print(f"     - {Fore.BLUE}{model}{Style.RESET_ALL}: {count} requests, avg latency {avg_latency:.2f}s")
