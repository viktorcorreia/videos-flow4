"""Monta os 4 finais: EDL -> render.py -> mux locucao (P1) sobre ambiente (P2).

Regras aplicadas (skill diretor-edicao-tiktok):
- corte seco entre clipes (render.py ja poe fade de audio 30ms nas bordas)
- locucao entra em 0,15s, fade-in 0,1s, fade-out 0,3s
- ambiente do clipe mantido a 20% sob a locucao
- grade none, sem legenda queimada, 1080x1920
"""
import json
import subprocess
import sys
from pathlib import Path

EDIT = Path(__file__).parent
MASS = EDIT.parent
RENDER = r"C:\Users\Usuario\Documents\videos-flow4\tools\video-use\helpers\render.py"

manifest = {m["arquivo"]: m for m in json.loads((EDIT / "catalogo" / "manifest.json").read_text(encoding="utf-8"))}


def dur(name: str) -> float:
    return manifest[name + ".mp4"]["duracao_s"]


# (produto, locucao, [(clipe, ordem)]) — alvo de video = locucao + 0.65s
def loc_dur(nome: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(EDIT / f"locucao_p_{nome}.mp3")],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


PRODUTOS = {
    "scarpin": {
        "clips": [
            "hf_20260723_110953_74b86e1e-3eee-400e-bc21-d431e017a61f",
            "hf_20260723_105703_0473a961-9dbf-4354-a56b-e70b041098fa",
            "hf_20260723_112400_caa75634-0082-4b38-8e03-b61da4dfec8c",
        ],
    },
    "mule": {
        "clips": [
            "hf_20260724_003712_66888abd-72f5-4433-8252-227a9d04b7fe",
            "hf_20260724_002116_c3066e1c-f267-49cb-bf4b-7c5b5150c008",
            "hf_20260724_002933_073a9c46-963b-4d26-a5fe-11799b397906",
        ],
    },
    "slouchy": {
        "clips": [
            "hf_20260724_014536_40ea87c8-aa88-4053-a2ae-ca9236e49c2a",
            "hf_20260724_012610_658af98d-181a-4a58-9d06-66dfdb91e728",
            "hf_20260724_013623_30e8974c-b98c-44ec-a44d-db95280cc8ff",
        ],
    },
    "caramelo": {
        "clips": [
            "hf_20260723_235829_08e4f07d-773f-4c02-8834-8220ec4f8cbf",
            "hf_20260723_234545_d8f12fe1-9b45-4ea3-896c-52538090bb0b",
            "hf_20260723_235213_b304da0b-c247-4c44-a80f-94dda2f9599e",
        ],
    },
}

HEAD = 0.10  # entra 0,1s depois do inicio do clipe (evita frame de assentamento)


def montar(nome: str, spec: dict) -> None:
    alvo = loc_dur(nome) + 0.65
    clips = spec["clips"]
    # distribui: corta primeiro das caudas dos clipes mais longos
    livres = [dur(c) - HEAD for c in clips]
    excesso = sum(livres) - alvo
    if excesso < 0:
        raise SystemExit(f"{nome}: material ({sum(livres):.1f}s) < alvo ({alvo:.1f}s)")
    segs = livres[:]
    while excesso > 0.001:
        i = max(range(len(segs)), key=lambda j: segs[j])
        corte = min(excesso, segs[i] - min(2.0, segs[i]))  # nunca deixar clipe < 2s
        if corte <= 0:
            corte = excesso  # distribui o resto no maior mesmo assim
        tira = min(excesso, max(corte, excesso / len(segs)))
        segs[i] -= tira
        excesso -= tira

    edl = {
        "version": 1,
        "sources": {f"c{i+1}": str(MASS / (c + ".mp4")) for i, c in enumerate(clips)},
        "ranges": [
            {"source": f"c{i+1}", "start": round(HEAD, 2), "end": round(HEAD + segs[i], 2),
             "beat": ["HOOK-PRECO", "ACABAMENTO/OBJECAO", "CTA"][i], "quote": "", "reason": "b-roll continuo, corte por duracao da locucao"}
            for i in range(len(clips))
        ],
        "grade": "none",
        "overlays": [],
        "total_duration_s": round(sum(segs), 2),
    }
    edl_path = EDIT / f"edl_{nome}.json"
    edl_path.write_text(json.dumps(edl, indent=2), encoding="utf-8")

    base = EDIT / f"base_{nome}.mp4"
    subprocess.run([sys.executable, RENDER, str(edl_path), "-o", str(base), "--no-subtitles"], check=True)

    loc = EDIT / f"locucao_p_{nome}.mp3"
    final = EDIT / f"final_{nome}.mp4"
    vd = sum(segs)
    fade_out_start = max(0.0, vd - 0.3)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", str(base), "-i", str(loc),
        "-filter_complex",
        (f"[0:a]volume=0.2[amb];"
         f"[1:a]adelay=150|150,afade=t=in:st=0:d=0.1[voz];"
         f"[amb][voz]amix=inputs=2:duration=first:normalize=0,"
         f"afade=t=out:st={fade_out_start:.2f}:d=0.3[a]"),
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(final),
    ], check=True)
    print(f"{nome}: video {vd:.2f}s | segs {[round(s,2) for s in segs]} -> {final.name}")


for nome, spec in PRODUTOS.items():
    montar(nome, spec)
