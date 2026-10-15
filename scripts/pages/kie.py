import os
# Parseur de la page de prix « kie » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys,json
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='kie'; U='https://kie.ai/pricing'
R={x['modelDescription']:x for x in json.load(open(os.path.join(os.environ.get('ATLAS_PAGES','cache'),'apipages/kie_rows.json')))}
rows=[]
def d(desc):
    x=R[desc]; return float(x['usdPrice'])
def txt(descs):
    out=[]
    for k in descs:
        x=R[k]; out.append(f"{k}: {x['creditPrice']} credits {x['creditUnit']} = ${x['usdPrice']}" )
    return '; '.join(out)
def V(mid,name,ep,descs,cols,note='',per=None):
    # cols: dict col-> (desc, divisor)
    kw={}
    for c,(k,div) in cols.items():
        kw[c]=round(d(k)/div,5)
    raw='kie.ai pricing table (credits and USD both listed; 1 credit = $0.005 as implied by the page): '+txt(descs)
    if any(div!=1 for k,div in cols.values()): raw+='. Per-second = per-video price / seconds (divisors as noted).'
    raw+=' '+note
    rows.append(row(P,name,mid,ep,'video','per_second',raw.strip(),U,**kw))
def I(mid,name,ep,desc,note='',div=1):
    x=R[desc]
    rows.append(row(P,name,mid,ep,'image','per_image',f"kie.ai pricing table: {desc}: {x['creditPrice']} credits {x['creditUnit']} = ${x['usdPrice']} (page's own reference 'official/fal' price {x['falPrice'] or 'n/a'}). {note}".strip(),U,pimg=round(float(x['usdPrice'])/div,5)))
s2='bytedance/seedance-2'
V('bytedance-seedance-2-0','Seedance 2.0',s2,[s2+', 480p no video input',s2+', 720p no video input',s2+', 1080p no video input',s2+', 4K no video input'],{'p480':(s2+', 480p no video input',1),'p720':(s2+', 720p no video input',1),'p1080':(s2+', 1080p no video input',1)},'Columns = no video input; with video input cheaper (480p $0.057, 720p $0.125, 1080p $0.31, 4K $0.64).')
f=s2+' fast'
V('bytedance-seedance-2-0-fast','Seedance 2.0 Fast',f,[f+', 480p no video input',f+', 720p no video input'],{'p480':(f+', 480p no video input',1),'p720':(f+', 720p no video input',1)},'Columns = no video input.')
m='bytedance/seedance-2-mini'
V('bytedance-seedance-2-0-mini','Seedance 2.0 Mini',m,[m+', 480P no video',m+', 720P no video'],{'p480':(m+', 480P no video',1),'p720':(m+', 720P no video',1)},'Columns = no video.')
s5='bytedance/seedance-2-5'
V('bytedance-seedance-2-5','Seedance 2.5',s5,[s5+', 480p no video',s5+', 720p no video',s5+', 1080p no video'],{'p480':(s5+', 480p no video',1),'p720':(s5+', 720p no video',1),'p1080':(s5+', 1080p no video',1)},'Columns = no video input.')
a='bytedance/seedance-1.5-pro, without audio-'
V('bytedance-seedance-1-5-pro','Seedance 1.5 Pro','bytedance/seedance-1.5-pro',[a+'480p (service ends 2026-11-11)',a+'720p (service ends 2026-11-11)',a+'1080p (service ends 2026-11-11)'],{'p480':(a+'480p (service ends 2026-11-11)',1),'p720':(a+'720p (service ends 2026-11-11)',1),'p1080':(a+'1080p (service ends 2026-11-11)',1)},'Columns = without audio; with audio is 2x. Page says service ends 2026-11-11.')
for q,mid,nm in [('pro','bytedance-seedance-1-pro','Seedance 1 Pro'),('lite','bytedance-seedance-1-lite','Seedance 1 Lite')]:
    p=f'bytedance/seedance-v1-{q}, text-to-video, '
    V(mid,nm,f'bytedance/seedance-v1-{q}',[p+'480p',p+'720p',p+'1080p'],{'p480':(p+'480p',1),'p720':(p+'720p',1),'p1080':(p+'1080p',1)})
