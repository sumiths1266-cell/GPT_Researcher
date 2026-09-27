# GPT_Researcher

Company research reports generated with [GPT Researcher](https://github.com/assafelovic/gpt-researcher).

## Setup
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in OPENAI_API_KEY and TAVILY_API_KEY
```

## Run
```bash
python run_research.py                      # default: Healthify research report
python run_research.py --report-type detailed_report
python run_research.py "Any other topic"
```
Reports are saved to `research/`.

## Reports
- `research/healthify.md` – manually compiled Healthify brief (web search, Sep 2026)
- `research/healthify-gptr.md` – GPT Researcher output (after running the script)
