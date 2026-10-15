#!/usr/bin/env python3
"""Construit data/audio-models.json (onglet AUDIO de l'atlas, état au 15/10/2026).
Toute valeur inconnue = None. Chaque ligne porte ses sources datées."""
import json, copy, sys

D = "2026-10-15"
OUT = sys.argv[1] if len(sys.argv) > 1 else "data/audio-models.json"

# --- Classements (URL lues le 15/10/2026) ---
AA_TTS = "https://artificialanalysis.ai/text-to-speech/leaderboard"
AA_CV = "https://artificialanalysis.ai/text-to-speech/leaderboard/controlled-voice"
AA_STT = "https://artificialanalysis.ai/speech-to-text"
AA_MV = "https://artificialanalysis.ai/music/leaderboard/vocals"
AA_MI = "https://artificialanalysis.ai/music/leaderboard/instrumental"
TTSA = "https://tts-agi-tts-arena-v2.hf.space/api/leaderboard"
OASR = "https://huggingface.co/datasets/hf-audio/open-asr-leaderboard-results/blob/main/english_short_latest.csv"
FAL = "https://api.fal.ai/v1/models/pricing"

K_TTS = "aa_speech_arena_provider_voice_elo"
K_CV = "aa_speech_arena_controlled_voice_elo"
K_TTSA = "hf_tts_arena_v2_elo"
K_STT = "aa_stt_wer_pct"
K_OASR = "open_asr_en_avg_wer_pct"
K_MV = "aa_music_vocals_elo"
K_MI = "aa_music_instrumental_elo"
LB_URL = {K_TTS: AA_TTS, K_CV: AA_CV, K_TTSA: TTSA, K_STT: AA_STT, K_OASR: OASR, K_MV: AA_MV, K_MI: AA_MI}


def S(url, typ="editeur", date=D):
    return {"url": url, "date": date, "type": typ}


def M(id, family, variant, vendor, country, task, released=None,
      ow=False, lic=None, api=None, app=None,
      scores=None, languages=None, fr="inconnu", fr_note=None,
      clone_s=None, zero_shot=None, consent="inconnu",
      emotions=None, latency=None, max_dur=None,
      unit=None, k=None, mn=None, track=None, platform=None, price_note=None,
      g5090=None, g4090=None, mac=None, tool=None, vram=None,
      celeb="inconnu", mod=None, pros=None, cons=None, src=None):
    scores = scores or {}
    sources = list(src or [])
    for key in scores:
        u = LB_URL[key]
        if not any(s["url"] == u for s in sources):
            sources.append(S(u, "independant"))
    return {
        "id": id, "family": family, "variant": variant, "vendor": vendor, "country": country,
        "task": task, "released": released,
        "access": {"open_weights": ow, "license": lic, "api": api, "consumer_app": app},
        "scores": scores,
        "languages": languages,
        "french_quality": fr, "french_note": fr_note,
        "clone": {"seconds_needed": clone_s, "zero_shot": zero_shot, "consent_check": consent},
        "emotions_control": emotions,
        "realtime_latency_ms": latency,
        "max_duration": max_dur,
        "price": {"unit": unit, "usd_per_1k_chars": k, "usd_per_min": mn, "usd_per_track": track,
                  "platform": platform, "note": price_note},
        "local": {"runs_on_rtx5090_32gb": g5090, "rtx4090_24gb": g4090, "mac_m5max_128gb": mac,
                  "tool": tool, "vram_note": vram},
        "moderation": {"voix_celebrites": celeb, "notes": mod},
        "pros": pros or [], "cons": cons or [],
        "sources": sources,
    }


R = []
A = R.append

# ============================ ELEVENLABS ============================
EL_MODELS = "https://elevenlabs.io/docs/overview/models"
EL_PRICE = "https://elevenlabs.io/pricing/api"
EL_V4 = "https://elevenlabs.io/fr/blog/eleven-v4"
EL_TL = "https://www.scriptbyai.com/elevenlabs-timeline/"
EL_CLONE = "https://elevenlabs.io/docs/product-guides/voices/voice-cloning"
EL_NOGO = "https://help.elevenlabs.io/hc/en-us/articles/22584327690897-What-are-No-Go-Voices"
EL_DUB = "https://elevenlabs.io/docs/product-guides/products/dubbing"
EL_SFX = "https://elevenlabs.io/docs/capabilities/sound-effects"
NOGO = "Liste « no-go voices » : bloque des personnalités politiques et des célébrités. Contournements documentés par 404 Media et le CCDH en 2024."
el_src = [S(EL_MODELS), S(EL_PRICE), S(EL_NOGO)]

A(M("elevenlabs-v4", "Eleven v4", "Eleven v4", "ElevenLabs", "US", "tts", "2026-09-28",
    api=True, app=True, scores={K_TTS: 1326, K_CV: 1157},
    languages="90+ langues", fr_note="Français pris en charge, aucune mesure propre au français publiée.",
    clone_s=10, zero_shot=True, consent="aucun",
    emotions="Balises entre crochets en langage libre ([excited], [laughs], [said angrily in French accent]).",
    max_dur="10 000 caractères par requête (environ 10 min)",
    unit="1k_chars", k=0.08, platform="ElevenLabs API",
    celeb="bloque", mod=NOGO,
    pros=["Premier du Speech Arena d'Artificial Analysis avec v4 Turbo (égalité statistique)", "Clonage instantané à partir de 10 s selon l'éditeur", "Direction de jeu par balises libres"],
    cons=["Deux fois plus cher que v4 Turbo", "Aucune mesure publiée sur le français"],
    src=el_src + [S(EL_V4), S(EL_TL, "independant")]))

A(M("elevenlabs-v4-turbo", "Eleven v4", "Eleven v4 Turbo", "ElevenLabs", "US", "tts", "2026-09-28",
    api=True, app=True, scores={K_TTS: 1328, K_CV: 1159},
    languages="90+ langues", clone_s=10, zero_shot=True, consent="aucun",
    emotions="Balises entre crochets.", latency=100,
    unit="1k_chars", k=0.04, platform="ElevenLabs API",
    price_note="Latence médiane d'inférence environ 100 ms, premier son environ 150 ms en WebSocket hors réseau (éditeur).",
    celeb="bloque", mod=NOGO,
    pros=["Score le plus haut du Speech Arena AA au 15/10/2026", "Temps réel, moitié prix de v4"],
    cons=["Limite de caractères par requête non publiée"],
    src=el_src + [S(EL_V4)]))

A(M("elevenlabs-v3", "Eleven v3", "Eleven v3", "ElevenLabs", "US", "tts", "2026-02-02",
    api=True, app=True, scores={K_TTS: 1175, K_CV: 1072, K_TTSA: 1496},
    languages="70+ langues", clone_s=None, zero_shot=True, consent="aucun",
    emotions="Jeu dramatique, balises audio.", max_dur="5 000 caractères par requête (environ 5 min)",
    unit="1k_chars", k=0.08, platform="ElevenLabs API",
    price_note="AA affiche 100 $ le million de caractères, la page tarifaire API affiche 0,08 $ les 1 000.",
    celeb="bloque", mod=NOGO,
    pros=["Très expressif, bien installé dans les outils"], cons=["Dépassé par v4 au même prix", "Requêtes limitées à 5 000 caractères"],
    src=el_src + [S(EL_TL, "independant")]))

A(M("elevenlabs-v3-conversational", "Eleven v3", "v3 Conversational", "ElevenLabs", "US", "tts", "2026-02-10",
    api=True, app=True, scores={K_TTS: 1207, K_CV: 1059},
    languages="70+ langues", emotions="Balises audio.", latency=280,
    unit="1k_chars", k=0.04, platform="ElevenLabs API", celeb="bloque", mod=NOGO,
    pros=["Version temps réel de v3 pour les agents"], cons=["Moins bien classé que v4 Turbo au même prix"],
    src=el_src + [S(EL_TL, "independant")]))

A(M("elevenlabs-multilingual-v2", "Eleven Multilingual", "Multilingual v2", "ElevenLabs", "US", "tts", "2023-08",
    api=True, app=True, scores={K_TTS: 1095, K_CV: 997, K_TTSA: 1504},
    languages="29 langues", emotions="Expression émotionnelle, pas de balises.",
    max_dur="10 000 caractères par requête (environ 10 min)",
    unit="1k_chars", k=0.08, platform="ElevenLabs API", celeb="bloque", mod=NOGO,
    pros=["Le plus stable sur les textes longs selon l'éditeur"], cons=["Génération précédente, même prix que v4"],
    src=el_src))

A(M("elevenlabs-flash-v2-5", "Eleven Flash", "Flash v2.5", "ElevenLabs", "US", "tts", "2024-12",
    api=True, app=True, scores={K_TTS: 1077, K_CV: 986, K_TTSA: 1505},
    languages="32 langues", latency=75, max_dur="40 000 caractères par requête (environ 40 min)",
    unit="1k_chars", k=0.04, platform="ElevenLabs API", celeb="bloque", mod=NOGO,
    pros=["Latence 75 ms hors réseau", "Très longues requêtes"], cons=["Moins expressif que v4 Turbo au même prix"],
    src=el_src))

A(M("elevenlabs-turbo-v2-5", "Eleven Turbo", "Turbo v2.5", "ElevenLabs", "US", "tts", "2024-07",
    api=True, app=True, scores={K_TTS: 1098, K_CV: 972, K_TTSA: 1504},
    languages="32 langues", unit="1k_chars", k=0.04, platform="ElevenLabs API", celeb="bloque", mod=NOGO,
    pros=[], cons=["Déprécié : remplacé par Flash v2.5"], src=el_src))

A(M("elevenlabs-instant-voice-clone", "ElevenLabs Voice Cloning", "Instant Voice Clone (IVC)", "ElevenLabs", "US", "voice_clone", None,
    api=True, app=True, languages="Celles du modèle de synthèse choisi",
    clone_s=10, zero_shot=True, consent="aucun",
    price_note="Inclus dans les forfaits, coût = synthèse du modèle utilisé.",
    celeb="bloque", mod=NOGO + " Aucune vérification d'identité décrite pour l'IVC dans la documentation.",
    pros=["10 s suffisent avec v4 (éditeur)", "1 à 2 min recommandées pour la meilleure qualité"],
    cons=["Plus de 2 à 3 min n'aide plus et peut nuire à la stabilité (doc)", "Pas de vérification que la voix appartient à l'utilisateur"],
    src=[S(EL_CLONE), S(EL_V4), S(EL_NOGO)]))

A(M("elevenlabs-professional-voice-clone", "ElevenLabs Voice Cloning", "Professional Voice Clone (PVC)", "ElevenLabs", "US", "voice_clone", None,
    api=True, app=True, languages="Celles du modèle de synthèse choisi",
    clone_s=1800, zero_shot=False, consent="captcha_vocale",
    price_note="Forfait Creator (22 $/mois) minimum : 1 emplacement PVC ; Scale 3 ; Business 10.",
    platform="ElevenLabs (abonnement)", celeb="bloque",
    mod="Vérification obligatoire : lecture à voix haute de phrases au micro. On ne peut cloner que sa propre voix, « même avec son consentement, vous ne pouvez pas cloner la voix de quelqu'un d'autre ». La personne crée son PVC et le partage par lien.",
    pros=["Meilleure ressemblance (30 min à 3 h d'audio)", "Partage contrôlé par le titulaire de la voix"],
    cons=["Entraînement de 3 à 24 h", "Impossible de cloner un comédien sans qu'il ouvre lui-même le compte"],
    src=[S(EL_CLONE), S(EL_PRICE)]))

A(M("elevenlabs-voice-changer", "ElevenLabs Voice Changer", "Multilingual STS v2", "ElevenLabs", "US", "speech_to_speech", "2023-11-22",
    api=True, app=True, languages="29 langues (eleven_multilingual_sts_v2)",
    emotions="Reprend le jeu de la prise source.", max_dur="10 000 caractères pour la version anglaise (environ 10 min)",
    unit="min", mn=0.12, platform="ElevenLabs API", celeb="bloque", mod=NOGO,
    pros=["Garde l'intention et le rythme d'une prise jouée", "Utile pour remplacer une voix témoin par une voix clonée consentie"],
    cons=["Basé sur la génération v2"], src=[S(EL_MODELS), S(EL_PRICE), S(EL_TL, "independant")]))

