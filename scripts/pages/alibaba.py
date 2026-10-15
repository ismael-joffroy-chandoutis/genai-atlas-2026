import os
# Parseur de la page de prix « alibaba » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='alibaba'; U='https://www.alibabacloud.com/help/en/model-studio/model-pricing'
rows=[]
def V(mid,name,ep,raw,p480=None,p720=None,p1080=None): rows.append(row(P,name,mid,ep,'video','per_second','Alibaba Cloud Model Studio pricing page, Singapore / International deployment (USD): '+raw,U,p480=p480,p720=p720,p1080=p1080))
def I(mid,name,ep,raw,p): rows.append(row(P,name,mid,ep,'image','per_image','Alibaba Cloud Model Studio pricing page, Singapore / International deployment (USD): '+raw,U,pimg=p))
V('alibaba-wan-3-0','Wan 3.0','wan3.0-video','Input and output billed (billable duration = input video + output video seconds). 480P List price $0.05/s, 720P $0.1/s, 1080P $0.2/s, each marked "Limited-time 30% off" (effective after discount = list x 0.7: $0.035 / $0.07 / $0.14 per s, my calculation, the page does not print the discounted figure). China (Beijing) list: $0.041256 / $0.082513 / $0.165025. Columns = list price.',0.05,0.10,0.20)
V('alibaba-wan-3-0-prime','Wan 3.0 Prime','wan3.0-video-prime','Input and output billed. 480P $0.068/s, 720P $0.14/s, 1080P $0.28/s (no promo shown). China (Beijing): $0.0636 / $0.127199 / $0.254399.',0.068,0.14,0.28)
for ver,nm in [('2.7','Wan 2.7'),('2.6','Wan 2.6')]:
    V(f'alibaba-wan-{ver.replace(".","-")}',f'{nm} (T2V)',f'wan{ver}-t2v','720P $0.10/s, 1080P $0.15/s (Wanx text-to-video; image-to-video wan2.7-i2v same: audio video 720P $0.10, 1080P $0.15).',None,0.10,0.15)
V('alibaba-wan-2-5','Wan 2.5 Preview (T2V)','wan2.5-t2v-preview','480P $0.05/s, 720P $0.10/s, 1080P $0.15/s.',0.05,0.10,0.15)
V('alibaba-wan-2-2-plus','Wan 2.2 Plus (T2V)','wan2.2-t2v-plus','480P $0.02/s, 1080P $0.10/s.',0.02,None,0.10)
V('alibaba-wan-2-1-turbo','Wan 2.1 Turbo (T2V)','wan2.1-t2v-turbo','480P $0.036/s, 720P $0.036/s.',0.036,0.036)
V('alibaba-happyhorse-1-1','HappyHorse 1.1 (T2V)','happyhorse-1.1-t2v','480P $0.07/s, 720P $0.14/s, 1080P $0.18/s (I2V/R2V tables exist; China region $0.0618845 / $0.123769 / $0.165026).',0.07,0.14,0.18)
V('alibaba-happyhorse-1-0','HappyHorse 1.0 (T2V)','happyhorse-1.0-t2v','720P $0.14/s, 1080P $0.24/s (China region $0.123769 / $0.220034).',None,0.14,0.24)
I('alibaba-qwen-image-3','Qwen-Image 3.0','qwen-image-3.0','Output $0.03/image at 1k and 2k; input image $0.003 each.',0.03)
I('alibaba-qwen-image-3-pro','Qwen-Image 3.0 Pro','qwen-image-3.0-pro','Output 1k $0.04, 2k $0.075; input image $0.003. Column = 1k.',0.04)
I('alibaba-qwen-image-2-1-pro','Qwen-Image 2.1 Pro','qwen-image-2.1-pro','$0.04/image.',0.04)
I('alibaba-qwen-image-2-1-turbo','Qwen-Image 2.1 Turbo','qwen-image-2.1-turbo','$0.016/image.',0.016)
I('alibaba-qwen-image-2-pro','Qwen-Image 2.0 Pro','qwen-image-2.0-pro','$0.075/image.',0.075)
I('alibaba-qwen-image-2','Qwen-Image 2.0','qwen-image-2.0','$0.035/image.',0.035)
I('alibaba-wan-2-7-image-pro','Wan 2.7 Image Pro','wan2.7-image-pro','$0.075/image.',0.075)
I('alibaba-wan-2-7-image','Wan 2.7 Image','wan2.7-image','$0.03/image.',0.03)
I('alibaba-wan-2-6-t2i','Wan 2.6 T2I','wan2.6-t2i','$0.03/image.',0.03)
save(P,[U],[],'Singapore (International) prices used; China/Germany/US/Japan regions print slightly lower USD figures (kept in raw for Wan 3.0 and HappyHorse). Wan 3.0 Std is marked Limited-time 30% off: list price in columns, discounted price computed in raw. This is consistent with Replicate banner "Wan 3.0 is 30% off this week" but Replicate shows 0.025/0.05/0.10 (half of list), WaveSpeed/Runware show list 0.05/0.10/0.20. Wan 3.0 billing counts input video seconds as well as output. Alibaba page does not list Qwen-Image 3 variant ids other than 3.0 / 3.0-pro.',rows)
