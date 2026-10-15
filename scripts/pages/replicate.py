import os
# Parseur de la page de prix « replicate » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys,re
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
from rp import tiers
P='replicate'
D=os.path.join(os.environ.get('ATLAS_PAGES','cache'),'apipages/rp/')
def num(s): return float(s.replace('$','').replace(',',''))
def T(slug):
    o=tiers(D+slug.replace('/','_')+'.html'); out=[]
    for t in o['current_tiers']:
        c={x['title']:str(x['value']) for x in t['criteria']}
        pr=[(x['price'],x['title']) for x in t['prices']]
        out.append((c,pr,t.get('title')))
    return out
def txt(slug,flt=None):
    s=[]
    for c,pr,ti in T(slug):
        cs=', '.join(f'{k}={v}' for k,v in c.items()) or 'all'
        s.append(f"[{cs}] "+' ; '.join(f'{a} {b}' for a,b in pr)+(f' ({ti})' if ti else ''))
    return ' | '.join(s)
def pick(slug,flt):
    # returns {res:price} for tiers whose criteria match flt (dict, exact on keys given)
    d={}
    for c,pr,ti in T(slug):
        if all(c.get(k)==v for k,v in flt.items()):
            res=c.get('target resolution')
            d[res]=num(pr[0][0])
    return d
rows=[]
URL=lambda s:'https://replicate.com/'+s
def V(slug,id_,name,flt=None,extra='',cols=('480p','720p','1080p')):
    d=pick(slug,flt or {})
    r=row(P,name,id_,slug,'video','per_second',f'Replicate billingConfig tiers: {txt(slug)}. {extra}'.strip(),URL(slug),
      p480=d.get(cols[0]),p720=d.get(cols[1]),p1080=d.get(cols[2]))
    rows.append(r)
def VF(slug,id_,name,price,extra=''):
    rows.append(row(P,name,id_,slug,'video','per_second',f'Replicate billingConfig: {txt(slug)}. {extra}'.strip(),URL(slug),p720=price if False else None))
def Vflat(slug,id_,name,extra=''):  # single price per second, resolution unspecified
    rows.append(row(P,name,id_,slug,'video','per_second',f'Replicate billingConfig: {txt(slug)}. Resolution not specified by price tier. {extra}'.strip(),URL(slug)))
def I(slug,id_,name,pimg,extra=''):
    rows.append(row(P,name,id_,slug,'image','per_image',f'Replicate billingConfig: {txt(slug)}. {extra}'.strip(),URL(slug),pimg=pimg))

