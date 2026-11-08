#!/usr/bin/env bash
# Recreates the GPU environment on a RunPod pod (Python 3.10 + torch 2.9.1 cu128 + models).
# Developed iteratively with the help of an AI assistant (Claude, Anthropic)
# and refined after test runs on RunPod (RTX PRO 4500, RTX 4090).
set -eo pipefail

usage() {
  cat <<'USAGE'
Usage on the pod:
  bash /workspace/setup_runpod.sh                    # base environment + AASIST (default)
  bash /workspace/setup_runpod.sh --rawnet2          # base environment + RawNet2
  bash /workspace/setup_runpod.sh --aasist --sonics  # several models
  bash /workspace/setup_runpod.sh --all              # all models

Model flags:
  --aasist     AASIST (clovaai/aasist; weights are in the repository)
  --rawnet2    RawNet2, ASVspoof 2021 baseline B04 (asvspoof-challenge/2021 + pre-trained DF model)
  --wav2vec2   wav2vec 2.0 + AASIST (TakHemlata/SSL_Anti-spoofing + bundled fairseq + XLS-R 300M)
  --sonics     SONICS sonics-spectttra-alpha-5s and -alpha-120s (awsaf49/sonics + Hugging Face)
  --all        all of the above
  -h, --help   show this help

Models that are already on /workspace are not downloaded again.
If one model fails (e.g. a download fails), the other models still run, and everything
that was already downloaded stays on /workspace. Run the script again to finish.
USAGE
}

DO_AASIST=0; DO_RAWNET2=0; DO_W2V2=0; DO_SONICS=0
for arg in "$@"; do
  case "$arg" in
    --aasist)   DO_AASIST=1 ;;
    --rawnet2)  DO_RAWNET2=1 ;;
    --wav2vec2) DO_W2V2=1 ;;
    --sonics)   DO_SONICS=1 ;;
    --all)      DO_AASIST=1; DO_RAWNET2=1; DO_W2V2=1; DO_SONICS=1 ;;
    -h|--help)  usage; exit 0 ;;
    *)          echo "Unknown option: $arg"; echo; usage; exit 1 ;;
  esac
done

if [ $((DO_AASIST + DO_RAWNET2 + DO_W2V2 + DO_SONICS)) -eq 0 ]; then DO_AASIST=1; fi

WS=/workspace
VENV="$WS/venv"
PY_VERSION=3.10
TORCH_INDEX=https://download.pytorch.org/whl/cu128
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# requirements-gpu.txt next to this script
REQS="$SCRIPT_DIR/requirements-gpu.txt"
[ -f "$REQS" ] || REQS=""

# Python and the uv cache on the volume, so they survive stopping the pod
export UV_PYTHON_INSTALL_DIR="$WS/uv-python"
export UV_CACHE_DIR="$WS/uv-cache"
# Hugging Face and torch.hub caches on the volume too (otherwise ~/.cache on the pod disk)
export HF_HOME="$WS/hf-cache"
export TORCH_HOME="$WS/torch-cache"

# ---------------------------------------------------------------------------
# Base environment (always)
# ---------------------------------------------------------------------------

echo "== [base] System tools (ffmpeg, git, wget, unzip) — installed on the pod disk, so on every start"
if ! command -v ffmpeg >/dev/null || ! command -v git >/dev/null \
   || ! command -v wget >/dev/null || ! command -v unzip >/dev/null; then
  apt-get update && apt-get install -y ffmpeg git wget unzip
else
  echo "   already installed"
fi

echo "== [base] uv"
if ! command -v uv >/dev/null; then
  pip install uv || pip install --break-system-packages uv
else
  echo "   already installed"
fi

echo "== [base] Python $PY_VERSION and venv in $VENV"
if [ ! -x "$VENV/bin/python" ]; then
  uv python install "$PY_VERSION"
  uv venv --python "$PY_VERSION" "$VENV"
else
  echo "   venv already exists"
fi

