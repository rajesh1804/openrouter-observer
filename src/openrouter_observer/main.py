import argparse
from openrouter_observer.observer.tracker import monitor_llm_requests

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
