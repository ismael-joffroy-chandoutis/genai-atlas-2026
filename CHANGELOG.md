# Journal des versions

Numéro de version = date de publication (vAAAA.MM.JJ, suffixe .N si plusieurs versions le même jour). La première ligne `## v…` de ce fichier donne la version affichée en tête de la page (scripts/build_atlas.py).

## v2026.11.07.1 · 07/11/2026

- Corrections, valeurs relues à la source le 07/11/2026. Prix fal : Kandinsky 6 Lite ramené à la seconde (0,032 et 0,034 $/s en 480p), FLUX 3 brouillon (0,06 $/s, prolongation 0,12 $/s), H3 Max et H3 Max Turbo (tarif de novembre). VibeMV daté de l'API PixVerse (24/09/2026). Classement Artificial Analysis relu pour GPT Image 2.5 Sunburst, 2.5 Flare et GPT Image 2 : Sunburst passe 3e, GPT Image 2.6 reste sans fiche. Six promotions expirées retirées, deux promotions fal en cours ajoutées. Les autres prix et scores restent ceux du 15/10/2026.

## v2026.11.07 · 07/11/2026

- Atlas interactif publié sur GitHub Pages (`docs/index.html`). Noms de machines et chemins locaux retirés des données. `open_weights` passé à `false` sur les cinq fiches d'API (MiniMax H3, LTX-2.3 Pro et Fast, LTX-2.5 Pro et Fast), qui décrivent un service ; les poids restent sur leurs propres fiches. Compteurs du README recalés sur les données (107 vidéo, 83 image, 51 plateformes, 1139 prix). Aucun autre chiffre modifié.

## v2026.10.16 · 16/10/2026

- Onglet « Par étape » : Écriture, Storyboard et animatique, Tournage, Effets et retouche de visage, Montage, Étalonnage, Son et voix, Agrandissement. Rangement automatique des modèles d'après leurs champs, corrections à la main et plateformes dans `data/stages.json`.
- Plateformes : ce que comprend l'offre (abonnement ou paiement à l'usage, lots illimités), notes plateforme par modèle. Higgsfield PLUS mesuré (coûts en crédits, illimité seulement sur le site, visages acceptés dans Seedance 2.5). Krea lu par son connecteur MCP. PiAPI ajouté.
- Modèle ajouté : OmniHuman V2 (fal, 0,105 $/s).
- Statut des modèles et des plateformes (actif, arrêté, racheté, pas encore sorti, bêta, à vérifier) dans `data/status.json`, avec date et source.
- Date de dernière vérification sur chaque fiche (date la plus récente de ses sources).
- Colonne « Visages acceptés » par plateforme et par modèle, avec source.
- Banc local du 16/10 : FLUX 3 Image Klein contre Qwen-Image 2.1 (et Turbo) sur RTX 5090 et RTX 4090.

## v2026.10.15 · 15/10/2026 (non taguée)

- Première version publiée : modèles vidéo et image variante par variante (entrées, sorties, prix, local), 1 138 prix, onglets 3D et audio, 50 plateformes (fiabilité, modération, abonnement contre API, promotions), intégrations locales (ComfyUI, Wan2GP, Pinokio, Draw Things, Maestro, Phosphene), colonnes Mac M5 Pro 64 Go et Mac Studio, vues Choisir et Comparer.
- Ajout du 16/10 à 01h17 dans la même série : FLUX 3 Image Klein (tests sur machine locale), Krea 3, Kling 4.0 sorti.
