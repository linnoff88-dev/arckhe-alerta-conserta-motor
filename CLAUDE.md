# CLAUDE.md — alerta-conserta-motor

Kit: transformar o trabalho repetitivo do agente em MOTOR (script fixo + modelo só onde julga), com alerta diário,
aprendizado semanal e medição de modelo × esforço. Python 3 puro, sem rede, sem API.

- Testes: `python3 -m unittest discover -s tests -v` (não chamam modelo).
- `medir.py` só roda pela assinatura (`claude -p` / `codex exec`), remove chaves de API do ambiente. Nunca trocar por API.
- Autor dos commits: conta linnoff88-dev. Versão em `VERSION` (semver do Nei: minor carrega o patch).
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`.

## Self-learning

Quando eu for corrigido, ou perceber um erro meu: antes de continuar, gravar a lição como uma regra de uma linha no TOPO de `## Lessons` abaixo, e a falha em `FALHAS.md`.

## Lessons

- Ao varrer muitos projetos, toda leitura de arquivo aceita OSError (pasta sem permissão) e a contagem deduplica cópias. (20/11/2026)