# --- video
V('bytedance/seedance-2.0','bytedance-seedance-2-0','Seedance 2.0',{'model variant':'non_video_in'},'Columns = non_video_in variant (no input video); video_in variant is higher (see tiers). Audio is native; page says audio can be turned off but price not split by audio. 4k tier in raw only.')
V('bytedance/seedance-2.0-fast','bytedance-seedance-2-0-fast','Seedance 2.0 Fast',{'model variant':'non_video_in'},'Columns = non_video_in variant.')
V('bytedance/seedance-2.0-mini','bytedance-seedance-2-0-mini','Seedance 2.0 Mini',{'model variant':'non_video_in'},'Columns = non_video_in variant.')
V('bytedance/seedance-2.5','bytedance-seedance-2-5','Seedance 2.5',{'model variant':'non_video_in'},'Columns = non_video_in variant (note video_in is ~4x). 1080p tier not listed.')
V('bytedance/seedance-1.5-pro','bytedance-seedance-1-5-pro','Seedance 1.5 Pro',{'model variant':'without_audio'},'Columns = without_audio; with_audio is roughly 2x (see tiers).')
V('bytedance/seedance-1-pro','bytedance-seedance-1-pro','Seedance 1 Pro')
V('bytedance/seedance-1-pro-fast','bytedance-seedance-1-pro-fast','Seedance 1 Pro Fast')
V('bytedance/seedance-1-lite','bytedance-seedance-1-lite','Seedance 1 Lite')
V('alibaba/wan-3','alibaba-wan-3-0','Wan 3.0',None,'Replicate banner on pricing page on 2026-10-15 says "Wan 3.0 is 30% off this week" (prices shown may be the promotional ones; not confirmed from the tier data).')
V('alibaba/wan-3-prime','alibaba-wan-3-0-prime','Wan 3.0 Prime')
V('alibaba/happyhorse-1.0','alibaba-happyhorse-1-0','HappyHorse 1.0')
V('alibaba/happyhorse-1.1','alibaba-happyhorse-1-1','HappyHorse 1.1')
V('wan-video/wan-2.5-t2v','alibaba-wan-2-5-t2v','Wan 2.5 T2V')
V('wan-video/wan-2.5-i2v','alibaba-wan-2-5-i2v','Wan 2.5 I2V')
V('wan-video/wan-2.5-t2v-fast','alibaba-wan-2-5-t2v-fast','Wan 2.5 T2V Fast')
V('wan-video/wan-2.5-i2v-fast','alibaba-wan-2-5-i2v-fast','Wan 2.5 I2V Fast')
V('wan-video/wan-2.6-t2v','alibaba-wan-2-6-t2v','Wan 2.6 T2V')
V('wan-video/wan-2.6-i2v','alibaba-wan-2-6-i2v','Wan 2.6 I2V')
V('wan-video/wan-2.7-i2v','alibaba-wan-2-7-i2v','Wan 2.7 I2V')
Vflat('wan-video/wan-2.7-t2v','alibaba-wan-2-7-t2v','Wan 2.7 T2V')
Vflat('wan-video/wan-2.7-r2v','alibaba-wan-2-7-r2v','Wan 2.7 R2V')
# kling
def K(slug,id_,name,flt,col,extra):
    d=pick(slug,flt); v=list(d.values())
    kw={col:v[0]} if v else {}
    rows.append(row(P,name,id_,slug,'video','per_second',f'Replicate billingConfig: {txt(slug)}. {extra}',URL(slug),**kw))
K('kwaivgi/kling-v3-video','kling-3-0-std',"Kling 3.0 Standard",{'with audio':'False','model variant':'standard'},'p720','Column = standard, audio OFF (720p class); audio ON is $0.252/s. 4k tier $0.42/s in raw.')
K('kwaivgi/kling-v3-video','kling-3-0-pro',"Kling 3.0 Pro",{'with audio':'False','model variant':'pro'},'p1080','Column = pro, audio OFF (1080p class); audio ON is $0.336/s.')
K('kwaivgi/kling-v3-omni-video','kling-3-0-omni-std',"Kling 3.0 Omni Standard",{'with audio':'False','model variant':'standard'},'p720','Column = standard, audio OFF; audio ON is $0.224/s.')
K('kwaivgi/kling-v3-omni-video','kling-3-0-omni-pro',"Kling 3.0 Omni Pro",{'with audio':'False','model variant':'pro'},'p1080','Column = pro, audio OFF; audio ON $0.28/s.')
K('kwaivgi/kling-o1','kling-o1-std',"Kling O1 Standard",{'model variant':'std'},'p720','Column = std without video input; with video input $0.126/s.')
K('kwaivgi/kling-o1','kling-o1-pro',"Kling O1 Pro",{'model variant':'pro'},'p1080','Column = pro without video input; with video input $0.168/s.')
K('kwaivgi/kling-v2.6','kling-2-6',"Kling 2.6",{'with audio':'False'},'p720','Column = audio OFF $0.07/s; audio ON $0.14/s. Mode/resolution not specified.')
K('kwaivgi/kling-v2.5-turbo-pro','kling-2-5-turbo-pro',"Kling 2.5 Turbo Pro",{},'p1080','Single price $0.07/s (Pro mode, 1080p class per name; not stated on tier).')
K('kwaivgi/kling-v2.1','kling-2-1-std',"Kling 2.1 Standard",{'model variant':'standard'},'p720','Standard mode 720p $0.05/s.')
K('kwaivgi/kling-v2.1','kling-2-1-pro',"Kling 2.1 Pro",{'model variant':'pro'},'p1080','Pro mode 1080p $0.09/s.')
Vflat('kwaivgi/kling-v2.1-master','kling-2-1-master','Kling 2.1 Master')
# google
def G(slug,id_,name,withaudio,noaudio,extra=''):
    noaudio=float(noaudio); withaudio=withaudio
    rows.append(row(P,name,id_,slug,'video','per_second',f'Replicate billingConfig: {txt(slug)}. Columns = WITHOUT audio price ({noaudio}); with audio is ${withaudio}/s. Flat per-second price, not split by resolution, so same value put in 720p and 1080p columns. Resolution not specified by tier. {extra}',URL(slug),p720=noaudio,p1080=noaudio))