A(M("elevenlabs-dubbing-v2", "ElevenLabs Dubbing", "Dubbing v2", "ElevenLabs", "US", "dubbing", "2026-05-28",
    api=True, app=True, languages="90+ langues",
    clone_s=None, zero_shot=True, consent="inconnu",
    emotions="Ressemblance au locuteur réglable de 0 à 10 (défaut 7).",
    max_dur="180 min et 2 Go par fichier, vidéo jusqu'en 4K",
    unit="min", mn=2.20, platform="ElevenLabs API", price_note="Facturé par langue cible. API depuis le 06/08/2026.",
    pros=["Clone chaque locuteur d'origine", "Fichier unique sans perte"],
    cons=["Pas de synchronisation labiale", "Sortie en un seul fichier stéréo, pas de pistes séparées", "Édition du transcript par API réservée à l'offre Enterprise"],
    src=[S(EL_DUB), S(EL_PRICE), S(EL_TL, "independant")]))

A(M("elevenlabs-dubbing-v1", "ElevenLabs Dubbing", "Dubbing v1 (Dubbing Studio)", "ElevenLabs", "US", "dubbing", None,
    api=True, app=True, languages="90+ langues",
    unit="min", mn=0.50, platform="ElevenLabs API", price_note="0,33 $/min avec filigrane, 0,50 $/min sans.",
    pros=["Exporte MP4, AAC, AAF, SRT et une piste WAV par locuteur : utilisable en montage son"],
    cons=["Studio en maintenance (correctifs critiques seulement)", "Sortie mono"],
    src=[S(EL_DUB), S(EL_PRICE)]))

for vid, var, rel, mv, mi in [("elevenlabs-music-v2-5", "Music v2.5", "2026-09-11", 1012, 1001),
                              ("elevenlabs-music-v2", "Music v2", "2026-05-26", 999, 1011),
                              ("elevenlabs-music-v1", "Eleven Music (v1)", "2025-08-05", 999, 1021)]:
    A(M(vid, "Eleven Music", var, "ElevenLabs", "US", "music", rel,
        api=True, app=True, scores={K_MV: mv, K_MI: mi},
        languages="« en, es, de, ja et autres » (doc)", unit="min", mn=0.15, platform="ElevenLabs API",
        pros=["Avec ou sans voix, édition par section (v2 et plus)"] + (["Plus récent modèle musique d'ElevenLabs"] if vid.endswith("2-5") else []),
        cons=["À environ 130 points de Suno v6 en vocal sur l'arène AA"] if mv > 1000 else (["Dépassé par v2 et v2.5 selon l'éditeur"] if vid.endswith("v1") else []),
        src=[S(EL_MODELS), S(EL_PRICE), S(EL_TL, "independant")]))

A(M("elevenlabs-sfx-v2", "ElevenLabs Sound Effects", "SFX v2 (eleven_text_to_sound_v2)", "ElevenLabs", "US", "sfx", "2025-09-02",
    api=True, app=True, max_dur="30 s par génération (0,1 à 30 s)",
    unit="min", mn=0.12, platform="ElevenLabs API", price_note="Dans l'app : 40 crédits par seconde quand la durée est fixée.",
    pros=["Boucles sans couture (ex. 30 s de pluie)", "WAV 48 kHz hors boucle"], cons=["30 s maximum"],
    src=[S(EL_SFX), S(EL_PRICE), S(EL_TL, "independant")]))

A(M("elevenlabs-scribe-v2", "ElevenLabs Scribe", "Scribe v2", "ElevenLabs", "US", "stt", "2026-01-09",
    api=True, app=True, scores={K_STT: 2.2, K_OASR: 5.37},
    languages="90+ langues", unit="min", mn=0.00367, platform="ElevenLabs API",
    price_note="0,22 $ l'heure.",
    pros=["Diarisation jusqu'à 32 locuteurs, 1 000 mots-clés", "Parmi les meilleurs WER mesurés par AA"],
    cons=["Pas de poids ouverts"],
    src=[S(EL_MODELS), S(EL_PRICE), S(EL_TL, "independant")]))

A(M("elevenlabs-scribe-v2-realtime", "ElevenLabs Scribe", "Scribe v2 Realtime", "ElevenLabs", "US", "stt", "2025-11-11",
    api=True, app=True, languages="90+ langues", latency=150,
    unit="min", mn=0.0065, platform="ElevenLabs API", price_note="0,39 $ l'heure.",
    pros=["Transcription en direct, environ 150 ms"], cons=[],
    src=[S(EL_MODELS), S(EL_PRICE), S(EL_TL, "independant")]))

# ============================ OPENAI ============================
OA_PRICE = "https://developers.openai.com/api/docs/pricing"
OA_CV = "https://developers.openai.com/api/docs/guides/custom-voices"
OA_RT2 = "https://developers.openai.com/api/docs/models/gpt-realtime-2"
OA_NEWS = "https://handyai.substack.com/p/model-drop-gpt-realtime-2"
OA_MOD = "Voix personnalisées réservées aux clients éligibles (contact commercial), avec enregistrement de consentement lu mot pour mot par la même personne. Échantillon de 30 s maximum, 20 voix maximum par organisation."

A(M("openai-gpt-4o-mini-tts", "OpenAI TTS", "gpt-4o-mini-tts", "OpenAI", "US", "tts", None,
    api=True, app=False, emotions="Consignes de style en langage naturel.",
    clone_s=None, zero_shot=True, consent="verification_identite",
    unit="tokens", platform="OpenAI API",
    price_note="0,60 $ le million de tokens texte en entrée, 12 $ le million de tokens audio en sortie. Aucun modèle TTS plus récent sur la page tarifaire.",
    mod=OA_MOD,
    pros=["Voix pilotable par instructions", "Voix personnalisées possibles avec consentement enregistré"],
    cons=["Absent des classements AA au 15/10/2026", "Voix personnalisées non ouvertes à tous"],
    src=[S(OA_PRICE), S(OA_CV)]))

A(M("openai-tts-1-hd", "OpenAI TTS", "tts-1-hd", "OpenAI", "US", "tts", "2023-11",
    api=True, scores={K_TTS: 1104}, unit="1k_chars", k=0.03, platform="OpenAI API",
    pros=["Simple et stable"], cons=["Ancienne génération, voix fixes"], src=[S(OA_PRICE)]))

A(M("openai-gpt-realtime-2", "OpenAI Realtime", "gpt-realtime-2", "OpenAI", "US", "realtime_dialogue", "2026-05-07",
    api=True, scores={K_TTS: 1078}, languages=None, clone_s=None, zero_shot=True, consent="verification_identite",
    unit="tokens", platform="OpenAI API",
    price_note="Audio : 32 $ entrée, 64 $ sortie par million de tokens. Texte : 4 $ et 24 $. Contexte 128 000 tokens.",
    mod=OA_MOD,
    pros=["Parole à parole avec raisonnement de classe GPT-5 (presse)", "Entrée image"],
    cons=["Prix au token difficile à convertir en minutes", "Score TTS AA moyen (1078)"],
    src=[S(OA_PRICE), S(OA_RT2), S(OA_CV), S(OA_NEWS, "independant")]))

A(M("openai-gpt-realtime-mini", "OpenAI Realtime", "gpt-realtime-mini", "OpenAI", "US", "realtime_dialogue", None,
    api=True, unit="tokens", platform="OpenAI API",
    price_note="Audio : 10 $ entrée, 20 $ sortie par million de tokens.",
    pros=["Environ trois fois moins cher que gpt-realtime-2 en audio"], cons=[], src=[S(OA_PRICE)]))

A(M("openai-gpt-live-1", "OpenAI GPT-Live", "gpt-live-1", "OpenAI", "US", "realtime_dialogue", None,
    api=True, clone_s=5, zero_shot=True, consent="verification_identite",
    unit="min", mn=0.05, platform="OpenAI API", price_note="Facturé à la seconde ; modèle de fond et outils facturés en plus.",
    mod="Voix personnalisées « avec accents anglais » : consentement et échantillon de la même personne, au moins 5 s de parole réelle (10 à 30 s conseillées).",
    pros=["Prix à la minute lisible"], cons=["Voix personnalisées limitées aux accents anglais"],
    src=[S(OA_PRICE), S(OA_CV)]))

A(M("openai-gpt-realtime-translate", "OpenAI Realtime", "gpt-realtime-translate", "OpenAI", "US", "dubbing", "2026-05-07",
    api=True, languages="70+ langues en entrée, 13 en sortie",
    unit="min", mn=0.034, platform="OpenAI API",
    pros=["Traduction parlée en direct à 2,04 $ l'heure"], cons=["Interprétation en direct, pas un doublage monté"],
    src=[S(OA_PRICE), S(OA_NEWS, "independant")]))

A(M("openai-gpt-transcribe", "OpenAI Transcribe", "gpt-transcribe", "OpenAI", "US", "stt", None,
    api=True, scores={K_STT: 3.3, K_OASR: 6.38}, unit="min", mn=0.0045, platform="OpenAI API",
    pros=["Meilleur WER OpenAI sur AA"], cons=[], src=[S(OA_PRICE)]))
A(M("openai-gpt-4o-transcribe", "OpenAI Transcribe", "gpt-4o-transcribe", "OpenAI", "US", "stt", None,
    api=True, scores={K_STT: 4.0}, unit="min", mn=0.006, platform="OpenAI API", src=[S(OA_PRICE)]))
A(M("openai-gpt-4o-mini-transcribe", "OpenAI Transcribe", "gpt-4o-mini-transcribe", "OpenAI", "US", "stt", None,
    api=True, scores={K_STT: 4.5}, unit="min", mn=0.003, platform="OpenAI API", src=[S(OA_PRICE)]))
A(M("openai-gpt-realtime-whisper", "OpenAI Transcribe", "gpt-realtime-whisper", "OpenAI", "US", "stt", "2026-05-07",
    api=True, unit="min", mn=0.017, platform="OpenAI API", pros=["Transcription en flux"], src=[S(OA_PRICE), S(OA_NEWS, "independant")]))

WH = "https://huggingface.co/openai/whisper-large-v3-turbo"
A(M("openai-whisper-large-v3-turbo", "Whisper", "large-v3-turbo", "OpenAI", "US", "stt", "2024-10-01",
    ow=True, lic="MIT (commercial autorisé)", api=True,
    scores={K_STT: 4.6, K_OASR: 8.39}, languages="Multilingue ; résultats forts dans environ 10 langues selon la fiche",
    unit="min", mn=0.00067, platform="Groq (via AA)",
    price_note="AA : 0,67 $ les 1 000 minutes chez Groq, 0,50 $ pour Wizper (fal).",
    g5090=True, g4090=True, mac=True, tool="faster-whisper, whisper.cpp, MLX (mlx-community/whisper-large-v3-turbo)",
    vram="Déduit de la taille (environ 0,8 milliard de paramètres), non mesuré ici.",
    pros=["Libre et commercial", "Tourne partout, y compris sur Mac"],
    cons=["Hallucinations et répétitions connues (fiche)", "WER Open ASR moins bon que Parakeet v3 ou Canary"],
    src=[S(WH)]))

A(M("openai-whisper-large-v3", "Whisper", "large-v3", "OpenAI", "US", "stt", "2023-11",
    ow=True, lic="MIT (commercial autorisé)", api=True, scores={K_STT: 4.1, K_OASR: 7.84},
    unit="min", mn=0.00115, platform="fal (via AA)", g5090=True, g4090=True, mac=True, tool="faster-whisper, whisper.cpp, MLX",
    vram="Déduit de la taille (environ 1,5 milliard de paramètres), non mesuré ici.",
    pros=["Référence historique"], cons=["Plus lent que turbo, dépassé en WER"], src=[S("https://huggingface.co/openai/whisper-large-v3")]))

