"""Monta os 2 finais do lote sapatos. Mesma receita de pov-lote1/montar_pov.py.
Ajustes FASE 1: 09/pov_hero descartado (virou slide) -> pov_hero2; 09/pov_charms entra em 1,8s
(morph do banner); 14/pov_hero e pov_detalhe entram em 1,0s (frame de catalogo)."""
import json, subprocess, sys
from pathlib import Path

LOTE = Path(__file__).parent
RENDER = r"C:\Users\Usuario\Documents\videos-flow4\tools\video-use\helpers\render.py"

# (pasta, [(clipe, start)])
PRODUTOS = {
    "09-sandalia-nuvem": [("pov_hero2", 0.10), ("pov_charms", 1.80), ("pov_detalhe", 0.10)],
    "14-bota-domidona": [("pov_hero", 1.00), ("pov_detalhe", 1.00), ("pov_uso", 0.10)],
}


def ffdur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def montar(pasta: str, clips: list):
    d = LOTE / pasta
    loc = d / "locucao.mp3"
    alvo = ffdur(loc) + 0.65
    starts = [s for _, s in clips]
    paths = [d / "geracoes" / f"{c}.mp4" for c, _ in clips]
    livres = [ffdur(p) - s for p, s in zip(paths, starts)]
    excesso = sum(livres) - alvo
    if excesso < 0:
        raise SystemExit(f"{pasta}: material ({sum(livres):.1f}s) < alvo ({alvo:.1f}s)")
    segs = livres[:]
    while excesso > 0.001:
        i = max(range(len(segs)), key=lambda j: segs[j])
        tira = min(excesso, max(segs[i] - 2.0, excesso / len(segs)))
        if tira <= 0:
            tira = excesso
        segs[i] -= tira
        excesso -= tira

    edl = {
        "version": 1,
        "sources": {f"c{i+1}": str(paths[i]).replace("\\", "/") for i in range(len(paths))},
        "ranges": [
            {"source": f"c{i+1}", "start": round(starts[i], 2), "end": round(starts[i] + segs[i], 2),
             "beat": ["HOOK-PRECO", "SENSORIAL/OBJECAO", "CTA"][i], "quote": "",
             "reason": "b-roll POV continuo, corte por duracao da locucao"}
            for i in range(len(paths))
        ],
        "grade": "none", "overlays": [],
        "total_duration_s": round(sum(segs), 2),
    }
    edl_path = d / "edl.json"
    edl_path.write_text(json.dumps(edl, indent=2), encoding="utf-8")

    base = d / "base.mp4"
    subprocess.run([sys.executable, RENDER, str(edl_path), "-o", str(base), "--no-subtitles"], check=True)

    final = LOTE / "final" / f"final_{pasta}.mp4"
    final.parent.mkdir(exist_ok=True)
    vd = sum(segs)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", str(base), "-i", str(loc),
        "-filter_complex",
        (f"[0:a]volume=0.2[amb];"
         f"[1:a]adelay=150|150,afade=t=in:st=0:d=0.1[voz];"
         f"[amb][voz]amix=inputs=2:duration=first:normalize=0,"
         f"afade=t=out:st={max(0.0, vd-0.3):.2f}:d=0.3[a]"),
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(final)], check=True)
    print(f"{pasta}: video {vd:.2f}s | segs {[round(s,2) for s in segs]} -> {final.name}")


for pasta, clips in PRODUTOS.items():
    montar(pasta, clips)
