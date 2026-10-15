import os
# Parseur de la page de prix « bfl » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
from lib import *
P='bfl'; U='https://docs.bfl.ai/quick_start/pricing'
r=[]
r.append(row(P,'FLUX 3 Video','bfl-flux-3-video','/v1/flux-3','video','per_second',
 'Sanity pricing feed (docs.bfl.ai pricing page): t2v/i2v standard render hd 15 credits/s, fhd 24, qhd 28, uhd 41; v2v hd 21, fhd 27; Draft (hd) 6 credits/s. 1 credit = $0.01 -> hd $0.15/s, fhd $0.24/s. Audio is synchronized (no audio-off price listed). hd=720p class, fhd=1080p class.',U,p720=0.15,p1080=0.24))
r.append(row(P,'FLUX 3 Video Draft','bfl-flux-3-video-draft','/v1/flux-3','video','per_second','Draft mode renders at hd: 6 credits/s = $0.06/s (credit=$0.01)',U,p720=0.06))
r.append(row(P,'FLUX 3 Image','bfl-flux-3-image','/v1/flux-3-image','image','per_image','Per image by resolution: 768sq 4.1 credits ($0.041), 1k 4.8 ($0.048), 1.5k 7 ($0.07), 2k 10 ($0.10), 4k 60.7 ($0.607). 1 credit=$0.01. Column = 1k.',U,pimg=0.048))
def f2(n,i,e,first,add,unit):
    r.append(row(P,n,i,e,'image','per_image',f'Megapixel pricing: first MP {first} credits (${first/100}) + {add} credits (${add/100}) per additional output MP; each input MP for editing billed {add} credits. 1 credit=$0.01. Column = ~1MP (1024x1024 ~1.05MP, priceUnit shown {unit}).',U,pimg=first/100))
f2('FLUX.2 [max]','bfl-flux-2-max','/v1/flux-2-max',7,3,'$0.07')
f2('FLUX.2 [pro]','bfl-flux-2-pro','/v1/flux-2-pro',3,1.5,'$0.03')
f2('FLUX.2 [flex]','bfl-flux-2-flex','/v1/flux-2-flex',5,5,'$0.05')
f2('FLUX.2 [klein] 9B','bfl-flux-2-klein-9b','/v1/flux-2-klein-9b',1.5,0.2,'$0.015')
f2('FLUX.2 [klein] 4B','bfl-flux-2-klein-4b','/v1/flux-2-klein-4b',1.4,0.1,'$0.014')
for n,i,e,p in [('FLUX.1 Kontext [max]','bfl-flux-1-kontext-max','/v1/flux-kontext-max',0.08),('FLUX.1 Kontext [pro]','bfl-flux-1-kontext-pro','/v1/flux-kontext-pro',0.04),('FLUX 1.1 [pro] Ultra','bfl-flux-1-1-pro-ultra','/v1/flux-pro-1.1-ultra',0.06),('FLUX 1.1 [pro]','bfl-flux-1-1-pro','/v1/flux-pro-1.1',0.04)]:
    r.append(row(P,n,i,e,'image','per_image',f'priceUnit {p} USD per image (Sanity feed, previous generation)',U,pimg=p))
save(P,[U,'https://bfl.ai/pricing','https://2gpum2i6.api.sanity.io (public pricing feed used by docs.bfl.ai)'],[],'bfl.ai/pricing is a JS calculator; prices taken from the public Sanity feed that docs.bfl.ai queries (values in credits=cents). FLUX.2 [dev] is local only (no hosted API). FLUX 3 Video price includes synchronized audio. FLUX.1 models treated as previous generation.',r)