w='wan 3.0 video, '
V('alibaba-wan-3-0','Wan 3.0','wan 3.0 video',[w+'480p, video',w+'720p, video',w+'1080p, video'],{'p480':(w+'480p, video',1),'p720':(w+'720p, video',1),'p1080':(w+'1080p, video',1)})
w='wan3.0 video prime, '
V('alibaba-wan-3-0-prime','Wan 3.0 Prime','wan3.0 video prime',[w+'480p, video',w+'720p, video',w+'1080p, video'],{'p480':(w+'480p, video',1),'p720':(w+'720p, video',1),'p1080':(w+'1080p, video',1)})
w='wan 2.7 video, text-to-video, '
V('alibaba-wan-2-7','Wan 2.7','wan 2.7 video',[w+'720p',w+'1080p'],{'p720':(w+'720p',1),'p1080':(w+'1080p',1)})
w='wan 2.6, text to video, '
V('alibaba-wan-2-6','Wan 2.6','wan 2.6',[w+'5.0s-720p',w+'5.0s-1080p'],{'p720':(w+'5.0s-720p',5),'p1080':(w+'5.0s-1080p',5)},'Priced per video; 5 s clips divided by 5.')
w='wan 2.5, text-to-video, default-'
V('alibaba-wan-2-5','Wan 2.5','wan 2.5',[w+'5.0s-720p',w+'5.0s-1080p'],{'p720':(w+'5.0s-720p',5),'p1080':(w+'5.0s-1080p',5)},'Priced per video; 5 s clips divided by 5.')
h='HappyHorse-1.0, text-to-video, '
V('alibaba-happyhorse-1-0','HappyHorse 1.0','HappyHorse-1.0',[h+'720p',h+'1080p'],{'p720':(h+'720p',1),'p1080':(h+'1080p',1)})
h='HappyHorse-1.1, text-to-video, '
V('alibaba-happyhorse-1-1','HappyHorse 1.1','HappyHorse-1.1',[h+'720p',h+'1080p'],{'p720':(h+'720p',1),'p1080':(h+'1080p',1)})
k='Kling 3.0, video, '
V('kling-3-0-std','Kling 3.0 (720p tier)','Kling 3.0',[k+'without audio-720P',k+'with audio-720P',k+'without audio-4K'],{'p720':(k+'without audio-720P',1)},'Column = without audio. Kie lists 720P and 1080P tiers (std/pro mapping to 720p/1080p by convention).')
V('kling-3-0-pro','Kling 3.0 (1080p tier)','Kling 3.0',[k+'without audio-1080P',k+'with audio-1080P'],{'p1080':(k+'without audio-1080P',1)},'Column = without audio.')
k='kling 3.0 omni, text-to-video, '
V('kling-3-0-omni','Kling 3.0 Omni','kling 3.0 omni',[k+'720p no native audio',k+'720p with native audio',k+'1080p no native audio',k+'1080p with native audio',k+'4k no native audio'],{'p720':(k+'720p no native audio',1),'p1080':(k+'1080p no native audio',1)},'Columns = no native audio.')
k='kling 3.0 turbo, text-to-video, '
V('kling-3-0-turbo','Kling 3.0 Turbo','kling 3.0 turbo',[k+'720P',k+'1080P'],{'p720':(k+'720P',1),'p1080':(k+'1080P',1)})
k='kling 2.6, text-to-video, '
V('kling-2-6','Kling 2.6','kling 2.6',[k+'without audio-5.0s',k+'with audio-5.0s'],{'p720':(k+'without audio-5.0s',5)},'Per video of 5 s divided by 5; resolution not stated on page (put in no column: column left null). Column below is NOT filled.'.replace('put in no column: column left null). Column below is NOT filled.','column 720p NOT assumed).'))
rows[-1]['price_usd_720p_s']=None
k='kling 2.5 turbo, text-to-video, Turbo Pro-5.0s'
V('kling-2-5-turbo-pro','Kling 2.5 Turbo Pro','kling 2.5 turbo',[k],{},'Per video 5 s: 0.21/5 = $0.042/s; resolution not stated, columns null.')
k='Kling 2.1, video-generation, '
V('kling-2-1-std','Kling 2.1 Standard','Kling 2.1',[k+'Standard-5.0s'],{'p720':(k+'Standard-5.0s',5)},'Per 5 s video / 5.')
V('kling-2-1-pro','Kling 2.1 Pro','Kling 2.1',[k+'Pro-5.0s'],{'p1080':(k+'Pro-5.0s',5)},'Per 5 s video / 5.')
V('kling-2-1-master','Kling 2.1 Master','Kling 2.1',['Kling 2.1, text-to-video, Master-5.0s'],{},'Per 5 s video: 0.8/5 = $0.16/s; resolution not stated.')
k='MiniMax H3, text to video, '
V('minimax-h3','MiniMax H3','MiniMax H3',[k+'768p',k+'2K'],{'p720':(k+'768p',1)},'768p put in 720p column; 2K $0.065 not in columns. Page reference (official/fal) is $0.08 / $0.13.')
for tier,mid,nm in [('Pro','minimax-hailuo-2-3-pro','Hailuo 2.3 Pro'),('Standard','minimax-hailuo-2-3-standard','Hailuo 2.3 Standard')]:
    k=f'hailuo 2.3, image-to-video, {tier}-6.0s-'
    V(mid,nm,'hailuo 2.3',[k+'768p',k+'1080p',f'hailuo 2.3, image-to-video, {tier}-10.0s-768p'],{'p720':(k+'768p',6),'p1080':(k+'1080p',6)},'Per 6 s video / 6; 768p in 720p column. Mapping of kie "Pro/Standard" to MiniMax Hailuo 2.3 vs 2.3-Fast is not stated on the page (reference price column shows 0.28 / 0.49 for both).')
