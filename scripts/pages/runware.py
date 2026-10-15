import os
# Parseur de la page de prix « runware » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys,json
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='runware'; U='https://runware.ai/pricing'
M=json.load(open(os.path.join(os.environ.get('ATLAS_PAGES','cache'),'apipages/rw_models.json')))
rows=[]
def R(key):
    v=M[key]; return v, '; '.join(f"{x.get('label') or 'default'}: ${x['amount']:.6g}/{x['unit']}" for x in v['rates'])
def lab(key,l):
    for x in M[key]['rates']:
        if (x.get('label') or '')==l: return x['amount']
    raise KeyError((key,l))
def V(mid,key,cols,note='',name=None):
    v,t=R(key); kw={}
    for c,l in cols.items(): kw[c]=lab(key,l)
    rows.append(row(P,name or v['name'],mid,v['air'] or key,'video','per_second',f'Runware pricing table (pricingRates): {t}. '+note,U,**kw))
def I(mid,key,l,note='',div=None,name=None,unit='per_image'):
    v,t=R(key)
    p=lab(key,l) if l is not None else None
    rows.append(row(P,name or v['name'],mid,v['air'] or key,'image',unit,f'Runware pricing table (pricingRates): {t}. '+note,U,pimg=p))
V('bytedance-seedance-2-0','bytedance-seedance-2-0',{'p480':'480p','p720':'720p','p1080':'1080p'},'Columns = text/image to video; 4K 0.8559; video-to-video higher.')
V('bytedance-seedance-2-0-fast','bytedance-seedance-2-0-fast',{'p480':'480p','p720':'720p'},'')
V('bytedance-seedance-2-0-mini','bytedance-seedance-2-0-mini',{'p480':'480p · text/image to video','p720':'720p · text/image to video'},'Columns = text/image to video.')
V('bytedance-seedance-2-5','bytedance-seedance-2-5',{'p480':'Text/Image to Video · 480p','p720':'Text/Image to Video · 720p','p1080':'Text/Image to Video · 1080p'},'Columns = text/image to video.')
V('bytedance-seedance-1-0-pro','bytedance-seedance-1-0-pro',{'p480':'480p','p1080':'1080p'},'720p tier not shown in extracted list.')
V('alibaba-wan-3-0','alibaba-wan3-0',{'p480':'480p','p720':'720p','p1080':'1080p'})
V('alibaba-wan-3-0-prime','alibaba-wan3-0-prime',{'p480':'480p','p720':'720p','p1080':'1080p'})
V('alibaba-wan-2-7','alibaba-wan2-7',{'p720':'720p','p1080':'1080p'}); V('alibaba-wan-2-6','alibaba-wan2-6',{'p720':'720p','p1080':'1080p'})
V('alibaba-wan-2-6-flash','alibaba-wan2-6-flash',{'p720':'720p · no audio','p1080':'1080p · no audio'},'Columns = no audio; audio doubles.')
V('alibaba-wan-2-5-preview','alibaba-wan2-5-preview',{'p720':'720p','p1080':'1080p'})
V('alibaba-happyhorse-1-0','alibaba-happyhorse-1-0',{'p720':'720p','p1080':'1080p'}); V('alibaba-happyhorse-1-1','alibaba-happyhorse-1-1',{'p720':'720p','p1080':'1080p'})
V('kling-3-0-std','klingai-video-3-0-standard',{'p720':'720p · no audio'},'Column = no audio; with audio $0.126/s.')
V('kling-3-0-pro','klingai-video-3-0-pro',{'p1080':'1080p · no audio'},'Column = no audio; with audio $0.168/s.')
V('kling-3-0-omni-std','klingai-video-3-0-omni-standard',{'p720':'720p · no input + no audio'},'Column = no input, no audio.')
V('kling-3-0-omni-pro','klingai-video-3-0-omni-pro',{'p1080':'1080p · no video input + no audio'},'Column = no video input, no audio; audio $0.14/s.')
V('kling-3-0-turbo','klingai-video-3-0-turbo',{'p720':'720p','p1080':'1080p'})
V('kling-3-0-4k','klingai-video-3-0-4k',{},'4K only, $0.42/s.')
V('kling-o1-std','klingai-video-o1-standard',{'p720':'720p · T2V'}); V('kling-o1-pro','klingai-video-o1-pro',{'p1080':'1080p · T2V'})
V('kling-2-6-pro','klingai-video-2-6-pro',{},'Column left null: resolution tier not stated; no audio $0.07/s, with audio $0.14/s.')
V('kling-2-5-turbo-standard','klingai-2-5-turbo-standard',{},'Single price, resolution not stated.'); V('kling-2-5-turbo-pro','klingai-2-5-turbo-pro',{},'Single price, resolution not stated.')
V('google-veo-3-1','google-veo-3-1',{'p720':'720p / 1080p · without audio','p1080':'720p / 1080p · without audio'},'Columns = without audio (same 720p/1080p price); with audio $0.40/s.')
V('google-veo-3-1-fast','google-veo-3-1-fast',{'p720':'720p / 1080p','p1080':'720p / 1080p'},'Columns = without audio (the unlabeled rate); with audio $0.15/s.')
V('google-veo-3-1-lite','google-veo-3-1-lite',{'p720':'720p · without audio','p1080':'1080p · without audio'},'Columns = without audio.')
V('minimax-h3','minimax-h3',{'p720':'768p'},'768p put in 720p column; 2K $0.13/s.')
V('minimax-h3-max','minimax-h3-max',{'p480':'480p','p720':'768p'},'768p in 720p column.')
V('minimax-h3-max-turbo','minimax-h3-max-turbo',{'p480':'480p','p720':'768p'},'768p in 720p column.')
V('minimax-h3-fast','minimax-h3-fast',{},'$0.046/s, resolution not stated.')
V('minimax-hailuo-2-3-fast','minimax-hailuo-2-3-fast',{'p720':'768p','p1080':'1080p'},'768p in 720p column.')
V('minimax-hailuo-02','minimax-hailuo-02',{'p720':'768p','p1080':'1080p'},'768p in 720p column.')
V('ltx-2-5-fast','lightricks-ltx-2-5-fast',{'p720':'720p','p1080':'1080p'}); V('ltx-2-5-pro','lightricks-ltx-2-5-pro',{'p720':'720p','p1080':'1080p'})
V('ltx-2-3','lightricks-ltx-2-3',{'p720':'720p','p1080':'1080p'}); V('ltx-2-3-fast','lightricks-ltx-2-3-fast',{'p720':'720p','p1080':'1080p'}); V('ltx-2','lightricks-ltx-2',{},'$0.03/s, resolution not stated.')
V('bfl-flux-3-video','bfl-flux-3-video',{'p720':'T2V & I2V. 720p','p1080':'T2V & I2V · 1080p'},'Draft 720p $0.04/s.')
V('xai-grok-imagine-video-1-5','xai-grok-imagine-video-1-5',{'p480':'480p','p720':'720p','p1080':'1080p'}); V('xai-grok-imagine-video-1-5-lite','xai-grok-imagine-video-1-5-lite',{'p480':'480p','p720':'720p','p1080':'1080p'})
v,t=R('xai-grok-imagine-video')
rows.append(row(P,v['name'],'xai-grok-imagine-video',v['air'] or 'xai-grok-imagine-video','video','per_second','Runware pricing table: '+t+'. Priced per output up to 6 s: 480p T2V $0.30 (=0.30/6=$0.05/s, consistent with $0.05/s beyond 6 s), 720p T2V $0.42 (=$0.07/s).',U,p480=0.05,p720=0.07))
V('luma-ray-3-2','luma-ray3-2',{'p720':'Text/image to video · 720p','p1080':'Text/image to video · 1080p'},'540p $0.03/s, 360p $0.012/s; HDR doubles.')
V('runway-gen-4-5','runway-gen-4-5',{},'$0.12/s, resolution not stated.'); V('runway-gen-4-turbo','runway-gen-4-turbo',{},'$0.05/s.'); V('runway-aleph-2-0','runway-aleph-2-0',{},'$0.28/s (video editing).')
V('vidu-q3','vidu-q3',{'p720':'720p','p1080':'1080p'},'540p $0.02925, 360p $0.0325.'); V('vidu-q3-turbo','vidu-q3-turbo',{'p720':'720p','p1080':'1080p'})
V('pixverse-v6','pixverse-v6',{'p720':'720p without audio','p1080':'1080p without audio'},'Columns = without audio.')
V('pixverse-v5-6','pixverse-v5-6',{'p720':'720p · no audio','p1080':'1080p · no audio'},'Columns = no audio.')
V('skywork-skyreels-v4','skywork-skyreels-v4',{'p480':'Text/image to video · 480p','p720':'Text/image to video · 720p','p1080':'Text/image to video · 1080p'})
V('prunaai-p-video-2','prunaai-p-video-2',{'p720':'720p · Standard','p1080':'1080p · Standard'},'Columns = Standard.')
# images
I('bfl-flux-3-image','bfl-flux-3-image','1K','Column = 1K.')
for mid,key,first,add in [('bfl-flux-2-pro','bfl-flux-2-pro',0.03,0.015),('bfl-flux-2-max','bfl-flux-2-max',0.07,0.03)]:
    v,t=R(key); rows.append(row(P,v['name'],mid,v['air'] or key,'image','per_image',f'Runware pricing table: {t}. Column = first megapixel out ({first}); extra output MP {add}; input MP {add}.',U,pimg=first))
