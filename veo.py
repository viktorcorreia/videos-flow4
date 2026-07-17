#!/usr/bin/env python3
"""
veo.py — gera 1 bloco de vídeo por chamada, com produto travado e seed reproduzível.

    pip install google-genai
    export GEMINI_API_KEY=...

    python veo.py --list                  # o que existe em prompts.json
    python veo.py A1 --dry                # custo, sem gastar
    python veo.py A1                      # gera os 3 blocos do A1
    python veo.py A1 --block 2            # regera só o bloco 2
    python veo.py A1 --block 2 --seed 771 # regera com a MESMA seed do take anterior

Saída: out/A1_b2_take3_seed771.mp4  +  out/log.jsonl

Por que seed importa: sem ela, mudar a fala muda rosto, luz e enquadramento junto,
e você não sabe o que causou o quê. Com seed fixa, uma variável muda por vez.
"""
import argparse, json, time
from pathlib import Path
from google import genai
from google.genai import types

MODEL_STD  = "veo-3.1-generate-preview"
MODEL_FAST = "veo-3.1-fast-generate-preview"
PRECO = {MODEL_STD: 0.40, MODEL_FAST: 0.15}   # USD/segundo — confira antes de escalar

NEGATIVE = ("subtitles, closed captions, burned-in text, on-screen text, lower thirds, "
            "watermark, logo, background music, studio audience, laugh track")

RAIZ    = Path(__file__).parent
FRAMES  = RAIZ / "frames"
OUT     = RAIZ / "out"
LOG     = OUT / "log.jsonl"


def carregar(nome):
    p = json.loads((RAIZ / "prompts.json").read_text(encoding="utf-8"))
    if nome not in p:
        raise SystemExit(f"'{nome}' não existe. Tem: {', '.join(p)}")
    return p[nome]


def refs(nomes):
    out = []
    for n in nomes:
        f = FRAMES / n
        if not f.exists():
            raise SystemExit(f"frame faltando: {f}")
        out.append(types.VideoGenerationReferenceImage(
            image=types.Image.from_file(location=str(f)),
            reference_type="ASSET",
        ))
    if len(out) > 3:
        raise SystemExit("Veo 3.1 aceita no máximo 3 reference images.")
    return out


def gerar(client, angulo, bloco, cfg, seed, modelo, enhance):
    b = cfg["blocos"][bloco - 1]
    print(f"  bloco {bloco} · {b['duracao']}s · seed {seed} · enhance={enhance} · {len(b['fala'].split())} palavras de fala")

    op = client.models.generate_videos(
        model=modelo,
        prompt=b["prompt"],
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16",
            resolution="1080p",
            duration_seconds=b["duracao"],
            number_of_videos=1,
            negative_prompt=NEGATIVE,
            person_generation="allow_adult",
            generate_audio=True,      # sem isso o servidor decide. UGC mudo é lixo.
            enhance_prompt=enhance,   # a reescrita de prompt que o Flow aplica por padrão
            seed=seed,
            reference_images=refs(cfg["frames"]),
        ),
    )
    while not op.done:
        time.sleep(10)
        op = client.operations.get(op)

    if op.error:
        print(f"  ERRO: {op.error}")
        return None

    v = op.response.generated_videos[0]
    take = 1 + sum(1 for f in OUT.glob(f"{angulo}_b{bloco}_take*.mp4"))
    dest = OUT / f"{angulo}_b{bloco}_take{take}_seed{seed}.mp4"

    # baixar JÁ: o Veo apaga o arquivo do servidor em 2 dias
    client.files.download(file=v.video)
    v.video.save(str(dest))

    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "arquivo": dest.name, "angulo": angulo, "bloco": bloco, "take": take,
            "seed": seed, "modelo": modelo, "duracao": b["duracao"], "enhance": enhance,
            "fala": b["fala"], "quando": time.strftime("%Y-%m-%d %H:%M"),
        }, ensure_ascii=False) + "\n")

    print(f"  -> {dest.name}")
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("angulo", nargs="?")
    ap.add_argument("--block", type=int, help="regerar só este bloco")
    ap.add_argument("--seed", type=int, help="reusar seed de um take anterior")
    ap.add_argument("--fast", action="store_true", help="veo-3.1-fast (2.7x mais barato)")
    ap.add_argument("--raw", action="store_true", help="enhance_prompt=False (o Flow usa True)")
    ap.add_argument("--dry", action="store_true", help="só o custo")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        p = json.loads((RAIZ / "prompts.json").read_text(encoding="utf-8"))
        for k, v in p.items():
            print(f"{k:4} {v['hipotese']}")
        return
    if not a.angulo:
        raise SystemExit("passa o ângulo (ex: A1) ou --list")

    cfg = carregar(a.angulo)
    modelo = MODEL_FAST if a.fast else MODEL_STD
    blocos = [a.block] if a.block else list(range(1, len(cfg["blocos"]) + 1))
    segs = sum(cfg["blocos"][b - 1]["duracao"] for b in blocos)

    print(f"\n{a.angulo} — {cfg['hipotese']}")
    print(f"{len(blocos)} bloco(s), {segs}s, {modelo}")
    print(f"custo estimado: US$ {segs * PRECO[modelo]:.2f}\n")
    if a.dry:
        return

    OUT.mkdir(exist_ok=True)
    client = genai.Client()
    for b in blocos:
        seed = a.seed if a.seed else cfg["blocos"][b - 1]["seed"]
        gerar(client, a.angulo, b, cfg, seed, modelo, not a.raw)

    print(f"\nPrimeira rodada: abra o mp4 e confira 3 coisas antes de gerar mais —")
    print("  1. saiu 9:16 mesmo? (a API já forçou 16:9 em versões anteriores)")
    print("  2. o rótulo do frasco está legível e igual ao frame?")
    print("  3. tem legenda queimada na tela?")


if __name__ == "__main__":
    main()