k='Google veo 3.1, text-to-video, '
V('google-veo-3-1','Veo 3.1 Quality','Google veo 3.1',[k+'Quality-720p',k+'Quality-1080p',k+'Quality-4K'],{'p720':(k+'Quality-720p',8),'p1080':(k+'Quality-1080p',8)},'Per video; duration not printed on page, 8 s assumed because the page reference price ($3.20) equals 8 s x $0.40 (with audio). Prices therefore likely WITH audio. Treat the per-second columns as inferred.')
V('google-veo-3-1-fast','Veo 3.1 Fast','Google veo 3.1',[k+'Fast-720p',k+'Fast-1080p',k+'Fast-4K'],{'p720':(k+'Fast-720p',8),'p1080':(k+'Fast-1080p',8)},'Per video; 8 s assumed (page reference $1.20 = 8 s x $0.15 with audio). Likely with audio; per-second columns inferred.')
V('google-veo-3-1-lite','Veo 3.1 Lite','Google veo 3.1',[k+'Lite-720p',k+'Lite-1080p',k+'Lite-4K'],{'p720':(k+'Lite-720p',8),'p1080':(k+'Lite-1080p',8)},'Per video; 8 s assumed (page reference $0.40 = 8 s x $0.05). Per-second columns inferred.')
V('xai-grok-imagine-video','Grok Imagine Video','grok-imagine',['grok-imagine, text-to-video, 480p','grok-imagine, text-to-video, 720p','grok-imagine, text-to-video, 1080p'],{'p480':('grok-imagine, text-to-video, 480p',1),'p720':('grok-imagine, text-to-video, 720p',1),'p1080':('grok-imagine, text-to-video, 1080p',1)})
V('xai-grok-imagine-video-1-5','Grok Imagine Video 1.5 (preview)','grok-imagine-video-1-5-preview',['grok-imagine-video-1-5-preview, 480p','grok-imagine-video-1-5-preview, 720p'],{'p480':('grok-imagine-video-1-5-preview, 480p',1),'p720':('grok-imagine-video-1-5-preview, 720p',1)})
k='pixverse-v6, Text /Image to Video, '
V('pixverse-v6','PixVerse V6','pixverse-v6',[k+'720p(no audio)',k+'1080p(no audio)',k+'720p(with audio)',k+'1080p(with audio)'],{'p720':(k+'720p(no audio)',1),'p1080':(k+'1080p(no audio)',1)},'Columns = no audio.')
k='Vidu Q4, image-to-video, '
V('vidu-q4','Vidu Q4','Vidu Q4',[k+'540p',k+'720p',k+'1080p'],{'p720':(k+'720p',1),'p1080':(k+'1080p',1)},'Image-to-video prices; 540p $0.036, 2k $0.152, 4k $0.312.')
k='google/gemini-omni-flash-1-1, video, 10s 720p no video input'
V('google-gemini-omni-1-1-flash','Gemini Omni 1.1 Flash','google/gemini-omni-flash-1-1',[k,'google/gemini-omni-flash-1-1, video, 4s 720p no video input'],{},'Per video, priced by duration (4 s $0.315, 6 s $0.42, 8 s $0.525, 10 s $0.63), same for 360p-1080p, 4k higher; per-second columns not filled because rate varies with duration.')
# images
I('google-nano-banana-2-1','Nano Banana 2.1','nano-banana-2-1','nano-banana-2-1, 1K','Column = 1K; 2K $0.03, 4K $0.045.')
I('google-nano-banana-2','Nano Banana 2','Google nano banana 2','Google nano banana 2, 1K','Column = 1K; 2K $0.06, 4K $0.09.')
I('google-nano-banana-2-lite','Nano Banana 2 Lite','nano-banana-2-lite','nano-banana-2-lite, 1k')
I('google-gemini-3-pro-image','Nano Banana Pro (Gemini 3 Pro Image)','Google nano banana pro','Google nano banana pro, 1/2K','Column = 1/2K; 4K $0.12.')
I('google-nano-banana','Nano Banana','Google nano banana','Google nano banana, text-to-image')
I('google-imagen-4','Imagen 4','google imagen4','google imagen4, text-to-image, default','Fast $0.02, Ultra $0.06.')
I('google-imagen-4-fast','Imagen 4 Fast','google imagen4','google imagen4, text-to-image, Fast'); I('google-imagen-4-ultra','Imagen 4 Ultra','google imagen4','google imagen4, text-to-image, Ultra')
I('bytedance-seedream-5-0-pro','Seedream 5.0 Pro','seedream 5 Pro','seedream 5 Pro, text-to-image, 1K','Column = 1K; 2K $0.07.')
I('bytedance-seedream-5-0-flash','Seedream 5.0 Flash','seedream 5 Flash','seedream 5 Flash, Text to image, 1K'); I('bytedance-seedream-5-0-lite','Seedream 5.0 Lite','seedream 5.0 Lite','seedream 5.0 Lite, text-to-image')
I('bytedance-seedream-4-5','Seedream 4.5','seedream 4.5','seedream 4.5, text-to-image'); I('bytedance-seedream-4','Seedream 4','seedream v4','seedream v4, text-to-image')
I('openai-gpt-image-2','GPT Image 2','gpt image 2','gpt image 2, text-to-image, 1k','Column = 1K; quality tier not stated on the page. 2K $0.05, 4K $0.08.')
I('openai-gpt-image-2-5-sunburst','GPT Image 2.5 Sunburst','gpt-image-2-5-sunburst','gpt-image-2-5-sunburst, text-to-image, 1K','Column = 1K; quality tier not stated. 2K $0.05, 4K $0.08.')
I('openai-gpt-image-2-5-flare','GPT Image 2.5 Flare','gpt-image-2-5-flare','gpt-image-2-5-flare, text-to-image, 1K','Column = 1K; quality not stated. 2K $0.05, 4K $0.08.')
I('openai-gpt-image-1-5','GPT Image 1.5','gpt image 1.5','gpt image 1.5, text-to-image, medium','Column = medium; high $0.11.')
I('alibaba-qwen-image-3','Qwen-Image 3.0','Qwen image 3.0','Qwen image 3.0, text to image, 1K','1K and 2K both $0.024.')
I('alibaba-qwen-image-3-pro','Qwen-Image 3.0 Pro','Qwen image 3.0 Pro','Qwen image 3.0 Pro, text to image, 1K','Column = 1K; 2K $0.06.')
I('alibaba-qwen-image-2-1','Qwen-Image 2.1','Qwen-Image-2.1','Qwen-Image-2.1, text to image, 1K','Column = 1K; 2K $0.04.')
I('alibaba-qwen-image-2','Qwen-Image 2','Qwen Image 2','Qwen Image 2, text-to-image')
I('alibaba-wan-2-7-image','Wan 2.7 Image','wan 2.7 image','wan 2.7 image'); I('alibaba-wan-2-7-image-pro','Wan 2.7 Image Pro','wan 2.7 image pro','wan 2.7 image pro')
I('xai-grok-imagine-image-2','Grok Imagine Image 2.0','grok-imagine-image-2-0','grok-imagine-image-2-0, Text to Image')
I('bfl-flux-2-pro','FLUX.2 [pro]','Black Forest Labs flux-2 pro','Black Forest Labs flux-2 pro, text-to-image, 1.0s-1K','Column = 1K; 2K $0.035.')
I('bfl-flux-2-flex','FLUX.2 [flex]','Black Forest Labs Flux 2 Flex','Black Forest Labs Flux 2 Flex, text to image, 1.0s-1K','Column = 1K; 2K $0.12.')
I('bfl-flux-1-kontext-pro','FLUX.1 Kontext [pro]','Black Forest Labs flux1-kontext','Black Forest Labs flux1-kontext, text-to-image, Pro'); I('bfl-flux-1-kontext-max','FLUX.1 Kontext [max]','Black Forest Labs flux1-kontext','Black Forest Labs flux1-kontext, text-to-image, Max')
I('ideogram-v3-quality','Ideogram V3 Quality','ideogram v3','ideogram v3, text-to-image, QUALITY'); I('ideogram-v3-balanced','Ideogram V3 Balanced','ideogram v3','ideogram v3, text-to-image, BALANCED'); I('ideogram-v3-turbo','Ideogram V3 Turbo','ideogram v3','ideogram v3, text-to-image, TURBO')
I('openai-gpt-4o-image','OpenAI 4o image','OpenAI 4o image','OpenAI 4o image, text-to-image')
pages=[U,'https://api.kie.ai/client/v1/model-pricing/page (public JSON endpoint behind the pricing page)']
save(P,pages,['Runway rows on kie.ai (per video 5s/10s, $0.06-$0.15) not turned into rows: the page does not say which Runway model','Recraft/Ideogram/Sora/H3 Max: Sora and Recraft V4 not seen in the video/image tables; Kie H3 Max not found'],
 'Prices come from the pricing table of kie.ai (pageProps pricingSeed and the public JSON behind it: 451 video+image rows read). The page lists both credits and USD per item (implied 1 credit = $0.005), so USD used directly; unit therefore per_second/per_image. Many kie prices are far below the reference "official/fal" price that the page itself prints (e.g. GPT Image 2 1K $0.03 vs ref $0.219). Veo 3.1 rows are per video and the 8 s duration is inferred from the page reference price. Kie rows with resolution not stated left null.',rows)