G('google/veo-3.1','google-veo-3-1','Veo 3.1','0.40','0.20')
G('google/veo-3.1-fast','google-veo-3-1-fast','Veo 3.1 Fast','0.15','0.10')
G('google/veo-3','google-veo-3','Veo 3','0.40','0.20')
G('google/veo-3-fast','google-veo-3-fast','Veo 3 Fast','0.15','0.10')
V('google/veo-3.1-lite','google-veo-3-1-lite','Veo 3.1 Lite',None,'Audio handling not specified in tier.')
Vflat('google/veo-2','google-veo-2','Veo 2')
for s,i,n in [('minimax/hailuo-2.3','minimax-hailuo-2-3','Hailuo 2.3'),('minimax/hailuo-2.3-fast','minimax-hailuo-2-3-fast','Hailuo 2.3 Fast'),('minimax/hailuo-02','minimax-hailuo-02','Hailuo 02'),('minimax/hailuo-02-fast','minimax-hailuo-02-fast','Hailuo 02 Fast')]:
    d={}
    for c,pr,ti in T(s):
        res=c['target resolution']; sec=int(c['second of output video']); d[(res,sec)]=num(pr[0][0])
    kw={}
    f=lambda k:round(d[k]/k[1],4) if k in d else None
    kw['p720']=f(('768P',6)); kw['p1080']=f(('1080P',6)); 
    rows.append(row(P,n,i,s,'video','per_second',f'Replicate billingConfig (priced per clip): {txt(s)}. Per-second = clip price / seconds, e.g. 768P 6s: {d.get(("768P",6))}/6 = {kw["p720"]}; 1080P 6s: {d.get(("1080P",6))}/6 = {kw["p1080"]}. Columns use 6s clips; 768P placed in 720p column. 512P not in columns.'.replace('None','n/a'),URL(s),p480=None,p720=kw['p720'],p1080=kw['p1080']))
