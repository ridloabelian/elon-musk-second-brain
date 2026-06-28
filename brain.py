#!/usr/bin/env python3
import glob, json, math, os, re, sys, urllib.request

IGNORE = {"README.md", "LICENSE"}
STOP = set("the a an and or to of in on for with is are was were be been being ini itu yang dan di ke dari untuk dengan apa akan bisa gak nggak tidak".split())

SYSTEM = """You are Elon Musk Second Brain: direct, first-principles, execution-obsessed.
Answer in Indonesian unless asked otherwise. Be blunt, practical, concise.
Use only the provided vault context when claiming knowledge from the brain.
If context is weak, say what is missing and give the fastest next action."""

def load_dotenv(path=".env"):
    if not os.path.exists(path): return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def tokens(text):
    return [t for t in re.findall(r"[a-zA-Z0-9_\-]+", text.lower()) if t not in STOP and len(t) > 2]

def chunks():
    out = []
    for f in glob.glob("**/*.md", recursive=True):
        if f in IGNORE or f.startswith(".git/"): continue
        text = open(f, encoding="utf-8").read()
        parts = re.split(r"\n(?=# )|\n(?=## )", text)
        for i, p in enumerate(parts):
            p = p.strip()
            if p: out.append({"file": f, "id": i, "text": p[:4000], "tok": tokens(p)})
    return out

def retrieve(query, k=4):
    q = tokens(query)
    if not q: return []
    docs = chunks()
    df = {t: sum(t in set(d["tok"]) for d in docs) for t in set(q)}
    scored = []
    for d in docs:
        score = 0
        counts = {t: d["tok"].count(t) for t in set(q)}
        for t, c in counts.items():
            if c: score += (1 + math.log(c)) * math.log((1 + len(docs)) / (1 + df[t]))
        if score: scored.append((score, d))
    return [d for _, d in sorted(scored, reverse=True, key=lambda x: x[0])[:k]]

def call_llm(prompt):
    load_dotenv()
    key = os.getenv("KIMI_API_KEY") or os.getenv("OPENAI_API_KEY")
    base = os.getenv("KIMI_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.moonshot.cn/v1"
    model = os.getenv("KIMI_MODEL") or os.getenv("OPENAI_MODEL") or "kimi-k2.6"
    if not key:
        raise SystemExit("Missing API key. Set KIMI_API_KEY or OPENAI_API_KEY in env/.env")
    data = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        "temperature": 0.2,
    }).encode()
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    res = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    return res["choices"][0]["message"]["content"]

def ask(query):
    hits = retrieve(query)
    if not hits:
        print("No vault context found. Fastest next action: add a note for this topic.")
        return
    ctx = "\n\n".join(f"SOURCE: {h['file']}\n{h['text']}" for h in hits)
    prompt = f"VAULT CONTEXT:\n{ctx}\n\nUSER QUESTION:\n{query}\n\nAnswer with citations like [Frameworks/First-Principles.md]."
    print(call_llm(prompt))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 brain.py <question>\n       python3 brain.py --search <query>")
        raise SystemExit(1)
    if sys.argv[1] == "--search":
        q = " ".join(sys.argv[2:])
        for h in retrieve(q): print(f"\n## {h['file']}\n{h['text'][:700]}")
    else:
        ask(" ".join(sys.argv[1:]))