# ============================ GOOGLE ============================
G_PRICE = "https://ai.google.dev/gemini-api/docs/pricing"
G_TTS = "https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts"
G_TTS_NEWS = "https://datanorth.ai/news/google-releases-gemini-3-8-flash-tts"
G_LYRIA = "https://invideo.io/blog/lyria-ai-music-generator/"

A(M("google-gemini-3-8-flash-tts", "Gemini TTS", "Gemini 3.8 Flash TTS", "Google", "US", "tts", "2026-09-23",
    api=True, app=True, scores={K_TTS: 1273, K_CV: 1048}, languages="130+ langues, détection automatique",
    clone_s=None, zero_shot=True, consent="inconnu",
    emotions="Directions de style par réplique et balises (<laugh>, <sigh>, <short pause>). Dialogues à plusieurs locuteurs.",
    max_dur="8 192 tokens en entrée, 16 384 en sortie",
    unit="tokens", platform="Gemini API",
    price_note="0,50 $ le million de tokens texte, 9 $ le million de tokens audio jusqu'au 31/12/2026 ; 18 $ à partir du 01/01/2027. Batch : moitié prix.",
    pros=["5e du Speech Arena AA, très bon rapport qualité-prix", "Réplication de voix et voix dessinées par description", "Dialogues multi-voix natifs"],
    cons=["Prix audio doublé au 01/01/2027", "Conditions de la réplication de voix non détaillées dans nos sources"],
    src=[S(G_TTS), S(G_PRICE), S(G_TTS_NEWS, "independant")]))

A(M("google-gemini-3-8-flash-lite-tts", "Gemini TTS", "Gemini 3.8 Flash-Lite TTS", "Google", "US", "tts", "2026-09-22",
    api=True, scores={K_TTS: 1247, K_CV: 1057}, languages="101 langues (presse)",
    unit="tokens", platform="Gemini API",
    price_note="0,50 $ le million de tokens texte, 6 $ le million de tokens audio jusqu'au 31/12/2026, 12 $ ensuite.",
    pros=["Variante la plus rapide, devant Flash en voix contrôlée"], cons=["Prix doublé en 2027"],
    src=[S(G_PRICE), S(G_TTS_NEWS, "independant")]))

A(M("google-gemini-3-1-flash-tts", "Gemini TTS", "Gemini 3.1 Flash TTS (préversion)", "Google", "US", "tts", "2026-04",
    api=True, scores={K_TTS: 1212}, unit="tokens", platform="Gemini API",
    price_note="1 $ texte, 20 $ audio par million de tokens.",
    cons=["Plus cher et moins bien classé que 3.8 Flash"], src=[S(G_PRICE)]))

A(M("google-chirp-3-hd", "Google Cloud TTS", "Chirp 3: HD", "Google", "US", "tts", "2025-03",
    api=True, scores={K_TTS: 1060}, unit="1k_chars", k=0.03, platform="Google Cloud (prix relevé par AA)",
    pros=["Voix Google Cloud de production"], cons=["Nettement sous Gemini 3.8 TTS au classement"],
    src=[S("https://cloud.google.com/text-to-speech/pricing")]))

A(M("google-gemini-3-8-live", "Gemini Live", "Gemini 3.8 Live", "Google", "US", "realtime_dialogue", None,
    api=True, app=True, unit="min", mn=0.023, platform="Gemini API",
    price_note="Entrée audio 0,005 $/min, sortie audio 0,018 $/min (3 $ et 12 $ par million de tokens).",
    pros=["Prix à la minute bas", "Ancrage dans la recherche Google"], cons=["Pas de classement indépendant trouvé"],
    src=[S(G_PRICE)]))

A(M("google-gemini-3-5-live-translate", "Gemini Live", "Gemini 3.5 Live Translate", "Google", "US", "dubbing", None,
    api=True, unit="min", mn=0.0368, platform="Gemini API",
    price_note="Entrée 0,0053 $/min, sortie audio 0,0315 $/min.",
    cons=["Interprétation en direct, pas un doublage monté"], src=[S(G_PRICE)]))

A(M("google-gemini-3-5-transcribe", "Gemini Transcribe", "Gemini 3.5 Transcribe", "Google", "US", "stt", None,
    api=True, scores={K_STT: 2.6}, unit="min", mn=0.005, platform="Gemini API",
    price_note="0,003 $/min audio en entrée + 0,002 $/min texte en sortie.",
    pros=["WER AA 2,6 %"], cons=[], src=[S(G_PRICE)]))

A(M("google-lyria-3-5", "Lyria", "Lyria 3.5", "Google", "US", "music", None,
    api=True, scores={K_MV: 1052, K_MI: 1078}, max_dur="Jusqu'à 3 min (presse)",
    unit="track", track=0.08, platform="Gemini API", mod="Filigrane SynthID sur toutes les pistes.",
    pros=["3e ex aequo en instrumental sur l'arène AA"], cons=["Date de sortie non trouvée", "Environ 95 points sous Suno v6 en vocal"],
    src=[S(G_PRICE), S(G_LYRIA, "independant")]))

A(M("google-lyria-3-pro", "Lyria", "Lyria 3 Pro (préversion)", "Google", "US", "music", "2026-03-25",
    api=True, scores={K_MV: 1051, K_MI: 1080}, languages="Paroles dans la langue du prompt",
    max_dur="184 s", unit="track", track=0.08, platform="Gemini API, Vertex AI",
    mod="Filigrane SynthID.", pros=["Paroles synchronisées, instrumental au niveau de Lyria 3.5"], cons=["Morceaux de 3 min maximum"],
    src=[S(G_PRICE), S(G_LYRIA, "independant")]))

A(M("google-lyria-3-clip", "Lyria", "Lyria 3 Clip (préversion)", "Google", "US", "music", "2026-03-25",
    api=True, max_dur="30 s", unit="track", track=0.04, platform="Gemini API, Vertex AI", mod="Filigrane SynthID.",
    pros=["Courts motifs à 0,04 $"], cons=["30 s maximum"], src=[S(G_PRICE), S(G_LYRIA, "independant")]))

A(M("google-lyria-2", "Lyria", "Lyria 2 (lyria-002)", "Google", "US", "music", "2025-05-20",
    api=True, scores={K_MI: 926}, max_dur="30 s", platform="Vertex AI", mod="Filigrane SynthID.",
    cons=["Orienté instrumental, 30 s", "Largement dépassé par Lyria 3"], src=[S(G_LYRIA, "independant")]))

A(M("google-lyria-realtime", "Lyria", "Lyria RealTime", "Google", "US", "music", None,
    api=None, cons=["Modèle de génération musicale en flux interactif, presque rien de documenté dans nos sources (prix absent de la page tarifaire Gemini)"],
    src=[S(G_LYRIA, "independant"), S(G_PRICE)]))

# ============================ MINIMAX ============================
MM_NEWS = "https://www.gradually.ai/en/ai-models/minimax-speech-2-8/"
MM_RUN = "https://runware.ai/models/minimax-speech-2-8"
MM3 = "https://huggingface.co/MiniMaxAI/MiniMax-Music3"
A(M("minimax-speech-2-8-hd", "MiniMax Speech", "Speech 2.8 HD", "MiniMax", "CN", "tts", "2026-01-23",
    api=True, app=True, scores={K_TTS: 1173, K_CV: 1020, K_TTSA: 1535}, languages="40+ langues (presse, chiffres divergents)",
    clone_s=10, zero_shot=True, consent="inconnu", emotions="Balises sonores ((laughs), (sighs)).",
    unit="1k_chars", k=0.10, platform="MiniMax API, Runware",
    pros=["7e de la TTS Arena V2", "Clonage à partir d'environ 10 s"], cons=["Cher (0,10 $ les 1 000 caractères)"],
    src=[S(MM_NEWS, "independant"), S(MM_RUN, "independant")]))
A(M("minimax-speech-2-8-turbo", "MiniMax Speech", "Speech 2.8 Turbo", "MiniMax", "CN", "tts", "2026-01-23",
    api=True, app=True, scores={K_TTS: 1151, K_CV: 1021, K_TTSA: 1519}, clone_s=10, zero_shot=True,
    unit="1k_chars", k=0.06, platform="MiniMax API, Runware",
    pros=["Même voix clonée que HD, moins cher"], src=[S(MM_NEWS, "independant"), S(MM_RUN, "independant")]))
A(M("minimax-speech-2-6-hd", "MiniMax Speech", "Speech 2.6 HD", "MiniMax", "CN", "tts", "2025-10",
    api=True, scores={K_TTS: 1129, K_TTSA: 1501}, unit="1k_chars", k=0.10, platform="MiniMax API (prix relevé par AA)",
    cons=["Remplacé par 2.8"], src=[]))
A(M("minimax-voice-clone", "MiniMax Speech", "Voice Cloning", "MiniMax", "CN", "voice_clone", None,
    api=True, app=True, clone_s=10, zero_shot=True, consent="inconnu",
    unit="voix", platform="MiniMax API", price_note="1,50 $ par voix créée selon deux sources, 3 $ selon une troisième (ancienne génération).",
    pros=["Coût fixe par voix, puis prix de synthèse"], cons=["Politique de consentement non trouvée"],
    src=[S(MM_NEWS, "independant"), S("https://invideo.io/blog/minimax-ai-voice-models/", "independant")]))
A(M("minimax-music-3", "MiniMax Music", "Music 3.0 (poids ouverts)", "MiniMax", "CN", "music", "2026-08-07",
    ow=True, lic="MiniMax-Music3 Community License : commercial autorisé avec mention « MiniMax-Music3 », accord écrit au-delà de 20 M$ de chiffre d'affaires annuel",
    api=True, scores={K_MV: 1000, K_MI: 1000}, languages=None,
    max_dur="5 min, WAV stéréo 32 kHz", emotions="Légende structurée (BPM, tonalité, voix, arrangement) et balises de sections dans les paroles.",
    g5090=True, g4090=True, mac=None, tool="diffusers, SGLang-Omni ; GGUF communautaires",
    vram="Fiche : tient sous 24 Go en pleine précision, environ 22 Go avec déchargement CPU, 8 Go en streaming couche par couche (plus lent).",
    pros=["Meilleur modèle musical à poids ouverts de l'arène AA (ancre 1000)", "Chansons complètes de 5 min", "Licence commerciale"],
    cons=["Environ 145 points sous Suno v6"], src=[S(MM3), S(MM3 + "/blob/main/LICENSE")]))
A(M("minimax-music-2-6", "MiniMax Music", "Music 2.6", "MiniMax", "CN", "music", None,
    api=True, scores={K_MV: 998, K_MI: 1001}, cons=["Égal à Music 3.0 ouvert sur l'arène AA"], src=[]))

# ============================ FISH AUDIO ============================
F_D3 = "https://huggingface.co/fishaudio/drama-3"
F_S2 = "https://huggingface.co/fishaudio/s2-pro"
FISH_LIC = "Fish Audio Research License : recherche et non commercial gratuits, commercial sur licence séparée"
A(M("fish-audio-drama-3", "Fish Audio Drama", "Drama 3 (préversion)", "Fish Audio", "US", "tts", "2026-10-01",
    ow=True, lic=FISH_LIC, api=True, app=True, scores={K_TTS: 1242, K_CV: 1055},
    languages="80+ langues listées dans la fiche, dont le français",
    clone_s=3.9, zero_shot=True, consent="inconnu",
    emotions="Balises ponctuelles, contrôle en langage naturel, jusqu'à 16 personnages dans un même texte, édition par continuation.",
    latency=89, unit="1k_chars", k=0.015, platform="Fish Audio API (prix relevé par AA)",
    g5090=None, g4090=None, mac=None, tool="SGLang-Omni",
    vram="35 milliards de paramètres (3 actifs), experts MoE en FP8 : non mesuré ici, probablement au-delà de 32 Go.",
    pros=["10e du Speech Arena AA, le mieux classé des modèles à poids publiés", "Scènes à plusieurs personnages, textes longs", "Clonage sur un extrait de 3,9 s dans l'exemple de la fiche", "Premier son en 88,9 ms médian sur H200 (éditeur)"],
    cons=["Licence non commerciale pour les poids", "Trop gros pour une carte grand public sans quantification"],
    src=[S(F_D3)]))
