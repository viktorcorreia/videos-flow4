# Body Splash My Sweet Delight — edit log

## Session 1 — 2026-07-21

**Strategy:** apenas 2 takes brutas disponíveis em `geracoes/` (ambas do mesmo produto, ~10s cada, fala completa sem cortes internos). Reordenei para HOOK+DICA (mito "body splash não fixa" + rotina de hidratação) → COMPARAÇÃO+CTA (comparação com perfume importado + "comenta aí"), em vez da ordem cronológica original, para abrir com gancho de atenção e fechar com CTA de engajamento.

**Decisões:**
- Editor: video-use (footage de fala/rosto, não motion graphics — hyperframes não se aplica aqui).
- Takes usadas: as 2 únicas disponíveis, integrais (sem trim de conteúdo, só padding de 50ms nas bordas de palavra).
- Grade: `warm_cinematic` (leve teal/orange, seguro para pele).
- Legendas: burned-in, 2 palavras por chunk, UPPERCASE, `MarginV=90` (estilo bold-overlay, ajustado pra não cortar no rodapé do formato 9:16).
- Áudio: loudnorm 2-pass (-14 LUFS / -1 dBTP / LRA 11), fades de 30ms em cada corte.
- Duração final: 19.9s (dentro da meta de 16-24s).

**Reasoning log:**
- Ordem invertida (spray→bottle) porque o mito "não fixa" prende mais no primeiro segundo que a comparação de preço.
- Bug de path do Windows no filtro `subtitles` do ffmpeg (dois-pontos no path absoluto quebra o parser do libass) — contornado rodando o ffmpeg com cwd em `edit/` e path relativo `master.srt`, em vez de via `render.py` direto.

**Outstanding:**
- Só existem 2 takes para este produto — se houver banco maior de geração de vídeo (Veo/Kling), vale gerar mais variações de hook/CTA para A/B.
- Comparação de editores (video-use vs hyperframes) não se aplica aqui: hyperframes é motion graphics/UI, e este material é 100% talking-head. Fica para produtos que tenham overlay de dados/UI.