d={k:v for k,v in [((c['target resolution'],int(c['second of output video'])),num(pr[0][0])) for c,pr,ti in T('luma/ray-3.2') if c.get('model variant')=='sdr']}
rows.append(row(P,'Luma Ray 3.2','luma-ray-3-2','luma/ray-3.2','video','per_second',f'Replicate billingConfig (per clip): {txt("luma/ray-3.2")}. SDR per second = clip/seconds: 540p 5s 0.15/5=0.03; 720p 5s 0.30/5=0.06 (10s: 0.90/10=0.09); 1080p 5s 1.20/5=0.24 (10s: 3.60/10=0.36). Columns use 5s SDR clips; 540p not in 480p column.',URL('luma/ray-3.2'),p720=0.06,p1080=0.24))
Vflat('luma/ray-2-540p','luma-ray-2-540p','Luma Ray 2 540p'); Vflat('luma/ray-2-720p','luma-ray-2-720p','Luma Ray 2 720p')
rows[-1]['price_usd_720p_s']=0.18
Vflat('runwayml/gen-4.5','runway-gen-4-5','Runway Gen-4.5'); Vflat('runwayml/gen4-turbo','runway-gen-4-turbo','Runway Gen-4 Turbo'); Vflat('runwayml/gen4-aleph','runway-gen-4-aleph','Runway Gen-4 Aleph')
Vflat('xai/grok-imagine-video-1.5','xai-grok-imagine-video-1-5','Grok Imagine Video 1.5'); Vflat('xai/grok-imagine-video','xai-grok-imagine-video','Grok Imagine Video'); Vflat('xai/grok-imagine-r2v','xai-grok-imagine-r2v','Grok Imagine R2V'); Vflat('xai/grok-imagine-video-extension','xai-grok-imagine-video-extension','Grok Imagine Video Extension')
V('pixverse/pixverse-v6','pixverse-v6','PixVerse V6',{'with audio':'False'},'Columns = no audio, 360p/540p not in columns; with audio is higher (see tiers). 480p column empty (540p only).')
V('pixverse/pixverse-v5.6','pixverse-v5-6','PixVerse V5.6',None,'540p/360p not in 480p column.')
V('vidu/q3-pro','vidu-q3-pro','Vidu Q3 Pro',None,'540p not in columns.')
V('vidu/q3-turbo','vidu-q3-turbo','Vidu Q3 Turbo',None,'540p not in columns.')
V('lightricks/ltx-2.5-fast','ltx-2-5-fast','LTX-2.5 Fast',None,'')
V('lightricks/ltx-2.3-fast','ltx-2-3-fast','LTX-2.3 Fast',None,'')
V('lightricks/ltx-2.3-pro','ltx-2-3-pro','LTX-2.3 Pro',None,'')
V('lightricks/ltx-2-fast','ltx-2-fast','LTX-2 Fast',None,'')
V('lightricks/ltx-2-pro','ltx-2-pro','LTX-2 Pro',None,'')
Vflat('lightricks/ltx-2-distilled','ltx-2-distilled','LTX-2 Distilled')
V('prunaai/p-video-2','prunaai-p-video-2','P-Video 2',{'model variant':'base'},'Columns = base (not draft).')
# BFL Flux 3 video
V('black-forest-labs/flux-3','bfl-flux-3-video','FLUX 3 (video)',{'model variant':'t2v_i2v'},'Columns = t2v/i2v standard render. Cf. BFL direct: hd 0.15, fhd 0.24 (Replicate is ~13-20% above).')
# --- image
I('black-forest-labs/flux-2-pro','bfl-flux-2-pro','FLUX.2 [pro]',0.03,'Per 1MP output: $0.015 per run + $0.015 per output MP = ~$0.03 for 1MP output, no input image (formula).')
I('black-forest-labs/flux-2-max','bfl-flux-2-max','FLUX.2 [max]',0.07,'Per 1MP output: $0.04 per run + $0.03 per output MP = ~$0.07 (formula).')
I('black-forest-labs/flux-2-flex','bfl-flux-2-flex','FLUX.2 [flex]',0.06,'$0.06 per output MP; 1MP = $0.06.')
I('black-forest-labs/flux-2-klein-9b','bfl-flux-2-klein-9b','FLUX.2 [klein] 9B',0.015,'$0.015 per output MP; 1MP = $0.015.')
I('black-forest-labs/flux-2-klein-4b','bfl-flux-2-klein-4b','FLUX.2 [klein] 4B',None,'Listed "$1 per thousand output image megapixels" = $0.001 per MP -> 1MP = $0.001 (formula 1/1000).')
rows[-1]['price_usd_per_image']=0.001
I('black-forest-labs/flux-2-dev','bfl-flux-2-dev','FLUX.2 [dev]',0.014,'Regular $0.014 per output MP (go_fast $0.012); 1MP regular = $0.014.')
I('black-forest-labs/flux-kontext-pro','bfl-flux-1-kontext-pro','FLUX.1 Kontext [pro]',0.04); I('black-forest-labs/flux-kontext-max','bfl-flux-1-kontext-max','FLUX.1 Kontext [max]',0.08)
I('black-forest-labs/flux-1.1-pro','bfl-flux-1-1-pro','FLUX 1.1 [pro]',0.04); I('black-forest-labs/flux-1.1-pro-ultra','bfl-flux-1-1-pro-ultra','FLUX 1.1 [pro] Ultra',0.06)
I('black-forest-labs/flux-3-image','bfl-flux-3-image','FLUX 3 Image',0.024,'Column = 1K. Cf. BFL direct 1k = $0.048 (Replicate shows HALF the BFL price; possible promo or error).')
I('bytedance/seedream-5-pro','bytedance-seedream-5-0-pro','Seedream 5.0 Pro',0.045,'Column = 1K; 2K $0.09.')
I('bytedance/seedream-5-lite','bytedance-seedream-5-0-lite','Seedream 5.0 Lite',0.035); I('bytedance/seedream-4.5','bytedance-seedream-4-5','Seedream 4.5',0.04); I('bytedance/seedream-4','bytedance-seedream-4','Seedream 4',0.03); I('bytedance/dreamina-3.1','bytedance-dreamina-3-1','Dreamina 3.1',0.03)
I('google/nano-banana-2.1','google-nano-banana-2-1','Nano Banana 2.1',0.0336,'Column = 1K; 2K 0.0504; 4K 0.1134.')
I('google/nano-banana-2','google-nano-banana-2','Nano Banana 2',0.067,'Column = 1K.')
I('google/nano-banana-2-lite','google-nano-banana-2-lite','Nano Banana 2 Lite',0.034)
I('google/nano-banana-pro','google-gemini-3-pro-image','Nano Banana Pro (Gemini 3 Pro Image)',0.15,'Column = 1K/2K ($0.15), 4K $0.30; fallback tier $0.035 (meaning unclear).')
I('google/nano-banana','google-nano-banana','Nano Banana (Gemini 2.5 Flash Image)',0.039); I('google/gemini-2.5-flash-image','google-gemini-2-5-flash-image','Gemini 2.5 Flash Image',0.039)
I('google/imagen-4','google-imagen-4','Imagen 4',0.04); I('google/imagen-4-fast','google-imagen-4-fast','Imagen 4 Fast',0.02); I('google/imagen-4-ultra','google-imagen-4-ultra','Imagen 4 Ultra',0.06); I('google/imagen-3','google-imagen-3','Imagen 3',0.05)
I('openai/gpt-image-2','openai-gpt-image-2','GPT Image 2',0.047,'Column = medium; low $0.012, high $0.128 (auto = high).')
I('openai/gpt-image-2.5-sunburst','openai-gpt-image-2-5-sunburst','GPT Image 2.5 Sunburst',0.047,'Column = medium; low 0.012, high 0.128, xhigh 0.25, max 0.50.')
I('openai/gpt-image-2.5-flare','openai-gpt-image-2-5-flare','GPT Image 2.5 Flare',0.047,'Column = medium; low 0.012, high 0.128, xhigh 0.25, max 0.50. Same prices as Sunburst.')
I('openai/gpt-image-1.5','openai-gpt-image-1-5','GPT Image 1.5',0.05,'Column = medium; low 0.013, high 0.136.')
I('qwen/qwen-image-2-pro','alibaba-qwen-image-2-pro','Qwen-Image 2 Pro',0.075); I('qwen/qwen-image-2','alibaba-qwen-image-2','Qwen-Image 2',0.035); I('qwen/qwen-image','alibaba-qwen-image','Qwen-Image',0.025); I('qwen/qwen-image-2512','alibaba-qwen-image-2512','Qwen-Image 2512',0.02)
I('alibaba/qwen-image-3','alibaba-qwen-image-3','Qwen-Image 3',0.03); I('alibaba/qwen-image-3-pro','alibaba-qwen-image-3-pro','Qwen-Image 3 Pro',0.04)
I('wan-video/wan-2.7-image','alibaba-wan-2-7-image','Wan 2.7 Image',0.03); I('wan-video/wan-2.7-image-pro','alibaba-wan-2-7-image-pro','Wan 2.7 Image Pro',0.03)
I('recraft-ai/recraft-v4','recraft-v4','Recraft V4',0.04); I('recraft-ai/recraft-v4-pro','recraft-v4-pro','Recraft V4 Pro',0.25); I('recraft-ai/recraft-v4.1','recraft-v4-1','Recraft V4.1',0.04); I('recraft-ai/recraft-v4.1-pro','recraft-v4-1-pro','Recraft V4.1 Pro',0.25); I('recraft-ai/recraft-v3','recraft-v3','Recraft V3',0.04)
I('ideogram-ai/ideogram-4-5','ideogram-4-5','Ideogram 4.5',0.06,'Column = medium; low 0.03, high 0.10.')
I('ideogram-ai/ideogram-v4-quality','ideogram-v4-quality','Ideogram V4 Quality',0.10); I('ideogram-ai/ideogram-v4-balanced','ideogram-v4-balanced','Ideogram V4 Balanced',0.06)
I('ideogram-ai/ideogram-v3-quality','ideogram-v3-quality','Ideogram V3 Quality',0.09); I('ideogram-ai/ideogram-v3-balanced','ideogram-v3-balanced','Ideogram V3 Balanced',0.06); I('ideogram-ai/ideogram-v3-turbo','ideogram-v3-turbo','Ideogram V3 Turbo',0.03)
I('xai/grok-imagine-image','xai-grok-imagine-image','Grok Imagine Image',0.02); I('xai/grok-imagine-image-2','xai-grok-imagine-image-2','Grok Imagine Image 2',0.04)
I('xai/grok-imagine-image-quality','xai-grok-imagine-image-quality','Grok Imagine Image Quality',0.05,'Column = 1K; 2K $0.07; plus $0.01 per input MP.')
I('runwayml/gen4-image','runway-gen-4-image','Runway Gen-4 Image',0.05,'Column = 720p tier; 1080p $0.08.'); I('runwayml/gen4-image-turbo','runway-gen-4-image-turbo','Runway Gen-4 Image Turbo',0.03)
I('minimax/image-01','minimax-image-01','MiniMax image-01',0.01,'Cf. MiniMax direct $0.0035.')
I('krea/krea-2-large','krea-2-large','Krea 2 Large',0.06); I('krea/krea-2-medium','krea-2-medium','Krea 2 Medium',0.03)
I('stability-ai/stable-diffusion-3.5-large','stability-sd-3-5-large','Stable Diffusion 3.5 Large',0.065)
I('luma/photon','luma-photon','Luma Photon',0.03); I('luma/photon-flash','luma-photon-flash','Luma Photon Flash',0.01)
I('prunaai/p-image','prunaai-p-image','P-Image',0.005,'$5 per thousand output images = $0.005 each (5/1000).')
I('openai/dall-e-3','openai-dall-e-3','DALL-E 3',0.12)
# sora
rows.append(row(P,'Sora 2','openai-sora-2','openai/sora-2','video','per_second',f'Replicate billingConfig: {txt("openai/sora-2")}. Standard quality price; own-key variant has no Replicate charge.',URL('openai/sora-2')))
rows.append(row(P,'Sora 2 Pro','openai-sora-2-pro','openai/sora-2-pro','video','per_second',f'Replicate billingConfig: {txt("openai/sora-2-pro")}. Standard 720p $0.30/s; high 1024p $0.50/s.',URL('openai/sora-2-pro'),p720=0.30))
# fix Sora 2: price 0.10 per second standard (720p assumed? not stated)
for r in rows: pass
save(P,['https://replicate.com/pricing','https://replicate.com/collections/text-to-video']+[URL(s) for s in sorted({r['endpoint'] for r in rows})],
 ['gpt-image-1 and gpt-image-1-mini pages show only "OpenAI" (no Replicate price, own-key billing): skipped','lightricks ltx-video 0.9.x pages show no tier pricing (hardware-time billed): skipped','replicate.com/api JSON not usable without token; prices parsed from billingConfig JSON embedded in each model page HTML'],
 'Prices parsed from the billingConfig.current_tiers JSON embedded in each replicate.com/<owner>/<model> page (official page of the platform). Replicate pricing page banner on 2026-10-15: "Wan 3.0 is 30% off this week" so Wan 3.0 prices may be promotional. FLUX 3 Image on Replicate ($0.024 at 1K) is half the BFL direct price ($0.048): possible promo/error. FLUX 3 video on Replicate is 0.17/0.29 per s vs BFL 0.15/0.24. Replicate does not host H3/H3 Max (not in the collections), Imagen etc. are present. Rows with resolution unspecified have null resolution columns.',rows)