# The cache locations also apply whenever the venv is activated (when models are run)
if ! grep -q "HF_HOME=" "$VENV/bin/activate"; then
  echo "export HF_HOME=$HF_HOME TORCH_HOME=$TORCH_HOME" >> "$VENV/bin/activate"
fi

source "$VENV/bin/activate"

echo "== [base] Packages"
# torch separately from the cu128 index; the rest from PyPI (versions from requirements-gpu.txt)
uv pip install torch==2.9.1 torchaudio==2.9.1 --index-url "$TORCH_INDEX"
if [ -n "$REQS" ]; then
  echo "   from file $REQS"
  uv pip install -r "$REQS"
else
  echo "   WARNING: requirements-gpu.txt not found, installing without pinned versions"
  uv pip install numpy soundfile pyyaml torchcontrib tensorboard
fi

mkdir -p "$WS/repos" "$WS/weights" "$WS/data" "$WS/outputs" "$WS/scripts"

# ---------------------------------------------------------------------------
# Helpers. Each one writes to a temporary name first and renames it only when the step is
# complete, so an interrupted step never looks finished and is simply repeated next time.
# ---------------------------------------------------------------------------

clone_at() {  # name, url, commit
  local dir="$WS/repos/$1"
  if [ ! -d "$dir/.git" ]; then
    rm -rf "$dir.tmp"
    git clone "$2" "$dir.tmp"
    rm -rf "$dir"
    mv "$dir.tmp" "$dir"
  fi
  if ! git -C "$dir" cat-file -e "$3^{commit}" 2>/dev/null; then
    git -C "$dir" fetch origin
  fi
  git -C "$dir" -c advice.detachedHead=false checkout -q "$3"
  echo "   $1 @ $(git -C "$dir" rev-parse --short HEAD)"
}

download() {  # url, target file; an interrupted download continues from where it stopped
  if [ -s "$2" ]; then
    echo "   already downloaded: $2"
    return
  fi
  mkdir -p "$(dirname "$2")"
  wget -q --show-progress -c -O "$2.part" "$1"
  mv "$2.part" "$2"
}

unzip_once() {  # zip file, target folder
  if [ -d "$2" ]; then
    echo "   already unpacked: $2"
    return
  fi
  rm -rf "$2.tmp"
  unzip -q "$1" -d "$2.tmp"
  mv "$2.tmp" "$2"
}

# ---------------------------------------------------------------------------
# Models (only the ones selected with flags)
# ---------------------------------------------------------------------------

install_aasist() {
  echo "== [aasist] Repository (the weights AASIST.pth, AASIST-L.pth are in the repository)"
  clone_at aasist https://github.com/clovaai/aasist.git a04c9863f63d44471dde8a6abcb3b082b07cd1d1
}

install_rawnet2() {
  echo "== [rawnet2] Repository, packages, weights"
  clone_at asvspoof2021 https://github.com/asvspoof-challenge/2021.git 9b33f5eca887bd3bf629e3fb79428cd9bb7ac972
  # The code needs librosa and tensorboardX (LA/Baseline-RawNet2/requirements.txt pins
  # librosa==0.7.2, which does not install on Python 3.10, so current versions are used)
  uv pip install librosa tensorboardX
  download https://www.asvspoof.org/asvspoof2021/pre_trained_DF_RawNet2.zip \
           "$WS/weights/rawnet2/pre_trained_DF_RawNet2.zip"
  unzip_once "$WS/weights/rawnet2/pre_trained_DF_RawNet2.zip" "$WS/weights/rawnet2/unpacked"
  echo "   weights in $WS/weights/rawnet2/unpacked"
}

