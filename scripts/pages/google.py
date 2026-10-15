import os
# Parseur de la page de prix « google » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='google'; G='https://ai.google.dev/gemini-api/docs/pricing'; Vx='https://cloud.google.com/vertex-ai/generative-ai/pricing'
rows=[]
def V(mid,name,ep,raw,url,p480=None,p720=None,p1080=None): rows.append(row(P,name,mid,ep,'video','per_second',raw,url,p480=p480,p720=p720,p1080=p1080))
def I(mid,name,ep,raw,url,p,unit='per_image'): rows.append(row(P,name,mid,ep,'image',unit,raw,url,pimg=p))
V('google-veo-3-1','Veo 3.1','veo-3.1-generate-preview','Vertex AI pricing: video+audio $0.40/s (720p, 1080p), $0.60/s (4k); video only (no audio) $0.20/s (720p, 1080p), $0.40/s (4k) ("count" = second). Gemini API page lists only the with-audio default: $0.40/s (720p and 1080p), $0.60/s (4k). Columns = no audio.',Vx,p720=0.20,p1080=0.20)
V('google-veo-3-1-fast','Veo 3.1 Fast','veo-3.1-fast-generate-preview','Vertex AI: video+audio $0.10 (720p), $0.12 (1080p), $0.30 (4k); video only $0.08 (720p), $0.10 (1080p), $0.25 (4k). Gemini API page (with audio default): $0.10 (720p), $0.12 (1080p), $0.30 (4k). Columns = no audio.',Vx,p720=0.08,p1080=0.10)
V('google-veo-3-1-lite','Veo 3.1 Lite','veo-3.1-lite-generate-preview','Vertex AI: video+audio $0.05 (720p), $0.08 (1080p); video only $0.03 (720p), $0.05 (1080p); 4k not supported. Gemini API (with audio default): $0.05 / $0.08. Columns = no audio.',Vx,p720=0.03,p1080=0.05)
V('google-veo-3','Veo 3','veo-3.0-generate','Vertex AI: video+audio $0.40/s (720p, 1080p); video only $0.20/s. Column = no audio.',Vx,p720=0.20,p1080=0.20)
V('google-veo-3-fast','Veo 3 Fast','veo-3.0-fast-generate','Vertex AI: video+audio $0.10 (720p), $0.12 (1080p); video only $0.08 (720p), $0.10 (1080p). Columns = no audio.',Vx,p720=0.08,p1080=0.10)
V('google-veo-2','Veo 2','veo-2.0-generate','Vertex AI: $0.50 per count (second) at 720p, no audio.',Vx,p720=0.50)
V('google-gemini-omni-1-1-flash','Gemini Omni Flash 1.1','gemini-omni-1.1-flash','Gemini API: output $17.50 per 1M video tokens, 5,792 tokens per second of 720p video = 5792 x 17.5/1e6 = $0.1014/s ("approximately $0.10 per second" per page); input $1.50/M (text/image/video/audio). Video generation and editing model; whether audio is included is not stated.',G,p720=0.10)
I('google-nano-banana-2-1','Nano Banana 2.1 (Gemini Nano Banana 2.1)','gemini-nano-banana-2.1','Gemini API: image output $30/M tokens = $0.0336 per 1K image (1120 tokens), $0.0504 per 2K (1680), $0.113 per 4K (3780); input $1.50/M. Column = 1K. Batch half price.',G,0.0336)
I('google-nano-banana-2','Nano Banana 2 (Gemini 3.1 Flash Image)','gemini-3.1-flash-image','Gemini API: image output $60/M tokens = $0.045 per 0.5K, $0.067 per 1K (1120 tokens), $0.101 per 2K, $0.151 per 4K; input $0.50/M. Column = 1K.',G,0.067)
I('google-nano-banana-2-lite','Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image)','gemini-3.1-flash-lite-image','Gemini API: image output $30/M tokens = ~$0.0336 per 1K image (page also rounds to $0.034 1K, $0.050 2K, $0.076 4K); input $0.25/M. Column = 1K.',G,0.0336)
I('google-gemini-3-pro-image','Nano Banana Pro (Gemini 3 Pro Image)','gemini-3-pro-image','Gemini API: image output $120/M tokens = $0.134 per 1K/2K image, $0.24 per 4K; input $2.00/M (=$0.0011 per input image). Batch: $0.067 1K/2K, $0.12 4K. Column = 1K.',G,0.134)
I('google-nano-banana','Nano Banana (Gemini 2.5 Flash Image)','gemini-2.5-flash-image','Gemini API: $0.039 per image; page warns the model is deprecated and shuts down on 2026-10-02.',G,0.039)
I('google-imagen-4','Imagen 4','imagen-4.0-generate','Vertex AI: image generation $0.04 per image (count). Imagen is not listed on the Gemini API pricing page.',Vx,0.04)
I('google-imagen-4-fast','Imagen 4 Fast','imagen-4.0-fast-generate','Vertex AI: $0.02 per image.',Vx,0.02)
I('google-imagen-4-ultra','Imagen 4 Ultra','imagen-4.0-ultra-generate','Vertex AI: $0.06 per image (upscaling to 2K-4K $0.06).',Vx,0.06)
I('google-imagen-3','Imagen 3','imagen-3.0-generate','Vertex AI: $0.04 per image.',Vx,0.04)
save(P,[G,Vx],['Veo duration unit on Vertex is "count": interpreted as per second (Veo is billed per second on the Gemini API page, same figures)','Gemini Omni Flash Preview (gemini-omni-flash-preview): same token pricing as 1.1, no separate row'],
 'Gemini API page lists Veo 3.1 only with the audio price ($0.40/$0.10/$0.05 default); Vertex AI page gives both audio and no-audio, used for the columns. Replicate/WaveSpeed list Veo 3.1 Fast with audio at $0.15, but Google lists $0.10 (720p) / $0.12 (1080p) with audio: third-party figures are higher than Google for Fast. Image prices on the Gemini API are token-derived ($ per 1M image tokens x tokens per image, page gives per-image equivalents). Gemini Omni video priced per token, converted using the page 5,792 tokens/s.',rows)
