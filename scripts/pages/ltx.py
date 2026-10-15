import os
# Parseur de la page de prix « ltx » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
from lib import *
P='ltx'; U='https://docs.ltx.io/pricing'
r=[]
d={('ltx-2-5-fast','LTX-2.5 Fast','ltx-2-5-fast'):(0.09,0.13),('ltx-2-5-pro','LTX-2.5 Pro','ltx-2-5-pro'):(0.12,0.17),('ltx-2-3-fast','LTX-2.3 Fast','ltx-2-3-fast'):(0.03,0.06),('ltx-2-3-pro','LTX-2.3 Pro','ltx-2-3-pro'):(0.04,0.08)}
extra={'ltx-2-5-fast':'1440p $0.19, 4K $0.30','ltx-2-5-pro':'1440p $0.25, 4K $0.39','ltx-2-3-fast':'1440p $0.12, 4K $0.24','ltx-2-3-pro':'1440p $0.16, 4K $0.32'}
for (ep,n,i),(a,b) in d.items():
    raw=f'Text-to-Video and Image-to-Video: {ep} 720p-class $ {a}/s, 1080p-class ${b}/s, {extra[ep]} (cost per second of output video; same table for v2/text-to-video and v2/image-to-video). Audio-to-video: '
    if ep=='ltx-2-3-pro': raw+='720p $0.06/s, 1080p $0.10/s'
    elif ep=='ltx-2-3-fast': raw+='not listed'
    else: raw+='same as t2v'
    r.append(row(P,n,i if False else 'ltx-'+i.replace('ltx-',''),ep,'video','per_second',raw.replace('$ ','$'),U,p720=a,p1080=b))
save(P,[U,'https://ltx.io/model/api-pricing (404)'],['https://ltx.io/model/api-pricing : 404 page; real pricing is on docs.ltx.io/pricing'],'Prices per second of output video, USD. LTX-2 (original) not listed on pricing page; only LTX-2.3 and LTX-2.5 (fast/pro). Audio inclusion not stated on page. No 480p tier. Other endpoints (retake $0.10/s, extend $0.10/s, HDR upscale, reframe) not in rows.',r)
