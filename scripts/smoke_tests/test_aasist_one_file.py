import json
import sys

import numpy as np
import soundfile as sf
import torch

sys.path.insert(0, "/workspace/repos/aasist")
from models.AASIST import Model

cfg = json.load(open("/workspace/repos/aasist/config/AASIST.conf"))["model_config"]
model = Model(cfg).cuda().eval()
model.load_state_dict(
    torch.load("/workspace/repos/aasist/models/weights/AASIST.pth", map_location="cuda")
)

x, sr = sf.read(sys.argv[1], dtype="float32")
assert sr == 16000, f"expected 16 kHz, got {sr} Hz"
assert x.ndim == 1, "expected mono audio"
n = 64600
x = np.tile(x, n // len(x) + 1)[:n]
with torch.no_grad():
    _, out = model(torch.from_numpy(x)[None].cuda())
print("file:", sys.argv[1])
print("GPU:", torch.cuda.get_device_name(0))
print("logits [spoof, bona fide]:", out[0].tolist())
print("score (bona fide):", out[0, 1].item())
print("GPU memory used by the model: %.1f MB" % (torch.cuda.max_memory_allocated() / 1e6))