install_wav2vec2() {
  echo "== [wav2vec2] Repository, fairseq, weights (untested)"
  clone_at SSL_Anti-spoofing https://github.com/TakHemlata/SSL_Anti-spoofing.git 4acaa61dcef5f7610f43aa4d0b29c4559b970cd2
  local SSL="$WS/repos/SSL_Anti-spoofing"
  local FAIRSEQ="$SSL/fairseq-a54021305d6b3c4c5959ac9395135f63202db8f1"

  # 1) fairseq bundled in the repository. Its setup.py imports torch and builds Cython / C++
  #    extensions, so it is built against the torch that is already installed.
  #    If this step fails on omegaconf 2.0.6 ("non-standard dependency specifier"), the install
  #    has to be done with an older pip instead of uv.
  if ! python -c "import importlib.util, sys; sys.exit(importlib.util.find_spec('fairseq') is None)"; then
    uv pip install cython
    uv pip install --no-build-isolation -e "$FAIRSEQ"
  else
    echo "   fairseq already installed"
  fi

  # 2) Patch for PyTorch >= 2.6: torch.load uses weights_only=True by default, but the fairseq
  #    checkpoint xlsr2_300m.pt also contains config objects (fairseq/checkpoint_utils.py l. 313).
  #    weights_only=False is only acceptable here because the file comes from the official fairseq server.
  python - "$FAIRSEQ/fairseq/checkpoint_utils.py" <<'EOF'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
old = 'torch.load(f, map_location=torch.device("cpu"))'
new = 'torch.load(f, map_location=torch.device("cpu"), weights_only=False)'
if new in text:
    print("   weights_only patch already applied")
elif old in text:
    open(path, "w", encoding="utf-8").write(text.replace(old, new, 1))
    print("   weights_only patch applied")
else:
    sys.exit("   ERROR: line to patch not found in " + path)
EOF

  # 2b) Patch for NumPy >= 1.24: the aliases np.float and np.int were removed, and fairseq uses them
  #     (fairseq/data/indexed_dataset.py l. 123, 330 at import time; data_utils.py l. 484 and
  #     modules/dynamic_crf_layer.py l. 108 at run time). They were aliases of the builtins float and
  #     int, so the replacement does not change any behaviour (NumPy 1.20 release notes).
  python - "$FAIRSEQ" <<'EOF'
import re, sys, os
root = sys.argv[1]
files = ["fairseq/data/indexed_dataset.py", "fairseq/data/data_utils.py", "fairseq/modules/dynamic_crf_layer.py"]
pattern = re.compile(r"\bnp\.(float|int)\b(?![0-9_])")
changed = 0
for rel in files:
    path = os.path.join(root, rel)
    text = open(path, encoding="utf-8").read()
    new, n = pattern.subn(lambda m: m.group(1), text)
    if n:
        open(path, "w", encoding="utf-8").write(new)
        changed += n
print("   numpy alias patch applied (%d replacements)" % changed if changed else "   numpy alias patch already applied")
EOF
  python -c "import fairseq; print('   fairseq imports OK:', fairseq.__version__)"

  # 3) Packages used by the repository code (requirements.txt pins librosa==0.9.1, tensorboardX==2.5)
  uv pip install librosa tensorboardX

  # 4) XLS-R 300M base checkpoint. model.py l. 24 loads 'xlsr2_300m.pt' from the current folder,
  #    so it is linked into the repository folder: run the model from $SSL.
  download https://dl.fbaipublicfiles.com/fairseq/wav2vec/xlsr2_300m.pt "$WS/weights/xlsr/xlsr2_300m.pt"
  ln -sf "$WS/weights/xlsr/xlsr2_300m.pt" "$SSL/xlsr2_300m.pt"

  # 5) Fine-tuned LA and DF models from the authors' Google Drive folder.
  #    Google Drive may refuse automated downloads (quota). Then download the folder in a browser
  #    and copy it to $WS/weights/ssl_anti_spoofing with scp.
  local GD="$WS/weights/ssl_anti_spoofing"
  if [ -n "$(ls -A "$GD" 2>/dev/null)" ]; then
    echo "   already downloaded: $GD"
  else
    uv pip install gdown
    rm -rf "$GD.tmp"
    gdown --folder "https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing" -O "$GD.tmp"
    rm -rf "$GD"
    mv "$GD.tmp" "$GD"
  fi
}

