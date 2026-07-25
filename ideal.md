# Workflow ideal — mesmo processo com R$1000 GCP + US$500 Modal

O que muda no `workflow.md` se usarmos os créditos que já temos parados (e que expiram). O formato do vídeo NÃO muda — corte seco, cara de celular. Os créditos atacam os 3 gargalos reais do pipeline: catalogação errada, resolução 720p e falta de material.

## Onde dói hoje vs. o que os créditos resolvem

| Gargalo hoje | Custo real | Solução com crédito | Ganho |
|---|---|---|---|
| Catalogação errada (crossfade fantasma) → verificação manual frame a frame de cada clipe | ~30-40 min/lote do modelo principal | **Vertex AI Gemini 2.5/3 Pro** com `response_schema` (JSON mode) + 4 frames/clipe (0%, 33%, 66%, 100%) | catálogo confiável de primeira; verificação vira amostragem |
| Clipes 720x1280 → upscale burro de 50% no render (imagem mole) | qualidade visível no feed | **Modal GPU**: Real-ESRGAN/video (A10G, ~US$1/h) upscale 720→1080 nativo em lote | nitidez de 1080 real; US$500 upscalam MILHARES de clipes |
| Transcrição depende da cota ElevenLabs Scribe | cota compartilhada com TTS | **Modal**: WhisperX serverless (word-level + alignment), ~US$0,01/h de áudio | transcrição ilimitada de graça na prática; cota ElevenLabs 100% pro TTS |
| 9 grupos com 1 clipe e 1 grupo com 2 → produtos parados na fila | 10 produtos sem vídeo | **Vertex Veo** (image-to-video a partir do frame bom do clipe existente) gera os 2 clipes complementares | destrava ~10 produtos com o mesmo catálogo |
| Vídeos saem 14-20s (clipes de 4-8s) | abaixo do alvo 24-30s da skill | Veo gera clipes de 8s extras por produto (4º clipe) | vídeos no alvo de retenção |

## Pipeline ideal (diferenças em negrito)

```
clipes .mp4
  ├─ FASE 0  catalogar.ps1 (4 frames) → **Vertex Gemini Pro JSON mode** → catálogo confiável
  ├─ FASE 1  verificação por AMOSTRAGEM (não mais 100% manual)
  ├─ FASE 1b **Veo (GCP): gerar clipes complementares** p/ grupos de 1-2 clipes
  ├─ FASE 1c **Modal: upscale 720→1080 Real-ESRGAN em lote** (fila GPU paralela)
  ├─ FASE 2  **Modal: WhisperX word-level** (quando houver fala)
  ├─ FASE 3-8 idênticas ao workflow.md (roteiro, TTS eleven_v3, render, mux, post)
```

## Orçamento estimado

| Item | Crédito | Estimativa de consumo |
|---|---|---|
| Vertex Gemini Pro (catalogação, ~50 imagens/lote) | GCP | centavos por lote — irrelevante |
| Veo image-to-video 8s/720p+ | GCP | ~R$2-4/clipe → R$1000 ≈ 250-500 clipes ≈ 80-150 produtos novos |
| Modal WhisperX (T4) | Modal | ~US$0,01 por hora de áudio — irrelevante |
| Modal Real-ESRGAN upscale (A10G) | Modal | ~US$0,02-0,05/clipe de 8s → US$500 ≈ 10.000+ clipes |

Ou seja: **os créditos cobrem meses de operação em volume 10-20x o atual.**

## O ganho concreto, em uma frase por eixo

- **Qualidade visual**: 1080 real em vez de 720 esticado — a diferença aparece no primeiro frame, que é onde o scroll decide.
- **Confiabilidade**: catálogo que não mistura produtos = zero risco de vídeo mostrando o sapato errado (erro que mata conta de afiliado).
- **Volume**: os 13 grupos do lote atual viram ~13 vídeos (não 4-5), e cada lote futuro rende quase 100% dos grupos.
- **Velocidade**: verificação por amostragem + GPU paralela derruba o tempo por lote de horas pra dezenas de minutos.
- **Custo de oportunidade**: são créditos que EXPIRAM — cada semana sem usar é dinheiro queimado.

## Ordem de implementação sugerida (maior retorno primeiro)

1. **Modal upscale batch** (1 script, resolve o problema visível em TODOS os vídeos já feitos e futuros) — ~1h de setup.
2. **Vertex Gemini catalogação** (troca o `agy` flash-low por chamada Vertex com schema) — ~1h.
3. **Veo complementar** (destrava os 10 produtos parados do lote atual) — ~2h incluindo prompts.
4. **Modal WhisperX** (só quando aparecer lote com fala real) — deixar pronto o esqueleto.
