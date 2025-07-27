import argparse
from openrouter_observer.observer.tracker import monitor_llm_requests
from openrouter_observer.config_loader import load_config

config = load_config()
print(f"🧪 Loaded config for {config.app.name} (mode={config.app.mode})")

def main():
    parser = argparse.ArgumentParser(description="🧠 OpenRouter Observer CLI")
    parser.add_argument("--run", action="store_true", help="Start the Observer pipeline")
    parser.add_argument("--hello", action="store_true", help="Say Hello and exit")
    args = parser.parse_args()

    if args.hello:
        print("👋 Hello from OpenRouter Observer CLI!")
    elif args.run:
        print("🚀 Starting OpenRouter Observer")
        monitor_llm_requests()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