install_sonics() {
  echo "== [sonics] Repository, package, weights"
  clone_at sonics https://github.com/awsaf49/sonics.git 9156ffad151f797c71556923c4a02fa01fa8fc91
  # Installs the sonics package with its requirements (timm, fvcore, librosa, ...);
  # torch is already installed and satisfies torch>=2.4.0
  uv pip install -e "$WS/repos/sonics"
  # The two chosen checkpoints, at fixed Hugging Face commits; a checkpoint whose
  # config.json and pytorch_model.bin are already there is not downloaded again
  WEIGHTS_DIR="$WS/weights/sonics" python - <<'EOF'
import os
from huggingface_hub import snapshot_download
out = os.environ["WEIGHTS_DIR"]
for name, rev in [("sonics-spectttra-alpha-5s", "d30e3553a5ab08a171bdffdbbd2d792ac7970d65"),
                  ("sonics-spectttra-alpha-120s", "094b32a5545098a71c113f6ae9d5c55310564268")]:
    local = os.path.join(out, name)
    if all(os.path.isfile(os.path.join(local, f)) for f in ("config.json", "pytorch_model.bin")):
        print("   already downloaded:", local)
        continue
    snapshot_download(repo_id=f"awsaf49/{name}", revision=rev, local_dir=local)
    print("  ", name, "->", local)
EOF
}

# Each model installation runs in its own subshell: if it fails, the error is recorded and the
# next model is still installed. Nothing that was already downloaded is deleted.
RESULTS=(); ANY_FAILED=0
run_model_installation() {  # label, install function
  set +e
  ( set -e; "$2" )
  local rc=$?
  set -e
  if [ "$rc" -eq 0 ]; then
    RESULTS+=("$1: OK")
  else
    RESULTS+=("$1: FAILED — run the script again to finish")
    ANY_FAILED=1
  fi
}

[ "$DO_AASIST" = 1 ]  && run_model_installation aasist   install_aasist
[ "$DO_RAWNET2" = 1 ] && run_model_installation rawnet2  install_rawnet2
[ "$DO_W2V2" = 1 ]    && run_model_installation wav2vec2 install_wav2vec2
[ "$DO_SONICS" = 1 ]  && run_model_installation sonics   install_sonics

# ---------------------------------------------------------------------------
# Check
# ---------------------------------------------------------------------------

echo "== [check]"
set +e
DO_W2V2=$DO_W2V2 DO_SONICS=$DO_SONICS python - <<'EOF'
import os, sys, torch
ok = True
print("Python:", sys.version.split()[0])
if sys.version_info[:2] != (3, 10):
    print("   ERROR: expected Python 3.10"); ok = False
print("torch:", torch.__version__)
if not torch.cuda.is_available():
    print("   ERROR: torch does not see the GPU"); sys.exit(1)
cc = torch.cuda.get_device_capability(0)
print("GPU:", torch.cuda.get_device_name(0), "| compute capability:", cc)
# 8.9 = RTX 4090 (Ada), 12.0 = RTX 5090 / RTX PRO 4500 / RTX PRO 6000 (Blackwell)
if cc not in [(8, 9), (12, 0)]:
    print("   WARNING: unusual GPU, check that the results are comparable")
if os.environ.get("DO_W2V2") == "1":
    try:
        import fairseq
        print("fairseq:", fairseq.__version__)
    except Exception as e:
        print("   ERROR: fairseq does not import:", e); ok = False
if os.environ.get("DO_SONICS") == "1":
    try:
        import sonics  # noqa: F401
        print("sonics: imports OK")
    except Exception as e:
        print("   ERROR: sonics does not import:", e); ok = False
sys.exit(0 if ok else 1)
EOF
CHECK_RC=$?
set -e

echo
echo "== [summary]"
for line in "${RESULTS[@]}"; do echo "   $line"; done

echo
echo "Activate the environment in terminal:"
echo "   source $VENV/bin/activate"
echo "After installing new models, update the pinned versions"
echo "(--exclude-editable: fairseq and sonics are installed by their own model steps):"
echo "   uv pip freeze --exclude-editable > /workspace/requirements-gpu.txt"

if [ "$ANY_FAILED" -ne 0 ] || [ "$CHECK_RC" -ne 0 ]; then exit 1; fi
