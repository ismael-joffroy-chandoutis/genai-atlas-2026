#!/usr/bin/env python3
"""Test optique 15/10/2026 : même scène, focale au prompt contre rendu Blender retexturé (Qwen-Image, ComfyUI, RTX 5090).
Usage : run_test_optique.py <hote> <dossier_blender> <dossier_sortie>"""
import json, os, sys, time, uuid, urllib.request

host, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
base = f"http://{host}:8188"
os.makedirs(out, exist_ok=True)
SEED = 20261015
SCENE = ("Realistic photograph of a woman in a red wool coat and dark trousers standing in the middle of a long "
         "neoclassical stone colonnade, rows of white columns receding on both sides, polished stone floor, "
         "soft overcast daylight, natural colors.")
NEG = "blurry, low quality, distorted, cartoon, illustration, text, watermark"
LENS = {
    "f24_plein-format": "Shot on a full-frame camera with a 24mm lens.",
    "f50_plein-format": "Shot on a full-frame camera with a 50mm lens.",
    "f100_plein-format": "Shot on a full-frame camera with a 100mm lens.",
    "f35_plein-format": "Shot with a 35mm lens on a full-frame camera.",
    "f35_super35": "Shot with a 35mm lens on a Super 35 cinema camera.",
}

def post(path, data, ctype="application/json"):
    r = urllib.request.Request(base + path, data=data, headers={"Content-Type": ctype})
    return json.load(urllib.request.urlopen(r))

def upload(p):
    b = "----t" + uuid.uuid4().hex
    body = (f'--{b}\r\nContent-Disposition: form-data; name="image"; filename="{os.path.basename(p)}"\r\n'
            f'Content-Type: image/png\r\n\r\n').encode() + open(p, "rb").read() + \
           f'\r\n--{b}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n--{b}--\r\n'.encode()
    return post("/upload/image", body, "multipart/form-data; boundary=" + b)["name"]

def graph(prompt, prefix, image=None, denoise=1.0):
    g = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen_image_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.1}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": NEG}},
        "8": {"class_type": "KSampler", "inputs": {"model": ["4", 0], "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0],
              "seed": SEED, "steps": 30, "cfg": 4.0, "sampler_name": "euler", "scheduler": "simple", "denoise": denoise}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "optique/" + prefix}},
    }
    if image:
        g["11"] = {"class_type": "LoadImage", "inputs": {"image": image}}
        g["7"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["11", 0], "vae": ["3", 0]}}
    else:
        g["7"] = {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1344, "height": 768, "batch_size": 1}}
    return g

def run(g, dst):
    pid = post("/prompt", json.dumps({"prompt": g}).encode())["prompt_id"]
    t0 = time.time()
    while True:
        time.sleep(3)
        h = json.load(urllib.request.urlopen(f"{base}/history/{pid}"))
        if pid in h: break
    st = h[pid]["status"]
    if st.get("status_str") != "success":
        print("ECHEC", dst, json.dumps(st.get("messages", []))[:1500]); return
    f = h[pid]["outputs"]["10"]["images"][0]
    urllib.request.urlretrieve(f"{base}/view?filename={f['filename']}&subfolder={f['subfolder']}&type=output", dst)
    print("ok", os.path.basename(dst), round(time.time() - t0), "s", flush=True)

for name, lens in LENS.items():
    run(graph(SCENE + " " + lens, "prompt_" + name), os.path.join(out, f"prompt_{name}.png"))
    img = upload(os.path.join(src, name + ".png"))
    run(graph(SCENE, "blender_" + name, img, 0.62), os.path.join(out, f"blender_{name}.png"))
print("TERMINE")