v,t=R('bfl-flux-2-flex'); rows.append(row(P,v['name'],'bfl-flux-2-flex',v['air'] or 'bfl-flux-2-flex','image','per_image',f'Runware pricing table: {t}. $0.06 per output megapixel; 1MP = $0.06.',U,pimg=0.06))
I('bfl-flux-1-kontext-pro','bfl-flux-1-kontext-pro',None,''); rows[-1]['price_usd_per_image']=0.04
I('bfl-flux-1-kontext-max','bfl-flux-1-kontext-max',None,''); rows[-1]['price_usd_per_image']=0.08
I('bfl-flux-1-1-pro','bfl-flux-1-1-pro',None,''); rows[-1]['price_usd_per_image']=0.04
I('bfl-flux-1-1-pro-ultra','bfl-flux-1-1-pro-ultra',None,''); rows[-1]['price_usd_per_image']=0.06
I('google-gemini-3-pro-image','google-nano-banana-pro','1K','Column = 1K/2K; 4K $0.244.',name='Nano Banana Pro (Gemini 3 Pro Image)')
I('google-nano-banana-2','google-nano-banana-2','1K','Column = 1K; 512 $0.04657, 2K $0.10255, 4K $0.15295.')
I('google-nano-banana-2-lite','google-nano-banana-2-lite','Example: 1K image output','Token-priced; page example for a 1K image output = $0.033603 (used as per-image value, example not guarantee).')
I('google-nano-banana-2-1','google-nano-banana-2-1',None,'Token-priced only (input $1.5/M, text out $7.5/M, image out $30/M); no per-image price.',unit='per_token')
for mid,key in [('openai-gpt-image-2','openai-gpt-image-2'),('openai-gpt-image-2-5-flare','openai-gpt-image-2-5-flare'),('openai-gpt-image-2-5-sunburst','openai-gpt-image-2-5-sunburst')]:
    I(mid,key,None,'Token-priced (text in $5/M, image in $8/M, image out $30/M); no per-image price on page.',unit='per_token')
