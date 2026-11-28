# Error Alarm — audits and proposes the fix

[![alerta-conserta-motor](guia/assets/banner-en.jpg)](https://linnoff88-dev.github.io/alerta-conserta-motor/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Leaving an AI agent free to create all the time gets expensive and repeats mistakes. This kit reads the notebooks where you record what went wrong (failures, blockers, rejections, and lessons) and sends an alert every day. Each week, it measures whether the same mistake has decreased and points out what should become an **engine**: a fixed step, run by a program, where AI is involved only where it needs to think. It also tests several models and effort levels on the same task, so you can use the cheapest one that still gets it right. It is for people who use Claude Code or Codex at work. You only need one of them. The AI installs the kit for you.

## 📖 User guide

Complete guide (landing page + walkthrough): **https://linnoff88-dev.github.io/alerta-conserta-motor/guia/en/**

<!-- VIDEO-README: entra o link do explicavideo quando publicado -->

## How to get started (without installing anything by hand)

Open Claude Code or Codex in your projects folder and paste:

```text
Read the "alerta-conserta-motor" kit at https://github.com/linnoff88-dev/alerta-conserta-motor (the README explains everything, including installation).
Then look through my projects and answer me in plain English:
1. Do I already record what goes wrong (failures, blockers, rejections, lessons)? If not, how do I start with one line per error?
2. Run today's alert on my projects and show me the error that has come back the most.
3. Which of my tasks repeats so often that it should become an engine (a fixed program, with AI only where it needs to think)?
4. For that task, is it worth measuring models and effort levels before choosing? How much would that use of my subscription cost?
Don't change anything or enable any scheduled tasks yet. Show me the plan and wait for me to say yes.
```

## The idea in one sentence

A free agent is useful for what is new. For what repeats, it spends too much and makes a different kind of mistake each time. When a repeated task becomes an **engine** (fixed steps + AI only for judgment + checking + one line in the notebook when it fails), and the engine is improved every week based on what the alert shows, repeated errors decrease, spending goes down, and delivery is consistent every day.

## The evidence (measured on 20/11/2026, across ARCKHé AI's 231 projects)

| What | Result |
|---|---|
| Same blocker repeated (AI looks for `python`/`identify`, which are not on the machine, to check an image) | **355 times** since 17/09, 103 on 18/11 alone |
| Weekly recurrence (records that had already occurred before) | **17%** (previous week: 18%) |
| Daily alert run by a **free agent** (Sonnet, medium effort) | 35 s · 7 turns · 182 thousand tokens read · **US$ 0.235** equivalent · read by sampling |
| Same alert run by the **engine** (`alerta.py`) | **1.2 s · 0 tokens · US$ 0** · read everything · same result every run |
| Classifying 24 real failures (prompt × infrastructure), scored by the hidden checker, average of 2 runs | Haiku low 9.2 · US$ 0.0019 — Sonnet low 9.4 · US$ 0.027 — Opus high 9.2 · US$ 0.060 (**31× Haiku**) |
| Codex `gpt-6-luna`, low/medium/high | 8.8 across all three; high took 11 s versus 6 s |
| Fable 5.2 | did not run: the account required extra usage credits |

The cost is the `total_cost_usd` reported by Claude Code. With a subscription, you don't pay per call, but it is the best measure of how much of your quota each run uses. The raw data is in `resultados/`.

---

## Technical installation

**Prerequisites:** Python 3.9+ (no dependencies). For `medir.py`: Claude Code (`claude`) and/or Codex (`codex`), signed in through your subscription.

```bash
git clone https://github.com/linnoff88-dev/alerta-conserta-motor.git && cd alerta-conserta-motor
python3 -m unittest discover -s tests -v        # 12 tests, no network or model

python3 alerta.py --raiz ~/projetos             # today's report (today + yesterday)
python3 alerta.py --raiz ~/projetos --curto     # short text for your phone
python3 semana.py --raiz ~/projetos --pasta semana   # weekly learnings + snapshot for comparison
python3 medir.py tarefas/classificar-falhas --modelos haiku,sonnet,opus --esforcos low,medium,high --rep 2
python3 medir.py tarefas/classificar-falhas --motor codex --modelos gpt-6-luna --esforcos low,medium,high
modelos/instalar-timers.sh                      # enables the alert at 08:00 and the weekly run on Mondays at 07:45 (user systemd)
```

### Files

| File | What it does |
|---|---|
| `motor/fontes.py` | Reads the 4 notebooks (formats below) at the root and up to 2 levels below, deduplicates copies, and groups similar records |
| `alerta.py` | Daily alert: what entered the window, **what came back** (grouped by topic), open limits, low scores, and owner feedback. Exits with 1 when there is something to address |
| `semana.py` | Weekly recurrence × previous week, prompt/infrastructure causes, reviewer's average score by workflow, recurring topics and their stage (lesson → test → block → engine), and what left the list |
| `medir.py` | Model × effort grid on the same task, score from a hidden checker, table with time, tokens, and cost; removes `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` from the environment (subscription only) and runs `claude -p` with a clean configuration |
| `medicao/agente-livre.sh` | Compares the alert run by a free agent with the one run by the engine |
| `tarefas/classificar-falhas/` | Example task: 24 real failures, answer key in `oculto/` |
| `modelos/` | Systemd timers (`avm-alerta`, `avm-semana`), `instalar-timers.sh`, and `motor-modelo.sh` (engine template) |

### Formats it reads (one line per occurrence)

```text
FALHAS.md          | AAAA-MM-DD | what broke | smallest fix | prompt|infra |
LIMITES.md         | AAAA-MM-DD | what I tried | what blocked it | workaround | proposal | open|accepted |
revisor-falhas.md  ## AAAA-MM-DD HH:MM · workflow · item · score N [· 🧑 owner feedback]
                   - **Reason:** ...
LESSONS.md         - one-line rule (DD/MM/YYYY)
```

### Send the alert to your phone

The `avm-alerta` service passes the short text via stdin to the command in `ENVIO=` (default `cat`). Replace it with your own Telegram, WhatsApp, or email script.

### Create a task for the benchmark

A folder with `pedido.txt`, `entrada.json` (optional), and `oculto/checar.py`, which receives the response file and prints `{"nota": 0–10}`. The model never sees the `oculto/` folder.

## The process, start to finish

🧠 session with you · ⚙️ script/timer · 🤖 `claude -p` / `codex exec`

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Record each error on one line in the project notebook | `FALHAS.md` / `LIMITES.md` / `revisor-falhas.md` / `LESSONS.md` | 🧠 🤖 |
| 2 | Every day at 08:00, the daily alert is generated and sent to your phone | `alerta.py --curto` (timer `avm-alerta`) | ⚙️ |
| 3 | Choose 1 topic that came back and decide its stage | read the alert | 🧠 |
| 4 | For a repeated task: measure model × effort before writing the engine | `medir.py <tarefa>` | 🤖 |
| 5 | Write the engine (fixed steps + AI only for judgment + checking + one line in the notebook when it fails) | use `modelos/motor-modelo.sh` as a starting point | 🧠 + 🤖 |
| 6 | Test the engine | `python3 -m unittest` / the engine's test | ⚙️ |
| 7 | Every Monday at 07:45: recurrence × previous week and what left the list | `semana.py --pasta semana` (timer `avm-semana`) | ⚙️ |
| 8 | Repeat: the next topic at the top | — | 🧠 |

## Works well with

- [agente-que-aprende](https://github.com/linnoff88-dev/agente-que-aprende): turns a lesson into a hook that blocks the wrong command (the “block” stage).
- [SIL Loop R](https://github.com/linnoff88-dev/sil-loop-r): a human gate for turning a lesson into a rule.

## License

MIT · free at [linnoff88-dev.github.io](https://linnoff88-dev.github.io), available directly on the internet.