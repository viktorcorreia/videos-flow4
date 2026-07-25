# STATUS — videos-flow4

**Situação:** pipeline UGC POV rodando fim-a-fim (geração Veo → montagem → upscale 1080×1920 → legendas); workflow versionado no git, mídias fora do repo.

## Próximo passo
Rodar o lote seguinte de produtos POV usando `produtos/pov-lote2-sapatos/gerar_pov.py` como template (copiar pasta, trocar `edl.json` + prompts) e publicar os 4 finais que já estão em `mass-edit/final/`.

## Onde está o quê
- `workflow.md` — descrição do pipeline completo (fonte da verdade)
- `ideal.md` — referência de qualidade alvo dos vídeos
- `produtos/pov-lote1/`, `produtos/pov-lote2-sapatos/` — `gerar_pov.py` (Veo/GCP) + `montar_pov.py` (concat/fade) + `edl.json` por produto + `final/legendas.txt`
- `mass-edit/edit/` — montagem em lote: `montar_finais.py`, `gen_tts.ps1`, `catalogo/` (scraping/geração do catálogo de produtos)
- `modal/upscale_modal.py` — Real-ESRGAN 1080×1920 no Modal
- `modal/llm_abliterated.py` — Qwen3.6-35B-A3B abliterated (H100, standby 15min, idle zero-custo)
- `edit/`, `download/edit/`, `produtos/*/edit/` — `project.md` + `edl.json` + `transcripts/` de cada montagem

## Decisões
- **Estilo:** todo prompt de geração é POV com mãos pegando o produto.
- **Voz:** ElevenLabs `GOkMqfyKMLVUcYfO2WbB` (jenifer, interior-SP), stability 0.3, tag `[excited]`. Testadas roberta→jenifer; jenifer venceu.
- **Legendas:** framework de 7 níveis — keyword na 1ª palavra, pergunta binária, 100–150 chars, 5 hashtags, plano B em 24h.
- **Repo:** só workflow/scripts/EDL/transcripts. `.gitignore` bloqueia vídeo, imagem, áudio e zips — as mídias vivem no disco, não no git.
- **Segredos:** nada hardcoded. `modal/llm_abliterated.py` lê `MODAL_LLM_API_KEY` do ambiente (era literal antes do commit 89f268a).
- **Workspace:** geração Veo/catálogo histórico também existe em `C:\dev\tiktok-ugc-pipeline`.

## Bloqueios conhecidos
- Higgsfield: trial unlimited é **web-only**, CLI bloqueado (v1.1.19 sem `use_unlim`, JWT 60s, DataDome).
- Dolphin/Hermes: sem native tool support.
