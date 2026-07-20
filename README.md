<h1 align="center">Enterprise AI Platform</h1>

<p align="center">
  <em>Production-grade open-source AI platform — copilot, agents, RAG, prompts, NVIDIA NIM gateway, and observability.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12">
  <img src="https://img.shields.io/badge/FastAPI-0.115-teal.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-15-black.svg" alt="Next.js 15">
  <img src="https://img.shields.io/badge/NVIDIA_NIM-API-76B900.svg" alt="NVIDIA NIM">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/status-ft1-brightgreen.svg" alt="Status: ft1">
</p>

---

## 📋 Overview

**Enterprise AI Platform** is a unified ecosystem of six interconnected production-grade AI services. Each service is a standalone project; together they form a complete enterprise AI infrastructure.

Born from the need to demonstrate principal-level engineering across AI/ML, the platform follows Clean Architecture, DDD, event-driven patterns, and enterprise observability standards.

### The Ecosystem

```
┌─────────────────────────────────────────────────────────────┐
│                    Enterprise AI Platform                     │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────────┐            │
│  │  Financial AI     │  │  Enterprise          │            │
│  │  Copilot          │  │  Knowledge Assistant  │            │
│  └────────┬─────────┘  └──────────┬───────────┘            │
│           │                       │                         │
│  ┌────────▼───────────────────────▼───────────┐            │
│  │         Enterprise Agent Platform          │            │
│  └────────┬───────────────────────┬───────────┘            │
│           │                       │                         │
│  ┌────────▼─────────┐  ┌─────────▼──────────┐            │
│  │  Prompt           │  │  AI Observability  │            │
│  │  Evaluation       │  │  Platform          │            │
│  └────────┬─────────┘  └─────────┬──────────┘            │
│           │                       │                         │
│  ┌────────▼───────────────────────▼───────────┐            │
│  │        Universal NVIDIA NIM Gateway        │            │
│  └─────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Projects

| # | Project | Description | Status |
|---|---------|-------------|--------|
| 1 | **[Financial AI Copilot](./financial-ai-copilot)** | AI-powered financial analysis assistant | `ft1` |
| 2 | **[Enterprise Knowledge Assistant](./enterprise-knowledge-assistant)** | Production RAG for enterprise knowledge | `ft1` |
| 3 | **[Enterprise Agent Platform](./enterprise-agent-platform)** | Multi-agent orchestration and execution | `ft1` |
| 4 | **[Prompt Evaluation Platform](./prompt-evaluation-platform)** | Prompt versioning, evaluation, and testing | `ft1` |
| 5 | **[Universal NVIDIA NIM Gateway](./nvidia-nim-gateway)** | Unified gateway to NVIDIA NIM API | `ft1` |
| 6 | **[AI Observability Platform](./ai-observability-platform)** | Distributed tracing, metrics, and monitoring | `ft1` |

## 🚀 Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/iv150320/enterprise-ai-platform.git
cd enterprise-ai-platform

# Start the entire ecosystem
docker compose up -d
```

## 🧩 Integration Map

- **Financial AI Copilot** uses → NIM Gateway, Agent Platform
- **Knowledge Assistant** uses → NIM Gateway, Observability Platform
- **Agent Platform** uses → NIM Gateway, Observability Platform, Prompts
- **Prompt Platform** uses → NIM Gateway, Observability Platform
- **NIM Gateway** sends events → Observability Platform
- **Observability Platform** receives from → all services

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy, Alembic, Celery |
| Frontend | Next.js 15, TypeScript, Tailwind, shadcn/ui |
| AI | NVIDIA NIM API (OpenAI-compatible) |
| Vector Store | Qdrant |
| Database | PostgreSQL, Redis, ClickHouse |
| Monitoring | OpenTelemetry, Prometheus, Grafana |
| Testing | pytest, integration, e2e |
| CI/CD | GitHub Actions, Docker Compose |

## 📚 Documentation

Each project includes:
- `README.md` — full project documentation
- `docs/architecture.md` — architectural overview
- `docs/adr/` — Architecture Decision Records
- `docs/api.md` — API contracts
- `docs/sequence-diagrams.md` — key flows

## 🔖 Releases

| Tag | Date | Description |
|-----|------|-------------|
| `ft1` | 2026-07-20 | First release — all projects scaffolded |

## 🗺️ Roadmap

- [ ] Full backend implementation for all projects
- [ ] Frontend application UIs
- [ ] Integration tests and e2e suites
- [ ] Helm charts for Kubernetes deployment
- [ ] CI/CD pipelines with GitHub Actions
- [ ] Comprehensive documentation and ADRs
- [ ] Performance benchmarks

## 📄 License

This project is licensed under the MIT License — see each project's `LICENSE` file.

## 🤝 Contributing

Contributions are welcome! Please read each project's contributing guidelines.

---

<p align="center">Built with ❤️ for the AI Engineering community</p>
