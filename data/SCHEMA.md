# Schéma des données (genai-atlas-2026)

Un fichier JSON par lot, tableau d'objets. Toute valeur inconnue = null (jamais deviner). Chaque objet a "sources": [{"url":..., "date":"AAAA-MM-JJ", "type":"editeur|independant|mesure"}].

## models (video-models.json, image-models.json)
{
 "id": "minimax-h3-max-turbo",           // kebab-case unique
 "family": "MiniMax H3", "variant": "H3 Max Turbo",
 "vendor": "MiniMax", "country": "CN",
 "modality": "video" | "image",
 "released": "AAAA-MM-JJ" | null,
 "access": {"open_weights": bool, "license": str|null, "api": bool, "consumer_app": bool},
 "ranking": {"aa_text_to_video": int|null, "aa_image_to_video": int|null, "aa_text_to_image": int|null, "aa_image_edit": int|null, "aa_note": str|null},
 "inputs": {
   "text": bool,
   "image_refs_max": int|null, "video_refs_max": int|null, "video_refs_total_s": num|null,
   "audio_refs_max": int|null, "audio_refs_total_s": num|null,
   "first_frame": bool|null, "last_frame": bool|null, "keyframes_max": int|null,
   "video_to_video": bool|null, "control": [ "depth","pose","canny","layout","3d" ... ] ,
   "camera_control": bool|null, "input_3d": bool|null,
   "image_edit": bool|null, "multi_image_edit_max": int|null,
   "lora_inference": bool|null, "lora_training": bool|null,
   "incompatible_combinations": str|null
 },
 "outputs": {"max_resolution": str|null, "min_s": num|null, "max_s": num|null, "fps": str|null,
             "native_audio": bool|null, "lip_sync": bool|null, "languages": str|null,
             "max_images_per_call": int|null, "text_rendering": str|null},
 "edit_functions": [str],
 "local": {"runs_on_rtx5090_32gb": bool|null, "vram_note": str|null},
 "moderation": {"real_faces": "bloque|verif_identite|autorise|inconnu", "public_figures": str|null, "notes": str|null},
 "pros": [str], "cons": [str],
 "sources": [...]
}

## prices (prices.json)
{"model_id": "...", "platform": "fal|openrouter|replicate|runware|wavespeed|kie|byteplus|official|krea|higgsfield|...",
 "endpoint": str|null, "unit": "per_second|per_image|per_token|credits|subscription",
 "price_usd_480p_s": num|null, "price_usd_720p_s": num|null, "price_usd_1080p_s": num|null,
 "price_usd_per_image": num|null, "raw": str, "retrieved_at": "2026-10-15", "source_url": str, "verified": "api_live|page|tiers"}
