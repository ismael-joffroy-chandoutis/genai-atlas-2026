[English](hybrid-look-matching.md) · [Français](raccord-look-hybride.fr.md)

# Raccord d'un film hybride (Blackmagic, iPhone, infrarouge, IA) dans un look « iPhone granuleux »

Étiquettes : **[éditeur]** = affirmation du fabricant ou du vendeur · **[vérifié]** = fait lu dans une source primaire ou constaté de façon concordante · **[pro]** = témoignage d'un technicien nommé · **[reco]** = recommandation de synthèse, à tester sur vos rushes.

Méthode : recherche web du 15/10/2026, pages officielles lues quand accessibles ; les points non confirmés sont signalés.

---

## 1. Gestion des couleurs du projet

**Choix de l'espace de travail [reco].** Pour un film qui finit en SDR Rec.709 avec un look « téléphone », prenez **DaVinci YRGB Color Managed** en mode manuel : espace de timeline **DaVinci Wide Gamut / DaVinci Intermediate**, sortie **Rec.709 Gamma 2.4**. ACEScct marche aussi, mais il n'apporte rien ici : aucun prestataire VFX ACES à alimenter, et la majorité des sources (iPhone HEVC, IA) ne sont pas des captations scène-référées. Le pipeline DWG vous donne des CST natifs pour Gen 5, Apple Log et Rec.709, et le Film Look Creator lit l'espace de timeline par défaut en mode Color Managed **[vérifié, 6]**.

Si vous préférez le mode non managé (YRGB classique), faites un « sandwich » CST par plan : entrée vers DWG/Intermediate, étalonnage, puis CST de sortie vers Rec.709. Dans ce cas, réglez les « Color Space Overrides » du Film Look Creator sur DWG/Intermediate, ce que des utilisateurs conseillent sur le forum Blackmagic **[pro, 6]**.

**Entrée de chaque source**

