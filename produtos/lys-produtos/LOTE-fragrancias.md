# Lote de fragrâncias — Lys · pronto pra colar no app web

> Trial ilimitado ativo até **24/07 04:37**. Gere tudo dentro dessa janela = custo zero.
> Fluxo: (1) gera a **imagem inicial** no Nano Banana Pro → (2) usa ela como start-image no **Seedance 2.0 Mini** pra virar vídeo.

---

## Configuração fixa (todos os vídeos)

No app web → **Create Video**:

- Modelo: **Seedance 2.0 Mini** · **Unlimited mode: ON** (marca o box)
- **8s · 9:16 · 720p** · Generate audio: ON

No app web → **Image** (Nano Banana Pro):

- Modelo: **Nano Banana Pro** · **Unlimited mode: ON** · **9:16 · 2K**

Estrutura de todo prompt de vídeo (não mexer no rodapé):
```
[direção de cena]
She speaks Brazilian Portuguese with a carioca accent, [tom]: "[fala em PT-BR]"
Ambient noise: quiet indoor room tone, no music.
Negative: subtitles, closed captions, burned-in text, on-screen text, watermark, logo, background music, studio audience, laugh track.
```

---

## Produto 01 — Body Splash My Sweet Delight (Barbour's, R$32,63)

Notas: lichia, peônia e cedro · doce e fresco · desodorante corporal 200ml.

### Imagem inicial → JÁ PRONTA ✅
Arquivo: `produtos/lys-produtos/01-body-splash-my-sweet-delight/geracoes/lys_start_frame.png`
(Sobe esse arquivo direto no card de imagem do Seedance. Não precisa gerar de novo.)

Se quiser variações de cenário, prompt Nano Banana Pro (ref 1 = `avatares/lys.png`, ref 2 = foto do produto):
```
The same young woman from the first reference photo, holding the body splash bottle from the second reference near her face, warm friendly smile, casual UGC selfie, soft natural window light, cozy bathroom vanity background slightly blurred, vertical 9:16, realistic skin, influencer beauty content
```

### Vídeos (3 hooks pra A/B)

**Hook A — mito "não fixa":**
```
The young woman speaks directly to the camera, friendly enthusiastic UGC selfie, natural lip-sync, holding the body splash bottle near her face.
She speaks Brazilian Portuguese with a carioca accent, upbeat: "Menina, dizem que body splash não fixa, mas esse aqui prova o contrário. Passo de manhã e sinto o cheirinho o dia todo. Testa e me conta!"
Ambient noise: quiet indoor room tone, no music.
Negative: subtitles, closed captions, burned-in text, on-screen text, watermark, logo, background music, studio audience, laugh track.
```

**Hook B — preço/perfume importado:**
```
The young woman speaks directly to the camera, excited UGC selfie, natural lip-sync, holding the body splash bottle.
She speaks Brazilian Portuguese with a carioca accent, surprised and happy: "Ninguém acredita que esse cheiro de perfume importado custou trinta reais. Doce, fresco e fixa demais. Corre na sacolinha!"
Ambient noise: quiet indoor room tone, no music.
Negative: subtitles, closed captions, burned-in text, on-screen text, watermark, logo, background music, studio audience, laugh track.
```

**Hook C — curiosidade/prova social:**
```
The young woman speaks directly to the camera, warm confiding UGC selfie, natural lip-sync, holding the body splash bottle.
She speaks Brazilian Portuguese with a carioca accent, playful: "Toda vez que uso esse body splash me perguntam que perfume é. Lichia com peônia, um doce viciante. Link aqui embaixo!"
Ambient noise: quiet indoor room tone, no music.
Negative: subtitles, closed captions, burned-in text, on-screen text, watermark, logo, background music, studio audience, laugh track.
```

---

## Produto 06 — Body Splash Carmed (cheiro de banho tomado)

Notas: sensação de "banho tomado o dia todo" · fixa bem · tamanho de bolsa.

### Imagem inicial → PRECISA GERAR
Sobe 2 referências no Nano Banana Pro: ref 1 = `avatares/lys.png` · ref 2 = **foto do body splash Carmed** (pega no catálogo/print da loja).
```
The same young woman from the first reference photo, holding the Carmed body splash bottle from the second reference near her face, fresh natural morning look, warm friendly smile, casual UGC selfie, soft daylight, cozy bedroom background slightly blurred, vertical 9:16, realistic skin, influencer beauty content
```

### Vídeos (2 hooks)

**Hook A — cheiro de banho tomado:**
```
The young woman speaks directly to the camera, friendly UGC selfie, natural lip-sync, holding the Carmed body splash bottle.
She speaks Brazilian Portuguese with a carioca accent, upbeat: "Sabe aquele cheirinho de banho tomado que dura o dia todo? É esse body splash da Carmed. Fixa demais e cabe na bolsa. Corre!"
Ambient noise: quiet indoor room tone, no music.
Negative: subtitles, closed captions, burned-in text, on-screen text, watermark, logo, background music, studio audience, laugh track.
```

**Hook B — segredo/custo-benefício:**
```
The young woman speaks directly to the camera, confiding UGC selfie, natural lip-sync, holding the Carmed body splash bottle.
She speaks Brazilian Portuguese with a carioca accent, playful: "Meu segredo pra cheirar bem o dia inteiro sem gastar muito: body splash da Carmed. Retoco na bolsa e pronto. Link na sacolinha!"
Ambient noise: quiet indoor room tone, no music.
Negative: subtitles, closed captions, burned-in text, on-screen text, watermark, logo, background music, studio audience, laugh track.
```

---

## Depois de gerar

1. Baixa cada MP4 pra `produtos/lys-produtos/<produto>/geracoes/`.
2. Me chama: eu monto o edit final (grade `warm_cinematic` + legendas burned-in 2 palavras/UPPERCASE + loudnorm -14 LUFS) no pipeline local, igual ao project.md do My Sweet Delight.
3. A/B: sobe os 3 hooks do My Sweet Delight, mede retenção nos primeiros 2s, escala o vencedor.