A(M("fish-audio-s2-1-pro", "Fish Audio S2", "S2.1 Pro", "Fish Audio", "US", "tts", "2026-10",
    ow=None, api=True, app=True, scores={K_TTS: 1190, K_CV: 1017}, unit="1k_chars", k=0.015,
    platform="Fish Audio API (prix relevé par AA)", cons=["Poids ouverts non trouvés pour la version 2.1"], src=[]))
A(M("fish-audio-s2-pro", "Fish Audio S2", "S2 Pro", "Fish Audio", "US", "tts", "2026-03",
    ow=True, lic=FISH_LIC, api=True, app=True, scores={K_TTS: 1116, K_CV: 1002, K_TTSA: 1515},
    languages="80+ langues ; palier 1 : ja, en, zh ; palier 2 : ko, es, pt, ar, ru, fr, de",
    fr="moyenne", fr_note="Français en palier 2 sur 3 selon l'éditeur (pas une mesure).",
    zero_shot=True, emotions="Balises libres au mot près ([whisper in small voice], [pitch up]), plus de 15 000 balises.",
    latency=100, unit="1k_chars", k=0.015, platform="Fish Audio API (prix relevé par AA)",
    g5090=True, g4090=True, mac=True, tool="fish-speech, SGLang ; MLX (mlx-community/fish-audio-s2-pro-8bit)",
    vram="4,4 milliards de paramètres (4 B + 0,4 B) : tient sur 24 Go en bf16 par déduction, non mesuré ici.",
    pros=["Contrôle d'émotion le plus fin des modèles ouverts", "Portage Mac MLX"], cons=["Non commercial sans licence"],
    src=[S(F_S2)]))
A(M("fish-openaudio-s1", "OpenAudio", "OpenAudio S1", "Fish Audio", "US", "tts", "2025-06",
    api=True, app=True, scores={K_TTS: 1080, K_CV: 1000, K_TTSA: 1504}, unit="1k_chars", k=0.015,
    platform="Fish Audio API (prix relevé par AA)", cons=["Remplacé par S2"], src=[]))
A(M("fish-openaudio-s1-mini", "OpenAudio", "OpenAudio S1 Mini", "Fish Audio", "US", "tts", "2025-05-31",
    ow=True, lic="CC BY-NC-SA 4.0 (non commercial)", api=True, scores={K_TTS: 1043, K_CV: 1002},
    g5090=True, g4090=True, tool="fish-speech", vram="Petit modèle, non mesuré ici.",
    cons=["Non commercial"], src=[S("https://huggingface.co/fishaudio/s1-mini")]))

# ============================ CARTESIA / HUME / INWORLD / QWEN / AUTRES API ============================
A(M("cartesia-sonic-3-6", "Cartesia Sonic", "Sonic 3.6 (bêta)", "Cartesia", "US", "tts", "2026-08-27",
    api=True, scores={K_TTS: 1283, K_CV: 1146}, languages="44 langues, 61 variantes régionales",
    clone_s=10, zero_shot=True, latency=90, unit="1k_chars", k=0.049, platform="Cartesia API (prix relevé par AA)",
    price_note="Latence : moins de 90 ms au premier son selon l'éditeur. 10 s de clonage : chiffre de sites tiers sur Sonic en général.",
    pros=["4e du Speech Arena AA", "Très faible latence"], cons=["Bêta"],
    src=[S("https://www.plushcap.com/content/cartesia/blog/cartesia-introducing-sonic-36", "independant"),
         S("https://menastartupdigest.com/?p=49615", "independant")]))
A(M("cartesia-sonic-3-5", "Cartesia Sonic", "Sonic 3.5", "Cartesia", "US", "tts", "2026-05",
    api=True, scores={K_TTS: 1191, K_CV: 1116}, unit="1k_chars", k=0.049, platform="Cartesia API (prix relevé par AA)", src=[]))

HUME = "https://dev.hume.ai/docs/text-to-speech-tts/overview.md"
A(M("hume-octave-2", "Hume Octave", "Octave 2 (préversion)", "Hume AI", "US", "tts", "2025-10",
    api=True, app=True, scores={K_TTS: 1050},
    languages="11 langues : anglais, japonais, coréen, espagnol, français, portugais, italien, allemand, russe, hindi, arabe",
    clone_s=15, zero_shot=True, emotions="Jeu dirigé en langage naturel (« acting instructions »).",
    latency=100, unit="1k_chars", k=0.0875, platform="Hume API (prix relevé par AA)",
    price_note="15 s de clonage : chiffre de source secondaire.",
    pros=["Direction de jeu par description"], cons=["Cher et loin derrière au classement AA"],
    src=[S(HUME), S("https://hume.ai/blog/octave-2-launch"), S("https://aiwiki.ai/wiki/hume_octave_2", "independant")]))
A(M("hume-octave-1", "Hume Octave", "Octave TTS", "Hume AI", "US", "tts", "2025-02",
    api=True, app=True, scores={K_TTS: 1039, K_TTSA: 1521}, languages="Anglais, espagnol",
    unit="1k_chars", k=0.0875, platform="Hume API (prix relevé par AA)", src=[S(HUME)]))

INW = "https://docs.inworld.ai/docs/tts"
A(M("inworld-realtime-tts-2", "Inworld TTS", "Realtime TTS-2", "Inworld", "US", "tts", "2026-08",
    api=True, scores={K_TTS: 1259, K_CV: 1142}, languages="200+ langues et variantes (doc), qualité inégale selon des tiers",
    clone_s=5, zero_shot=True, latency=120, unit="1k_chars", k=0.025, platform="Inworld API",
    price_note="25 $ le million de caractères à la demande, 12,50 $ sur forfaits élevés (secondaire). Clonage 5 à 15 s (revue tierce).",
    pros=["7e du Speech Arena AA, 6e en voix contrôlée"], cons=["Date de sortie générale incertaine"],
    src=[S(INW), S("https://howaiworks.ai/blog/inworld-realtime-tts-2-launch-2026", "independant")]))
A(M("inworld-tts-max", "Inworld TTS", "Inworld TTS MAX", "Inworld", "US", "tts", None,
    api=True, scores={K_TTSA: 1553}, pros=["1er de la TTS Arena V2 de Hugging Face au 15/10/2026 (à égalité statistique avec Vocu et Aurora)"],
    src=[S(INW)]))
A(M("qwen-audio-3-1-tts-plus", "Qwen-Audio", "Qwen-Audio-3.1-TTS-Plus", "Alibaba", "CN", "tts", "2026-09-23",
    api=True, scores={K_TTS: 1297, K_CV: 1184}, unit="1k_chars", k=0.0193, platform="Alibaba Cloud Model Studio (prix relevé par AA)",
    pros=["3e du Speech Arena AA, 2e en voix contrôlée", "Moins cher que les leaders"], cons=["Langues et durée de clonage non confirmées"],
    src=[S("https://ai-tldr.dev/models/qwen-audio-3-1-tts/", "independant")]))
A(M("speechify-simba-3-2", "Speechify Simba", "Simba 3.2", "Speechify", "US", "tts", "2026-07",
    api=True, scores={K_TTS: 1243, K_CV: 1089}, unit="1k_chars", k=0.0066, platform="Speechify API (prix relevé par AA)",
    pros=["Le moins cher du haut du classement AA"], src=[]))
A(M("heygen-voice", "HeyGen Voice", "HeyGen Voice", "HeyGen", "US", "voice_clone", None,
    api=True, app=True, scores={K_CV: 1200}, unit="1k_chars", k=0.03, platform="HeyGen (prix relevé par AA)",
    pros=["1er du classement AA en voix contrôlée (mêmes 8 voix clonées)"], cons=["Absent du classement voix fournisseur"], src=[]))
A(M("vocu-v3", "Vocu", "Vocu V3.0", "Vocu", None, "tts", None, scores={K_TTSA: 1559},
    pros=["En tête de la TTS Arena V2 à égalité statistique"], cons=["Peu documenté"], src=[]))

GRAD = "https://gradium.ai/pricing"
A(M("gradium-tts", "Gradium TTS", "Gradium TTS (sept. 2026)", "Gradium (issu de Kyutai)", "FR", "tts", "2026-09",
    api=True, scores={K_TTS: 1173, K_CV: 1056, K_TTSA: 1520}, languages="Anglais, français, espagnol, portugais, allemand",
    clone_s=10, zero_shot=True, consent="inconnu", unit="1k_chars", k=0.0478, platform="Gradium API (prix relevé par AA)",
    price_note="Forfaits de 13 $ à 1 615 $/mois ; clonage instantané dès l'offre gratuite (5 voix), clonage pro à partir de l'offre M. Offre gratuite non commerciale. Score TTS Arena = version antérieure à 08/2026.",
    pros=["Société parisienne", "Français parmi 5 langues seulement : priorité éditeur"], cons=["5 langues"],
    src=[S(GRAD), S("https://humannessindex.vapi.ai/providers/gradium", "independant")]))

A(M("playht", "PlayHT / PlayAI", "Play 3.0 et PlayDialog", "PlayAI (racheté par Meta)", "US", "tts", None,
    api=False, app=False,
    cons=["Racheté par Meta en juillet 2025 ; API fermée aux requêtes le 26/07/2025 selon plusieurs sources ; service, comptes et voix clonées supprimés au 31/12/2025", "Ne plus utiliser"],
    src=[S("https://murf.ai/blog/play-ai-transition-guide", "independant"), S("https://anyspeech.io/playht-alternatives", "independant")]))

# ============================ RESEMBLE ============================
CB = "https://huggingface.co/ResembleAI/chatterbox"
DB = "https://huggingface.co/ResembleAI/Dramabox"
PERTH = "Filigrane neuronal Perth intégré à la sortie."
A(M("resemble-chatterbox-multilingual-v3", "Chatterbox", "Chatterbox Multilingual V3", "Resemble AI", "US", "tts", None,
    ow=True, lic="MIT (commercial autorisé)", api=True,
    languages="23+ langues dont le français (ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh)",
    clone_s=None, zero_shot=True, consent="aucun",
    g5090=True, g4090=True, mac=True, tool="chatterbox ; MLX (mlx-community/chatterbox-multilingual-v3)",
    vram="500 millions de paramètres : petit, non mesuré ici.", mod=PERTH,
    pros=["Clonage multilingue libre et commercial", "Packs monolingues dédiés"], cons=["Pas de score de classement propre à V3"],
    src=[S(CB), S("https://huggingface.co/mlx-community/chatterbox-multilingual-v3")]))
A(M("resemble-chatterbox", "Chatterbox", "Chatterbox (original)", "Resemble AI", "US", "tts", "2025-05",
    ow=True, lic="MIT (commercial autorisé)", api=True, scores={K_TTS: 1025, K_CV: 930, K_TTSA: 1476},
    zero_shot=True, consent="aucun", g5090=True, g4090=True, mac=True, tool="chatterbox, MLX",
    vram="500 millions de paramètres.", mod=PERTH, unit="1k_chars", k=0.025, platform="Resemble API (prix relevé par AA)",
    pros=["Gratuit et local"], cons=["Classé bas en voix contrôlée"], src=[S(CB)]))
A(M("resemble-chatterbox-turbo", "Chatterbox", "Chatterbox Turbo", "Resemble AI", "US", "tts", "2025-12-18",
    ow=True, lic="MIT (commercial autorisé)", zero_shot=True, consent="aucun",
    emotions="Balises paralinguistiques ([laugh], [cough], [chuckle]).", latency=200,
    g5090=True, g4090=True, mac=True, tool="chatterbox ; ONNX ; MLX (mlx-community/chatterbox-turbo-4bit)",
    vram="350 millions de paramètres.", mod=PERTH,
    pros=["Rires, toux en ligne, moins de 200 ms"], cons=["Sources secondaires pour les chiffres"],
    src=[S("https://thursdai.news/companies/resemble-ai", "independant"), S("https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX")]))
