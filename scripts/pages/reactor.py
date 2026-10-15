import os
# Parseur de la page de prix « reactor » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
from lib import *
P='reactor'; A='https://api.reactor.inc/pricing'
r=[]
for n,i,ep,rate,u in [('MiniMax FastH3','minimax-fast-h3','reactor/fast-h3','0.0350','https://reactor.inc/models/fast-h3'),
 ('MiniMax FastH3 Omni','minimax-fast-h3-omni','reactor/fast-h3-omni','0.0125','https://reactor.inc/models/fast-h3-omni'),
 ('H3 Reference Turbo Realtime','minimax-h3-reference-turbo-realtime','reactor/h3-reference-to-video-turbo-realtime','0.0350','https://api.reactor.inc/pricing')]:
    raw=f'{rate} USD per second of session time (api.reactor.inc/pricing amount_per_sec_usd; credits_per_dollar 10000). Billed per second of wall-clock session holding a GPU, not per second of generated video. Native synchronized audio (no audio-off price). Resolution not documented; resolution columns left null.'
    if n.endswith('Omni'): raw+=' Model page shows "$2.10/MINUTE $0.0125/SEC $0.75/MINUTE" (extra per-minute figures unexplained; API says 0.0125/s = $0.75/min).'
    else: raw+=f' Model page: $0.035/SEC $2.10/MINUTE.'
    r.append(row(P,n,i,ep,'video','per_second',raw,u))
save(P,['https://reactor.inc','https://reactor.inc/models/fast-h3','https://reactor.inc/models/fast-h3-omni',A,'https://docs.reactor.inc/resources/billing','https://docs.reactor.inc/model-api-reference/fast-h3/overview.md'],['https://reactor.inc/pricing : 404'],'Reactor bills per second of live session (wall-clock), not per generated second; FastH3 is real-time so approx equivalent but a session idle still bills. Output resolution not found in docs, so no resolution price columns. Other Reactor models (LTX-Avatar 0.03/s, Happy Oyster 0.0278/s, Helios 0.0017/s, etc.) not rows as outside scope. FastH3 Omni page shows a stray "$2.10/MINUTE" next to $0.0125/SEC, possibly a comparison/strikethrough; API says 0.0125.',r)
