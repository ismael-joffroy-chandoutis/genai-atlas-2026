import os
# Parseur de la page de prix « openai » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='openai'; Pr='https://developers.openai.com/api/docs/pricing'; G='https://developers.openai.com/api/docs/guides/image-generation'
rows=[]
def I(mid,name,ep,raw,url,p,unit='per_image'): rows.append(row(P,name,mid,ep,'image',unit,raw,url,pimg=p))
I('openai-gpt-image-2','GPT Image 2','gpt-image-2','Guide table, output-image cost at 1024x1024: low $0.006, medium $0.053, high $0.211 (1024x1536 / 1536x1024: low $0.005, medium $0.041, high $0.165). Excludes text/image input tokens. Pricing page lists gpt-image-2 only under Batch: image tokens $4.00 in / $15.00 out per M, text $2.50 (standard = 2x batch). Column = 1024x1024 medium.',G,0.053)
for mid,nm,ep in [('openai-gpt-image-2-5-sunburst','GPT Image 2.5 Sunburst','gpt-image-2.5-sunburst'),('openai-gpt-image-2-5-flare','GPT Image 2.5 Flare','gpt-image-2.5-flare')]:
    I(mid,nm,ep,'Pricing page (per 1M tokens, standard): image input $8.00, cached image input $2.00, image output $30.00, text input $5.00, cached text $1.25. Batch: $4/$1/$15, text $2.50. Quality options low/medium/high/xhigh/max; per-image cost depends on output token count from an interactive calculator not available in static text (example on guide: 196 output tokens = $0.00588). No per-image price extracted, so column null.',Pr,None,'per_token')
I('openai-gpt-image-1-5','GPT Image 1.5','gpt-image-1.5','Guide legacy table at 1024x1024: low $0.009, medium $0.034, high $0.133 (1024x1536 / 1536x1024: $0.013 / $0.05 / $0.20). Column = 1024x1024 medium.',G,0.034)
I('openai-gpt-image-1','GPT Image 1','gpt-image-1','Guide legacy table at 1024x1024: low $0.011, medium $0.042, high $0.167 (portrait/landscape $0.016 / $0.063 / $0.25). Column = medium.',G,0.042)
I('openai-gpt-image-1-mini','GPT Image 1 Mini','gpt-image-1-mini','Guide legacy table at 1024x1024: low $0.005, medium $0.011, high $0.036. Column = medium.',G,0.011)
S='https://developers.openai.com/api/docs/models/sora-2'
rows.append(row(P,'Sora 2','openai-sora-2','sora-2','video','per_second','Model page: "Video generation per second: $0.10" (Portrait 720x1280 / Landscape 1280x720). The same page states "The Sora 2 models and Videos API were shut down on September 24, 2026 and are no longer available" (status Deprecated). Price shown for reference only.',S,p720=0.10))
rows.append(row(P,'Sora 2 Pro','openai-sora-2-pro','sora-2-pro','video','per_second','Model page: per second $0.30 (720x1280 / 1280x720), $0.50 (1024x1792 / 1792x1024), $0.70 (larger, 1080p-class). Page states Sora 2 models and Videos API shut down on 2026-09-24 (Deprecated). Reference only.',S+'-pro',p720=0.30,p1080=0.70))
save(P,[Pr,G,S,S+'-pro'],['https://platform.openai.com/docs/pricing : redirect/SPA, developers.openai.com used instead','No page lists GPT Image 2.5 per-image prices (token calculator is interactive)'],
 'OpenAI image prices are token-based; per-image figures taken from the image-generation guide tables (gpt-image-2, 1.5, 1, mini at 1024x1024). GPT Image 2.5 (Sunburst/Flare) only have token rates in static text: rows have unit per_token and null per-image column; third parties (Replicate: medium $0.047, WaveSpeed medium 1k $0.024) disagree with each other and cannot be checked against OpenAI. Sora 2 / 2 Pro are SHUT DOWN since 2026-09-24 per the OpenAI model pages. WaveSpeed GPT Image 2 medium 1k $0.06 vs OpenAI medium $0.053.',rows)
