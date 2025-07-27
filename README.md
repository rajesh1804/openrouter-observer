# 🧠 OpenRouter Observer

[![PyPI version](https://badge.fury.io/py/openrouter-observer.svg)](https://pypi.org/project/openrouter-observer/)

OpenRouter Observer is a CLI utility that monitors and analyzes LLM requests from structured logs — built for teams using [OpenRouter](https://openrouter.ai/) and logging structured JSON per request.

It provides a streamlined way to:
- 📄 Tail logs live
- 📊 Aggregate stats (successes, failures, model breakdown)
- 📤 Export parsed entries to JSONL
- 🔍 Run dry-run parsing validations

---

## 📦 Installation

Requires **Python 3.10+** and [Poetry](https://python-poetry.org/):

```bash
git clone https://github.com/rajesh1804/openrouter_observer.git
cd openrouter_observer
poetry install
```

---

## ⚙️ Configuration

Edit `config/default.yaml` to configure paths and behavior:

```yaml
app:
  name: "OpenRouter Observer"
  mode: "dev"
  log_path: "logs/sample.log"
  export_path: "exports/observer_output.jsonl"
  poll_interval: 1.0
```

---

## 🚀 Usage

Run all CLI commands via:

```bash
poetry run python -m openrouter_observer.main [OPTIONS]
```

### ✅ Available Commands

| Command         | Description |
|----------------|-------------|
| `--hello`       | Print a welcome message |
| `--run`         | Run the main observer (WIP) |
| `--tail`        | Tail the log file in real time |
| `--report`      | Ingest full log and print aggregated stats |
| `--export`      | Export valid log entries to JSONL |
| `--head N`      | Show the last N log entries |
| `--dry-run`     | Parse and count valid/invalid lines, without output |

---

### 🔁 Log Format (Input)

The observer expects each log line to be **a valid JSON object** like:

```json
{
  "model": "mistralai/mistral-7b-instruct",
  "prompt": "Write a story about...",
  "latency": 1.24,
  "status": "success"
}
```

---

## 📂 Project Structure

```
openrouter_observer/
├── config/             # YAML config files
├── exports/            # Exported JSONL logs
├── logs/               # Source log files
├── src/                # Main source code
├── tests/              # Pytest-based test suite
```

---

## 🧪 Example

```bash
poetry run python -m openrouter_observer.main --report
```

Outputs:

```
📊 Ingest Summary from sample.log
-------------------------------
🔢 Total Requests     : 42
✅ Successes          : 40
❌ Failures           : 2
🤖 Models Used        : 3
✍️ Longest Prompt     : 123 characters
→ Tell me a story about the ocean and...

📈 Model Breakdown:
- gpt-4: 20 reqs | ⏱️ Avg Latency: 2.34s
- mistral: 15 reqs | ⏱️ Avg Latency: 1.12s
...
```

---

## 🛠️ Limitations

- Only works with structured JSON logs (one per line)
- No real-time alerts or metrics yet
- No web UI or dashboard (yet)

---

## 📌 Road to v0.1.x

The following are out of scope for `v0.0.1` but coming soon:

- Rich TUI mode
- Filtering/sorting by model or latency
- Exporting to CSV or SQLite
- Alerts or anomaly detection
- Plugins for non-OpenRouter logs

---

## 🏁 Version

This is `v0.0.1`. Ready for internal use and light testing.

---

## 📄 License

MIT License