A(M("resemble-chatterbox-hd", "Chatterbox", "Chatterbox HD", "Resemble AI", "US", "tts", "2025-05",
    api=True, scores={K_TTS: 1103}, unit="1k_chars", k=0.04, platform="Resemble API (prix relevé par AA)", src=[]))
A(M("resemble-dramabox", "Dramabox", "Dramabox", "Resemble AI", "US", "tts", "2026-04-17",
    ow=True, lic="LTX-2 Community License (affinage de LTX-2.3)", languages="Anglais",
    clone_s=10, zero_shot=True, consent="aucun",
    emotions="Le prompt dirige tout : répliques entre guillemets, didascalies hors guillemets (soupirs, voix qui se brise, pauses).",
    max_dur="Durée réglable, 20 à 60 s conseillées pour scènes longues ou musique",
    g5090=None, g4090=None, mac=True, tool="ltx-audio-tts ; MLX (mlx-community/ResembleAI-Dramabox)",
    vram="LTX-2.3 audio 3,3 milliards + encodeur texte Gemma 3 12B : non mesuré ici.", mod=PERTH,
    pros=["Écrit comme une scène de scénario", "Idéal pour des voix de personnages jouées"], cons=["Anglais seulement", "Licence LTX-2 à lire avant usage commercial"],
    src=[S(DB)]))

# ============================ MICROSOFT ============================
VV = "https://github.com/microsoft/VibeVoice"
AZ = "https://azure.microsoft.com/en-us/pricing/details/speech/"
A(M("microsoft-vibevoice-1-5b", "VibeVoice", "VibeVoice-TTS 1.5B", "Microsoft", "US", "tts", "2025-08-25",
    ow=True, lic="MIT", scores={K_TTS: 956}, languages="Anglais, chinois",
    max_dur="90 min, 4 locuteurs", g5090=True, g4090=True, tool="transformers ; GGUF communautaires",
    vram="1,5 milliard de paramètres, non mesuré ici.",
    mod="Microsoft a retiré le code TTS du dépôt le 05/09/2025 après des usages contraires à l'intention ; les poids restent sur Hugging Face.",
    pros=["Podcasts et dialogues longs à 4 voix"], cons=["Code d'inférence officiel retiré", "Bas au classement AA"],
    src=[S(VV), S("https://huggingface.co/microsoft/VibeVoice-1.5B")]))
A(M("microsoft-vibevoice-realtime-0-5b", "VibeVoice", "VibeVoice-Realtime 0.5B", "Microsoft", "US", "tts", "2025-12-03",
    ow=True, lic="MIT", languages="Anglais ; voix expérimentales en 9 langues dont le français", fr="inconnu",
    fr_note="Voix françaises « expérimentales » selon l'éditeur.", latency=300,
    g5090=True, g4090=True, tool="transformers", vram="0,5 milliard de paramètres.",
    pros=["Lecture en flux, environ 300 ms"], cons=["Pensé pour l'anglais"], src=[S(VV), S("https://huggingface.co/microsoft/VibeVoice-Realtime-0.5B")]))
A(M("microsoft-azure-hd-2-5", "Azure AI Speech", "Azure HD 2.5", "Microsoft", "US", "tts", "2026-03",
    api=True, scores={K_TTS: 1133}, consent="verification_identite", unit="1k_chars", k=0.022, platform="Azure (prix relevé par AA)",
    mod="Personal Voice et Custom Voice sont en accès limité : demande d'accès et cas d'usage pré-approuvés.",
    pros=["Cadre de consentement strict pour le clonage"], cons=["Clonage soumis à approbation"], src=[S(AZ)]))
A(M("microsoft-azure-neural", "Azure AI Speech", "Azure Neural", "Microsoft", "US", "tts", "2018-09",
    api=True, scores={K_TTS: 1035}, unit="1k_chars", k=0.015, platform="Azure (prix relevé par AA)", src=[S(AZ)]))
A(M("microsoft-mai-voice-1", "MAI Voice", "MAI-Voice-1", "Microsoft", "US", "tts", "2026-04",
    api=None, scores={K_TTS: 1031}, src=[]))
A(M("microsoft-mai-transcribe-2", "MAI Transcribe", "MAI-Transcribe-2", "Microsoft", "US", "stt", None,
    api=True, scores={K_STT: 2.0}, unit="min", mn=0.00167, platform="Microsoft (prix relevé par AA)",
    pros=["Meilleur WER des modèles occidentaux sur AA, très rapide (facteur 316)"], src=[]))
A(M("microsoft-vibevoice-asr", "VibeVoice", "VibeVoice-ASR 7B", "Microsoft", "US", "stt", "2026-01-21",
    ow=True, lic="MIT", scores={K_OASR: 8.23}, languages="50+ langues dont le français",
    max_dur="60 min d'un seul tenant", g5090=True, g4090=True, tool="transformers ; VibeASR.cpp (CPU, BitNet)",
    vram="7 milliards de paramètres, non mesuré ici ; version BitNet de 1,58 Go en temps réel sur CPU.",
    pros=["Qui parle, quand et quoi en une passe (diarisation et horodatage)", "Mots-clés personnalisés"], cons=["WER anglais en retrait"],
    src=[S(VV), S("https://huggingface.co/microsoft/VibeVoice-ASR")]))

# ============================ KYUTAI ============================
KM = "https://github.com/kyutai-labs/moshi"
KD = "https://github.com/kyutai-labs/delayed-streams-modeling"
A(M("kyutai-moshi", "Moshi", "Moshiko / Moshika", "Kyutai", "FR", "realtime_dialogue", "2024-09-11",
    ow=True, lic="CC-BY 4.0 (poids), MIT et Apache (code)", app=True, languages="Anglais",
    latency=200, g5090=True, g4090=True, mac=True, tool="moshi (PyTorch), Rust/Candle, MLX (kyutai/moshiko-mlx-q4)",
    vram="Version PyTorch : carte de 24 Go. Latence théorique 160 ms, environ 200 ms sur L4.",
    pros=["Dialogue en duplex intégral, libre et local", "Tourne sur Mac en MLX"], cons=["Anglais seulement", "Voix fixes"],
    src=[S(KM), S("https://huggingface.co/kyutai/moshiko-pytorch-bf16")]))
A(M("kyutai-tts-1-6b-en-fr", "Kyutai TTS", "tts-1.6b-en_fr", "Kyutai", "FR", "tts", "2025-06-30",
    ow=True, lic="CC-BY 4.0", languages="Anglais, français", fr="inconnu", fr_note="Entraîné pour l'anglais et le français, pas de mesure publique de qualité française trouvée.",
    zero_shot=False, consent="aucun",
    emotions=None, g5090=True, g4090=True, mac=True, tool="moshi, MLX",
    vram="1,8 milliard de paramètres.",
    mod="Clonage volontairement limité à des empreintes de voix précalculées (dépôt tts-voices) : pas de clonage libre d'une voix quelconque.",
    pros=["Flux texte vers voix dès les premiers mots", "Français natif"], cons=["Pas de clonage libre"],
    src=[S("https://huggingface.co/kyutai/tts-1.6b-en_fr"), S(KD)]))
A(M("kyutai-stt-1b-en-fr", "Kyutai STT", "stt-1b-en_fr", "Kyutai", "FR", "stt", "2025-06-25",
    ow=True, lic="CC-BY 4.0", languages="Anglais, français", latency=500,
    g5090=True, g4090=True, mac=True, tool="moshi, Rust, MLX", vram="Environ 1 milliard de paramètres.",
    pros=["Flux avec 0,5 s de délai et détection sémantique de fin de parole", "Robuste jusqu'à 2 h d'audio"],
    cons=["Absent des classements"], src=[S("https://huggingface.co/kyutai/stt-1b-en_fr-trfs"), S(KD)]))
A(M("kyutai-stt-2-6b-en", "Kyutai STT", "stt-2.6b-en", "Kyutai", "FR", "stt", "2025-06-25",
    ow=True, lic="CC-BY 4.0", languages="Anglais", latency=2500, g5090=True, g4090=True, mac=True, tool="moshi, Rust, MLX",
    vram="2,6 milliards de paramètres.", src=[S(KD)]))

# ============================ SESAME ============================
A(M("sesame-csm-1b", "Sesame CSM", "CSM-1B", "Sesame", "US", "tts", "2025-03-13",
    ow=True, lic="Apache-2.0", languages="Anglais (autres langues peu fiables selon l'éditeur)",
    zero_shot=True, consent="aucun", g5090=True, g4090=True, mac=True, tool="csm (PyTorch, MPS) ; MLX (mlx-community/csm-1b)",
    vram="1 milliard de paramètres.",
    pros=["Voix conversationnelle avec contexte de dialogue"], cons=["Seule la taille 1B est publiée", "Anglais"],
    src=[S("https://github.com/SesameAILabs/csm"), S("https://huggingface.co/sesame/csm-1b")]))
A(M("sesame-maya-miles", "Sesame", "Maya et Miles (application)", "Sesame", "US", "realtime_dialogue", None,
    app=True, api=False, cons=["Application compagnon, bêta iOS fermée depuis octobre 2025 selon une source ; aucune annonce 2026 trouvée"],
    src=[S("https://timewell.jp/en/columns/sesame-ai", "independant")]))

# ============================ AUTRES TTS OUVERTS ============================
A(M("f5-tts", "F5-TTS", "F5-TTS v1", "SWivid (université SJTU)", "CN", "tts", "2024-10-07",
    ow=True, lic="CC-BY-NC 4.0 (poids, à cause du jeu Emilia) ; code MIT", zero_shot=True, consent="aucun",
    g5090=True, g4090=True, mac=True, tool="f5-tts ; f5-tts-mlx",
    vram="Petit modèle, non mesuré ici.", pros=["Clonage zéro-shot rapide, nombreux affinages par langue"], cons=["Non commercial"],
    src=[S("https://github.com/SWivid/F5-TTS")]))
A(M("kokoro-82m", "Kokoro", "Kokoro-82M v1.0", "hexgrad", None, "tts", "2025-01",
    ow=True, lic="Apache-2.0", api=True, scores={K_TTS: 1061, K_TTSA: 1473},
    languages="Plusieurs langues dont le français (lang_code 'f')", fr="inconnu",
    fr_note="Voix française entraînée sur le corpus SIWIS, moins de 11 h (fiche).", zero_shot=False, consent="aucun",
    unit="1k_chars", k=0.0007, platform="API tierces (prix relevé par AA)",
    g5090=True, g4090=True, mac=True, tool="kokoro, ONNX, MLX (mlx-community/Kokoro-82M-bf16)", vram="82 millions de paramètres : tourne aussi sur CPU.",
    pros=["Minuscule, libre et commercial", "Égale des modèles bien plus gros sur AA"], cons=["Pas de clonage", "Peu de voix françaises"],
    src=[S("https://huggingface.co/hexgrad/Kokoro-82M"), S("https://github.com/hexgrad/kokoro")]))
A(M("coqui-xtts-v2", "XTTS", "XTTS-v2", "Coqui (société fermée)", "DE", "voice_clone", "2023-10-31",
    ow=True, lic="Coqui Public Model License (CPML), non commerciale", api=True, scores={K_TTS: 914, K_CV: 830},
    languages="17 langues dont le français", clone_s=6, zero_shot=True, consent="aucun",
    g5090=True, g4090=True, mac=True, tool="coqui-tts (fork idiap, roues macOS)", vram="Petit modèle, non mesuré ici.",
    pros=["Clonage multilingue avec 6 s"], cons=["Dernier au classement en voix contrôlée", "Société Coqui fermée, licence non commerciale"],
    src=[S("https://huggingface.co/coqui/XTTS-v2"), S("https://github.com/idiap/coqui-ai-TTS")]))
