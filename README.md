# 📧 Email Scheduling Agent with Judgeval Tracing

This repository implements an **LLM-powered email scheduling agent** that:
- Extracts events (e.g. meetings, store visits) from raw email content
- Builds and maintains a persistent schedule across email cycles
- Sends appropriate responses based on scheduling status
- Uses [Judgeval](https://github.com/judgmentlabs/judgeval) to **trace the full agent pipeline**

---

## 🔧 Features

- ✅ **Event Extraction**: Parses sender, title, and body from emails using LLMs
- 🗓️ **Schedule Management**: Maintains evolving event store and daily schedule
- 📍 **Reasoning Pipeline**: Determines when to schedule, hold, or cancel events
- 📡 **Langfuse Tracing**: Traces every step (LLM calls, decisions, email actions)
- 📁 **Modular Design**: Easy-to-read pipeline with clear component structure

---

## 🗂️ Directory Overview

```
core/                       # Core logic of the agent
├── email_generator.py      # Generates test emails
├── event_parser.py         # Parses raw emails and extracts events
├── event_store.py          # Persistent event memory across cycles
├── ingest.py               # Main email ingestion pipeline
├── schedule_manager.py     # Assigns time/venue/status to events
├── utils.py                # Shared helper functions

core/judgeval_integration/  # Judgeval tracer integration
└── tracer.py               # Langfuse tracing logic for each agent step

data/                       # Input emails per cycle
└── emails_cycle_*.json     # Raw test data used in each cycle

output/
├── emails/                 # Parsed emails after each cycle
├── schedules/              # Final generated schedule per cycle
├── expected_schedules/     # Ground-truth schedule for evaluation
└── store/event_store.json  # Current persistent event memory

test/                       # Custom scorers and test scaffolding
├── test_custom_scorer.py   # Custom scorer example
└── test_run.py             # Run evaluator with dummy scorers

agent.py                    # Main agent loop
config.py                   # Constants & path management
main.py                     # Entrypoint script
requirements.txt            # Python dependencies
README.md                   # You're here!
```

---

## 🚀 Quickstart

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Before running**
   - Event memory: if first time, create a file `event_store.json` with empty array `[]` and make to sure emtpy it before every run.
   - Clear outputs: Clear these folders before every run: `output/emails/` and `output/schedules/`

3. **Run the agent**
   ```bash
   python main.py
   ```

4. **Inspect outputs**
   - Final schedules: `output/schedules/schedule_cycle_*.json`
   - Event memory: `output/store/event_store.json`
   - Traces: via [Langfuse](https://langfuse.com)

---

## 🧪 Judgeval Integration

The `judgeval_integration/tracer.py` file connects the agent with **Judgeval tracing** via Langfuse.

To use evaluation (WIP):
- Add examples to `test/test_run.py`
- Define scorers in `test/test_custom_scorer.py`
- Run evaluation with:
  ```bash
  python test/test_run.py
  ```

---

## 🧠 Powered by
- Gemini / OpenAI (LLM-based reasoning)
- Judgeval SDK (evaluation & tracing)
- Langfuse (observability)

---

## 📬 Contact

Built by Adwait Mahadar as part of a technical assessment for [Judgment Labs](https://www.judgmentlabs.ai/).
