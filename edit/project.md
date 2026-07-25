## Session 1 — 2026-07-20

**Strategy:** Unir os 3 clipes Veo da raiz (1-lys.mp4, Woman_applying_Hidrabene, Woman_holding_sunscreen) na ordem HOOK → BENEFÍCIO → CTA, só com cortes de correção (sem grade/legendas).

**Decisions:**
- Lys (HOOK): removido gaguejo "não some com as, não some com as manchas" → mantida só a versão limpa. Dois ranges: 1.57-4.15 e 4.93-6.30.
- Hidrabene (BENEFIT): cortada cauda de 2.4s de silêncio + som de pássaro após a fala terminar (7.22s); mantido até 8.00s pra segurar o sorriso final.
- Sunscreen (CTA): cortado lead-in de 2.6s de silêncio antes da fala; range final 2.20-7.90.
- Sem grade de cor nem legendas (pedido explícito do usuário).
- Duração final: 17.73s.

**Reasoning log:** stutter fix na Lys é jump-cut inevitável (mesmo plano contínuo), mascarado só pelo fade de áudio de 30ms — aceitável pois é uma correção pontual de fala.

**Outstanding:** nenhum.

## Session 2 — 2026-07-21

**Strategy:** analisei todos os 18 vídeos soltos na raiz e separei por produto: (A) Hidrabene protetor solar — já coberto pela Sessão 1, mais 6 clipes de b-roll mudo do produto ainda não usados (2aa1e536, 36742ead, 68433c34, 96744c04, c2bc098a, ca108adb — todos mesma criadora, tubo Hidrabene em close/aplicação); (B) Body Splash/perfume My Sweet Delight — 4 clipes de fala + 1 duplicata em resolução menor; (C) descartados: `Person_sprays_product_on_neck` (inglês, "warm vanilla scent" — produto/idioma diferente, não bate com a linha lichia/bergamota/cedro) e `Girl_smiles_showing_collarbone_hair` (criadora diferente, produto tipo sérum, já tem botão "Shop Now" queimado — é material de referência/concorrente, não footage nosso).

**Decisions:**
- Cena 2 (Body Splash, `scene2_perfume.mp4`, editor: video-use): HOOK "body splash não substitui perfume" (myth-bust, alinhado ao risco/não-fazer do README do produto) → ROTINA "meu cheiro de todo dia... tecido segura mais que a pele" → CTA (só a cauda de `Woman_holding_bottle_speaking_1080p`, 7.89-9.99s, pra não duplicar o clipe inteiro já usado em `produtos/lys-produtos/01-body-splash-my-sweet-delight/edit/final.mp4`). Grade `warm_cinematic`, legendas queimadas, loudnorm. Duração 17.2s.
- Não testei HyperFrames nesta rodada: nenhum dos dois grupos de produto tinha necessidade real de motion graphics/overlay de UI — forçar o uso teria sido pior que a ferramenta certa (video-use, cortes de fala por transcript).
- Bug reincidente: filtro `subtitles` do ffmpeg quebra com path absoluto do Windows (dois-pontos). Contorno: sempre `cd` para `edit/` e usar path relativo pro `.srt`.

**Outstanding:**
- Hidrabene tem 6 clipes de b-roll mudo (produto em close, aplicação, gesto) ainda não incorporados — dá pra fazer uma Cena 1B com cutaways entre as falas da Sessão 1, se o usuário quiser.
- `Person_sprays_product_on_neck` e `Girl_smiles_showing_collarbone_hair` ficaram de fora — confirmar com o usuário se são de outro produto/teste antes de descartar de vez.
