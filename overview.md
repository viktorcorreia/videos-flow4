# overview.md — Pipeline UGC (videos-flow4)

Documento de referência: workflow, ferramentas e por que escolhemos cada uma. Atualizar sempre que o processo mudar.

## O que é este projeto

Pipeline de vídeos UGC afiliados pra TikTok Shop, usando a avatar de IA **Maya** (Veo/Kling/Seedance geram os clipes brutos com a Maya usando o produto). O trabalho do Claude Code aqui é: analisar o material bruto, cortar/editar, dublar/ajustar áudio quando preciso, corrigir glitches visuais de geração por IA, e entregar o vídeo final pronto pra postar. Contexto de monetização e status da conta em `MONETIZE.md`.

## Estrutura de pastas

```
videos-flow4/
├── .env                          ← chaves de API (ElevenLabs, MuAPI, OpenAI, Apify, Groq)
├── MONETIZE.md                   ← modelo de receita, status da conta, metas
├── overview.md                   ← este arquivo
├── avatares/                     ← fotos de referência da Maya (corpo/rosto), não ligadas a um produto específico
├── _triagem/                     ← arquivos órfãos/soltos aguardando revisão manual (não classificados em nenhum produto)
├── capilar/                      ← projeto/nicho separado (fora do padrão de produtos)
└── produtos/
    └── <NN>-<slug-do-produto>/
        ├── produto.json / README.md / README-origem.md   ← metadata do produto (preço, comissão, hooks, ângulo criativo)
        ├── referencia/            ← material FONTE do produto (fotos de catálogo, não gerado por IA)
        ├── geracoes/              ← TUDO gerado por IA: vídeos brutos (Veo/Kling/Seedance) + imagens da Maya com o produto
        └── edit/                 ← output de trabalho do skill video-use (ver abaixo)
            ├── transcripts/<nome>.json   ← cache de transcrição (ElevenLabs Scribe, nunca re-gerar se a fonte não mudou)
            ├── takes_packed.md           ← transcrição em nível de frase, a "visão de leitura" principal
            ├── edl.json                  ← decisão de corte (Edit Decision List)
            ├── master.srt                ← legendas com offset da timeline final
            ├── preview.mp4 / final.mp4
            └── project.md                ← memória da sessão de edição (decisões, motivo)
```

## Skills disponíveis e qual usamos

| Skill | Pra que serve | Usamos neste projeto? |
|---|---|---|
| **`watch`** | Analisar um vídeo (baixar se for URL, extrair frames, ler transcript/legenda) e responder perguntas visuais sobre ele — ex: "em que timestamp aparece o glitch de braço extra?" | **Sim** — é a ferramenta de QC visual. Usada pra detectar glitches de geração por IA (membros extras, artefatos) em momentos específicos do vídeo. |
| **`video-use`** | Skill principal de edição: transcrição word-level (ElevenLabs Scribe) → transcript compactado → estratégia de corte confirmada com o usuário → EDL → render (extract por segmento + concat lossless + overlays + legendas) → self-eval automático antes de mostrar. | **Sim — é o motor de tudo.** Todo corte, dublagem, correção de glitch e composição final passa por aqui. |
| **Remotion** (motor de animação dentro do video-use) | Composições React/CSS com estado, bom quando já existe um design system em React. | **Não usado ainda.** Chegamos a ter um projeto Remotion solto (`ugc-editor/`) mas não fazia parte do fluxo real — foi removido na limpeza de 2026-07-17. |
| **HyperFrames** (motor de animação dentro do video-use) | Composições HTML/CSS/GSAP nativas de browser: motion de UI, tipografia cinética, overlays com verificação determinística de frame (lint/validate/render). | **Não usado ainda**, mas é o motor recomendado *se* algum dia precisarmos de um overlay tipo card de preço ou callout animado — mais leve e mais fácil de validar frame-a-frame que Remotion pra esse tipo de peça simples. |
| **PIL + PNG sequence + ffmpeg** (motor de animação dentro do video-use) | Overlays simples: contador, texto datilografado, barra de progresso. Rápido de iterar. | Não usado ainda. |
| **Manim** (motor de animação dentro do video-use) | Diagramas formais, equações, grafos. | Não se aplica a este tipo de conteúdo (UGC de produto, não educacional/técnico). |

