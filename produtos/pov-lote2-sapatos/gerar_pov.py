# Lote POV 2 — sapatos. Mesma receita do pov-lote1/gerar_pov.py (retomável).
import json, subprocess, sys, time
from pathlib import Path

LOTE = Path(__file__).resolve().parent
VEO = Path(r"C:\dev\tiktok-ugc-pipeline\scripts\veo\veo_generate.py")
PRESETS = Path(r"C:\dev\tiktok-ugc-pipeline\scripts\prompts\presets.json")
NEG = json.loads(PRESETS.read_text(encoding="utf-8"))["negative_venda"]

BASE = (
    "First-person POV vertical smartphone video, UGC style. A young Brazilian woman's hands "
    "with natural short nails, no flashy nail polish. Handheld phone feel with slight natural "
    "shake, soft daylight, shallow depth of field, realistic skin texture, no on-screen text. "
)
AMB = " Ambient noise: quiet indoor room tone, subtle object handling sounds, no music, no speech."

CLIPES = [
    # ── 09 Sandália Nuvem EVA + charms ──
    ("09-sandalia-nuvem", "pov_hero",
     BASE + "Her hands reach into frame and pick up the exact cloud slide sandal from the image "
     "from a bedroom floor, lifting it toward the camera, showing the puffy pillow-like EVA shape." + AMB),
    ("09-sandalia-nuvem", "pov_detalhe",
     BASE + "Close-up: her hands squeeze and press the exact soft EVA cloud sandal sole from the image, "
     "fingers sinking slightly into the cushioned foam to show softness, then run a fingertip along the smooth surface." + AMB),
    ("09-sandalia-nuvem", "pov_charms",
     BASE + "Close-up: her hands snap small decorative charms onto the strap of the exact cloud sandal "
     "from the image, one by one, then tilt the decorated sandal toward the camera." + AMB),
    # ── 14 Bota Domidona cano alto ──
    ("14-bota-domidona", "pov_hero",
     BASE + "Her hands pick up the exact high-shaft block-heel boot from the image from a closet shelf, "
     "lifting it toward the camera, showing the full silhouette with pointed toe." + AMB),
    ("14-bota-domidona", "pov_detalhe",
     BASE + "Close-up: her hands slowly slide the side zipper of the exact boot from the image down and up, "
     "then run fingers over the smooth material of the tall shaft and the block heel." + AMB),
    ("14-bota-domidona", "pov_uso",
     BASE + "Her hands hold the exact boot from the image while she slips her foot into it, seated on a bed, "
     "then zips the side zipper up along her calf, camera looking down POV." + AMB),
]

def main():
    log = (LOTE / "gerar_pov.log").open("a", encoding="utf-8")
    falhas = []
    for pasta, nome, prompt in CLIPES:
        out = LOTE / pasta / "geracoes" / f"{nome}.mp4"
        if out.exists():
            print(f"SKIP {pasta}/{nome}", flush=True)
            continue
        cmd = [sys.executable, str(VEO),
               "--image", str(LOTE / pasta / "produto.png"),
               "--prompt", prompt,
               "--out", str(out),
               "--model", "veo-3.1-fast",
               "--duration", "8",
               "--aspect", "9:16",
               "--resolution", "720p",
               "--resize-mode", "crop",
               "--negative", NEG,
               "--audio"]
        print(f"GEN  {pasta}/{nome} ...", flush=True)
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=r"C:\dev\tiktok-ugc-pipeline")
        ok = out.exists()
        msg = f"[{time.strftime('%H:%M:%S')}] {pasta}/{nome} ok={ok} {time.time()-t0:.0f}s\n"
        log.write(msg + (r.stdout[-2000:] or "") + (r.stderr[-2000:] or "") + "\n")
        log.flush()
        print(msg.strip(), flush=True)
        if not ok:
            falhas.append(f"{pasta}/{nome}")
    print(f"FIM. Falhas: {falhas or 'nenhuma'}", flush=True)

if __name__ == "__main__":
    main()
