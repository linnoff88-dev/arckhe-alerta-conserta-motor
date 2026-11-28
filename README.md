# Alarme dos Erros — audita e propõe o conserto

[![alerta-conserta-motor](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/alerta-conserta-motor/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Deixar um agente de IA livre para criar o tempo todo sai caro e repete erros. Este kit lê os cadernos onde você anota o que deu errado (falhas, bloqueios, reprovações e lições) e manda um alerta todo dia. Toda semana ele mede se o mesmo erro diminuiu e aponta o que deve virar **motor**: um passo fixo, feito por um programa, em que a IA só entra onde precisa pensar. Ele também testa vários modelos e níveis de esforço na mesma tarefa, para você usar o mais barato que ainda acerta. Serve para quem usa o Claude Code ou o Codex no trabalho. Você só precisa de um deles. A IA instala o kit para você.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://linnoff88-dev.github.io/alerta-conserta-motor/guia/**

<!-- VIDEO-README: entra o link do explicavideo quando publicado -->

## Como começar (sem instalar nada à mão)

Abra o Claude Code ou o Codex na pasta dos seus projetos e cole:

```text
Leia o kit "alerta-conserta-motor" em https://github.com/linnoff88-dev/alerta-conserta-motor (o README explica tudo, inclusive a instalação).
Depois olhe os meus projetos e me responda em português simples:
1. Eu já anoto o que dá errado (falhas, bloqueios, reprovações, lições)? Se não, como começo com uma linha por erro?
2. Rode o alerta do dia nos meus projetos e me mostre o erro que mais voltou.
3. Qual tarefa minha se repete tanto que deveria virar motor (programa fixo, com a IA só onde precisa pensar)?
4. Para essa tarefa, vale medir modelos e esforços antes de escolher? Quanto isso gastaria da minha assinatura?
Não mude nada nem ligue nenhum agendamento ainda. Mostre o plano e espere eu dizer sim.
```

## A ideia em uma frase

Agente livre serve para o que é novo. Para o que se repete, ele gasta demais e erra de um jeito diferente a cada vez. Quando a tarefa repetida vira **motor** (passos fixos + IA só no julgamento + conferência + uma linha no caderno quando falha), e o motor é melhorado toda semana pelo que o alerta mostra, o erro repetido cai, o gasto cai e a entrega fica igual todo dia.

## A prova (medida em 20/11/2026, nos 231 projetos do ARCKHé AI)

| O quê | Resultado |
|---|---|
| Mesmo bloqueio repetido (a IA procura `python`/`identify`, que não existem na máquina, para conferir imagem) | **355 vezes** desde 17/09, 103 só em 18/11 |
| Reincidência da semana (registros que já tinham acontecido antes) | **17%** (semana anterior: 18%) |
| Alerta do dia feito por **agente livre** (Sonnet, esforço médio) | 35 s · 7 turnos · 182 mil tokens lidos · **US$ 0,235** equivalentes · leu por amostra |
| O mesmo alerta feito pelo **motor** (`alerta.py`) | **1,2 s · 0 token · US$ 0** · leu tudo · resultado igual a cada rodada |
| Classificar 24 falhas reais (prompt × infra), nota pelo checador oculto, média de 2 rodadas | Haiku low 9,2 · US$ 0,0019 — Sonnet low 9,4 · US$ 0,027 — Opus high 9,2 · US$ 0,060 (**31× o Haiku**) |
| Codex `gpt-6-luna`, low/medium/high | 8,8 nos três; high levou 11 s contra 6 s |
| Fable 5.2 | não rodou: a conta pedia créditos de uso extra |

O custo é o `total_cost_usd` que o Claude Code informa. Na assinatura você não paga por chamada, mas é a melhor régua de quanto da cota cada rodada consome. Os dados brutos estão em `resultados/`.

---

## Instalação técnica

**Pré-requisitos:** Python 3.9+ (sem dependências). Para `medir.py`: o Claude Code (`claude`) e/ou o Codex (`codex`) logados pela assinatura.

```bash
git clone https://github.com/linnoff88-dev/alerta-conserta-motor.git && cd alerta-conserta-motor
python3 -m unittest discover -s tests -v        # 12 testes, sem rede e sem modelo

python3 alerta.py --raiz ~/projetos             # relatório do dia (hoje + ontem)
python3 alerta.py --raiz ~/projetos --curto     # texto curto para o celular
python3 semana.py --raiz ~/projetos --pasta semana   # aprendizado da semana + foto para comparar
python3 medir.py tarefas/classificar-falhas --modelos haiku,sonnet,opus --esforcos low,medium,high --rep 2
python3 medir.py tarefas/classificar-falhas --motor codex --modelos gpt-6-luna --esforcos low,medium,high
modelos/instalar-timers.sh                      # liga alerta às 08:00 e semana às segundas 07:45 (systemd do usuário)
```

### Arquivos

| Arquivo | O que faz |
|---|---|
| `motor/fontes.py` | Lê os 4 cadernos (formatos abaixo) na raiz e até 2 níveis abaixo, deduplica cópias, agrupa registros parecidos |
| `alerta.py` | Alerta do dia: o que entrou na janela, **o que voltou** (agrupado por assunto), limites abertos, notas baixas e críticas do dono. Sai 1 quando há o que fazer |
| `semana.py` | Reincidência da semana × semana anterior, causas prompt/infra, nota média do revisor por fluxo, assuntos repetidos com o degrau (lição → teste → trava → motor) e o que saiu da lista |
| `medir.py` | Grade modelo × esforço na mesma tarefa, nota por checador oculto, tabela com tempo, tokens e custo; remove `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` do ambiente (só assinatura) e roda o `claude -p` numa config limpa |
| `medicao/agente-livre.sh` | Compara o alerta feito por agente livre com o feito pelo motor |
| `tarefas/classificar-falhas/` | Tarefa de exemplo: 24 falhas reais, gabarito em `oculto/` |
| `modelos/` | Timers systemd (`avm-alerta`, `avm-semana`), `instalar-timers.sh` e `motor-modelo.sh` (esqueleto de motor) |

### Formatos que ele lê (uma linha por ocorrência)

```text
FALHAS.md          | AAAA-MM-DD | o que quebrou | menor correção | prompt|infra |
LIMITES.md         | AAAA-MM-DD | o que tentei | o que barrou | contorno | proposta | aberto|aceito |
revisor-falhas.md  ## AAAA-MM-DD HH:MM · fluxo · item · nota N [· 🧑 crítica do dono]
                   - **Motivo:** ...
LESSONS.md         - regra em uma linha (DD/MM/AAAA)
```

### Mandar o alerta para o celular

O serviço `avm-alerta` passa o texto curto pelo stdin para o comando em `ENVIO=` (padrão `cat`). Troque por um script seu de Telegram, WhatsApp ou e-mail.

### Criar uma tarefa para a balança

Uma pasta com `pedido.txt`, `entrada.json` (opcional) e `oculto/checar.py`, que recebe o arquivo da resposta e imprime `{"nota": 0–10}`. O modelo nunca vê a pasta `oculto/`.

## O processo, do início ao fim

🧠 sessão com você · ⚙️ script/timer · 🤖 `claude -p` / `codex exec`

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Anotar cada erro numa linha, no caderno do projeto | `FALHAS.md` / `LIMITES.md` / `revisor-falhas.md` / `LESSONS.md` | 🧠 🤖 |
| 2 | Todo dia às 08:00, o alerta do dia sai e vai para o celular | `alerta.py --curto` (timer `avm-alerta`) | ⚙️ |
| 3 | Escolher 1 assunto que voltou e decidir o degrau | ler o alerta | 🧠 |
| 4 | Se for tarefa repetida: medir modelo × esforço antes de escrever o motor | `medir.py <tarefa>` | 🤖 |
| 5 | Escrever o motor (passos fixos + IA só no julgamento + conferência + linha no caderno quando falha) | `modelos/motor-modelo.sh` como base | 🧠 + 🤖 |
| 6 | Testar o motor | `python3 -m unittest` / o teste do motor | ⚙️ |
| 7 | Toda segunda às 07:45: reincidência × semana anterior e o que saiu da lista | `semana.py --pasta semana` (timer `avm-semana`) | ⚙️ |
| 8 | Repetir: o próximo assunto do topo | — | 🧠 |

## Combina com

- [agente-que-aprende](https://github.com/linnoff88-dev/agente-que-aprende): transforma uma lição em gancho que bloqueia o comando errado (o degrau "trava").
- [SIL Loop R](https://github.com/linnoff88-dev/sil-loop-r): portão humano para lição virar regra.

## Licença

MIT · grátis no [linnoff88-dev.github.io](https://linnoff88-dev.github.io), direto na internet.
