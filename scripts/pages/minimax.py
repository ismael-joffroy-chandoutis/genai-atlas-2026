import os
# Parseur de la page de prix « minimax » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
from lib import *
P='minimax'; U='https://platform.minimax.io/docs/guides/pricing-paygo'
r=[]
def v(n,i,ep,raw,**k): r.append(row(P,n,i,ep,'video','per_second',raw,U,**k))
v('MiniMax-H3','minimax-h3','MiniMax-H3','Video generation output: 768P $0.08/second; 2K $0.13/second (billed per second). Input: audio free, first 5 images free then $0.04/extra image; input video billed per second at output res rate. 768P mapped to 720p column (768P is not exactly 720p). 2K price not placed in 1080p column. Audio-inclusion not stated.',p720=0.08)
v('MiniMax-H3-Max','minimax-h3-max','MiniMax-H3-Max','Video generation output: 480P $0.05/second; 768P $0.08/second. Input: audio free, first 2 images free then $0.074/extra image; input video 480P $0.0553/sec, 768P $0.143/sec (differs from output rates, as listed). 768P mapped to 720p column.',p480=0.05,p720=0.08)
v('MiniMax-H3-Regeneration','minimax-h3-regeneration','MiniMax-H3-Regeneration','Regenerate a 768P video into 2K: $0.05/second of regenerated output (on top of the original 768P generation). Not a standalone price; no resolution column filled.')
v('Hailuo 2.3','minimax-hailuo-2-3','MiniMax-Hailuo-2.3','Legacy: $0.28 per 768P 6s video (=0.28/6=$0.0467/s); $0.56 per 768P 10s (=0.056/s); $0.49 per 1080P 6s (=0.49/6=$0.0817/s). Column 720p = 768P at 6s. No audio.',p720=round(0.28/6,4),p1080=round(0.49/6,4))
v('Hailuo 2.3 Fast','minimax-hailuo-2-3-fast','MiniMax-Hailuo-2.3-Fast','Legacy: $0.19 per 768P 6s (=0.19/6=$0.0317/s); $0.32 per 768P 10s (=0.032/s); $0.33 per 1080P 6s (=0.33/6=$0.055/s). Column 720p = 768P at 6s.',p720=round(0.19/6,4),p1080=0.055)
v('Hailuo 02','minimax-hailuo-02','MiniMax-Hailuo-02','Legacy: $0.28 per 768P 6s (=$0.0467/s); $0.56 per 768P 10s; $0.49 per 1080P 6s (=$0.0817/s); $0.10 per 512P 6s (=0.10/6=$0.0167/s, 512P put in 480p column); $0.15 per 512P 10s (=$0.015/s).',p480=round(0.10/6,4),p720=round(0.28/6,4),p1080=round(0.49/6,4))
r.append(row(P,'image-01','minimax-image-01','image-01','image','per_image','$0.0035 per image',U,pimg=0.0035))
save(P,[U],[],'H3 / H3-Max priced per second of output by resolution tier (480P/768P/2K). 768P is placed in the 720p column and flagged in raw; 2K (H3) left out of columns. Whether H3 price includes audio is not stated on the page (H3 FastH3 on Reactor advertises synchronized audio). Hailuo 2.3 price per second differs between 6s and 10s clips (0.0467 vs 0.056 for 768P): 6s used. No "H3 Max Turbo" listed on this page (searched "turbo": only text models). Video Packages exist (points) but do not support H3.',r)
