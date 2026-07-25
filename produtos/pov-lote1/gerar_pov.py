# Lote POV 1 — cenas em primeira pessoa, mãos pegando e mostrando o produto.
# Roda sequencial e é retomável: pula clipe cujo .mp4 já existe.
import json, subprocess, sys, time
from pathlib import Path

LOTE = Path(__file__).resolve().parent
VEO = Path(r"C:\dev\tiktok-ugc-pipeline\scripts\veo\veo_generate.py")
PRESETS = Path(r"C:\dev\tiktok-ugc-pipeline\scripts\prompts\presets.json")
NEG = json.loads(PRESETS.read_text(encoding="utf-8"))["negative_venda"]

BASE = (
    "First-person POV vertical smartphone video, UGC style. A young Brazilian woman's hands "
    "with natural short nails, no flashy nail polish. Handheld phone feel with slight natural "
    "shake, soft daylight from a window, shallow depth of field, realistic skin texture, "
    "no on-screen text. "
)
AMB = " Ambient noise: quiet indoor room tone, subtle object handling sounds, no music, no speech."

CLIPES = [
    # ── 04 Body Splash My Sweet Delight ──
    ("04-body-splash-msd", "produto.png", "pov_hero",
     BASE + "Her hands reach into frame and pick up the exact body splash bottle from the image, "
     "lifting it from a cozy bathroom vanity toward the camera, label facing the lens, held steady close to camera." + AMB),
    ("04-body-splash-msd", "produto.png", "pov_detalhe",
     BASE + "Close-up: her hands slowly rotate the exact body splash bottle from the image, "
     "showing the front label and the spray cap, fingertips tilting it under soft light on a bathroom vanity." + AMB),
    ("04-body-splash-msd", "produto.png", "pov_uso",
     BASE + "Her hand holds the exact body splash bottle from the image and sprays a fine mist "
     "onto her other wrist and forearm, tiny droplets catching the light, cozy bedroom background blurred." + AMB),
    # ── 07 Ruby Rose Gloss Tint ──
    ("07-rubyrose-gloss", "produto.jpg", "pov_hero",
     BASE + "Her hands pick up the exact lip gloss tint tube from the image from a vanity table "
     "with makeup items blurred behind, bringing it close to the camera, label readable." + AMB),
    ("07-rubyrose-gloss", "produto.jpg", "pov_detalhe",
     BASE + "Close-up: her hands open the exact lip gloss tint from the image, slowly pulling out "
     "the doe-foot applicator covered in glossy tinted product, strand of gloss stretching, light reflecting on the shiny texture." + AMB),
    ("07-rubyrose-gloss", "produto.jpg", "pov_swatch",
     BASE + "Her hand swatches the exact lip gloss tint from the image on the back of her other hand, "
     "applicator gliding leaving a glossy pigmented stripe, then tilts the hand so the shine catches the light." + AMB),
    # ── 08 KISS Cílios Magnéticos ──
    ("08-kiss-cilios", "produto.jpg", "pov_hero",
     BASE + "Her hands pick up the exact magnetic false eyelashes package from the image from a vanity "
     "table, bringing it toward the camera, packaging front visible and readable." + AMB),
    ("08-kiss-cilios", "produto.jpg", "pov_detalhe",
     BASE + "Close-up: her hands open the exact eyelash package from the image and lift one wispy "
     "false lash band with fingertips, showing the tiny magnets along the lash band, rotating it gently under soft light." + AMB),
    ("08-kiss-cilios", "produto.jpg", "pov_uso",
     BASE + "Her hand holds one magnetic false lash close to the camera with the eyelash applicator tool, "
     "clicking the magnetic lash strips together to demo the magnets snapping, vanity mirror blurred in background." + AMB),
]

def main():
    log = (LOTE / "gerar_pov.log").open("a", encoding="utf-8")
    falhas = []
    for pasta, img, nome, prompt in CLIPES:
        out = LOTE / pasta / "geracoes" / f"{nome}.mp4"
        if out.exists():
            print(f"SKIP {pasta}/{nome}", flush=True)
            continue
        cmd = [sys.executable, str(VEO),
               "--image", str(LOTE / pasta / img),
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
