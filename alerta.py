#!/usr/bin/env python3
"""alerta.py — o alerta do dia: o que deu errado ontem/hoje e o que Já tinha dado errado antes.

Lê FALHAS.md, LIMITES.md, revisor-falhas.md e LESSONS.md da raiz e dos projetos abaixo dela.
Não chama modelo, não usa rede. Custa zero token.

  python3 alerta.py --raiz ~/projetos                 # últimas 24 h (hoje + ontem)
  python3 alerta.py --raiz ~/projetos --dias 3 --saida alertas/$(date +%F).md
  python3 alerta.py --raiz ~/projetos --curto | <seu envio>   # texto curto para Telegram/WhatsApp/e-mail

Saída 0 = nada pede ação · 1 = tem alerta (reincidência, limite aberto, nota baixa) · 2 = erro de uso.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from motor import fontes  # noqa: E402

ICONE = {"falha": "🔴", "limite": "🟠", "revisor": "🟣", "licao": "🟢"}


def montar(regs, hoje: dt.date, dias: int, nota_baixa: float, limiar: float):
    ini = hoje - dt.timedelta(days=dias - 1)
    novos = [r for r in regs if ini <= r.data <= hoje]
    antigos = [r for r in regs if r.data < ini]
    voltaram = []
    for r in novos:
        if r.tipo == "licao":
            continue
        ant = fontes.ja_aconteceu(r, antigos, limiar)
        if ant:
            voltaram.append((r, ant))
    # junta os repetidos do mesmo assunto: "arte.png sem identify" 12× hoje vira UM alerta
    temas = []
    for grupo in fontes.agrupar([r for r, _ in voltaram], limiar):
        ids = {id(g) for g in grupo}
        ant = {id(x): x for r, a in voltaram if id(r) in ids for x in a}
        temas.append((grupo, list(ant.values())))
    temas.sort(key=lambda t: -(len(t[0]) + len(t[1])))
    abertos = [r for r in novos if r.tipo == "limite" and r.status.startswith("aberto")]
    baixas = [r for r in novos if r.tipo == "revisor" and r.nota is not None and r.nota < nota_baixa]
    dono = [r for r in novos if r.tipo == "revisor" and r.dono]
    return dict(ini=ini, novos=novos, voltaram=temas, abertos=abertos, baixas=baixas, dono=dono)


def texto_longo(a, hoje) -> str:
    c = collections.Counter(r.tipo for r in a["novos"])
    causa = collections.Counter(("prompt" in r.causa, "infra" in r.causa) for r in a["novos"] if r.tipo == "falha")
    out = [f"# Alerta do dia — {hoje.isoformat()}", "",
           f"Janela: {a['ini'].isoformat()} a {hoje.isoformat()}. "
           f"{c['falha']} falha(s) · {c['limite']} limite(s) · {c['revisor']} reprovação(ões) · {c['licao']} lição(ões) nova(s).",
           ""]
    if c["falha"]:
        p = sum(v for (pp, _), v in causa.items() if pp)
        i = sum(v for (_, ii), v in causa.items() if ii)
        out += [f"Falhas por causa: prompt {p} · infra {i} (as duas contam quando a linha diz as duas).", ""]
    out += ["## ⚠️ Voltou a acontecer (o mais importante)", ""]
    if a["voltaram"]:
        for grupo, ant in a["voltaram"][:12]:
            r = grupo[0]
            primeira = min(x.data for x in ant)
            projs = sorted({x.projeto for x in ant} | {g.projeto for g in grupo})
            extra = f" — exemplo: {r.detalhe[:90]}" if r.detalhe else ""
            out.append(f"- {ICONE[r.tipo]} **{r.texto[:150]}**{extra} · {len(grupo)}× na janela, {len(ant)}× antes, "
                       f"desde {primeira.isoformat()} ({', '.join(projs[:5])}). → vira trava ou motor, não mais uma linha de texto.")
    else:
        out.append("- Nada se repetiu. Bom sinal.")
    out += ["", "## 🟠 Limites ainda abertos", ""]
    out += [f"- {r.texto[:160]} ({r.projeto})" for r in a["abertos"][:10]] or ["- Nenhum."]
    out += ["", "## 🟣 Revisor e críticas do dono", ""]
    linhas = [f"- nota {r.nota:g} · {r.fluxo} · {r.texto[:140]}" for r in a["baixas"][:10]]
    linhas += [f"- 🧑 crítica do dono · {r.fluxo} · {r.texto[:140]}" for r in a["dono"][:10]]
    out += linhas or ["- Nada abaixo da nota mínima."]
    out += ["", "## 🔴 Tudo que entrou na janela", ""]
    for r in sorted(a["novos"], key=lambda x: (x.tipo, x.projeto))[:60]:
        out.append(f"- {ICONE[r.tipo]} {r.projeto}: {r.texto[:150]}")
    return "\n".join(out) + "\n"


def texto_curto(a, hoje) -> str:
    c = collections.Counter(r.tipo for r in a["novos"])
    out = [f"Alerta {hoje.strftime('%d/%m')}: {c['falha']} falhas, {c['limite']} limites, "
           f"{c['revisor']} reprovações, {c['licao']} lições."]
    if a["voltaram"]:
        out.append(f"VOLTOU A ACONTECER ({len(a['voltaram'])} assuntos):")
        for grupo, ant in a["voltaram"][:5]:
            out.append(f"• {grupo[0].texto[:100]} — {len(grupo)}× agora, {len(ant)}× antes")
    if a["abertos"]:
        out.append(f"Limites abertos: {len(a['abertos'])}")
    if a["baixas"] or a["dono"]:
        out.append(f"Revisor: {len(a['baixas'])} nota baixa · {len(a['dono'])} crítica do dono")
    if not (a["voltaram"] or a["abertos"] or a["baixas"] or a["dono"]):
        out.append("Nada pede ação hoje.")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=".", help="pasta com os projetos (lê os 4 arquivos em até --profundidade níveis)")
    ap.add_argument("--profundidade", type=int, default=2)
    ap.add_argument("--dias", type=int, default=2, help="janela em dias contando hoje (padrão 2 = hoje + ontem)")
    ap.add_argument("--hoje", help="AAAA-MM-DD (para testar)")
    ap.add_argument("--nota-baixa", type=float, default=7.0)
    ap.add_argument("--limiar", type=float, default=0.34, help="parecença mínima (0–1) para dizer 'já aconteceu'")
    ap.add_argument("--curto", action="store_true", help="texto curto para mandar no celular")
    ap.add_argument("--saida", help="grava o relatório longo neste arquivo")
    o = ap.parse_args(argv)
    raiz = pathlib.Path(o.raiz).expanduser()
    if not raiz.is_dir():
        print(f"raiz não existe: {raiz}", file=sys.stderr)
        return 2
    hoje = dt.date.fromisoformat(o.hoje) if o.hoje else dt.date.today()
    regs = [r for r in fontes.ler_tudo(raiz, o.profundidade) if r.data <= hoje]
    a = montar(regs, hoje, o.dias, o.nota_baixa, o.limiar)
    longo = texto_longo(a, hoje)
    if o.saida:
        p = pathlib.Path(o.saida).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(longo, encoding="utf-8")
    sys.stdout.write(texto_curto(a, hoje) if o.curto else longo)
    return 1 if (a["voltaram"] or a["abertos"] or a["baixas"] or a["dono"]) else 0


if __name__ == "__main__":
    sys.exit(main())
