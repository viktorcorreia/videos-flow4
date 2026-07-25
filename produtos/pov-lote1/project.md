# Sessão 2026-07-25 — Lote POV 1

Primeiro lote no novo formato padrão: POV, mãos pegando/mostrando o produto (memória `estilo-pov-maos`).

## Entregue (`final/`)
- `final_04-body-splash-msd.mp4` — 16,95s, 1080x1920 (hero 2,0s → detalhe 6,99s → uso-crop 7,9s)
- `final_07-rubyrose-gloss.mp4` — 15,05s (detalhe 2,0s → hero t≥2,5 5,4s → swatch 7,57s)
- `final_08-kiss-cilios.mp4` — 16,59s (hero 2,0s → detalhe 6,59s → uso 7,9s)
- `legendas.txt` — legenda + variação + hashtags por vídeo

## Pipeline
Geração: `gerar_pov.py` (veo-3.1-fast, 8s, 720p, conta GCP vikatohugo) — 9/9 ok, ~1min/clipe.
Verificação FASE 1: 9/9 aprovados. Ajustes: 04/pov_uso barras brancas → crop 576x1024→720x1280; 07/pov_hero abre no frame de catálogo (i2v) → entrada em t=2,5s; 08 rótulo com texto levemente embaralhado em movimento (tolerável).
Locução: voz `jenifer` (GOkMqfyKMLVUcYfO2WbB, paulista do interior, stability 0.3 + [excited]) — escolhida após testar achadinhos → roberta → carla/jenifer. Finais: 21,7s / 18,2s / 21,9s. Montagem: `montar_pov.py` (alvo = locução+0,65s, ambiente 20%, loudnorm -14 LUFS, upscale 1080x1920 no render).

## Lições
- i2v Veo: o 1º frame É a imagem de produto crua — hero de catálogo com fundo branco precisa de trim de entrada ou usar foto ambientada como start.
- POV sem fala elimina QA de WER → ciclo por produto ~5 min de geração + edição. Escala fácil.
