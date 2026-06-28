# Elon Musk Second Brain 🧠⚡

Open-source Elon Musk-style second brain: **First Principles Thinking**, **10x Execution**, speed, scale, and brutal prioritization.

## Use

```bash
# keyword-only retrieval, no API key
python3 brain.py --search "first principles"

# RAG mentor answer, needs KIMI_API_KEY or OPENAI_API_KEY
cp .env.example .env
python3 brain.py "gimana cara mikir first principles buat SaaS?"
```

## Env

`brain.py` uses only Python stdlib. No LangChain. No dependency bloat.

Supported env:
- `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL`
- or `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`

## Vault

- `Frameworks/First-Principles.md`
- `Frameworks/10x-Urgency.md`
- `Routine/Daily-Routine.md`
- `Principles/Rp-1-Triliun.md`

## Principle

If it can be done with a few stdlib lines, don't install a framework.

## License
MIT
