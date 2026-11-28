# Alarma de Errores — audita y propone el arreglo

[![alerta-conserta-motor](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/alerta-conserta-motor/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Dejar a un agente de IA libre para crear todo el tiempo sale caro y hace que repita errores. Este kit lee los cuadernos donde anotas lo que salió mal (fallos, bloqueos, rechazos y lecciones) y envía una alerta cada día. Cada semana mide si el mismo error disminuyó y señala qué debería convertirse en **motor**: un paso fijo, realizado por un programa, en el que la IA solo interviene cuando necesita pensar. También prueba varios modelos y niveles de esfuerzo en la misma tarea, para que puedas usar el más barato que todavía acierta. Sirve para quienes usan Claude Code o Codex en el trabajo. Solo necesitas uno de los dos. La IA instala el kit por ti.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://linnoff88-dev.github.io/alerta-conserta-motor/guia/es/**

<!-- VIDEO-README: entra o link do explicavideo quando publicado -->

## Cómo empezar (sin instalar nada a mano)

Abre Claude Code o Codex en la carpeta de tus proyectos y pega esto:

```text
Lee el kit "alerta-conserta-motor" en https://github.com/linnoff88-dev/alerta-conserta-motor (el README explica todo, incluida la instalación).
Después, revisa mis proyectos y respóndeme en español sencillo:
1. ¿Ya anoto lo que sale mal (fallos, bloqueos, rechazos, lecciones)? Si no, ¿cómo empiezo con una línea por error?
2. Ejecuta la alerta del día en mis proyectos y muéstrame el error que más se repitió.
3. ¿Qué tarea mía se repite tanto que debería convertirse en motor (programa fijo, con la IA solo donde necesita pensar)?
4. Para esa tarea, ¿vale la pena medir modelos y niveles de esfuerzo antes de elegir? ¿Cuánto consumiría de mi suscripción?
No cambies nada ni actives ningún horario todavía. Muéstrame el plan y espera a que te diga que sí.
```

## La idea en una frase

Un agente libre sirve para lo que es nuevo. Para lo que se repite, gasta demasiado y se equivoca de forma distinta cada vez. Cuando la tarea repetida se convierte en **motor** (pasos fijos + IA solo para juzgar + revisión + una línea en el cuaderno cuando falla), y el motor mejora cada semana con lo que muestra la alerta, los errores repetidos disminuyen, el gasto baja y el resultado es el mismo todos los días.

## La prueba (medida el 20/11/2026, en los 231 proyectos de ARCKHé AI)

| Qué | Resultado |
|---|---|
| El mismo bloqueo repetido (la IA busca `python`/`identify`, que no existen en la máquina, para revisar una imagen) | **355 veces** desde el 17/09, 103 solo el 18/11 |
| Reincidencia de la semana (registros que ya habían aparecido antes) | **17%** (semana anterior: 18%) |
| Alerta del día hecha por un **agente libre** (Sonnet, esfuerzo medio) | 35 s · 7 turnos · 182 mil tokens leídos · equivalentes a **US$ 0,235** · leyó una muestra |
| La misma alerta hecha por el **motor** (`alerta.py`) | **1,2 s · 0 tokens · US$ 0** · leyó todo · mismo resultado en cada ejecución |
| Clasificar 24 fallos reales (prompt × infraestructura), puntuación del evaluador oculto, promedio de 2 rondas | Haiku low 9,2 · US$ 0,0019 — Sonnet low 9,4 · US$ 0,027 — Opus high 9,2 · US$ 0,060 (**31× Haiku**) |
| Codex `gpt-6-luna`, low/medium/high | 8,8 en los tres; high tardó 11 s, frente a 6 s |
| Fable 5.2 | no se ejecutó: la cuenta pedía créditos de uso extra |

El costo es el `total_cost_usd` que informa Claude Code. Con la suscripción no pagas por llamada, pero es la mejor medida de cuánto consume cada ejecución de tu cuota. Los datos sin procesar están en `resultados/`.

---

## Instalación técnica

**Requisitos:** Python 3.9+ (sin dependencias). Para `medir.py`: Claude Code (`claude`) y/o Codex (`codex`) con sesión iniciada mediante la suscripción.

```bash
git clone https://github.com/linnoff88-dev/alerta-conserta-motor.git && cd alerta-conserta-motor
python3 -m unittest discover -s tests -v        # 12 pruebas, sin red y sin modelo

python3 alerta.py --raiz ~/projetos             # informe del día (hoy + ayer)
python3 alerta.py --raiz ~/projetos --curto     # texto breve para el celular
python3 semana.py --raiz ~/projetos --pasta semana   # aprendizaje de la semana + foto para comparar
python3 medir.py tarefas/classificar-falhas --modelos haiku,sonnet,opus --esforcos low,medium,high --rep 2
python3 medir.py tarefas/classificar-falhas --motor codex --modelos gpt-6-luna --esforcos low,medium,high
modelos/instalar-timers.sh                      # activa la alerta a las 08:00 y la semana los lunes a las 07:45 (systemd del usuario)
```

### Archivos

| Archivo | Qué hace |
|---|---|
| `motor/fontes.py` | Lee los 4 cuadernos (formatos abajo) en la raíz y hasta 2 niveles más abajo, elimina duplicados y agrupa registros parecidos |
| `alerta.py` | Alerta del día: qué se agregó en el período, **qué se repitió** (agrupado por tema), límites abiertos, puntuaciones bajas y críticas del responsable. Devuelve 1 cuando hay algo que hacer |
| `semana.py` | Reincidencia de la semana × semana anterior, causas de prompt/infraestructura, puntuación promedio del revisor por flujo, temas repetidos con su etapa (lección → prueba → bloqueo → motor) y lo que salió de la lista |
| `medir.py` | Tabla modelo × esfuerzo para la misma tarea, puntuación del evaluador oculto, tabla con tiempo, tokens y costo; elimina `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` del entorno (solo suscripción) y ejecuta `claude -p` con una configuración limpia |
| `medicao/agente-livre.sh` | Compara la alerta hecha por un agente libre con la hecha por el motor |
| `tarefas/classificar-falhas/` | Tarea de ejemplo: 24 fallos reales, respuestas correctas en `oculto/` |
| `modelos/` | Timers de systemd (`avm-alerta`, `avm-semana`), `instalar-timers.sh` y `motor-modelo.sh` (plantilla de motor) |

### Formatos que lee (una línea por incidencia)

```text
FALHAS.md          | AAAA-MM-DD | o que quebrou | menor correção | prompt|infra |
LIMITES.md         | AAAA-MM-DD | o que tentei | o que barrou | contorno | proposta | aberto|aceito |
revisor-falhas.md  ## AAAA-MM-DD HH:MM · fluxo · item · nota N [· 🧑 crítica do dono]
                   - **Motivo:** ...
LESSONS.md         - regra em uma linha (DD/MM/AAAA)
```

### Enviar la alerta al celular

El servicio `avm-alerta` pasa el texto breve por stdin al comando de `ENVIO=` (por defecto, `cat`). Cámbialo por tu propio script de Telegram, WhatsApp o correo electrónico.

### Crear una tarea para la balanza

Una carpeta con `pedido.txt`, `entrada.json` (opcional) y `oculto/checar.py`, que recibe el archivo de respuesta e imprime `{"nota": 0–10}`. El modelo nunca ve la carpeta `oculto/`.

## El proceso, de principio a fin

🧠 sesión contigo · ⚙️ script/timer · 🤖 `claude -p` / `codex exec`

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Anotar cada error en una línea, en el cuaderno del proyecto | `FALHAS.md` / `LIMITES.md` / `revisor-falhas.md` / `LESSONS.md` | 🧠 🤖 |
| 2 | Cada día a las 08:00, se genera la alerta del día y se envía al celular | `alerta.py --curto` (timer `avm-alerta`) | ⚙️ |
| 3 | Elegir un tema que se repitió y decidir su etapa | leer la alerta | 🧠 |
| 4 | Si es una tarea repetida: medir modelo × esfuerzo antes de escribir el motor | `medir.py <tarefa>` | 🤖 |
| 5 | Escribir el motor (pasos fijos + IA solo para juzgar + revisión + una línea en el cuaderno cuando falla) | usar `modelos/motor-modelo.sh` como base | 🧠 + 🤖 |
| 6 | Probar el motor | `python3 -m unittest` / la prueba del motor | ⚙️ |
| 7 | Cada lunes a las 07:45: reincidencia frente a la semana anterior y lo que salió de la lista | `semana.py --pasta semana` (timer `avm-semana`) | ⚙️ |
| 8 | Repetir: el siguiente tema de la parte superior | — | 🧠 |

## Se combina con

- [agente-que-aprende](https://github.com/linnoff88-dev/agente-que-aprende): convierte una lección en un gancho que bloquea el comando incorrecto (la etapa «bloqueo»).
- [SIL Loop R](https://github.com/linnoff88-dev/sil-loop-r): puerta humana para convertir una lección en una regla.

## Licencia

MIT · gratis en [linnoff88-dev.github.io](https://linnoff88-dev.github.io), directamente en internet.