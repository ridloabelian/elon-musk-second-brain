---
tags: [hermes, deepteam, llm-security, red-team, saif]
source: https://github.com/confident-ai/deepteam
---

# DeepTeam × Hermes Agent

## Verdict

DeepTeam tidak diimplementasikan ke Hermes core. Gunakan sebagai **external red-team harness** untuk menguji agent SAIF/Hermes di staging.

DeepTeam menyediakan 50+ vulnerability checks, 20+ adversarial attacks, single-turn/multi-turn testing, LLM-as-a-Judge, guardrails, serta pemetaan OWASP LLM/Agents, NIST AI RMF, dan MITRE ATLAS.

## Prioritas pengujian

P0:
- Excessive agency
- Tool orchestration abuse
- Prompt injection
- Indirect instruction
- Unexpected code execution
- Secret/PII leakage

P1:
- RBAC bypass
- BOLA/BFLA
- Cross-context retrieval
- Inter-agent communication compromise

P2:
- Bias
- Toxicity
- Misinformation

## Arsitektur adopsi

```text
deepteam/
├── targets/       # callback ke agent/endpoint staging
├── tests/         # attack + vulnerability cases
└── reports/       # JSON risk reports
```

Minimum pipeline:
- target staging, bukan production;
- 10 attack cases;
- 5 vulnerability categories;
- JSON report;
- exit code gagal jika critical vulnerability ditemukan;
- dijalankan sebelum deployment besar.

## Prinsip security

DeepTeam menguji perilaku model. Security Hermes tetap harus berbasis control fisik:

- least-privilege toolset;
- isolated workspace;
- restricted credentials;
- approval untuk destructive action;
- audit log;
- deterministic policy di luar LLM;
- deny-by-default untuk tool berbahaya.

Prompt “jangan hapus database” bukan security control. Permission OS, sandbox, dan approval gate adalah control.

## Implementasi ditunda jika

Belum ada target staging yang bisa dipanggil ulang. Jangan install atau membangun framework baru tanpa boundary yang perlu diuji.

## Related

- [[Zero-Cost-AI-Architecture]]
- [[Hermes Agent]]
- [[SAIF]]
- [[AI Security]]