A(M("nari-dia-1-6b", "Dia", "Dia-1.6B", "Nari Labs", "KR", "tts", "2025-04-20",
    ow=True, lic="Apache-2.0", languages="Anglais", emotions="Dialogue à balises [S1] [S2], sons non verbaux.",
    g5090=True, g4090=True, tool="dia", vram="1,6 milliard de paramètres.",
    pros=["Dialogues à deux voix en une passe"], cons=["Anglais seulement"], src=[S("https://huggingface.co/nari-labs/Dia-1.6B")]))
A(M("nari-dia2-2b", "Dia", "Dia2-2B", "Nari Labs", "KR", "tts", "2025-11-15",
    ow=True, lic="Apache-2.0", languages="Anglais", max_dur="2 min", zero_shot=True, consent="aucun",
    g5090=True, g4090=True, tool="dia2 (CUDA 12.8+)", vram="2 milliards de paramètres.",
    mod="La fiche interdit de produire la voix de personnes réelles sans permission (pas de contrôle technique).",
    pros=["Flux : commence à parler dès les premiers mots", "Conditionnement sur l'audio précédent pour des échanges naturels"],
    cons=["2 min maximum, anglais seulement"], src=[S("https://huggingface.co/nari-labs/Dia2-2B")]))
A(M("canopy-orpheus-3b", "Orpheus", "Orpheus 3B 0.1", "Canopy Labs", "US", "tts", "2025-03-17",
    ow=True, lic="Apache-2.0 (étiquette Hugging Face)", languages="Anglais ; modèles multilingues en préversion de recherche (avril 2025)",
    zero_shot=True, consent="aucun", emotions="Balises <laugh>, <chuckle>, <sigh>, <cough>, <sniffle>, <groan>, <yawn>, <gasp>.",
    g5090=True, g4090=True, mac=True, tool="orpheus-speech (vLLM), GGUF, MLX", vram="3 milliards de paramètres.",
    pros=["Voix empathiques à balises"], cons=["Absent des classements au 15/10/2026"],
    src=[S("https://github.com/canopyai/Orpheus-TTS"), S("https://huggingface.co/canopylabs/orpheus-3b-0.1-ft")]))
HG = "https://github.com/boson-ai/higgs-audio"
A(M("boson-higgs-audio-v3-tts", "Higgs Audio", "Higgs Audio v3 TTS 4B", "Boson AI", "US", "tts", "2026-06",
    ow=True, lic="Boson Higgs Audio v3 Research and Non-Commercial License", api=True, scores={K_TTS: 1037, K_CV: 959},
    languages="100+ langues", zero_shot=True, consent="aucun", emotions="Contrôle d'émotion, de style et de prosodie en ligne.",
    unit="1k_chars", k=0.015, platform="Boson API (prix relevé par AA)",
    g5090=True, g4090=True, tool="SGLang, transformers ; Higgs Audio v3 Studio (Windows, GGUF)", vram="Base Qwen3-4B.",
    pros=["Multi-locuteurs, continuation de parole"], cons=["Non commercial sans licence"],
    src=[S(HG), S("https://huggingface.co/multimodalart/higgs-audio-v3-tts-4b-transformers"), S("https://huggingface.co/drbaph/Higgs-Audio-v3-Studio")]))
A(M("boson-higgs-audio-v3-stt", "Higgs Audio", "Higgs Audio v3 STT", "Boson AI", "US", "stt", "2026-03-25",
    ow=True, lic="Apache-2.0", scores={K_OASR: 6.19}, g5090=True, g4090=True, tool="transformers ; GGUF",
    src=[S("https://huggingface.co/bosonai/higgs-audio-v3-stt")]))
A(M("indextts-2", "IndexTTS", "IndexTTS-2", "Bilibili (IndexTeam)", "CN", "tts", "2025-06-18",
    ow=True, lic="bilibili Model Use License Agreement", languages="Chinois, anglais",
    zero_shot=True, consent="aucun", emotions="Émotion séparée du timbre, contrôle de durée.",
    g5090=True, g4090=True, mac=True, tool="indextts ; MLX (mlx-community/index-tts2-mlx)", vram="Non mesuré ici.",
    pros=["Durée contrôlable : utile pour caler une réplique sur une image"], cons=["Ni français ni licence permissive"],
    src=[S("https://huggingface.co/IndexTeam/IndexTTS-2"), S("https://github.com/index-tts/index-tts/blob/main/LICENSE")]))
A(M("indextts-2-5", "IndexTTS", "IndexTTS-2.5", "Bilibili (IndexTeam)", "CN", "tts", "2026-08-10",
    ow=True, lic="bilibili Model Use License Agreement", languages="Chinois, anglais, japonais, espagnol, arabe",
    zero_shot=True, consent="aucun", emotions="Émotion séparée du timbre (texte ou référence), vitesse réglable.",
    g5090=True, g4090=True, mac=True, tool="indextts ; MLX (mlx-community/IndexTTS-2.5-fp16)", vram="Environ 6 Go de VRAM (fiche).",
    mod="La fiche précise que le modèle ne vérifie pas le consentement de la personne clonée.",
    pros=["Clonage avec une seule référence, émotion pilotable"], cons=["Pas de français"],
    src=[S("https://huggingface.co/IndexTeam/IndexTTS-2.5")]))
A(M("cosyvoice-3", "CosyVoice", "Fun-CosyVoice3-0.5B-2512", "Alibaba (FunAudioLLM)", "CN", "tts", "2025-12-11",
    ow=True, lic="Apache-2.0", languages="9 langues dont le français, 18+ dialectes chinois",
    zero_shot=True, consent="aucun", emotions="Instructions de langue, dialecte, émotion, vitesse, volume.",
    g5090=True, g4090=True, mac=True, tool="CosyVoice ; MLX (mlx-community/Fun-CosyVoice3-0.5B-2512-fp16)", vram="0,5 milliard de paramètres.",
    pros=["Libre et commercial, clonage interlangue"], cons=["Absent des classements"],
    src=[S("https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512")]))
A(M("spark-tts-0-5b", "Spark-TTS", "Spark-TTS 0.5B", "SparkAudio", "CN", "tts", "2025-02-27",
    ow=True, lic="CC BY-NC-SA 4.0 (passée d'Apache 2.0 à cause des données)", languages="Chinois, anglais",
    zero_shot=True, consent="aucun", g5090=True, g4090=True, mac=True, tool="Spark-TTS ; MLX", vram="0,5 milliard de paramètres.",
    cons=["Non commercial, pas de français"], src=[S("https://huggingface.co/SparkAudio/Spark-TTS-0.5B")]))
A(M("zyphra-zonos-v0-1", "Zonos", "Zonos-v0.1 (transformer)", "Zyphra", "US", "tts", "2025-02-06",
    ow=True, lic="Apache-2.0", api=True, scores={K_TTS: 1000}, zero_shot=True, consent="aucun",
    emotions="Réglages de joie, peur, tristesse, colère, débit, hauteur.", unit="1k_chars", k=0.02, platform="Zyphra (prix relevé par AA)",
    g5090=True, g4090=True, tool="zonos ; GGUF", vram="Non mesuré ici.",
    pros=["Curseurs d'émotion explicites"], cons=["Remplacé par ZONOS2"], src=[S("https://huggingface.co/Zyphra/Zonos-v0.1-transformer")]))
A(M("zyphra-zonos2", "Zonos", "ZONOS2", "Zyphra", "US", "tts", "2026-06-11",
    ow=True, lic="Apache-2.0", api=True,
    languages="Palier 1 : anglais, mandarin, japonais ; palier 2 dont le français ; palier 3 : 21 langues",
    fr="moyenne", fr_note="Français en palier 2 sur 3 selon l'éditeur (pas une mesure).", zero_shot=True, consent="aucun",
    g5090=None, g4090=None, mac=True, tool="Serveur Mini-SGLang (Linux x86_64) ; MLX (mlx-community/Zyphra-ZONOS2)",
    vram="Architecture MoE, taille non relevée ; serveur officiel Linux seulement.",
    pros=["Clonage de haute fidélité, libre et commercial"], cons=["Serveur officiel Linux uniquement"],
    src=[S("https://huggingface.co/Zyphra/ZONOS2")]))
A(M("openbmb-voxcpm2", "VoxCPM", "VoxCPM2", "OpenBMB", "CN", "tts", "2026-04-03",
    ow=True, lic="Apache-2.0", languages="30 langues dont le français, 9 dialectes chinois",
    zero_shot=True, consent="aucun", emotions="Dessin de voix par description, clonage guidé par style.",
    g5090=True, g4090=True, mac=True, tool="voxcpm, Nano-VLLM ; MLX (mlx-community/VoxCPM2-8bit)",
    vram="2 milliards de paramètres ; RTF 0,3 sur RTX 4090 (fiche).",
    pros=["Sortie 48 kHz", "Voix créée par description sans référence", "Libre et commercial"], cons=["Absent des classements"],
    src=[S("https://huggingface.co/openbmb/VoxCPM2")]))
A(M("qwen3-tts", "Qwen3-TTS", "Qwen3-TTS 12Hz 1.7B (Base, CustomVoice, VoiceDesign)", "Alibaba (Qwen)", "CN", "tts", "2026-01-21",
    ow=True, lic="Apache-2.0", api=True, scores={K_TTS: 931},
    languages="10 langues : chinois, anglais, japonais, coréen, allemand, français, russe, portugais, espagnol, italien",
    clone_s=3, zero_shot=True, consent="aucun", emotions="Ton, débit et émotion par instructions ; voix dessinée par description.",
    latency=97, unit="1k_chars", k=0.0138, platform="Alibaba Cloud (prix relevé par AA)",
    g5090=True, g4090=True, mac=None, tool="qwen-tts ; GGUF", vram="1,7 milliard de paramètres.",
    pros=["Clonage en 3 s, libre et commercial", "97 ms de latence de bout en bout (éditeur)"], cons=["Bas au classement AA (931)"],
    src=[S("https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base")]))
VOXT = "https://the-decoder.com/mistrals-first-open-weight-tts-model-voxtral-clones-voices-from-three-seconds-of-audio-across-nine-languages/"
A(M("mistral-voxtral-tts", "Voxtral", "Voxtral TTS", "Mistral AI", "FR", "tts", "2026-03-26",
    ow=True, lic="CC BY-NC 4.0 (poids) ; commercial via l'API", api=True, scores={K_TTS: 1088, K_CV: 1002},
    languages="9 langues : anglais, français, allemand, espagnol, néerlandais, portugais, italien, hindi, arabe",
    clone_s=3, zero_shot=True, consent="inconnu", unit="1k_chars", k=0.016, platform="Mistral API",
    g5090=True, g4090=True, tool="vLLM", vram="16 Go de GPU ou plus (presse).",
    mod="Selon Slator, la version à poids ouverts serait limitée à des voix fixes, le clonage passant par la plateforme : non résolu.",
    pros=["Éditeur français, français natif"], cons=["Poids non commerciaux", "Clonage local incertain"],
    src=[S(VOXT, "independant"), S("https://slator.com/mistral-text-to-speech-model/", "independant")]))
A(M("nvidia-magpie-tts-multilingual", "Magpie TTS", "Magpie TTS Multilingual 357M", "NVIDIA", "US", "tts", "2026-07-21",
    ow=True, lic="NVIDIA Open Model License", scores={K_TTS: 1064}, languages="12 langues (fiche)",
    g5090=True, g4090=True, tool="NeMo", vram="357 millions de paramètres.",
    src=[S("https://huggingface.co/nvidia/magpie_tts_multilingual_357m")]))

