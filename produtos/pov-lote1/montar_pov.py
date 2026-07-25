"""Monta os 3 finais do lote POV: EDL -> render.py -> mux locucao (P1) sobre ambiente (P2).

Regras (skill diretor-edicao-tiktok, igual mass-edit/edit/montar_finais.py):
- corte seco, grade none, sem legenda queimada, alvo = locucao + 0.65s
- locucao entra em 0,15s, fade-in 0,1s, fade-out 0,3s; ambiente a 20%
Ajustes da verificacao FASE 1:
- 04/pov_uso tem barras brancas laterais -> crop central 9:16 + rescale
- 07/pov_hero abre no frame de catalogo -> entra em t=2,5s
"""
import json, subprocess, sys
from pathlib import Path

LOTE = Path(__file__).parent
RENDER = r"C:\Users\Usuario\Documents\videos-flow4\tools\video-use\helpers\render.py"
HEAD = 0.10

# (pasta, [(clipe, start_extra)])
PRODUTOS = {
    "04-body-splash-msd": [("pov_hero", 0), ("pov_detalhe", 0), ("pov_uso_crop", 0)],
    "07-rubyrose-gloss": [("pov_detalhe", 0), ("pov_hero", 2.5), ("pov_swatch", 0)],
    "08-kiss-cilios": [("pov_hero", 0), ("pov_detalhe", 0), ("pov_uso", 0)],
}


def ffdur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def preprocess():
    src = LOTE / "04-body-splash-msd/geracoes/pov_uso.mp4"
    dst = LOTE / "04-body-splash-msd/geracoes/pov_uso_crop.mp4"
    if not dst.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
                        "-vf", "crop=576:1024:(iw-576)/2:(ih-1024)/2,scale=720:1280",
                        "-c:a", "copy", str(dst)], check=True)
        print("crop ok: pov_uso_crop.mp4")


def montar(pasta: str, clips: list):
    d = LOTE / pasta
    loc = d / "locucao.mp3"
    alvo = ffdur(loc) + 0.65
    starts = [HEAD + extra for _, extra in clips]
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


preprocess()
for pasta, clips in PRODUTOS.items():
    montar(pasta, clips)