- **BRAW (Gen 5)** : BRAW 2.0 a apporté la colorimétrie Gen 5 et le décodage direct en DaVinci Wide Gamut / DaVinci Intermediate **[vérifié, 8]**. Onglet Camera Raw : *Decode using Clip*, Color Science Gen 5, gamut/gamma **DWG / Intermediate**, ISO de décodage ajusté au besoin (c'est une métadonnée, sans perte), Highlight Recovery activé si les hautes lumières clippent. Le Pocket 6K G2 est double ISO natif jusqu'à 25 600 **[éditeur, 8]**. Ne débruitez pas au décodage : vous allez de toute façon remplacer la texture.
- **iPhone Apple Log** : Apple fournit sur developer.apple.com un paquet « Apple Log profile » contenant une LUT Log vers linéaire, une LUT Log vers Rec.709 et un livre blanc PDF, selon un message du forum Blackmagic **[pro, non revérifié sur la page Apple, 10]**. Dans Resolve, préférez un **CST Apple Log vers DWG/Intermediate** (Resolve propose Apple Log en gamma d'entrée) plutôt qu'une LUT vers Rec.709, qui écraserait les hautes lumières avant l'étalonnage. Sur iPhone 17 Pro, Apple Log 2 existe : la courbe et le gamut diffèrent d'Apple Log, réglez donc l'entrée selon le clip **[éditeur, 11]**.
- **iPhone HEVC « standard » (HDR Dolby Vision / HLG)** : c'est le piège. Par défaut, l'iPhone filme en HDR **Rec.2100 HLG avec métadonnées Dolby Vision**. Dans un projet SDR, l'image paraît délavée si Resolve lit la mauvaise fonction de transfert ou n'a pas de conversion HDR vers SDR définie **[pro, 12]**. Vérifiez les métadonnées de chaque clip, forcez l'entrée **Rec.2100 HLG** puis un CST avec tone mapping vers votre espace de travail, une seule fois ; n'empilez pas une « LUT iPhone » par-dessus **[pro, 12]**. Si le clip est en SDR (réglage HDR désactivé), entrée Rec.709 Gamma 2.4.
- **Infrarouge** : pas de transformée colorimétrique « juste ». Décodez en Rec.709 ou en log selon la caméra, faites la balance des blancs sur la végétation ou une charte IR, puis choisissez : **monochrome** (canal rouge ou mélange de canaux, le plus simple à fondre dans le reste) ou **fausse couleur** (échange de canaux R/B dans le Mélangeur RVB). Considérez l'IR comme une source « affichage » et non scène-référée **[reco]**.
- **Plans IA en Rec.709 8 bits** : entrée **Rec.709 Gamma 2.4** puis CST inverse vers DWG. Vous gagnez des calculs propres, pas de latitude : les hautes lumières clippées restent clippées, les aplats 8 bits compressés montrent des bandes dès qu'on pousse le contraste **[reco]**. Corrigez peu, en douceur, et avant tout ajout de grain.
- **EXR de LTX (IC-LoRA HDR)** : la doc Lightricks présente l'IC-LoRA HDR comme un **post-traitement qui convertit une vidéo SDR existante** en EXR image par image, « scene-linear 16-bit » selon ltx.io, validé sur LTX-2.3 et pas encore sur LTX-2.5 **[éditeur, 13]**. Un guide tiers parle de « LogC3 », ce qui contredit la page officielle : ouvrez un fichier et vérifiez avant de choisir l'entrée (Linear/Rec.709 primaires probables) **[vérifié : contradiction entre sources, 13]**. Piège : dans ComfyUI, sans `OPENCV_IO_ENABLE_OPENEXR=1`, l'export EXR échoue en silence **[éditeur, 13]**. Rappel : cette conversion devine les hautes lumières, elle ne les restitue pas.

**SDR ou HDR ?** Livrez en **SDR Rec.709**. Raisons : la majorité des plans IA sont nés en SDR 8 bits, leurs hautes lumières n'existent pas, et l'IC-LoRA HDR les invente ; le look « iPhone Smart HDR » est justement un tone mapping qui compresse tout dans un affichage SDR ; enfin l'écart entre plans IA et BRAW est maximal en HDR, où l'on voit le clipping et le banding. Si un master HDR est exigé plus tard, faites-le à partir du même étalonnage avec un plafond bas (environ 300 nits) pour que les plans IA ne paraissent pas éteints **[reco]**.

---

## 2. Ce qui compose le « look iPhone »

Décomposition technique **[reco, appuyée par 4, 14]** :

1. **Bruit de capteur petit format** : luminance fine et chroma marbré dans les ombres dès que la lumière baisse.
2. **Débruitage temporel agressif** : textures qui « bavent » et se figent, aplats cireux, traînées sur les mouvements.
3. **Accentuation** : halos clairs autour des contours, micro-contraste artificiel. Des tests de raccord iPhone/ALEXA situent l'essentiel de l'écart dans la netteté **[pro, 14]**.
4. **HDR multi-images et tone mapping local** : ombres relevées, ciels récupérés de façon synthétique, noirs un peu levés **[pro, 14]**.
5. **Compression HEVC** : blocs dans les dégradés, perte de détail fin dans le mouvement, chroma 4:2:0. Sur *28 Years Later*, Union VFX a dû gérer le sous-échantillonnage 4:2:0 et a recréé les artefacts de compression **[pro, 4]**.
6. **Optique** : grand angle 24-26 mm équivalent, distorsion corrigée par logiciel (bords étirés), profondeur de champ quasi infinie.
7. **Temps** : 30 ou 60 i/s, obturation courte en plein jour (mouvements saccadés), rolling shutter, stabilisation électronique qui « flotte ».

**Reconstruction sur une image propre (BMD, IA) [reco]**, dans cet ordre :

1. Recadrage et **distorsion** (Resolve, Lens Correction dans l'inspecteur ou outil Lens Distortion dans Fusion ; légère distorsion en barillet si vous partez d'une focale longue).
2. **Profondeur de champ** : impossible à restaurer proprement ; tournez la Blackmagic diaphragmée (f/8 et au-delà) et focale courte. Pour l'IA, ne demandez pas de bokeh au prompt.
3. **Tone mapping « Smart HDR »** : courbe qui relève les ombres, compresse les hautes lumières, plus du contraste local (outil Contrast Pop ou Midtone Detail positif).
4. **Lissage puis accentuation** : un passage de Noise Reduction temporel exagéré pour reproduire la bave, puis Sharpen avec un rayon de 1 à 2 pixels pour générer des halos.
5. **Bruit numérique** (luminance plus chroma, plus fort dans les ombres).
6. **Compression** : rendu intermédiaire en HEVC ou H.264 à bas débit (par ex. 8 à 15 Mb/s en 1080p, 4:2:0, GOP long), réimporté sur la timeline. C'est la seule façon d'obtenir de vrais blocs de macroblocs qui bougent.

**Outils, avec leur statut**

- **Resolve Studio** : *Film Grain* (ResolveFX), *Film Look Creator* (grain, flou, halation, vignettage ; indisponible dans la version gratuite) **[vérifié, 6]**, Noise Reduction temporelle et spatiale, Sharpen, Blur, Motion Blur. Un effet nommé « Digital Noise » **n'a pas été trouvé** : ne le cherchez pas sous ce nom.
- **FilmConvert Nitrate / CineMatch** : profils Apple Log (iPhone 15 Pro, 2023) et iPhone 12 Pro **[éditeur, 15]**. Ils servent à faire correspondre la couleur, pas à fabriquer du bruit de téléphone, et le plug-in vise un grain argentique.
- **Dehancer** : émulation de film (grain, halation) **[éditeur]**, aucun profil smartphone trouvé.
- **Video Village Filmbox** : émulation de film **[éditeur]**. **LensNode** (Node Mill, distribué par Video Village depuis le 23/07/2026) : simulation d'objectifs à partir de plus de 111 profils mesurés (bokeh, aberrations, distorsion, vignettage), en ACES, pour Resolve, Baselight, Premiere, After Effects et FCP ; 149 $ par an ou 399 $ en licence perpétuelle **[éditeur et revue indépendante, 24]**. « Scatter » non confirmé.
- **Boris FX Sapphire, Red Giant Universe** : effets de grain, de bruit et de dégradation vidéo **[éditeur, non revérifié pour cette version]**.
- **Neat Video** : profil de bruit par caméra et par mode, réutilisable, filtrage temporel et spatial **[éditeur, 16]**. Aucune fonction « ajouter du bruit » confirmée dans Neat Video 6.
- **Topaz** : réglages Add noise et Grain ; Topaz reconnaît que sans eux le rendu peut paraître « plastique » dans les dégradés **[éditeur, 17]**.

**Profils extraits des vrais rushes iPhone [reco, appuyée par 2, 3]** :

- *Nuke, DasGrain* (gizmo gratuit de Fabian Holtz) : trois entrées (plaque débruitée, comp, plaque d'origine), analyse sur une zone plate et sombre, puis réinjection du bruit réel. Il ne marche ni dans Nuke Indie ni dans Nuke NC, et il exige un bon débruitage **[pro, 2]**. Pour l'appliquer à un plan Blackmagic, créez une « plaque donneuse » : un plan iPhone gris neutre et flou (mur, ciel couvert) tourné à l'ISO voulu, dont vous extrayez le bruit.
- *onegrain* (sync. labs, annoncé le 07/07/2026) : débruitage et regrain dans un même pipeline, en ligne de commande, API et plug-in OFX pour Nuke, Resolve et Baselight ; l'auteur le dit « pas encore parfait » **[éditeur, 3]**.
- *Méthode manuelle dans Resolve* : filmez à l'iPhone une charte grise et un mur neutre à plusieurs ISO, soustrayez la version débruitée (mode de fusion Différence ou Soustraction dans un nœud Layer Mixer), gardez le résidu centré sur 50 % de gris et superposez-le en Lumière douce ou Incrustation sur vos plans propres. Vous obtenez un bruit réel, à la bonne structure, qui reste du bruit d'iPhone.

---

## 3. Dégrain et regrain

Règle de toute la postproduction : « enlever le grain, faire le travail, remettre le grain » **[pro, 3]**.

- **Avant l'IA** : débruitez les images de départ que vous donnez aux modèles (photogrammes extraits des rushes). sync. labs constate que tout bruit retiré avant le traitement améliore la sortie **[pro, 3]**. Un modèle de diffusion lit le bruit comme du contenu : il l'efface, le transforme en motifs ou en invente un qui scintille d'une image à l'autre. **Ne demandez jamais de grain au prompt** : vous obtiendriez une texture « peinte » qui bouge avec l'image et que personne ne peut enlever ensuite **[reco]**.
- **Avant l'upscale** : débruitez si nécessaire, sinon l'upscaler accentue le bruit **[éditeur, 17]**. Un message sur le forum Topaz conseille de passer ses logiciels en dernier **[témoignage non vérifié, 17]**.
- **Avant l'étalonnage** : débruitez les sources bruitées (iPhone de nuit, IR, BMD à haut ISO) dans le premier nœud ou en amont (Neat Video, Resolve NR temporel), pour que chaque source parte d'une base propre.
- **Après tout** : générez le grain ou le bruit **en dernier, à la résolution de sortie, identique sur toutes les sources**, via un nœud de timeline ou un calque d'ajustement. Le même bruit sur tout le film unifie les sources hétérogènes **[éditeur, 19]**. Ensuite seulement vient la compression finale.

Point de désaccord : certains guides de fournisseurs placent le grain **avant** l'étalonnage final **[éditeur, 18]**. Pour un bruit de capteur, placez-le **après** l'étalonnage et **avant** la compression simulée : le bruit d'un téléphone apparaît avant l'encodage HEVC, et ce dernier le transforme **[reco]**.

---

## 4. Raccord des plans IA

- **Image de départ neutre ou étalonnée ?** Donnez au modèle une image **déjà étalonnée dans la couleur du look, mais propre** (sans bruit ni accentuation). Avantage : le modèle produit directement la bonne palette et la bonne exposition, donc moins d'étalonnage destructeur en 8 bits. Risque : les modèles poussent souvent la saturation et le contraste, vérifiez la dérive sur les longs plans. Une image neutre laisse plus de marge en théorie, mais un rendu 8 bits n'en a presque pas **[reco]**.
- **Références de style** : photogrammes des rushes, débruités. **LoRA de style** : entraînez-la sur des images propres. Sur des images granuleuses, le LoRA apprend le bruit comme un motif fixe et le reproduit mal **[reco]**.
- **Upscale** (Topaz Starlight ou Proteus, SeedVR2, FlashVSR) : **avant** le grain, toujours.
- **Fréquence d'images** : choisissez une cadence de timeline unique. Si l'iPhone a tourné en 30 i/s et que le look veut « téléphone », une timeline en **30 i/s** est cohérente ; générez alors l'IA en 30 i/s ou interpolez-la. En 24 i/s, conformez les plans iPhone en 24 (accéléré ou ralenti selon le cas) et évitez le pulldown **[reco]**.
- **Flou de bouger** : les modèles en ajoutent peu ou mal. Resolve (Motion Effects, Motion Blur) ou RSMB pour l'ajouter. Le look iPhone de jour veut un flou **faible** (obturation courte), donc dosez peu.
- **Rolling shutter** : simulable avec un déplacement vertical par ligne (Fusion, expression ou plug-in de type Sapphire), à réserver aux mouvements rapides.
- **Distorsion grand angle** : appliquez-la aux plans IA et BMD avant le bruit, jamais après.

---

## 5. Ordre global du pipeline

| # | Passe | BMD (BRAW) | iPhone Apple Log | iPhone HEVC HLG | IR | IA (Rec.709) | IA (EXR LTX) |
|---|---|---|---|---|---|---|---|
| 1 | Ingest | BRAW natif, sauvegarde | ProRes Log | Vérifier métadonnées DV/HLG | Selon caméra | Lister modèle, seed, 8 bits | Contrôler l'espace réel |
| 2 | Conformation | Cadence timeline unique, recadrage, distorsion | Idem | Idem | Idem | Upscale ici, interpolation | Idem |
| 3 | Débruitage | Léger si ISO élevé | Neat Video / NR temporel | Idem | Fort | Rarement | Rarement |
| 4 | Gestion couleur | Decode Gen 5 vers DWG/Intermediate | CST Apple Log vers DWG | HLG vers DWG avec tone mapping | Monochrome ou échange de canaux | CST Rec.709 vers DWG | Linéaire vers DWG |
| 5 | Primaire de raccord | Expo, balance | Idem | Idem | Densité | Petites corrections | Idem |
| 6 | Look créatif (timeline) | Courbe Smart HDR, contraste local, palette | Idem | Idem | Idem | Idem | Idem |
| 7 | Texture | NR temporel « bave » + Sharpen rayon 1-2 px | Plus léger (déjà présent) | Rien ou presque | Idem BMD | Idem BMD | Idem BMD |
| 8 | Bruit | Bruit iPhone extrait (DasGrain, onegrain ou résidu Resolve), même calque partout | Idem | Idem | Idem | Idem | Idem |
| 9 | Compression simulée | Aller-retour HEVC bas débit | Idem | Idem | Idem | Idem | Idem |
| 10 | Sortie | Rec.709 Gamma 2.4, master ProRes 422 HQ, puis livrables | | | | | |

Point de contrôle **[reco]** : après la passe 9, regardez les plans en vrai téléphone, côte à côte avec un plan iPhone d'origine. Ce qui trahit un plan, ce sont d'abord les halos et la profondeur de champ, la couleur vient après.

---

## 6. Exemples documentés

- **28 Years Later** (Danny Boyle, Anthony Dod Mantle, 2025) : tourné en partie sur iPhone 15 Pro Max modifiés, avec drone DJI Inspire 3 et GoPro sur drone FPV **[vérifié, 1, 4]**. Chez Union VFX, Gascoyne dit que le pipeline couleur des iPhone était « fairly good », mais que le 4:2:0 posait problème sur fond bleu ; l'équipe a « matching the grain structure », en précisant « it was not really grain », et a reproduit ce que le téléphone fait à l'image, compression comprise ; il a fallu aussi raccorder les bords flous et vignetés des optiques anciennes. Dillan Nicholls cite sous-échantillonnage chromatique, artefacts de stabilisation, hautes lumières clippées et sauts de point. La conversion Apple Log vers ARRI Log a été un obstacle pour le montage et le monitoring. La stabilisation interne était coupée pour permettre le tracking **[pro, 4, befores & afters, 07/08/2026]**. L'étalonneur n'est pas nommé dans les sources lues.
- **Tangerine** (Sean Baker, 2015) : trois iPhone 5s, FiLMiC Pro (contrôle de l'expo, du point, de la balance, encodage 50 Mb/s en 1080p), adaptateur anamorphique Moondog Labs 1,33x, focale autour de 24 mm. La saturation a été poussée volontairement en postproduction dans Final Cut Pro **[vérifié, 20, 21]**. Pas d'étalonneur nommé.
- **Unsane** (Soderbergh, 2018) : trois iPhone 7 Plus en 4K, FiLMiC Pro (courbe log ou plate), optiques Moment 18 mm, 60 mm et fisheye **[vérifié, 22]**. **High Flying Bird** (2019) : iPhone 8, Moondog 1,33x, FiLMiC Pro **[vérifié, 23]**. Aucune interview d'étalonneur trouvée pour ces deux films.
- **Raccord iPhone / cinéma (tests publiés)** : même après raccord couleur avec CineMatch ou FilmConvert, il reste le bruit, les blancs clippés et l'accentuation artificielle ; les noirs sont levés par le tone mapping dynamique ; « l'iPhone garde le look d'un petit capteur » **[pro, 14]**.
- **Publicités « Shot on iPhone »** et clips : aucune interview d'étalonneur sur le raccord ou le grain trouvée lors de cette recherche. À creuser par noms de maisons de postproduction.

Conclusion pratique : sur le seul cas récent bien documenté (*28 Years Later*), les professionnels n'ont pas ajouté du « grain de film » sur les plans VFX ; ils ont reproduit **le traitement du téléphone** (bruit, compression, défauts d'optique). C'est la méthode à suivre pour la Blackmagic et pour l'IA.

---

## Sources

1. Definition Magazine, « Production: 28 Years Later », 2025. https://definitionmagazine.com/features/production-28-years-later/
2. Nukepedia, DasGrain v1.8 (Fabian Holtz) et notes de cours UAL. https://www.nukepedia.com/gizmos/other/dasgrain · https://mngonzalezsanchez.myblog.arts.ac.uk/?p=764
3. sync. labs (Hadi), « The film grain problem », 07/07/2026. https://sync.so/blog/the-film-grain-problem
4. befores & afters (Ian Failes), « What it took to film with iPhones on 28 Years Later », 07/08/2026. https://beforesandafters.com/2026/08/07/what-it-took-to-film-with-iphones-on-28-years-later/
5. Filmmaker Magazine, entretien Anthony Dod Mantle (page en 403, non lue). https://filmmakermagazine.com/132924-interview-cinematographer-anthony-dod-mantle-28-years-later/
6. Forum Blackmagic, placement du Film Look Creator dans un workflow CST ; Mixing Light, présentation du Film Look Creator. https://forum.blackmagicdesign.com/viewtopic.php?p=1144897 · https://mixinglight.com/color-grading-tutorials/film-look-creator-resolvefx-overview-workflow
7. DaVinci Resolve Club, Film Look Creator. https://davinciresolveclub.com/davinci-resolve-film-look-creator/
8. 4K Shooters, firmware 7.3 et Gen 5 sur Pocket 4K/6K, 27/04/2021 ; BusinessWire, Pocket 6K G2, 23/06/2022. https://4kshooters.net/2021/04/27/blackmagic-camera-7-3-update-adds-gen-5-color-science-to-the-pocket-4k-and-6k-cameras · https://www.businesswire.com/news/home/20220623005759/en
9. Wolfcrow, Pocket 6K Pro. https://wolfcrow.com/important-quirks-and-features-of-the-blackmagic-pocket-cinema-camera-6k-pro-for-cinematography/
10. Forum Blackmagic, « Where can I download the Apple Log to Rec709 LUT cube? ». https://forum.blackmagicdesign.com/viewtopic.php?p=1052853
11. Gamut, « Apple Log vs Apple Log 2 in DaVinci Resolve ». https://gamut.io/apple-log-vs-apple-log-2-in-davinci-resolve-why-color-space-matters/
12. DaVinci Resolve Club, iPhone HDR vers SDR ; DPReview, iPhone 12 Dolby Vision et Resolve. https://davinciresolveclub.com/iphone-hdr-to-sdr-davinci-resolve/ · https://www.dpreview.com/forums/thread/4591722
13. Lightricks, docs « HDR Video (IC-LoRA) Beta » et « Working with EXR & HDR » ; ltx.io, AI video to HDR. https://docs.ltx.io/open-source-model/advanced-workflows/hdr-video-beta · https://docs.ltx.io/open-source-model/usage-guides/working-with-exr-hdr · https://ltx.io/model/capabilities/ai-video-to-hdr
14. No Film School, iPhone 12 Pro avec FilmConvert/CineMatch ; RedShark, ALEXA contre iPhone ; Noam Kroll, iPhone 13 contre ALEXA. https://nofilmschool.com/color-match-your-iphone-12-pro-different-camera-profiles-filmconvert-or-cinematch · https://www.redsharknews.com/alexa-vs-iphone-impressive-results-but-whats-the-catch · https://noamkroll.com/iphone-13-vs-arri-alexa-comparison-why-apples-color-science-is-so-impressive/
15. Newsshooter, FilmConvert Nitrate et CineMatch prennent en charge Apple Log, 12/10/2023. https://www.newsshooter.com/2023/10/12/filmconvert-nitrate-and-cinematch-now-support-apple-log/
16. Neat Video, « How does it work ». https://www.neatvideo.com/overview/how-does-it-work
17. Topaz Labs, réglages bruit, détail et grain ; forum Topaz « Video AI Workflow? ». https://www.topazlabs.com/learn/topaz-video-enhancements-2-noise-detail-focus-grain · https://community.topazlabs.com/t/video-ai-workflow/59211
18. invideo, « Should you upscale AI video before or after colour? » (fournisseur). https://invideo.io/faq/should-you-upscale-ai-video-before-or-after-colour/
19. Vindral, opérateur Film Grain. https://composer-docs.vindral.com/operators/operators-film-grain.html
20. American Cinematographer (ASC), « Tangerine: iPhone enables streetwise story ». https://theasc.com/articles/tangerine-iphone-enables-streetwise-story
21. Videomaker, « Tangerine dream ». https://www.videomaker.com/article/c02/18673-tangerine-dream-how-a-film-shot-on-an-iphone-made-it-to-the-big-screen/
22. Inverse, Unsane tourné sur iPhone 7 Plus, 2018. https://www.inverse.com/article/42571-unsane-steven-soderbergh-shot-with-iphone-7-plus
23. AppleInsider, High Flying Bird, 28/01/2019 ; Wikipédia, High Flying Bird. https://appleinsider.com/articles/19/01/28/soderbergh-returns-to-iphone-filmography-with-high-flying-bird · https://en.wikipedia.org/wiki/High_Flying_Bird
24. Newsshooter, « LensNode is now with Video Village », 23/07/2026 ; postPerspective, revue de LensNode, 03/2026. https://www.newsshooter.com/2026/07/23/lensnode-is-now-with-video-village-alongside-filmbox-scatter/ · https://postperspective.com/review-node-mills-lensnode-lens-simulation-plugin-for-resolve/

---

État vérifié au 15 octobre 2026. Texte sous licence [CC BY-SA 4.0](../LICENSE).
