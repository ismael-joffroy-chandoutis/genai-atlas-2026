import os
# Parseur de la page de prix « kling » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import sys
sys.path.insert(0,os.path.join(os.environ.get('ATLAS_PAGES','cache'),''))
from lib import *
P='kling'; U='https://klingai.com/global/dev/pricing'
rows=[]
def V(mid,name,ep,raw,p720=None,p1080=None): rows.append(row(P,name,mid,ep,'video','per_second','Kling developer pricing page (redirects to kling.ai/dev/pricing), 1 unit = $0.14 list price: '+raw,U,p720=p720,p1080=p1080))
V('kling-3-0-std','Kling 3.0 (720P)','kling-v3','No native audio: 0.6 units ($0.084)/s at 720P; with native audio, no voice control: 0.9 units ($0.126)/s. Column = no audio.',0.084)
V('kling-3-0-pro','Kling 3.0 (1080P)','kling-v3','No native audio: 0.8 units ($0.112)/s at 1080P; with native audio, no voice control: 1.2 units ($0.168)/s. Column = no audio.',None,0.112)
V('kling-3-0-4k','Kling 3.0 (4K)','kling-v3','4K: 3.0 units ($0.42)/s with or without native audio.')
V('kling-3-0-omni-std','Kling 3.0 Omni (720P)','kling-v3-omni','No video input: no audio 0.6 units ($0.084)/s, with audio 0.8 units ($0.112)/s; with video input no audio 0.9 units ($0.126)/s. Column = no video input, no audio.',0.084)
V('kling-3-0-omni-pro','Kling 3.0 Omni (1080P)','kling-v3-omni','No video input: no audio 0.8 units ($0.112)/s, with audio 1.0 unit ($0.14)/s; with video input no audio 1.2 units ($0.168)/s; 4K 3.0 units ($0.42)/s. Column = no video input, no audio.',None,0.112)
V('kling-3-0-turbo','Kling 3.0 Turbo','kling-v3-turbo','Only with native audio listed: 720P 0.8 units ($0.112)/s, 1080P 1.0 unit ($0.14)/s. Columns include audio (no audio-off tier listed).',0.112,0.14)
save(P,[U],['Kling 4.0 is mentioned on the page ("These plans currently don\'t support Kling 4.0") but has no price on the page','Kling O1, 2.6, 2.5, 2.1 and image API (Image API tab) not priced on the page','Page is a SPA: read with a headless browser (innerText) rather than a plain HTTP fetch'],
 'Prepaid resource-package model: list unit price $0.14, 10% off for packages >= $3780 (unit $0.126), packages are 180-day, no rollover, minimum $700 package. Per-second prices above are list. These match Replicate/Runware for Kling 3.0 (0.084/0.112 no audio). Kling 3.0 Turbo audio price (0.112/0.14) matches Runware Turbo.',rows)
