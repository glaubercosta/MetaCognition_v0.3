# Roadmap — Ações Futuras (resumo)

Data: 2025-11-02

Esta página lista iniciativas de médio/alto impacto identificadas durante as sprints e que precisam de planejamento dedicado.

Prioridade alta (Backlog)

- Separação Frontend / Backend
  - Objetivo: desacoplar o ciclo de vida do frontend (React + Vite) do backend (FastAPI), permitindo builds, CI/CD e deploys independentes.
  - Motivação: evita sobrescrita de assets por bind-mounts, torna builds reproduzíveis e facilita pipelines separados.
  - Próximos passos (planejar): definir modelo de repositório, adaptar CI para builds separados, documentar fluxo dev/production, criar scripts de migração e rollout.

Status: Backlog — ainda a ser estimado e agendado em sprint futura.