# ============================ STT OUVERTS ET AUTRES ============================
PK = "https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3"
A(M("nvidia-parakeet-tdt-0-6b-v3", "Parakeet", "parakeet-tdt-0.6b-v3", "NVIDIA", "US", "stt", "2025-08-04",
    ow=True, lic="CC-BY 4.0 (commercial autorisé)", api=True, scores={K_STT: 4.5, K_OASR: 6.51},
    languages="25 langues européennes dont le français, détection automatique", fr="bonne",
    fr_note="WER français 5,15 % sur FLEURS, 4,97 % sur MLS, 6,05 % sur CoVoST (mesures éditeur).",
    max_dur="24 min en attention complète (A100 80 Go), jusqu'à 3 h en attention locale",
    unit="min", mn=0.0015, platform="Together AI (prix relevé par AA)",
    g5090=True, g4090=True, mac=True, tool="NeMo ; MLX (mlx-community/parakeet-tdt-0.6b-v3) ; CoreML ; ONNX",
    vram="600 millions de paramètres.",
    pros=["Extrêmement rapide (RTFx de 6 000 à 13 000)", "Français mesuré et bon", "Licence commerciale"],
    cons=["25 langues seulement"], src=[S(PK)]))
A(M("nvidia-canary-qwen-2-5b", "Canary", "canary-qwen-2.5b", "NVIDIA", "US", "stt", "2025-06-26",
    ow=True, lic="CC-BY 4.0", api=True, scores={K_STT: 4.3, K_OASR: 6.37}, languages="Anglais seulement", fr="faible",
    fr_note="Entraîné sur l'anglais seulement ; le français n'est « pas fiable » selon la fiche.",
    unit="min", mn=0.00074, platform="Replicate (prix relevé par AA)",
    g5090=True, g4090=True, tool="NeMo ; GGUF", vram="2,5 milliards de paramètres.",
    pros=["Mode LLM pour résumer la transcription"], cons=["Anglais seulement"], src=[S("https://huggingface.co/nvidia/canary-qwen-2.5b")]))
A(M("nvidia-canary-1b-v2", "Canary", "canary-1b-v2", "NVIDIA", "US", "stt", "2025-08-04",
    ow=True, lic="CC-BY 4.0", scores={K_OASR: 7.91}, languages="25 langues européennes dont le français ; traduction vers et depuis l'anglais",
    g5090=True, g4090=True, mac=True, tool="NeMo ; ONNX ; MLX communautaire", vram="1 milliard de paramètres.",
    pros=["Transcrit et traduit (sous-titres anglais d'un rush français)"], cons=["WER anglais en retrait de Parakeet v3"],
    src=[S("https://huggingface.co/nvidia/canary-1b-v2")]))
VXR = "https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602"
A(M("mistral-voxtral-mini-transcribe-2", "Voxtral", "Voxtral Mini Transcribe 2", "Mistral AI", "FR", "stt", None,
    api=True, scores={K_STT: 3.6}, fr="bonne", fr_note="WER français 4,32 % (tableau éditeur, hors ligne).",
    unit="min", mn=0.003, platform="Mistral API (prix relevé par AA)", src=[S(VXR)]))
A(M("mistral-voxtral-mini-4b-realtime", "Voxtral", "Voxtral Mini 4B Realtime 2602", "Mistral AI", "FR", "stt", "2026-02",
    ow=True, lic="Apache-2.0", scores={K_OASR: 9.01}, languages="13 langues dont le français",
    fr="moyenne", fr_note="WER français 6,42 % avec 480 ms de délai (tableau éditeur).", latency=480,
    g5090=True, g4090=True, mac=True, tool="vLLM ; mlx-audio, voxmlx ; GGUF", vram="4 milliards de paramètres.",
    pros=["Sous-titrage en direct, délai réglable de 80 ms à 2,4 s"], cons=["Moins précis que la version hors ligne"], src=[S(VXR)]))
A(M("mistral-voxtral-small-24b", "Voxtral", "Voxtral Small 24B 2507", "Mistral AI", "FR", "stt", "2025-07",
    ow=True, lic="Apache-2.0", api=True, scores={K_STT: 2.8, K_OASR: 6.90},
    unit="min", mn=0.004, platform="Mistral API (prix relevé par AA)",
    g5090=None, g4090=None, tool="vLLM ; GGUF (handy-computer)", vram="24 milliards de paramètres : environ 48 Go en bf16, quantification nécessaire sur 32 ou 24 Go (non mesuré ici).",
    pros=["WER AA 2,8 %, ouvert et commercial"], cons=["Lourd en local"], src=[S("https://huggingface.co/mistralai/Voxtral-Small-24B-2507")]))
A(M("mistral-voxtral-mini-3b", "Voxtral", "Voxtral Mini 3B 2507", "Mistral AI", "FR", "stt", "2025-07",
    ow=True, lic="Apache-2.0", api=True, scores={K_STT: 3.8, K_OASR: 7.84}, unit="min", mn=0.001, platform="DeepInfra (prix relevé par AA)",
    g5090=True, g4090=True, mac=True, tool="vLLM ; MLX ; GGUF", vram="3 milliards de paramètres.",
    src=[S("https://huggingface.co/mistralai/Voxtral-Mini-3B-2507")]))
A(M("qwen3-asr-1-7b", "Qwen3-ASR", "Qwen3-ASR-1.7B", "Alibaba (Qwen)", "CN", "stt", "2026-01-28",
    ow=True, lic="Apache-2.0", scores={K_OASR: 5.75}, languages="30 langues dont le français et 22 dialectes chinois ; chant et musique de fond",
    g5090=True, g4090=True, mac=True, tool="qwen-asr (transformers, vLLM) ; MLX ; GGUF", vram="1,7 milliard de paramètres.",
    pros=["Meilleur WER Open ASR des modèles ouverts au 15/10/2026", "Aligneur temporel séparé (11 langues dont le français)"],
    cons=[], src=[S("https://huggingface.co/Qwen/Qwen3-ASR-1.7B")]))
A(M("stepfun-stepaudio-3-asr", "StepAudio", "StepAudio 3 ASR", "StepFun", "CN", "stt", None,
    api=True, scores={K_STT: 1.7}, unit="min", mn=0.00667, platform="StepFun (prix relevé par AA)",
    pros=["WER AA le plus bas (1,7 %, ex aequo)"], src=[]))
A(M("xai-grok-voice-transcribe-2", "Grok Voice", "Grok Voice Transcribe 2.0", "SpaceXAI (xAI)", "US", "stt", None,
    api=True, scores={K_STT: 2.3}, unit="min", mn=0.00167, platform="xAI (prix relevé par AA)", src=[]))
A(M("reson8-resonant-1-flash", "Resonant", "resonant-1-flash", "Reson8", None, "stt", None,
    api=True, scores={K_OASR: 4.02}, pros=["1er de l'Open ASR Leaderboard (anglais) au 15/10/2026"], src=[]))

# ============================ MUSIQUE ============================
SUNO = "https://datanorth.ai/news/suno-launches-v6-v6-wild-and-v6-mini"
A(M("suno-v6", "Suno", "v6", "Suno", "US", "music", "2026-09-09",
    api=None, app=True, scores={K_MV: 1146, K_MI: 1148}, max_dur="Jusqu'à 8 min (une seule source)",
    unit="abonnement", platform="Suno (Pro 8 $/mois en annuel, Premier 24 $/mois en annuel)",
    price_note="Droits commerciaux sur les morceaux téléchargés pendant un abonnement payant ; offre gratuite sans droits commerciaux.",
    pros=["1er des deux classements musique AA (vocal et instrumental)"], cons=["Pas d'API officielle trouvée", "Données d'entraînement non publiées"],
    src=[S(SUNO, "independant"), S("https://myclaw.ai/blog/suno-v6-review", "independant")]))
A(M("suno-v6-mini", "Suno", "v6-mini", "Suno", "US", "music", "2026-09-09",
    app=True, scores={K_MV: 1130, K_MI: 1114}, pros=["2e des deux classements, rapide, sur tous les forfaits"], src=[S(SUNO, "independant")]))
A(M("suno-v6-wild", "Suno", "v6-wild", "Suno", "US", "music", "2026-09-09", app=True,
    pros=["Générations plus expérimentales"], cons=["Absent des classements AA"], src=[S(SUNO, "independant")]))
A(M("udio", "Udio", "v1.5 Allegro", "Udio", "US", "music", None, app=True,
    cons=["Téléchargements audio, vidéo et stems coupés depuis le 30/10/2025 (accord avec Universal Music)", "Plateforme sous licence annoncée sans date confirmée", "Absent des classements AA"],
    src=[S("https://ppc.land/udio-settles-copyright-lawsuit-partners-with-universal-music-group/", "independant"),
         S("https://www.digitalmusicnews.com/2025/10/29/umg-udio-deal-everything-we-know/", "independant")]))
A(M("mureka-v9-5", "Mureka", "V9.5", "Kunlun Tech (Mureka)", "CN", "music", "2026-08-31",
    api=True, app=True, scores={K_MV: 1107, K_MI: 1084}, unit="track", track=0.225, platform="WaveSpeedAI",
    price_note="0,225 $ par morceau (chanson ou fond musical), 0,75 $ en prompt vers chanson.",
    pros=["3e en vocal sur l'arène AA"], cons=["Durée demandée mal respectée (tests sur V9)"],
    src=[S("https://wavespeed.ai/blog/audio-and-voice-models/mureka-v9-5-music-api/", "independant"), S("https://invideo.io/blog/mureka-ai-music-generator/", "independant")]))
A(M("sonauto-melodia-v3", "Melodia", "Melodia v3", "Sonauto", "US", "music", None, api=True, scores={K_MV: 972, K_MI: 986}, src=[]))
SA3 = "https://the-decoder.com/stability-ai-launches-stable-audio-3-0-with-up-to-six-minute-tracks-and-open-weights/"
A(M("stable-audio-3-large", "Stable Audio 3", "Large (2,7 B)", "Stability AI", "GB", "music", "2026-05-20",
    ow=False, api=True, scores={K_MI: 1014}, max_dur="Plus de 6 min", platform="Stability API, fal",
    pros=["Entraîné sur données sous licence (éditeur)"], cons=["Pas de voix chantée évaluée", "Poids fermés"],
    src=[S(SA3, "independant"), S("https://www.digitalmusicnews.com/2026/05/21/stability-ai-3-0-release/", "independant")]))
A(M("stable-audio-3-medium", "Stable Audio 3", "Medium (1,4 B)", "Stability AI", "GB", "music", "2026-05-20",
    ow=True, lic="Licence Stability (« other » sur Hugging Face, Community License selon la presse)", scores={K_MI: 996},
    max_dur="6 min 20", g5090=True, g4090=True, tool="stable-audio-tools ; ComfyUI (Comfy-Org/stable-audio-3)", vram="1,4 milliard de paramètres.",
    pros=["Instrumental ouvert au niveau de MiniMax Music", "Données sous licence"], cons=["Licence à lire pour l'usage commercial"],
    src=[S("https://huggingface.co/stabilityai/stable-audio-3-medium"), S(SA3, "independant")]))
A(M("stable-audio-3-small", "Stable Audio 3", "Small music (459 M)", "Stability AI", "GB", "music", "2026-05-20",
    ow=True, lic="Licence Stability (« other » sur Hugging Face)", scores={K_MI: 946}, max_dur="2 min",
    g5090=True, g4090=True, tool="stable-audio-tools ; ComfyUI", vram="459 millions de paramètres.",
    src=[S("https://huggingface.co/stabilityai/stable-audio-3-small-music"), S(SA3, "independant")]))
A(M("stable-audio-3-small-sfx", "Stable Audio 3", "Small SFX (459 M)", "Stability AI", "GB", "sfx", "2026-05-20",
    ow=True, lic="Licence Stability (« other » sur Hugging Face)", max_dur="2 min",
    g5090=True, g4090=True, tool="stable-audio-tools ; ComfyUI", vram="459 millions de paramètres.",
    pros=["Bruitages ouverts entraînés sur données sous licence"], cons=["Pas de classement indépendant"],
    src=[S("https://huggingface.co/stabilityai/stable-audio-3-small-sfx"), S(SA3, "independant")]))
A(M("stable-audio-open-1-0", "Stable Audio Open", "1.0", "Stability AI", "GB", "sfx", "2024-05-24",
    ow=True, lic="Licence Stability (« other » sur Hugging Face)", g5090=True, g4090=True, tool="stable-audio-tools ; ComfyUI",
    cons=["Remplacé par Stable Audio 3"], src=[S("https://huggingface.co/stabilityai/stable-audio-open-1.0")]))
