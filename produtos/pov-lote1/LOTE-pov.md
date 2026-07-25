# Lote POV 1 — mãos + produto (2026-07-25)

Novo formato padrão: **POV primeira pessoa**, mãos pegando/mostrando o produto, cara de celular. Sem avatar falando — a fala entra depois via locução TTS (FASE 4 do workflow.md).

## Geração

- `gerar_pov.py` → chama `C:\dev\tiktok-ugc-pipeline\scripts\veo\veo_generate.py`
- Conta GCP: `vikatohugo` (massive-dryad-497003-h2, expira 2026-08-20)
- Config: veo-3.1-fast · 8s · 9:16 · 720p · crop · áudio ambiente nativo · negative anti-distorção de mãos (preset `negative_venda`)
- Retomável: rodar de novo pula clipes já gerados.

## Produtos e cenas (3 por produto)

| Produto | hero | detalhe | uso |
|---|---|---|---|
| 04 Body Splash My Sweet Delight (R$32,63, com. 14%) | mãos pegam o frasco na pia | rotação close no rótulo/tampa | borrifa no pulso |
| 07 Ruby Rose Gloss Tint (R$14,92) | mãos pegam o tubo na penteadeira | abre e puxa o aplicador com fio de gloss | swatch no dorso da mão |
| 08 KISS Cílios Magnéticos (R$76,23) | mãos pegam a embalagem | mostra os ímãs na banda do cílio | clique dos ímãs com aplicador |

## Próximas fases (workflow.md)

1. FASE 1 — verificar f1/f2 de cada clipe (produto certo, mãos sem distorção)
2. FASE 3-4 — roteiro 4 beats + locução TTS voz `achadinhos`
3. FASE 5-8 — EDL, render, mux (ambiente a 20%), self-check, `final/`
