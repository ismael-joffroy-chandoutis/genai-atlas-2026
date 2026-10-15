import os
# Parseur de la page de prix « byteplus » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='byteplus'; U='https://docs.byteplus.com/docs/ModelArk/1544106'
rows=[]
def V(mid,name,ep,raw,p480=None,p720=None,p1080=None): rows.append(row(P,name,mid,ep,'video','per_second','BytePlus ModelArk pricing page: '+raw,U,p480=p480,p720=p720,p1080=p1080))
def I(mid,name,ep,raw,p): rows.append(row(P,name,mid,ep,'image','per_image','BytePlus ModelArk pricing page: '+raw,U,pimg=p))
V('bytedance-seedance-2-5','Dreamina Seedance 2.5','dreamina-seedance-2-5-260628','Online inference USD per million tokens: 480p/720p input without video $10.70 (with video $6.40); 1080p without video $11.7 (with video $7.0). Price example 16:9, 5 s, input without video: 480p $0.514 per video = $0.103/s; 720p $1.156 = $0.231/s; 1080p $2.843 = $0.569/s. Columns use these per-second figures.',0.103,0.231,0.569)
V('bytedance-seedance-2-0','Dreamina Seedance 2.0','dreamina-seedance-2-0-260128','Online inference USD/M tokens: 480p/720p without video $7.0 (with video $4.3); 1080p $7.7 ($4.7); 4K $4.0 ($2.4). Price example 16:9, 5 s, input without video: 480p $0.35 = $0.07/s; 720p $0.76 = $0.15/s; 1080p $1.87 = $0.37/s; 4K $3.89 = $0.78/s. Native audio, price not split.',0.07,0.15,0.37)
V('bytedance-seedance-2-0-fast','Dreamina Seedance 2.0 Fast','dreamina-seedance-2-0-fast-260128','USD/M tokens (480p/720p): without video $5.6, with video $3.3. 5 s example: 480p $0.28 = $0.06/s; 720p $0.60 = $0.12/s; 1080p/4K not supported.',0.06,0.12)
V('bytedance-seedance-2-0-mini','Dreamina Seedance 2.0 Mini','dreamina-seedance-2-0-mini-260615','USD/M tokens (480p/720p): without video $3.5, with video $2.1. 5 s example: 480p $0.18 = $0.04/s; 720p $0.38 = $0.08/s.',0.04,0.08)
V('bytedance-seedance-1-5-pro','Seedance 1.5 Pro','seedance-1-5-pro-251215','Per 5 s video 16:9: silent 480p $0.06 (=$0.012/s), 720p $0.13 (=$0.026/s), 1080p $0.29 (=$0.058/s); audio+video $0.12 / $0.26 / $0.58 (=$0.024 / $0.052 / $0.116 per s); token price $1.2/M silent, $2.4/M with audio. Columns = silent.',0.012,0.026,0.058)
V('bytedance-seedance-1-0-pro','Seedance 1.0 Pro','seedance-1-0-pro-250528','$2.5/M tokens online. 5 s 16:9 examples: 480p (864x480) $0.12 (=$0.024/s), 720p (1248x704) $0.26 (=$0.052/s), 1080p (1920x1088) $0.61 (=$0.122/s). Silent.',0.024,0.052,0.122)
V('bytedance-seedance-1-0-pro-fast','Seedance 1.0 Pro Fast','seedance-1-0-pro-fast-251015','$1/M tokens online. 5 s 16:9 examples: 480p $0.05 (=$0.01/s), 720p $0.10 (=$0.02/s), 1080p $0.24 (=$0.048/s).',0.01,0.02,0.048)
I('bytedance-seedream-5-0-pro','Seedream 5.0 Pro','dola-seedream-5-0-pro-260628','Single image generation: <= 2.61 MP (1.5K or lower) $0.045; > 2.61 MP $0.09; layer decomposition $0.0225 / $0.045; input image: first free then $0.003. Column = <= 1.5K.',0.045)
I('bytedance-seedream-5-0-flash','Seedream 5.0 Flash','dola-seedream-5-0-flash-260915','Output $0.018 per image; input free.',0.018)
I('bytedance-seedream-5-0-lite','Seedream 5.0 Lite','seedream-5-0-lite-260128','Output $0.035 per image.',0.035)
I('bytedance-seedream-4-5','Seedream 4.5','seedream-4-5-251128','Output $0.04 per image.',0.04)
I('bytedance-seedream-4','Seedream 4.0','seedream-4-0-250828','Output $0.03 per image.',0.03)
save(P,[U,'https://docs.byteplus.com/docs/ModelArk/1544106 (tables reconstructed from the page source: the page body is client-rendered)'],['https://docs.byteplus.com/en/docs/ModelArk/1544106 returned navigation only; tables rebuilt from the embedded document data'],
 'Prices read from the BytePlus ModelArk pricing doc (USD). Seedance 2.x are billed per million tokens; the page gives 5 s price examples with per-second figures, used for the columns (input without video, 16:9). Coherence check: BytePlus Seedance 2.0 (0.07/0.15/0.37) is cheaper than Replicate (0.08/0.18/0.45) and Runware (0.07/0.16/0.40); BytePlus page rounds per-second values. The page names Seedance 2.5 as "Dreamina Seedance 2.5" model id dreamina-seedance-2-5-260628.',rows)
