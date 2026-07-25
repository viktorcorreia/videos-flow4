# Workflow — Vídeos TikTok Shop (calçados/moda) a partir de clipes gerados

Processo validado no lote `mass-edit/` (41 clipes → 4 vídeos prontos). A skill que governa as decisões editoriais é a `diretor-edicao-tiktok` (`~/.claude/skills/diretor-edicao-tiktok/`).

## A regra que manda em tudo

Os vídeos que vendem nesta categoria são take único, cara de celular: **sem** filtro, transição, SFX, música adicionada, texto na tela, zoom, slow-motion. Corte seco + áudio nivelado. Toda "melhoria" empurra pra comercial, e comercial a pessoa rola.

## Visão geral

```
lote de clipes .mp4 (HeyGen/Veo, 4-10s, b-roll com jingle)
  │
  ├─ FASE 0  Catalogar        (ffmpeg local + Gemini via agy — barato)
  ├─ FASE 1  Verificar        (frames conferidos por IA forte — obrigatório)
  ├─ FASE 2  Transcrever      (Scribe word-level — só se houver fala)
  ├─ FASE 3  Roteiro          (beats da skill, sem inventar ficha)
  ├─ FASE 4  Locução TTS      (ElevenLabs eleven_v3)
  ├─ FASE 5  EDL + Render     (video-use render.py)
  ├─ FASE 6  Mux áudio        (locução P1 + ambiente P2 a 20%)
  ├─ FASE 7  Self-check       (ffprobe + timeline_view nas bordas)
  └─ FASE 8  Post             (descrição 1 frase + 3-5 hashtags)
```

## FASE 0 — Catalogar o lote

1. `pwsh <skill>/scripts/catalogar.ps1 -PastaClipes <pasta>` → extrai 2 frames/clipe + `manifest.json` (duração real, áudio, resolução).
2. UMA chamada `agy` (Gemini flash-low) classifica todos os frames → `catalogo.json` com grupos por produto. Flags antes, `-p "<prompt>"` por último (o `-p` consome o próximo token).

## FASE 1 — Verificar (a lição mais cara do lote 1)

**Nenhum catálogo automático é confiável sozinho.** Clipes HeyGen podem abrir/fechar com crossfade de OUTRO produto; tanto Gemini flash quanto Sonnet erraram agrupamentos. Antes de usar um clipe num vídeo: conferir f1 E f2 dele com o modelo principal. Só entra no EDL clipe cujos dois frames mostram o produto certo. Grupos com menos de 3 clipes limpos não rendem vídeo neste formato.

## FASE 2 — Transcrever (quando houver fala)

- `python tools/video-use/helpers/transcribe_batch.py <pasta>` (key ElevenLabs no `.env` de `C:\dev\tiktok-ugc-pipeline`).
- `pack_transcripts.py --edit-dir <pasta>/edit` → `takes_packed.md`.
- Word-level sempre (corte nunca cai no meio de palavra). Transcript por frase (Gemini) NÃO serve pra corte.
- Se o lote for b-roll sem fala (caso do mass-edit): pular — a fala vem da locução TTS.

## FASE 3 — Roteiro (beats da skill)

- 4 beats: DESCRENÇA DE PREÇO → ACABAMENTO/CONFORTO → OBJEÇÃO DE CORPO → NUMERAÇÃO+CTA. Com 3 clipes, funde beat 2 e 3.
- Objeção por categoria: `references/objecoes-calcados.md` da skill. Excluir parte do público é o que faz o beat funcionar.
- **Sem ficha, sem número**: nunca inventar preço/numeração. Descrença de preço genérica ("tá parecendo erro") e CTA pedindo o número nos comentários.
- CTA condicional, nunca imperativo. Proibido: corre, precinho, últimas unidades, imperdível.
- Tamanho: ~2,6 palavras/segundo. O roteiro TEM que caber no material (soma dos clipes − trims). Medir, regravar se estourar.

## FASE 4 — Locução

- `pwsh mass-edit/edit/gen_tts.ps1 -Texto "..." -Saida loc.mp3` — voz padrão `achadinhos` (Achadinhos Empolgada oficial), modelo `eleven_v3`.
- Pontuação agressiva no texto (reticências, dois-pontos, vírgulas) — o v3 respeita e é isso que dá o ritmo.
- Alternativas: `-Voice maya-clean|maya-clone2|roberta|keren`.

## FASE 5 — EDL + Render

- `python mass-edit/edit/montar_finais.py` monta EDL por produto (lê duração real da locução via ffprobe, alvo = locução + 0,65s), renderiza via `render.py` do video-use.
- Ordem dos clipes: hero → detalhe/acabamento → fechamento (lineup de cores fecha bem com fala de cores).
- Corte seco, `grade: none`, sem legenda queimada, cada clipe entra em t=0,10s. Nunca deixar segmento < 2s.
- O render já aplica: extract por segmento + concat lossless, fades de áudio 30ms nas bordas, loudnorm -14 LUFS.

## FASE 6 — Mux de áudio (2 pistas)

- P1 locução: entra em 0,15s, fade-in 0,1s, fade-out 0,3s no fim.
- P2 ambiente (jingle que veio no clipe): mantido a 20% sob a locução (`amix normalize=0`).
- SEM SFX, SEM música adicionada.

## FASE 7 — Self-check antes de mostrar

- `ffprobe`: duração = locução + ~0,6s, 1080x1920, áudio AAC.
- `timeline_view.py <final> <corte-1s> <corte+1s>`: mesmo produto dos dois lados do corte, sem pop no waveform.

## FASE 8 — Entrega

Toda pasta de lote termina com uma subpasta `final/` contendo **só o que vai pro ar**:

```
<lote>/final/
├── final_<produto>.mp4     (1080x1920, já upscalado)
└── legendas.txt            legenda + hashtags de cada vídeo
```

- Legenda: 1 frase, caso de uso concreto, termina pedindo resposta. Zero markdown, zero marca de terceiro.
- Hashtags: 1 ampla + 2-3 específicas do produto + 1 de contexto de uso.
- Incluir uma VARIAÇÃO por vídeo: se a legenda principal não performar em ~24h, repostar com ela antes de descartar o produto.
- Registrar a sessão em `edit/project.md`.

## Papéis das ferramentas

| Ferramenta | Papel | Nunca usar para |
|---|---|---|
| Gemini via `agy` (flash-low) | catalogar lote, executar render mecânico | decisão editorial, agrupamento final |
| Claude (principal) | verificação visual, roteiro, EDL, decisões | trabalho mecânico em volume |
| video-use (`tools/video-use/`) | transcript word-level, render, timeline_view | — |
| ElevenLabs | TTS (eleven_v3) e Scribe (transcrição) | — |
| HyperFrames / Remotion | overlay SÓ sob pedido explícito ("fora da referência medida") | qualquer coisa por padrão |

## Limitações conhecidas

- Clipes HeyGen saem 720x1280 → upscale de 50% no render (postável; ver `ideal.md` pra resolver).
- Clipes de 4-8s limitam vídeo a ~15-20s com 3 clipes (alvo da skill é 24-30s) — gerar clipes mais longos ou 4 por produto.
- Grupos de 1-2 clipes ficam na fila até gerar material complementar.