### Por que video-use é o motor central e não Remotion/HyperFrames direto

O material de origem já vem com a Maya falando (áudio nativo com narração do produto). O trabalho não é "criar uma animação do zero" — é **selecionar a melhor tomada, cortar no ponto certo, corrigir imperfeições e legendar**. Isso é edição audio-first (corte por palavra/silêncio), não motion design. Por isso os motores de animação (Remotion/HyperFrames/Manim) ficaram parados: eles só entram em cena se um vídeo específico pedir um overlay gráfico (ex: card de preço animado, callout de "R$27,22"), o que até agora não foi necessário — a fala + legenda já comunicam o preço e a oferta.

Se/quando precisarmos de overlay animado: **HyperFrames é a escolha padrão** (mais leve, checagem determinística de frame, ideal pra cards simples de preço/CTA) — **Remotion só entraria** se precisássemos de lógica de componente React reutilizável entre muitos vídeos (não é o caso hoje, catálogo de produtos é editado um a um).

## Ferramentas externas (APIs)

- **ElevenLabs**
  - *Scribe* (transcrição word-level verbatim) — todo corte se baseia nisso.
  - *Text-to-Speech* — quando o roteiro precisa ser gerado do zero numa voz específica (`MAYA_VOICE_ID`, custom).
  - *Dubbing API* — traduz + dubla com clonagem automática da voz original; bom quando não precisamos de voz de marca fixa.
  - *Speech-to-Speech (STS)* — converte a voz mantendo texto e timing originais; melhor opção quando o áudio já está no idioma certo e só queremos trocar o timbre pra voz da marca (usado no fix do vídeo 33).
- **ffmpeg/ffprobe** — extração de segmento, concat lossless, fades de 30ms nos cortes, grade de cor, mux de áudio, `atempo` pra ajustar duração de áudio sem cortar palavra.
- **Kling / MuAPI** — avaliados para lipsync automatizado; não viáveis no momento (Kling limita a 10s de lipsync, insuficiente pra clipes de 15-23s; MuAPI sem saldo suficiente). Geração de vídeo bruto (Kling/Seedance) continua sendo usada.

## Fluxo típico de uma tarefa

1. **Inventário**: `ffprobe` nos vídeos fonte, `transcribe_batch.py` na pasta, `pack_transcripts.py` gera `takes_packed.md`.
2. **QC visual** (se suspeita de glitch): skill `watch`, ou extração de frames + subagentes `explorador` (haiku) rodando em paralelo pra escanear muitos frames sem pesar no contexto principal.
3. **Conversa + estratégia**: proponho corte/dublagem/grade em português simples, **espero confirmação** antes de tocar em qualquer arquivo.
4. **Execução**: EDL → render.py (extract por segmento → concat → overlays → legendas por último) → self-eval automático (checa pop de áudio, flash visual, legenda escondida) antes de mostrar o preview.
5. **Persistência**: decisões registradas em `edit/project.md` de cada produto.

## Organização de arquivos (convenção, 2026-07-17)

- `referencia/` = fonte do produto, nunca gerado por IA.
- `geracoes/` = tudo que saiu de IA (Veo/Kling/Seedance + imagens compostas da Maya).
- `edit/` = meu output de trabalho (video-use).
- `_triagem/` = qualquer arquivo órfão que apareça solto — não decido sozinho o destino, fica ali até revisão.

## Limpeza — 2026-07-17

Removidos por não fazerem parte do fluxo ativo: `ugc-editor/` (projeto Remotion solto, 491MB), `edit.zip` (backup manual antigo, 802MB), `generated/` (renders de teste validados, 584MB), `.playwright-mcp/` (cache de logs de debug, 0.5MB).
