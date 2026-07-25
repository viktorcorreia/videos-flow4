r"""LLM abliterada (censura minima) via vLLM na Modal — Qwen3.6-35B-A3B (MoE).

MoE: 35B de pesos, so ~3B ativos por token -> rapido por request,
mas TODOS os experts ficam na VRAM (67 GB de pesos). Por isso: H100 80GB.

Deploy:  modal deploy llm_abliterated.py
Trocar p/ o denso 27B: MODEL = "huihui-ai/Huihui-Qwen3.5-27B-abliterated" (51,7 GB)

STANDBY: depois do deploy NENHUM container fica de pe. A GPU so liga quando
chega uma requisicao e desliga sozinha 15 min depois da ultima. Custo parado = 0.
  - 1a chamada da vida: baixa ~67 GB de pesos (demorada, uma vez so)
  - chamadas frias seguintes: ~2-4 min carregando do Volume pra GPU
  - com a GPU quente: resposta normal

API compativel com OpenAI. Custo: H100 ~US$3,95/h apenas com o container ativo.

Teste (PowerShell):
  $h = @{ Authorization = 'Bearer 0ifbkajx9odmeqr6cvty43z87sl5hpw1' }
  $b = '{"model":"huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated","messages":[{"role":"user","content":"oi"}]}'
  Invoke-RestMethod -Method Post -Uri "$URL/v1/chat/completions" -Headers $h -ContentType 'application/json' -Body $b -TimeoutSec 1800
"""
import os
import subprocess

import modal

MODEL = "huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated"
# Chave do endpoint: definir em MODAL_LLM_API_KEY (nunca versionar).
API_KEY = os.environ["MODAL_LLM_API_KEY"]
PORT = 8000

# Qwen3_5MoeForConditionalGeneration exige vLLM recente.
# CUDA devel (traz nvcc): o vLLM compila kernels em runtime e falha sem ele.
image = (
    modal.Image.from_registry("nvidia/cuda:12.8.1-devel-ubuntu22.04", add_python="3.12")
    .pip_install("vllm==0.25.1", "huggingface_hub")
    .env({"HF_XET_HIGH_PERFORMANCE": "1", "VLLM_USE_V1": "1"})
)

hf_cache = modal.Volume.from_name("hf-cache", create_if_missing=True)
vllm_cache = modal.Volume.from_name("vllm-cache", create_if_missing=True)

app = modal.App("llm-abliterated")


@app.function(
    image=image,
    gpu="H100",
    # STANDBY: zero container parado. Nada roda (e nada e cobrado) ate chegar
    # uma requisicao; 5 min depois da ultima, o container morre sozinho.
    min_containers=0,
    scaledown_window=900,
    timeout=3600,
    volumes={
        "/root/.cache/huggingface": hf_cache,
        "/root/.cache/vllm": vllm_cache,
    },
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=PORT, startup_timeout=2700)
def serve():
    subprocess.Popen([
        "vllm", "serve", MODEL,
        "--host", "0.0.0.0",
        "--port", str(PORT),
        "--api-key", API_KEY,
        # O Qwen Code CLI pede max_tokens=32000 numa tirada; abaixo disso ele 400.
        "--max-model-len", "49152",
        "--gpu-memory-utilization", "0.95",
        # Qwen3.6 e hibrido (atencao + Mamba). Cada sequencia em decode ocupa um
        # bloco de cache Mamba; com o padrao (1024) o vLLM nem inicializa.
        # Uso e single-user, entao 16 sobra e libera KV cache pro contexto longo.
        "--max-num-seqs", "16",
        # Sem isto o raciocinio sai como texto normal e o modelo entra em loop
        # se auto-revisando. Com o parser ele vai pro campo reasoning_content.
        "--reasoning-parser", "qwen3",
        # Tool calling nativo: e o que permite usar como cerebro de agente (Qwen Code).
        "--enable-auto-tool-choice",
        "--tool-call-parser", "hermes",
    ])
