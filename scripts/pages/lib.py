import os
# Parseur de la page de prix « lib » (relevé du 15/10/2026). Lit des copies HTML faites ce jour-là
# (copies HTML des pages de prix, rangées dans le dossier ATLAS_PAGES, par défaut cache/) : pour relancer, re-télécharger les pages dans ce dossier.
import json,sys
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','data','raw','%s-2026-10-15.json')
def row(platform,name,mid,endpoint,modality,unit,raw,url,v='page',p480=None,p720=None,p1080=None,pimg=None):
    return dict(model_name=name,model_id=mid,platform=platform,endpoint=endpoint,modality=modality,unit=unit,
      price_usd_480p_s=p480,price_usd_720p_s=p720,price_usd_1080p_s=p1080,price_usd_per_image=pimg,raw=raw,source_url=url,verified=v)
def save(platform,pages,unreach,notes,rows):
    json.dump(dict(source=platform,retrieved_at='2026-10-15',pages=pages,unreachable=unreach,notes=notes,rows=rows),open(OUT%platform,'w'),ensure_ascii=False,indent=1)
    print(platform,len(rows))