v,t=R('bytedance-seedream-5-0-pro'); rows.append(row(P,v['name'],'bytedance-seedream-5-0-pro',v['air'] or 'bytedance-seedream-5-0-pro','image','per_image','Runware pricing table: '+t+'. No 1K tier listed (1.5K $0.04815, 2K $0.0963); column left null.',U))
for mid,key,l in [('bytedance-seedream-5-0-lite','bytedance-seedream-5-0-lite',None),('bytedance-seedream-5-0-flash','bytedance-seedream-5-0-flash',None),('bytedance-seedream-4-5','bytedance-seedream-4-5',None),('bytedance-seedream-4','bytedance-seedream-4-0',None),
  ('alibaba-qwen-image-3','alibaba-qwen-image-3-0',None),('alibaba-qwen-image-3-pro','alibaba-qwen-image-3-0-pro','1K output image'),('alibaba-qwen-image-2-1-pro','alibaba-qwen-image-2-1-pro',None),('alibaba-qwen-image-2-1-turbo','alibaba-qwen-image-2-1-turbo',None),('alibaba-qwen-image-2','alibaba-qwen-image-2-0',None),('alibaba-qwen-image-2-pro','alibaba-qwen-image-2-0-pro',None),
  ('alibaba-wan-2-7-image','alibaba-wan2-7-image',None),('alibaba-wan-2-7-image-pro','alibaba-wan2-7-image-pro',None),('xai-grok-imagine-image','xai-grok-imagine-image',None),('xai-grok-imagine-image-2','xai-grok-imagine-image-2-0','quality medium · 1K'),
  ('ideogram-4-5','ideogram-4-5','Medium'),('ideogram-4-0','ideogram-4-0','Default'),('ideogram-3-0','ideogram-3-0','Default'),('recraft-v4','recraft-v4',None),('recraft-v4-pro','recraft-v4-pro',None),('recraft-v4-1','recraft-v4-1',None),('recraft-v4-1-pro','recraft-v4-1-pro',None),('recraft-v4-1-flash','recraft-v4-1-flash',None),
  ('krea-2-large','krea-2-large','1024x1024'),('krea-2-medium','krea-2-medium','1024x1024'),('runway-gen-4-image','runway-gen-4-image','1024x1024 · 1K'),('runway-gen-4-image-turbo','runway-gen-4-image-turbo',None),('meta-muse-image','meta-muse-image',None)]:
    I(mid,key,l,'' if l is None else f'Column = "{l}".')
    if l is None: rows[-1]['price_usd_per_image']=M[key]['rates'][0]['amount']
save(P,[U,'https://runware.ai/pricing?page=1..8 (396 priced models, server-rendered; tiers read from the embedded pricingRates data)'],['Models without published tiers or non-standard structure (e.g. FLUX.2 [klein]/[dev], open-source image models, about 94 of 396 rows) not parsed','Kling 4.0, Gemini Omni video, Sora, Veo 3 (non 3.1) not found among the parsed Runware rates','Seedance/Kling pages per model do not show tiers in text; data taken from the embedded JSON'],
 'Prices from the Runware published rate sheet (runware.ai/pricing, pages 1-8). Runware is among the cheapest: e.g. Veo 3.1 $0.20/s no audio, Kling 3.0 std $0.084/s, H3 Max Turbo $0.025/$0.04 per s. Rates may include "Save ~N%" sale tiers (not separately visible in the extracted data). Token-priced image models (GPT Image 2/2.5, Nano Banana 2.1) are unit per_token with no per-image price. Resolution labels 768p are mapped to the 720p column and flagged in raw.',rows)