ACE = "https://huggingface.co/ACE-Step/Ace-Step1.5"
A(M("ace-step-1-5", "ACE-Step", "ACE-Step 1.5", "ACE Studio et StepFun", "CN", "music", "2026-01-23",
    ow=True, lic="MIT (commercial autorisé)", languages="50+ langues", max_dur="Des boucles courtes à 10 min",
    emotions="Reprise (cover), repaint, extraction, passage voix vers fond musical.",
    g5090=True, g4090=True, mac=True, tool="ACE-Step (CUDA, MPS, ROCm) ; ComfyUI ; GGUF", vram="Moins de 4 Go (fiche). Moins de 10 s par chanson sur RTX 3090.",
    pros=["Libre, commercial et entraîné sur données sous licence ou libres (éditeur)", "Très rapide, tourne sur Mac"], cons=["Absent des classements AA"],
    src=[S(ACE), S("https://github.com/ace-step/ACE-Step-1.5")]))
YUE2 = "https://huggingface.co/m-a-p/YuE2-3B"
A(M("yue2-3b", "YuE", "YuE2-3B", "M-A-P et HKUST", "CN", "music", "2026-09-09",
    ow=True, lic="CC BY-NC 4.0 (non commercial)", languages="Chinois, anglais (fiche)",
    max_dur="Exemples de 3 à 5 min", emotions="Partition éditable (mélodie et accords en ABC), reprise de chansons, édition par agent.",
    g5090=True, g4090=True, mac=None, tool="transformers (Linux, GPU NVIDIA 24 Go, bf16) ; ComfyUI ; GGUF",
    vram="Mesure éditeur sur RTX 4090 : pic 11,18 Gio, chanson de 3,6 min en 71 s. 24 Go de RAM système conseillés.",
    pros=["Meilleur score SongBench de son propre banc (WildSongBench, éditeur), devant Suno v5 et v6", "Partition modifiable"],
    cons=["Non commercial", "Pas encore dans l'arène AA"], src=[S(YUE2)]))
A(M("yue-s1-7b", "YuE", "YuE s1 7B (v1)", "M-A-P et HKUST", "CN", "music", "2025-01-26",
    ow=True, lic="Apache-2.0", languages="Anglais (variante en-cot)", g5090=True, g4090=None, tool="YuE",
    cons=["Remplacé par YuE2"], src=[S("https://huggingface.co/m-a-p/YuE-s1-7B-anneal-en-cot"), S("https://github.com/multimodal-art-projection/YuE")]))
A(M("meta-musicgen-large", "MusicGen", "musicgen-large", "Meta", "US", "music", "2023-06-08",
    ow=True, lic="CC BY-NC 4.0 (non commercial)", scores={K_MI: 868}, g5090=True, g4090=True, tool="audiocraft, transformers",
    cons=["Dernier de l'arène instrumentale AA", "Non commercial"], src=[S("https://huggingface.co/facebook/musicgen-large")]))

# ============================ SON À PARTIR DE LA VIDÉO ============================
MMA = "https://github.com/hkchengrex/MMAudio"
A(M("mmaudio", "MMAudio", "MMAudio (large 44 kHz)", "Université de l'Illinois et Sony AI", "US", "audio_from_video", "2024-12-10",
    ow=True, lic="CC-BY-NC 4.0 (poids), MIT (code)", api=True, max_dur="8 s par défaut (durée d'entraînement)",
    unit="min", mn=0.06, platform="fal (0,001 $/s)",
    g5090=True, g4090=True, tool="MMAudio ; ComfyUI (Kijai)", vram="Environ 6 Go en 16 bits (éditeur).",
    pros=["Léger, synchronisé à l'image"], cons=["Non commercial, 8 s", "Usage commercial non garanti par les auteurs"],
    src=[S(MMA), S(FAL, "mesure")]))
HVF = "https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley"
HVF_LIC = "Tencent Hunyuan Community License ; téléchargement refusé depuis l'UE (porte Hugging Face « eu_disallowed »)"
A(M("hunyuanvideo-foley-xxl", "HunyuanVideo-Foley", "XXL (défaut)", "Tencent", "CN", "audio_from_video", "2025-08-28",
    ow=True, lic=HVF_LIC, api=True, languages="Prompts anglais et chinois", unit="min", mn=0.60, platform="fal (0,10 $ les 10 s)",
    g5090=True, g4090=True, tool="HunyuanVideo-Foley ; ComfyUI", vram="20 Go, ou 12 Go avec déchargement (éditeur).",
    pros=["Sortie 48 kHz, équilibre image et texte"], cons=["Licence excluant l'Union européenne : problème pour un film produit en France"],
    src=[S(HVF), S("https://huggingface.co/tencent/HunyuanVideo-Foley"), S(FAL, "mesure")]))
A(M("hunyuanvideo-foley-xl", "HunyuanVideo-Foley", "XL", "Tencent", "CN", "audio_from_video", "2025-09-29",
    ow=True, lic=HVF_LIC, g5090=True, g4090=True, tool="HunyuanVideo-Foley ; ComfyUI", vram="16 Go, ou 8 Go avec déchargement (éditeur).",
    cons=["Même licence excluant l'UE"], src=[S(HVF)]))
TS = "https://github.com/FunAudioLLM/ThinkSound"
A(M("thinksound", "ThinkSound", "ThinkSound", "Alibaba Tongyi (FunAudioLLM)", "CN", "audio_from_video", "2025-07-01",
    ow=True, lic="Apache-2.0", api=True, unit="min", mn=0.06, platform="fal (0,001 $/s)",
    emotions="Raisonnement en chaîne : son de base, affinage objet par objet, édition par instruction.",
    g5090=True, g4090=None, tool="ThinkSound (Linux, macOS, Windows) ; GGUF", vram="Non mesuré ici.",
    pros=["Libre et commercial", "Édition interactive du son par objet"], cons=["Suite PrismAudio publiée en 2026"],
    src=[S(TS), S("https://huggingface.co/FunAudioLLM/ThinkSound"), S(FAL, "mesure")]))
A(M("prismaudio", "ThinkSound", "PrismAudio", "Alibaba Tongyi (FunAudioLLM)", "CN", "audio_from_video", "2026-03-24",
    ow=True, lic=None, cons=["Licence et matériel non relevés (branche prismaudio du dépôt ThinkSound)"], src=[S(TS)]))
A(M("foley-omni", "Foley-Omni", "Foley-Omni 5.5B", "NJU-Speech (université de Nankin)", "CN", "audio_from_video", "2026-06-02",
    ow=True, lic="MIT (commercial autorisé)", max_dur="Vidéos de 10 s maximum",
    g5090=None, g4090=None, tool="Foley-Omni", vram="5,5 milliards de paramètres, non mesuré ici.",
    pros=["Parole, bruitages et musique en une passe à partir de la vidéo"], cons=["10 s maximum, jeune projet"],
    src=[S("https://github.com/NJU-Speech/Foley-Omni"), S("https://studio.aifilms.ai/blog/foley-omni-video-soundtrack-generation", "independant")]))
A(M("kling-video-to-audio", "Kling-Foley", "Kling Video-to-Audio", "Kuaishou", "CN", "audio_from_video", None,
    ow=False, api=True, platform="WaveSpeedAI, Layer",
    pros=["Bruitages, ambiances, musique et voix synchronisés à partir d'un plan muet"], cons=["Aucune publication des poids confirmée"],
    src=[S("https://wavespeed.ai/blog/ja/posts/introducing-kwaivgi-kling-video-to-audio-on-wavespeedai/", "independant"), S("https://www.layer.ai/models/kling-video-to-audio", "independant")]))

# ============================ SYNCHRONISATION LABIALE ============================
SY = "https://sync.so/docs/models"
A(M("sync-3", "Sync Labs", "sync-3", "Sync Labs", "US", "lip_sync", "2026-04-06",
    api=True, max_dur="Selon le forfait : 1 min (Hobbyist) à 30 min (Scale+)", unit="min", mn=8.0, platform="fal (8 $/min) ; sync.so 0,107 à 0,133 $/s",
    pros=["Traite le plan entier, détecte les obstructions, sortie 4K"], cons=["Cher"], src=[S(SY), S(FAL, "mesure")]))
A(M("sync-lipsync-2-pro", "Sync Labs", "lipsync-2-pro", "Sync Labs", "US", "lip_sync", "2025-09-02",
    api=True, unit="min", mn=5.0, platform="fal (5 $/min) ; sync.so 0,067 à 0,083 $/s",
    pros=["Super-résolution par diffusion sur la bouche"], cons=["512 × 512 de zone traitée"], src=[S(SY), S(FAL, "mesure")]))
A(M("latentsync-1-6", "LatentSync", "LatentSync 1.6", "ByteDance", "CN", "lip_sync", "2025-06-11",
    ow=True, lic="OpenRAIL++", api=True, unit="min", mn=0.30, platform="fal (0,005 $/s)",
    g5090=True, g4090=None, tool="LatentSync ; ComfyUI", vram="Non mesuré ici.",
    pros=["Ouvert, entraîné en 512 × 512 pour des dents et lèvres moins floues"], cons=["Synchronisation moins exacte que les modèles commerciaux (revue tierce)"],
    src=[S("https://huggingface.co/ByteDance/LatentSync-1.6"), S(FAL, "mesure"), S("https://www.pixazo.ai/blog/best-open-source-ai-lip-sync-models", "independant")]))


# ============================ CONVERSION DE VOIX OUVERTE ============================
A(M("seed-vc", "Seed-VC", "Seed-VC v1.0/v2", "Plachta (communauté)", None, "speech_to_speech", "2024-09-03",
    ow=True, lic="GPL-3.0", clone_s=1, zero_shot=True, consent="aucun",
    emotions="Garde le jeu de la prise source ; conversion de voix chantée avec suivi de hauteur.",
    latency=400, g5090=True, g4090=True, mac=True, tool="seed-vc ; MLX (Avdpro/MLX-Seed-VC-v2)",
    vram="Modèles de 25 à 200 millions de paramètres.",
    price_note=None,
    pros=["Conversion zéro-shot avec 1 à 30 s de référence", "Temps réel : environ 300 ms d'algorithme + 100 ms côté machine", "Voix chantée"],
    cons=["Licence GPL-3.0", "Aucun garde-fou de consentement"],
    src=[S("https://github.com/Plachtaa/seed-vc"), S("https://huggingface.co/Plachta/Seed-VC")]))
A(M("resemble-chatterbox-vc", "Chatterbox", "Chatterbox VC (conversion de voix)", "Resemble AI", "US", "speech_to_speech", None,
    ow=True, lic="MIT (commercial autorisé)", zero_shot=True, consent="aucun",
    g5090=True, g4090=True, mac=None, tool="chatterbox (example_vc.py)", vram="Non mesuré ici.", mod=PERTH,
    pros=["Conversion de voix libre et commerciale dans le même paquet que la synthèse"], cons=["Peu documentée"],
    src=[S("https://github.com/resemble-ai/chatterbox")]))

# ---------------- contrôles ----------------
ids = [r["id"] for r in R]
dup = {i for i in ids if ids.count(i) > 1}
assert not dup, dup
TASKS = {"tts", "voice_clone", "speech_to_speech", "dubbing", "stt", "music", "sfx", "audio_from_video", "lip_sync", "realtime_dialogue"}
for r in R:
    assert r["task"] in TASKS, r["id"]
    assert r["french_quality"] in {"bonne", "moyenne", "faible", "inconnu"}, r["id"]
    assert r["clone"]["consent_check"] in {"aucun", "captcha_vocale", "verification_identite", "inconnu"}, r["id"]
    assert r["sources"], r["id"]
    for s in r["sources"]:
        assert s["type"] in {"editeur", "independant", "mesure"}
json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(R), dict(Counter(r["task"] for r in R)))
