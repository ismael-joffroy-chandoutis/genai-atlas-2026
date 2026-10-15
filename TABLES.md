# Tables

Generated from `data/*.json` by `scripts/export_tables.py`. Data as of 15 October 2026. `?` = not documented. Prices: cheapest pay-per-use price found, in USD per second of video or per image, with the platform. Local columns: RTX 5090 32 GB, RTX 4090 24 GB, Mac M5 Max 128 GB. "Integrated in" = the model ships in the official ComfyUI templates (local, not API nodes), in Wan2GP, Pinokio, Draw Things, Maestro or Phosphene. Notes inside the JSON files are in French.

## Video

| Model | Vendor | Open weights | Duration | Max res | Audio | Image refs | Video refs | Audio refs | First / last frame | Keyframes | LoRA | 5090 | 4090 | Mac 128 GB | AA T2V | AA I2V | Integrated in | Cheapest 720p $/s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Agnes Video · 2.5 | Sapiens AI | no | ? | ? | ? | ? | ? | ? | ? / ? | ? | ? | no | ? | ? | 1069 | ? | – |  |
| Bach · 1.0 Pro | Video Rebirth | no | ?–30 s | ? | ? | ? | ? | ? | yes / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| Boreal · Boreal | Creatify | no | 1–20 s | 2K (2016 px de grand côté en 16:9 et 9:16) | yes | 1 | ? | 1 | no / no | ? | no | no | ? | ? | 830 | ? | – |  |
| FLUX 3 · FLUX 3 Dev (poids ouverts annoncés) | Black Forest Labs | ? | ? | ? | ? | ? | ? | ? | ? / ? | ? | ? | ? | ? | ? | ? | ? | – |  |
| FLUX 3 · FLUX 3 Video | Black Forest Labs | no | 5–20 s | 4K selon bfl.ai et OpenRouter ; 1080p maximum sur fal (contradiction) | yes | 0 | ? | 0 | yes / yes | 10 | no | no | ? | ? | 1145 | 1089 | – | 0.060 (bfl) |
| FLUX 3 · FLUX Video Edit [fast] | Black Forest Labs | no | ?–15 s | ? | no | ? | 1 | ? | no / no | ? | no | no | ? | ? | ? | ? | – | 0.030 (openrouter) |
| Gemini Omni Flash · Gemini Omni Flash 1.0 | Google | no | 3–10 s | ? | yes | 10 | ? | ? | yes / ? | ? | no | no | ? | ? | ? | ? | – |  |
| Gemini Omni Flash · Gemini Omni Flash 1.1 | Google | no | 3–10 s | 4K (1080p et 4K par agrandissement ; 720p par défaut) | yes | 10 | 3 (9 s) | 0 | yes / yes | ? | no | no | ? | ? | 1132 | 1134 | – | 0.100 (fal) |
| Grok Imagine · Grok Imagine Video (1.0) | xAI (SpaceXAI) | no | 1–15 s | 720p | yes | 7 | ? | ? | yes / no | ? | ? | no | ? | ? | ? | ? | – | 0.022 (kie) |
| Grok Imagine · Grok Imagine Video 1.5 | xAI (SpaceXAI) | no | 1–15 s | 1080p | yes | 14 | ? | 3 | yes / yes | 4 | ? | no | ? | ? | 1059 | 1068 | – | 0.022 (kie) |
| Grok Imagine · Grok Imagine Video 1.5 Lite | xAI (SpaceXAI) | no | 1–15 s | 1080p (720p agrandi) | yes | 0 | ? | ? | yes / no | 0 | ? | no | ? | ? | 998 | ? | – | 0.030 (openrouter) |
| HappyHorse · 1.0 | Alibaba (unité ATH) | no | 3–15 s | 1080p | ? | 9 | ? | ? | yes / no | ? | ? | no | ? | ? | 1034 | 1043 | – | 0.099 (openrouter) |
| HappyHorse · 1.1 | Alibaba (unité ATH) | no | 3–15 s | 1080p | yes | 9 | ? | ? | yes / no | 0 | ? | no | ? | ? | 1054 | 1061 | – | 0.099 (openrouter) |
| Hedra · Character-3 | Hedra | no | ?–600 s | 1080p | no | ? | ? | 1 (600 s) | yes / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| HeyGen · Avatar IV | HeyGen | no | ? | 1080p | ? | ? | ? | 1 | yes / ? | ? | ? | no | ? | ? | ? | ? | – | 0.050 (openrouter) |
| HeyGen · HeyGen Video 1 | HeyGen | no | 5–15 s | 2K | ? | ? | ? | ? | yes / no | ? | ? | no | ? | ? | ? | ? | – | 0.036 (openrouter) |
| Higgsfield Cinema Studio · Cinema Studio 4.0 | Higgsfield | no | 4–30 s | 1080p | yes | 50 | ? | ? | yes / yes | ? | ? | no | ? | ? | ? | ? | – |  |
| Higgsfield Cinema Studio · Cinema Studio Video 3.0 | Higgsfield | no | 4–15 s | 4K | yes | ? | ? | ? | yes / yes | ? | ? | no | ? | ? | ? | ? | – |  |
| HunyuanVideo · 1.5 (8,3B) | Tencent Hunyuan | yes | ? | 720p natif, 1080p par super-résolution intégrée | no | 0 | 0 | 0 | yes / no | ? | yes | yes | yes | ? | ? | ? | ComfyUI, Wan2GP, Pinokio, Maestro | 0.040 (wavespeed) |
| Kling · 2.5 Turbo Pro | Kuaishou (KlingAI) | no | 5–10 s | 1080p | no | 0 | 0 | 0 | yes / yes | 0 | ? | no | ? | ? | ? | ? | – |  |
| Kling · 2.6 Pro | Kuaishou (KlingAI) | no | 5–10 s | ? | yes | 0 | 0 | 0 | yes / yes | 0 | ? | no | ? | ? | ? | ? | – | 0.070 (replicate) |
| Kling · 2.6 Standard | Kuaishou (KlingAI) | no | ? | ? | ? | ? | 1 | ? | ? / ? | ? | ? | no | ? | ? | ? | ? | – | 0.042 (wavespeed) |
| Kling · 3.0 Motion Control (Standard et Pro) | Kuaishou (KlingAI) | no | ?–30 s | ? | no | 1 | 1 | ? | no / no | ? | ? | no | ? | ? | ? | ? | – |  |
| Kling · 3.0 Omni Pro (O3 Pro) | Kuaishou (KlingAI) | no | 3–15 s | 4K (points d'entrée o3/4k) ; 1080p en Pro | yes | ? | 1 (15 s) | 0 | yes / yes | 0 | ? | no | ? | ? | 1020 | 1004 | – | 0.070 (kie) |
| Kling · 3.0 Omni Standard (O3 Standard) | Kuaishou (KlingAI) | no | 3–15 s | 720p | yes | ? | 1 (15 s) | 0 | yes / yes | 0 | ? | no | ? | ? | ? | ? | – | 0.084 (kling) |
| Kling · 3.0 Pro | Kuaishou (KlingAI) | no | 3–15 s | 4K (point d'entrée v3/4k, serveur de Singapour seulement) ; 1080p en Pro standard | yes | ? | 1 | 0 | yes / yes | 0 | ? | no | ? | ? | 1000 | 1000 | – | 0.112 (openrouter) |
| Kling · 3.0 Standard | Kuaishou (KlingAI) | no | 3–15 s | 720p | yes | ? | 1 | 0 | yes / yes | 0 | ? | no | ? | ? | ? | ? | – | 0.070 (kie) |
| Kling · 3.0 Turbo (Standard et Pro) | Kuaishou (KlingAI) | no | 3–15 s | 1080p (Pro) | yes | 0 | 0 | 0 | yes / ? | 0 | ? | no | ? | ? | ? | ? | – | 0.090 (kie) |
| Kling · 4.0 | Kuaishou (KlingAI) | no | 3–30 s | 4K (10 bits HDR annoncé « bientôt ») | yes | 10 | 5 (30 s) | ? | yes / yes | 10 | ? | no | ? | ? | ? | ? | – |  |
| Kling · 4.0 Flash | Kuaishou (KlingAI) | no | 3–20 s | 720p (8 bits SDR) | ? | ? | ? | ? | yes / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| Kling · AI Avatar v2 (Standard et Pro) | Kuaishou (KlingAI) | no | ? | ? | no | 1 | ? | 1 | yes / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| Kling · Video O1 (Pro) | Kuaishou (KlingAI) | no | 3–10 s | 720p (OpenRouter) | ? | ? | 1 | 0 | yes / yes | 0 | ? | no | ? | ? | 885 | ? | – | 0.112 (openrouter) |
| LTX · LTX-2.3 (poids ouverts dev et distillé 22B) | Lightricks | yes | ? | 4K (via upscaler spatial ; largeur et hauteur multiples de 32) | yes | ? | ? | ? | yes / yes | ? | yes | ? | yes | yes | ? | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro, Phosphene | 0.030 (wavespeed) |
| LTX · LTX-2.3 Fast (API) | Lightricks | yes | 6–20 s | 4K (3840x2160) | yes | ? | ? | ? | yes / ? | ? | no | no | no | no | 845 | 889 | – | 0.030 (ltx) |
| LTX · LTX-2.3 IC-LoRA de contrôle (Union, Motion-Track, HDR, DubIt, In-Outpainting, Relight, Foley V2A) | Lightricks | yes | ? | 4K HDR (IC-LoRA HDR, sortie EXR) | yes | ? | ? | ? | yes / yes | 3 | yes | ? | ? | ? | ? | ? | Pinokio, Maestro, Phosphene |  |
| LTX · LTX-2.3 Pro (API) | Lightricks | yes | 6–10 s | 4K (3840x2160) | yes | ? | ? | ? | yes / ? | ? | no | no | no | no | 894 | 903 | – | 0.040 (ltx) |
| LTX · LTX-2.5 Fast (API) | Lightricks | yes | 6–20 s | 4K (3840x2160) | yes | ? | ? | ? | yes / yes | ? | no | no | no | no | 951 | 985 | – | 0.030 (replicate) |
| LTX · LTX-2.5 IC-LoRA Layout-To-Render | Lightricks | yes | ? | 1920x1088 (deuxième passe) | ? | ? | ? | ? | yes / yes | 3 | yes | ? | ? | ? | ? | ? | Wan2GP, Pinokio |  |
| LTX · LTX-2.5 IC-LoRA officielles (Refine-Details, Restore, SDR-To-HDR, Alpha-Gen, Ingredients, Clean-Plate, Deblur, Decompression, Colorization, Day-To-Night, Water-Simulation, Pixel-Spatial-Upscaler) | Lightricks | yes | ? | 4K HDR (via Pixel-Spatial-Upscaler et SDR-To-HDR) | ? | ? | ? | ? | yes / ? | ? | yes | ? | ? | ? | ? | ? | Pinokio |  |
| LTX · LTX-2.5 Pro (API) | Lightricks | yes | 6–10 s | 4K selon docs.ltx.io ; 1080p maximum sur fal (contradiction) | yes | ? | ? | ? | yes / yes | ? | no | no | no | no | 948 | 957 | – | 0.120 (fal) |
| LTX · LTX-2.5 dev 22B (bf16) | Lightricks | yes | ? | 4K HDR (3840x2176 dans l'exemple officiel, upscaler spatial x2 et DFR) | yes | ? | ? | ? | yes / yes | ? | yes | ? | ? | ? | ? | ? | ComfyUI, Wan2GP, Pinokio, Maestro, Phosphene | 0.100 (wavespeed) |
| LTX · LTX-2.5 distillé 22B (8 étapes) | Lightricks | yes | ? | 4K HDR (3840x2176 dans l'exemple officiel, upscaler spatial x2 et DFR) | yes | ? | ? | ? | yes / yes | ? | yes | ? | yes | yes | ? | ? | ComfyUI, Wan2GP, Pinokio, Maestro, Phosphene |  |
| LTX · LTX-2.5 distillé quantifié (NVFP4, int8 convrot) | Lightricks | yes | ? | 4K HDR (3840x2176 dans l'exemple officiel, upscaler spatial x2 et DFR) | yes | ? | ? | ? | yes / yes | ? | yes | ? | yes | no | ? | ? | Wan2GP, Pinokio, Maestro |  |
| Luma Ray · Ray 3 | Luma AI | no | 5–10 s | 1080p | no | ? | ? | ? | yes / yes | ? | ? | no | ? | ? | ? | ? | – |  |
| Luma Ray · Ray 3.14 | Luma AI | no | 5–10 s | 1080p | no | 0 | ? | ? | yes / yes | ? | ? | no | ? | ? | ? | ? | – |  |
| Luma Ray · Ray 3.2 | Luma AI | no | 5–10 s | 1080p | ? | ? | ? | ? | yes / yes | 64 | ? | no | ? | ? | ? | ? | – | 0.060 (replicate) |
| LynnReal-Omni · LynnReal-Omni 32B | LynnReal AI | yes | ?–30 s | 768p natif (1344x768 par défaut) | yes | ? | ? | ? | yes / ? | ? | ? | ? | ? | no | ? | ? | – |  |
| LynnReal-Omni · LynnReal-Omni Flash 27B | LynnReal AI | yes | ?–30 s | 768p natif (1344x768 par défaut) | yes | ? | ? | ? | yes / ? | ? | ? | ? | ? | no | ? | ? | – |  |
| MAGI · MAGI-2 Preview | Sand.ai | yes | 10–10 s | 1080p (aperçu 512x896 puis affineur 1088x1920) | yes | 0 | ? | ? | yes / ? | ? | ? | no | no | no | 1044 | 1046 | – |  |
| Midjourney Video · V1 | Midjourney | no | 5–21 s | 480p | no | ? | ? | ? | yes / yes | ? | ? | no | ? | ? | ? | ? | – |  |
| MiniMax H3 · FastH3 Preview v1 4 étapes (VSA) | FastVideo (Hao AI Lab) | yes | ? | ? | yes | 0 | 0 | 0 | no / no | 0 | ? | ? | ? | no | ? | ? | Pinokio |  |
| MiniMax H3 · FastH3 V2 8 étapes (INT8 ConvRot, NVFP4, FP8) | FastVideo (Hao AI Lab) | yes | ? | 768p (petit côté 768, plafond 768x1344) | yes | 0 | 0 | 0 | yes / yes | 2 | ? | yes | ? | no | ? | ? | ComfyUI |  |
| MiniMax H3 · FastH3-Omni (Reactor) | Reactor | no | 5–15 s | 1344x768 (16:9), 768x1344 (9:16), 1024x768, 768x768 | yes | 9 | ? | 3 | yes / yes | 2 | ? | no | ? | ? | ? | ? | – |  |
| MiniMax H3 · H3 (API MiniMax et fal) | MiniMax | yes | 4–15 s | 4K sur fal (agrandi d'une base 768p) ; 2K chez MiniMax et OpenRouter | yes | 9 | 3 (15 s) | 3 (15 s) | yes / yes | 2 | yes | no | no | no | 1158 | 1141 | – | 0.040 (kie) |
| MiniMax H3 · H3 FL2VA 33B (poids ouverts) | MiniMax | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | 0 | 0 | 0 | yes / yes | 2 | yes | yes | yes | yes | 1158 | 1141 | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro |  |
| MiniMax H3 · H3 Fun ControlNet Union (1.0 puis 2.0) | Alibaba PAI | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | ? | ? | ? | yes / yes | ? | yes | ? | ? | ? | ? | ? | ComfyUI, Wan2GP, Pinokio |  |
| MiniMax H3 · H3 Max | fal (post-entraînement de MiniMax H3) | no | 0.92–15 s | 1080p (raffinage latent depuis 768p) ; 2K pour relight, extend et lip-sync | yes | 9 | 3 (15 s) | 3 (15 s) | yes / yes | 3 | no | no | ? | ? | 1156 | 1124 | – | 0.048 (fal) |
| MiniMax H3 · H3 Max Turbo | fal (post-entraînement de MiniMax H3) | no | 0.92–15 s | 1080p (raffinage latent depuis 768p) ; 2K pour relight, extend et lip-sync | yes | ? | ? | 3 | yes / yes | ? | no | no | ? | ? | ? | ? | – | 0.024 (fal) |
| MiniMax H3 · H3 PDD 8 étapes (33B et 20B, Wan2GP) | MiniMax / Wan2GP | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | ? | ? | ? | yes / yes | 2 | yes | yes | yes | no | ? | ? | Wan2GP, Pinokio, Maestro |  |
| MiniMax H3 · H3 Ref2VA 33B (poids ouverts) | MiniMax | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | 9 | 3 (15 s) | 3 (15 s) | no / no | 0 | yes | yes | yes | yes | ? | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro |  |
| MiniMax H3 · H3 Turbo LoRA (communautaires : lightx2v, larryvrh et dérivés) | Communauté (lightx2v, larryvrh) | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | ? | ? | ? | yes / yes | 2 | yes | yes | yes | ? | ? | ? | Wan2GP, Pinokio, Maestro, Phosphene |  |
| MiniMax H3 · H3 Veda Sparse (attention creuse apprise, Wan2GP v18) | MiniMax / Wan2GP | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | 9 | 3 | 3 | yes / yes | ? | yes | yes | ? | no | ? | ? | Wan2GP, Pinokio |  |
| MiniMax H3 · H3 élagué 20B FL2VA (communautaire) | MiniMax (élagage multimodalart) | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | 0 | 0 | 0 | yes / yes | 2 | yes | yes | yes | ? | ? | ? | ComfyUI, Wan2GP, Pinokio, Maestro, Phosphene |  |
| MiniMax H3 · H3 élagué 20B REF2VA (communautaire) | MiniMax (élagage multimodalart) | yes | 4–15 s | 768p natif (petit côté 768 px) ; 2K via H3-Regenerate-2K non publié | yes | 9 | 3 (15 s) | 3 (15 s) | no / no | 0 | yes | yes | yes | ? | ? | ? | ComfyUI, Wan2GP, Pinokio, Maestro |  |
| MiniMax Hailuo · Hailuo 2.3 | MiniMax | no | 6–10 s | 1080p (Pro), 768p (Standard) | no | 0 | 0 | 0 | yes / no | 1 | no | no | ? | ? | ? | ? | – | 0.025 (kie) |
| MiniMax Hailuo · Hailuo 2.3 Fast | MiniMax | no | 6–10 s | 1080p (Pro), 768p (Standard) | no | 0 | 0 | 0 | yes / no | 1 | no | no | ? | ? | ? | ? | – | 0.032 (runware) |
| Moonvalley Marey · Marey | Moonvalley | no | 5–10 s | 1080p | ? | ? | ? | ? | ? / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| NVIDIA Cosmos3 · Cosmos3 Super Image2Video (64B) | NVIDIA | yes | ? | 720p | ? | 1 | ? | 0 | yes / no | ? | ? | no | no | ? | ? | ? | – |  |
| NVIDIA Cosmos3 · Cosmos3 Super Image2Video 4Step (64B distillé) | NVIDIA | yes | ? | 720p | ? | 1 | ? | 0 | yes / no | ? | ? | no | no | ? | ? | ? | – |  |
| OmniHuman · OmniHuman 1.5 | ByteDance | no | ?–60 s | 1080p | no | ? | ? | 1 (60 s) | yes / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| P-Video · P-Video | Pruna AI | ? | 1–10 s | 1080p | yes | 0 | ? | 1 | yes / ? | ? | ? | ? | ? | ? | 803 | ? | – | 0.025 (runware) |
| Pika · Pika 2.2 Pikaframes | Pika Labs | no | ?–25 s | 1080p | ? | ? | ? | ? | yes / yes | 5 | ? | no | ? | ? | ? | ? | – | 0.040 (fal) |
| Pika · Pika 2.5 | Pika Labs | no | ? | ? | ? | ? | ? | ? | ? / ? | ? | ? | no | ? | ? | 838 | ? | – |  |
| PixVerse · C1 | PixVerse (AISphere) | no | 1–15 s | 1080p | yes | 7 | ? | ? | yes / yes | ? | ? | no | ? | ? | ? | ? | – | 0.050 (fal) |
| PixVerse · V6 | PixVerse (AISphere) | no | 1–15 s | 1080p | yes | ? | ? | ? | yes / yes | 0 | ? | no | ? | ? | 989 | 1025 | – | 0.036 (kie) |
| PixVerse · VibeMV (clip musical) | PixVerse (AISphere) | no | ? | 1080p | no | 2 | ? | 1 (360 s) | no / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| Runway Act · Act-Two | Runway | no | 3–30 s | ? | ? | 1 | 2 | ? | ? / ? | ? | ? | no | ? | ? | ? | ? | – |  |
| Runway Aleph · Aleph 2.0 | Runway | no | ?–30 s | 1080p | no | ? | 1 (30 s) | ? | ? / ? | 5 | ? | no | ? | ? | ? | ? | – | 0.280 (openrouter) |
| Runway Gen · Gen-4.5 | Runway | no | 2–10 s | 720p | no | ? | ? | ? | yes / no | ? | ? | no | ? | ? | 912 | ? | – | 0.120 (openrouter) |
| Seedance · 1.5 Pro | ByteDance Seed | no | 4–12 s | 1080p | yes | 0 | 0 | 0 | yes / yes | ? | no | no | ? | ? | ? | ? | – | 0.018 (kie) |
| Seedance · 2.0 | ByteDance Seed | no | 4–15 s | 4K (fal, OpenRouter) | yes | 9 | 3 (15 s) | 3 (15 s) | yes / yes | ? | no | no | ? | ? | 1138 | 1121 | – | 0.150 (byteplus) |
| Seedance · 2.0 Fast | ByteDance Seed | no | 4–15 s | 720p | yes | 9 | 3 (15 s) | 3 (15 s) | yes / yes | ? | no | no | ? | ? | ? | ? | – | 0.091 (openrouter) |
| Seedance · 2.0 Mini | ByteDance Seed | no | 4–15 s | 720p | yes | 9 | 3 (15 s) | 3 (15 s) | yes / yes | ? | no | no | ? | ? | ? | ? | – | 0.041 (kie) |
| Seedance · 2.5 | ByteDance Seed | no | 4–30 s | 1080p (fal ; 720p sur OpenRouter ; « jusqu'au 4K » selon des sources tierces) | yes | 30 | 10 (30.2 s) | 10 (30.2 s) | yes / yes | ? | no | no | ? | ? | 1159 | 1139 | – | 0.230 (runware) |
| Sora · Sora 2 | OpenAI | no | ? | ? | ? | ? | ? | ? | ? / ? | ? | ? | no | ? | ? | ? | ? | – | 0.100 (openai) |
| Sora · Sora 2 Pro | OpenAI | no | ? | ? | ? | ? | ? | ? | ? / ? | ? | ? | no | ? | ? | ? | ? | – | 0.300 (openai) |
| Utopai X · Utopai X | Utopai Studios | no | ? | ? | ? | ? | ? | ? | ? / ? | ? | ? | no | ? | ? | 1166 | ? | – |  |
| Veo · Veo 3.1 | Google | no | 4–8 s | 4K (8 s seulement) | yes | 3 | 0 | 0 | yes / yes | ? | no | no | ? | ? | 968 | 1031 | – | 0.156 (kie) |
| Veo · Veo 3.1 Fast | Google | no | 4–8 s | 4K (8 s seulement) | yes | 3 | 0 | 0 | yes / yes | ? | no | no | ? | ? | 964 | 1017 | – | 0.037 (kie) |
| Veo · Veo 3.1 Lite | Google | no | 4–8 s | 1080p | yes | ? | 0 | 0 | yes / yes | ? | no | no | ? | ? | 952 | ? | – | 0.019 (kie) |
| Vidu · Q2 Pro | Shengshu Technology | no | 1–8 s | 1080p | no | 7 | 2 | ? | yes / yes | 0 | ? | no | ? | ? | ? | ? | – |  |
| Vidu · Q2 Turbo | Shengshu Technology | no | 2–8 s | 1080p | no | ? | ? | ? | yes / yes | 0 | ? | no | ? | ? | ? | ? | – |  |
| Vidu · Q3 Mix (référence vers vidéo) | Shengshu Technology | no | 1–16 s | 1080p | yes | 4 | ? | ? | no / no | ? | ? | no | ? | ? | ? | ? | – |  |
| Vidu · Q3 Pro | Shengshu Technology | no | 1–16 s | 1080p | yes | 0 | ? | ? | yes / yes | 0 | ? | no | ? | ? | 943 | 1015 | – | 0.065 (runware) |
| Vidu · Q3 Turbo | Shengshu Technology | no | 1–16 s | 1080p | yes | ? | ? | ? | yes / yes | 0 | ? | no | ? | ? | 918 | 967 | – | 0.036 (runware) |
| Vidu · Q4 Preview | Shengshu Technology | no | 3–16 s | 4K (10 bits en 2K et 4K) | yes | 12 | ? | 3 | yes / ? | ? | ? | no | ? | ? | ? | ? | – | 0.067 (fal) |
| Vimoo · 1.0 | Vimoo | no | ? | ? | ? | ? | ? | ? | yes / ? | ? | ? | ? | ? | ? | ? | ? | – |  |
| Wan · 2.2 A14B (T2V / I2V) | Alibaba (Tongyi Wan) | yes | ? | 720p | no | 0 | 0 | 0 | yes / yes | ? | yes | yes | yes | yes | ? | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.060 (wavespeed) |
| Wan · 2.2 Animate-2 14B (et Animate 14B) | Alibaba (Tongyi Wan / HumanAIGC) | yes | ? | 720p | no | 1 | 1 | 0 | ? / ? | ? | ? | no | yes | ? | ? | ? | Wan2GP, Pinokio, Maestro |  |
| Wan · 2.2 S2V 14B (parole vers vidéo) | Alibaba (Tongyi Wan) | yes | ? | 720p | no | 1 | 0 | 1 | yes / no | ? | ? | ? | ? | ? | ? | ? | Pinokio |  |
| Wan · 2.2 TI2V 5B | Alibaba (Tongyi Wan) | yes | ? | 720p | no | 0 | 0 | 0 | yes / ? | ? | ? | yes | yes | yes | ? | ? | Wan2GP, Pinokio, Draw Things, Maestro |  |
| Wan · 2.2 VACE Fun A14B (contrôle et édition) | Alibaba (PAI, VideoX-Fun) | yes | ? | 720p | no | ? | 1 | 0 | yes / yes | ? | ? | ? | ? | ? | ? | ? | Wan2GP, Pinokio, Maestro |  |
| Wan · 2.6 | Alibaba (Tongyi Wan) | no | 5–15 s | 1080p | yes | 0 | 3 | 1 | yes / no | ? | no | no | ? | ? | ? | ? | – | 0.070 (kie) |
| Wan · 2.7 | Alibaba (Tongyi Wan) | no | 2–15 s | 1080p | yes | ? | ? | 1 (30 s) | yes / yes | ? | no | no | ? | ? | 1040 | 1033 | – | 0.080 (kie) |
| Wan · 3.0 | Alibaba (Tongyi Wan) | no | 2–30 s | 1080p | yes | 10 | 5 (15 s) | 5 (15 s) | yes / yes | ? | no | no | ? | ? | 1173 | 1127 | – | 0.050 (replicate) |
| Wan · 3.0 Prime | Alibaba (Tongyi Wan) | no | 2–30 s | 1080p | yes | 10 | 5 (15 s) | 5 (15 s) | yes / yes | ? | no | no | ? | ? | ? | ? | – | 0.126 (kie) |

## Image

| Model | Vendor | Open weights | License | Max res | Image refs | Edit | LoRA | 5090 | 4090 | Mac 128 GB | AA T2I | AA edit | Integrated in | Cheapest $/image |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FLUX 3 · FLUX 3 Image | Black Forest Labs | no | Propriétaire (API BFL, Replicate, partenaires) | 4K natif (source tierce) | 10 | yes | no | no | ? | ? | 1114 | ? | – | 0.024 (fal) |
| FLUX.1 · FLUX.1 Krea [dev] | Black Forest Labs / Krea | yes | FLUX.1 [dev] Non-Commercial License | ? | ? | ? | yes | yes | yes | ? | 829 | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.025 (fal) |
| FLUX.1 Kontext · FLUX.1 Kontext [dev] | Black Forest Labs | yes | FLUX.1 [dev] Non-Commercial License | ? | 1 | yes | yes | yes | yes | yes | ? | 893 | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.025 (fal) |
| FLUX.1 Kontext · FLUX.1 Kontext [max] | Black Forest Labs | no | Propriétaire (API BFL) | ? | 1 | yes | no | no | ? | ? | 929 | 918 | – | 0.050 (kie) |
| FLUX.1 Kontext · FLUX.1 Kontext [pro] | Black Forest Labs | no | Propriétaire (API BFL) | ? | 1 | yes | no | no | ? | ? | 920 | 911 | – | 0.025 (kie) |
| FLUX.2 · FLUX.2 [dev] | Black Forest Labs | yes | FLUX Non-Commercial License (usage commercial = licence payante) | 4 MP | 6 | yes | yes | yes | yes | yes | 1000 | 1000 | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.014 (replicate) |
| FLUX.2 · FLUX.2 [flex] | Black Forest Labs | no | Propriétaire (API BFL) | 4 MP | 8 | yes | no | no | ? | ? | 1027 | 1009 | – | 0.050 (bfl) |
| FLUX.2 · FLUX.2 [klein] 4B | Black Forest Labs | yes | Apache 2.0 (commercial autorisé) | 4 MP (famille) | 4 | yes | yes | yes | yes | yes | 840 | 935 | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro, Phosphene | 0.001 (replicate) |
| FLUX.2 · FLUX.2 [klein] 9B | Black Forest Labs | yes | FLUX Non-Commercial License | 4 MP (famille) | 4 | yes | yes | yes | ? | yes | 932 | 1011 | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.006 (fal) |
| FLUX.2 · FLUX.2 [max] | Black Forest Labs | no | Propriétaire (API BFL) | 4 MP | 8 | yes | no | no | ? | ? | 1021 | 995 | – | 0.070 (bfl) |
| FLUX.2 · FLUX.2 [pro] | Black Forest Labs | no | Propriétaire (API BFL) | 4 MP | 8 | yes | no | no | ? | ? | 1003 | 1009 | – | 0.025 (kie) |
| Firefly Image · Firefly Image Model 5 | Adobe | no | Propriétaire (Creative Cloud, API Firefly Services) | 4 MP natif (environ 2304x1792 constaté par un utilisateur) | ? | yes | no | no | ? | ? | ? | ? | – |  |
| GPT Image · GPT Image 1 Mini | OpenAI | no | Propriétaire (API OpenAI) | ? | ? | yes | no | no | ? | ? | 942 | 924 | – | 0.011 (openai) |
| GPT Image · GPT Image 1.5 | OpenAI | no | Propriétaire (API OpenAI) | ? | ? | yes | no | no | ? | ? | 1120 | 1116 | – | 0.020 (kie) |
| GPT Image · GPT Image 2 | OpenAI | no | Propriétaire (API OpenAI) | 3840x2160 (4K, 8,3 MP) | ? | yes | no | no | ? | ? | 1187 | 1133 | – | 0.030 (kie) |
| GPT Image · GPT Image 2.5 Flare | OpenAI | no | Propriétaire (API OpenAI) | 3840 px côté long, 8,3 MP max (au-delà de 2560x1440 = expérimental) | ? | yes | no | no | ? | ? | 1207 | 1178 | – | 0.024 (wavespeed) |
| GPT Image · GPT Image 2.5 Sunburst | OpenAI | no | Propriétaire (API OpenAI) | 3840 px côté long, 8,3 MP max (au-delà de 2560x1440 = expérimental) | ? | yes | no | no | ? | ? | 1217 | 1199 | – | 0.024 (wavespeed) |
| Grok Imagine Image · Grok Imagine Image 2.0 | xAI (SpaceXAI) | no | Propriétaire (API xAI) | 2K (1K, 2K) | 5 | yes | no | no | ? | ? | 1166 | 1112 | – | 0.020 (kie) |
| Grok Imagine Image · grok-imagine-image | xAI (SpaceXAI) | no | Propriétaire (API xAI) | ? | ? | yes | no | no | ? | ? | 1021 | 1071 | – | 0.020 (fal) |
| Grok Imagine Image · grok-imagine-image-quality | xAI (SpaceXAI) | no | Propriétaire (API xAI) | ? | ? | yes | no | no | ? | ? | 1049 | 1091 | – | 0.050 (replicate) |
| HiDream-O1 · HiDream-O1-Image | HiDream.ai | yes | MIT (commercial autorisé) | 2048x2048 | 10 | yes | ? | yes | ? | ? | 976 | 953 | ComfyUI, Wan2GP, Pinokio, Maestro | 0.010 (fal) |
| HiDream-O1 · HiDream-O1-Image-1.5 | HiDream.ai | ? | ? | ? | ? | yes | no | ? | ? | ? | 1018 | ? | – |  |
| HiDream-O1 · HiDream-O1-Image-Dev | HiDream.ai | yes | MIT (commercial autorisé) | 2048x2048 | ? | yes | no | yes | ? | ? | 811 | 879 | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.005 (fal) |
| HunyuanImage (Hy Image) · HunyuanImage 3.0 | Tencent | yes | Tencent Hunyuan Community License (exclut UE, Royaume-Uni, Corée du Sud ; commercial soumis à seuil d'utilisateurs) | ? | ? | no | no | no | no | ? | 936 | 1023 | – |  |
| HunyuanImage (Hy Image) · HunyuanImage 3.0 Instruct | Tencent | yes | Tencent Hunyuan Community License (exclut UE, Royaume-Uni, Corée du Sud ; commercial soumis à seuil d'utilisateurs) | ? | ? | yes | no | no | no | ? | 990 | 1063 | – |  |
| HunyuanImage (Hy Image) · Hy Image 3.5 Preview (HunyuanImage 3.5) | Tencent | no | Propriétaire (Tencent Cloud TokenHub) | 2K ou 4K selon la source | ? | yes | no | no | ? | ? | 969 | 1088 | – | 0.007 (openrouter) |
| Ideogram · Ideogram 3.0 | Ideogram | no | Propriétaire (API, app) | ? | ? | yes | no | no | ? | ? | 914 | ? | – | 0.030 (fal) |
| Ideogram · Ideogram 4.0 (Quality, API) | Ideogram | no | Propriétaire (API Ideogram) | 2K | ? | ? | no | no | ? | ? | 1024 | ? | – | 0.100 (replicate) |
| Ideogram · Ideogram 4.0 (poids ouverts) | Ideogram | yes | Ideogram 4 Non-Commercial | 2048 (256-2048 par pas de 16, ratios jusqu'à 6:1) | ? | no | yes | yes | ? | yes | 1001 | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Phosphene | 0.050 (wavespeed) |
| Ideogram · Ideogram 4.5 (High) | Ideogram | no | Propriétaire (API, app) | ? | 4 | yes | no | no | ? | ? | 1019 | 1065 | – | 0.060 (replicate) |
| Imagen · Imagen 4 Ultra (imagen-4.0-ultra-generate-001) | Google | no | Propriétaire (Vertex AI, Gemini API) | ? | ? | no | no | no | ? | ? | ? | ? | – | 0.060 (google) |
| Krea 1 · Krea 1 | Krea | no | Propriétaire (app Krea) | 1,5K natif (4K via Enhancer) | 3 | no | no | no | ? | ? | ? | ? | – |  |
| Krea 2 · Krea 2 Large | Krea | no | Propriétaire (API et app Krea) | 1K via l'API (source tierce, non confirmée) | ? | ? | no | no | ? | ? | 1034 | ? | ComfyUI | 0.060 (openrouter) |
| Krea 2 · Krea 2 Medium | Krea | no | Propriétaire (API et app Krea) | 1K via l'API (source tierce) | ? | ? | no | no | ? | ? | 1013 | ? | ComfyUI | 0.015 (openrouter) |
| Krea 2 · Krea 2 Turbo / Raw (poids ouverts) | Krea | yes | Krea 2 Community License (gratuit sous 50 postes, plafond de CA cité à 1 M$ par une source ; Enterprise au-delà) | 2K natif (Turbo, 8 pas) | ? | no | yes | yes | yes | yes | 1018 | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.008 (fal) |
| Leonardo · Lucid Origin Fast | Leonardo.Ai (Canva) | no | Propriétaire (app et API Leonardo) | Full HD (1920x1080) | ? | ? | yes | no | ? | ? | 851 | ? | – |  |
| Leonardo · Lucid Origin Ultra | Leonardo.Ai (Canva) | no | Propriétaire (app et API Leonardo) | Full HD (1920x1080) | ? | ? | yes | no | ? | ? | 885 | ? | – |  |
| Leonardo · Phoenix 0.9 Ultra | Leonardo.Ai (Canva) | no | Propriétaire (app et API Leonardo) | ? | ? | ? | yes | no | ? | ? | 839 | ? | – |  |
| Leonardo · Phoenix 1.0 Fast | Leonardo.Ai (Canva) | no | Propriétaire (app et API Leonardo) | 5 MP (Phoenix 1.0) | ? | ? | yes | no | ? | ? | 833 | ? | – |  |
| Luma Photon · Photon (photon-1) | Luma AI | no | Propriétaire (API Luma, ligne héritée) | ? | ? | yes | no | no | ? | ? | 847 | ? | – | 0.019 (fal) |
| Luma Photon · Photon Flash (photon-flash-1) | Luma AI | no | Propriétaire (API Luma) | ? | ? | ? | no | no | ? | ? | 775 | ? | – | 0.005 (fal) |
| Luma UNI-1 · UNI-1 | Luma AI | no | Propriétaire (API, Dream Machine) | ? | 9 | yes | no | no | ? | ? | 992 | 1043 | – | 0.042 (wavespeed) |
| Luma UNI-1 · UNI-1 Max | Luma AI | no | Propriétaire (API, Dream Machine) | 2K | 9 | yes | no | no | ? | ? | 1020 | 1076 | – | 0.129 (segmind) |
| MAI-Image · MAI-Image-2.5 | Microsoft AI | no | Propriétaire (Azure AI Foundry) | ? | ? | yes | no | no | ? | ? | 1116 | 1125 | – | 0.196 (openrouter) |
| MAI-Image · MAI-Image-2.5-Flash | Microsoft AI | no | Propriétaire (Azure AI Foundry) | ? | ? | yes | no | no | ? | ? | 1029 | 1095 | – |  |
| MAI-Image · MAI-Image-2.5-Pro | Microsoft AI | no | Propriétaire (Azure AI Foundry) | ? | ? | yes | no | no | ? | ? | 1113 | 1117 | – | 0.451 (openrouter) |
| MAI-Image · MAI-Image-2.6 | Microsoft AI | no | Propriétaire (Azure AI Foundry, MAI Playground) | 1,5K (formats dynamiques) | ? | yes | no | no | ? | ? | 1164 | 1151 | – | 0.159 (openrouter) |
| MAI-Image · MAI-Image-2.6-Flash | Microsoft AI | no | Propriétaire (Azure AI Foundry) | ? | 5 | yes | no | no | ? | ? | 1116 | 1142 | – | 0.079 (openrouter) |
| Midjourney · Midjourney V7 | Midjourney | no | Propriétaire (abonnement) | ? | 1 | yes | no | no | ? | ? | ? | ? | – |  |
| Midjourney · Midjourney V8.1 | Midjourney | no | Propriétaire (abonnement) | 2048x2048 (HD par défaut) | ? | yes | no | no | ? | ? | ? | ? | – |  |
| Midjourney · Midjourney V8.2 (défaut) | Midjourney | no | Propriétaire (abonnement) | 2048x2048 (HD natif 2K) | 4 | yes | no | no | ? | ? | ? | ? | – |  |
| Muse · Muse Image | Meta | no | Propriétaire | ? | ? | yes | no | no | ? | ? | 1127 | 1126 | – | 0.010 (fal) |
| Nano Banana (Gemini Image) · Nano Banana (gemini-2.5-flash-image) | Google | no | Propriétaire (Gemini API) | ? | ? | yes | no | no | ? | ? | 984 | 984 | – | 0.020 (kie) |
| Nano Banana (Gemini Image) · Nano Banana 2 (gemini-3.1-flash-image) | Google | no | Propriétaire (Gemini API, Vertex AI) | 4K (0,5K, 1K, 2K, 4K) | 14 | yes | no | no | ? | ? | 1138 | 1121 | – | 0.040 (kie) |
| Nano Banana (Gemini Image) · Nano Banana 2 Lite (gemini-3.1-flash-lite-image) | Google | no | Propriétaire (Gemini API) | 1K | 14 | yes | no | no | ? | ? | 1106 | 1050 | – | 0.020 (kie) |
| Nano Banana (Gemini Image) · Nano Banana 2.1 (gemini-nano-banana-2.1) | Google | no | Propriétaire (Gemini API, Vertex AI) | 4K (1K, 2K, 4K) | 14 | yes | no | no | ? | ? | 1172 | 1150 | – | 0.020 (kie) |
| Nano Banana (Gemini Image) · Nano Banana Pro (gemini-3-pro-image) | Google | no | Propriétaire (Gemini API, Vertex AI) | 4K (1K défaut, 2K, 4K) | 14 | yes | no | no | ? | ? | 1115 | 1109 | – | 0.090 (kie) |
| Qwen-Image 1 · Qwen-Image (20B, révision 2512) | Alibaba (Qwen) | yes | Apache 2.0 (commercial autorisé) | ? | ? | no | yes | yes | yes | yes | 898 | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro | 0.020 (fal) |
| Qwen-Image 2 · Qwen Image 2.0 Pro (2026-04-22) | Alibaba (Qwen) | no | Propriétaire (API) | ? | ? | yes | no | no | ? | ? | 1027 | 1057 | – | 0.070 (wavespeed) |
| Qwen-Image 2 · Qwen-Image-2.1 | Alibaba (Qwen) | yes | Qwen Research License (commercial = accord séparé) | 2048x2048 (exemples ; max non publié) | 10 | yes | yes | yes | ? | yes | 1041 | 1080 | Wan2GP, Pinokio, Draw Things, Maestro | 0.020 (kie) |
| Qwen-Image 3 · Qwen-Image-3.0 | Alibaba (Qwen) | no | Propriétaire (Qwen Chat, Alibaba Cloud) | ? | ? | yes | no | no | ? | ? | 1069 | 1064 | – | 0.024 (kie) |
| Qwen-Image 3 · Qwen-Image-3.0-Pro | Alibaba (Qwen) | no | Propriétaire (Qwen Chat, Alibaba Cloud / Qwen Cloud) | ? | ? | yes | no | no | ? | ? | 1094 | 1087 | – | 0.032 (kie) |
| Qwen-Image-Edit · Qwen Image Edit Max 2601 | Alibaba (Qwen) | no | Propriétaire (API) | ? | ? | yes | no | no | ? | ? | ? | 985 | – |  |
| Qwen-Image-Edit · Qwen-Image-Edit-2511 (Edit Plus) | Alibaba (Qwen) | yes | Apache 2.0 (commercial autorisé) | ? | 3 | yes | yes | yes | ? | yes | ? | 991 | ComfyUI, Pinokio, Draw Things, Maestro, Phosphene | 0.030 (fal) |
| Recraft V4.1 · Recraft V4.1 Flash | Recraft | no | Propriétaire (API) | ? | ? | ? | no | no | ? | ? | 950 | ? | – | 0.007 (fal) |
| Recraft V4.1 · Recraft V4.1 Text-to-Vector / Pro Vector (SVG) | Recraft | no | Propriétaire (API, Cloudflare, OpenRouter) | Vectoriel (SVG, sans limite de pixels) | ? | ? | no | no | ? | ? | ? | ? | – | 0.080 (openrouter) |
| Recraft V4.1 · Recraft V4.1 Utility | Recraft | no | Propriétaire (API, app) | ? | ? | ? | no | no | ? | ? | 1027 | ? | – | 0.035 (fal) |
| Recraft V4.1 · Recraft V4.1 Utility Pro | Recraft | no | Propriétaire (API, app) | Haute résolution (valeur non publiée) | ? | ? | no | no | ? | ? | 1016 | ? | – | 0.210 (fal) |
| Reve · Reve 2.1 | Reve | no | Propriétaire (API api.reve.com, app) | 4K (Reve 2.0, modèle à mise en page) | 8 | yes | no | no | ? | ? | ? | ? | – |  |
| Reve · Reve V1 (décembre) | Reve | no | Propriétaire (API, app) | ? | ? | yes | no | no | ? | ? | ? | 982 | – |  |
| SANA · SANA 1.5 4.8B | NVIDIA (avec MIT, Tsinghua) | yes | Apache 2.0 (étiquette HF ; vérifier la fiche, certaines variantes SANA sont sous NVIDIA Open Model License) | 4096x4096 (famille SANA) | ? | ? | yes | yes | yes | ? | ? | ? | – |  |
| SANA · SANA-Sprint 1.6B | NVIDIA (avec MIT, Tsinghua) | yes | Apache 2.0 selon l'étiquette HF ; un tiers indique NVIDIA Open Model License orientée recherche | 1024x1024 | ? | ? | ? | yes | yes | ? | ? | ? | Pinokio |  |
| Seedream · Seedream 4.0 | ByteDance Seed | no | Propriétaire (BytePlus) | ? | 10 | yes | no | no | ? | ? | ? | ? | – | 0.025 (kie) |
| Seedream · Seedream 4.5 | ByteDance Seed | no | Propriétaire (BytePlus) | 4096x4096 (une fiche dit 3K) | 14 | yes | no | no | ? | ? | 1028 | 1041 | – | 0.033 (kie) |
| Seedream · Seedream 5.0 Lite | ByteDance Seed | no | Propriétaire (BytePlus) | 4K (selon un blog ; non confirmé) | 14 | yes | no | no | ? | ? | 1015 | 1061 | – | 0.028 (kie) |
| Seedream · Seedream 5.0 Pro | ByteDance Seed | no | Propriétaire (BytePlus ModelArk, Volcengine) | 2K (une place de marché annonce 4K) | 10 | yes | no | no | ? | ? | 1096 | 1126 | – | 0.035 (kie) |
| Stable Diffusion · SDXL 1.0 (base) | Stability AI | yes | CreativeML OpenRAIL++-M (commercial autorisé) | 1024x1024 | ? | yes | yes | yes | yes | yes | ? | ? | ComfyUI, Pinokio, Draw Things |  |
| Stable Diffusion · Stable Diffusion 3.5 Large | Stability AI | yes | Stability AI Community License (commercial gratuit sous 1 M$ de CA annuel) | 1 MP | ? | no | yes | yes | yes | yes | ? | ? | Draw Things | 0.065 (replicate) |
| Z-Image · Z-Image (Base) | Alibaba (Tongyi-MAI) | yes | Apache 2.0 (commercial autorisé) | ? | ? | no | yes | yes | yes | yes | 890 | ? | Wan2GP, Pinokio, Draw Things, Maestro | 0.010 (fal) |
| Z-Image · Z-Image Turbo | Alibaba (Tongyi-MAI) | yes | Apache 2.0 (commercial autorisé) | ? | ? | no | yes | yes | yes | yes | 936 | ? | ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro, Phosphene | 0.005 (fal) |
| Z-Image · Z-Image-Edit | Alibaba (Tongyi-MAI) | no | ? | ? | ? | yes | no | ? | ? | ? | ? | ? | – |  |
