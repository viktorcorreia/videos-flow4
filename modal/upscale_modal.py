r"""Upscale de video 720x1280 -> 1080x1920 com Real-ESRGAN na Modal (GPU A10G).

Uso:
  modal run upscale_modal.py --entrada caminho\video.mp4            # um arquivo -> video_1080.mp4
  modal run upscale_modal.py --entrada caminho\pasta                # todos os .mp4 da pasta (paralelo)

Custo aproximado: A10G ~US$1,10/h; clipe de 8s ~30-60s de GPU.
"""
import modal

app = modal.App("upscale-video")

MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "libgl1", "libglib2.0-0", "wget")
    # torch precisa existir ANTES do basicsr: o setup.py dele resolve deps em build time
    .pip_install("torch==2.1.2", "torchvision==0.16.2", "numpy<2", "opencv-python-headless")
    .pip_install("basicsr==1.4.2", "realesrgan==0.3.0", "numpy<2")
    .run_commands(
        # basicsr 1.4.2 importa um modulo removido do torchvision novo
        "sed -i 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/"
        "from torchvision.transforms.functional import rgb_to_grayscale/' "
        "/usr/local/lib/python3.11/site-packages/basicsr/data/degradations.py",
        f"mkdir -p /weights && wget -q -O /weights/realesr-general-x4v3.pth {MODEL_URL}",
    )
)


@app.function(image=image, gpu="A10G", timeout=1800)
def upscale(video: bytes, largura: int = 1080, altura: int = 1920) -> bytes:
    import subprocess
    from pathlib import Path

    import cv2
    from basicsr.archs.srvgg_arch import SRVGGNetCompact
    from realesrgan import RealESRGANer

    work = Path("/tmp/work")
    (work / "in").mkdir(parents=True, exist_ok=True)
    (work / "out").mkdir(parents=True, exist_ok=True)
    src = work / "src.mp4"
    src.write_bytes(video)

    fps = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=r_frame_rate", "-of", "csv=p=0", str(src)],
        capture_output=True, text=True, check=True).stdout.strip()

    subprocess.run(["ffmpeg", "-v", "error", "-i", str(src),
                    str(work / "in" / "%06d.png")], check=True)

    model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64,
                            num_conv=32, upscale=4, act_type="prelu")
    upsampler = RealESRGANer(scale=4, model_path="/weights/realesr-general-x4v3.pth",
                             model=model, tile=0, half=True)

    frames = sorted((work / "in").glob("*.png"))
    escala = None
    for f in frames:
        img = cv2.imread(str(f), cv2.IMREAD_COLOR)
        if escala is None:
            escala = max(largura / img.shape[1], altura / img.shape[0])
        out, _ = upsampler.enhance(img, outscale=escala)
        out = cv2.resize(out[:altura, :largura], (largura, altura),
                         interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(work / "out" / f.name), out)

    dst = work / "dst.mp4"
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-framerate", fps, "-i", str(work / "out" / "%06d.png"),
        "-i", str(src),
        "-map", "0:v", "-map", "1:a?",
        "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart",
        str(dst),
    ], check=True)
    return dst.read_bytes()


@app.local_entrypoint()
def main(entrada: str):
    from pathlib import Path

    p = Path(entrada)
    arquivos = sorted(p.glob("*.mp4")) if p.is_dir() else [p]
    alvos = [a for a in arquivos if not a.stem.endswith("_1080")]
    print(f"{len(alvos)} video(s) para upscalar")
    dados = [a.read_bytes() for a in alvos]
    for arq, resultado in zip(alvos, upscale.map(dados)):
        saida = arq.with_name(arq.stem + "_1080.mp4")
        saida.write_bytes(resultado)
        print(f"OK: {saida} ({len(resultado)/1e6:.1f} MB)")
