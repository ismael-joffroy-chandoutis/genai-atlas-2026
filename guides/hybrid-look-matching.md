[English](hybrid-look-matching.md) · [Français](raccord-look-hybride.fr.md)

# Matching a hybrid film (Blackmagic, iPhone, infrared, AI) to a grainy "iPhone" look

Labels: **[vendor]** = claim by the manufacturer or seller · **[verified]** = read in a primary source or confirmed by concordant sources · **[pro]** = statement by a named technician · **[rec]** = synthesis recommendation, to test on your own rushes.

Method: web research on 15 October 2026, official pages read when accessible; unconfirmed points are flagged.

---

## 1. Project colour management

**Choice of working space [rec].** For a film that ends in SDR Rec.709 with a "phone" look, use **DaVinci YRGB Color Managed** in manual mode: timeline space **DaVinci Wide Gamut / DaVinci Intermediate**, output **Rec.709 Gamma 2.4**. ACEScct also works, but brings nothing here: no ACES VFX vendor to feed, and most sources (iPhone HEVC, AI) are not scene-referred captures. The DWG pipeline gives you native colour space transforms (CST) for Gen 5, Apple Log and Rec.709, and the Film Look Creator reads the timeline space by default in Color Managed mode **[verified, 6]**.

If you prefer the unmanaged mode (classic YRGB), build a CST "sandwich" per shot: input to DWG/Intermediate, grade, then output CST to Rec.709. In that case, set the Film Look Creator "Color Space Overrides" to DWG/Intermediate, as users advise on the Blackmagic forum **[pro, 6]**.

**Input of each source**

- **BRAW (Gen 5)**: BRAW 2.0 brought Gen 5 colour science and direct decoding to DaVinci Wide Gamut / DaVinci Intermediate **[verified, 8]**. Camera Raw tab: *Decode using Clip*, Color Science Gen 5, gamut/gamma **DWG / Intermediate**, decode ISO adjusted as needed (it is metadata, lossless), Highlight Recovery on if highlights clip. The Pocket 6K G2 has dual native ISO up to 25,600 **[vendor, 8]**. Do not denoise at decode: you are going to replace the texture anyway.
- **iPhone Apple Log**: Apple provides on developer.apple.com an "Apple Log profile" package with a Log to linear LUT, a Log to Rec.709 LUT and a PDF white paper, according to a Blackmagic forum post **[pro, not re-checked on Apple's page, 10]**. In Resolve, prefer a **CST from Apple Log to DWG/Intermediate** (Resolve offers Apple Log as an input gamma) over a LUT to Rec.709, which would crush highlights before grading. On iPhone 17 Pro, Apple Log 2 exists: its curve and gamut differ from Apple Log, so set the input per clip **[vendor, 11]**.
- **iPhone HEVC "standard" (HDR Dolby Vision / HLG)**: this is the trap. By default the iPhone records HDR **Rec.2100 HLG with Dolby Vision metadata**. In an SDR project the picture looks washed out if Resolve reads the wrong transfer function or has no HDR to SDR conversion set **[pro, 12]**. Check each clip's metadata, force the input to **Rec.2100 HLG**, then one CST with tone mapping to your working space, once; do not stack an "iPhone LUT" on top **[pro, 12]**. If the clip is SDR (HDR setting off), input Rec.709 Gamma 2.4.
- **Infrared**: there is no "correct" colour transform. Decode in Rec.709 or log depending on the camera, white-balance on foliage or an IR chart, then choose: **monochrome** (red channel or a channel mix, the easiest to blend with the rest) or **false colour** (R/B channel swap in the RGB Mixer). Treat IR as a display-referred source, not a scene-referred one **[rec]**.
- **AI shots in 8-bit Rec.709**: input **Rec.709 Gamma 2.4**, then an inverse CST to DWG. You gain clean maths, not latitude: clipped highlights stay clipped, and compressed 8-bit flat areas band as soon as you push contrast **[rec]**. Correct lightly, gently, and before any grain.
- **LTX EXR (HDR IC-LoRA)**: Lightricks presents the HDR IC-LoRA as a **post-process that converts an existing SDR video** into EXR frame by frame, "scene-linear 16-bit" according to ltx.io, validated on LTX-2.3 and not yet on LTX-2.5 **[vendor, 13]**. A third-party guide says "LogC3", which contradicts the official page: open a file and check before choosing the input (Linear / Rec.709 primaries are likely) **[verified: sources contradict, 13]**. Trap: in ComfyUI, without `OPENCV_IO_ENABLE_OPENEXR=1`, the EXR export fails silently **[vendor, 13]**. Reminder: this conversion guesses highlights, it does not recover them.

**SDR or HDR?** Deliver in **SDR Rec.709**. Reasons: most AI shots are born in 8-bit SDR, their highlights do not exist and the HDR IC-LoRA invents them; the "iPhone Smart HDR" look is precisely a tone mapping that squeezes everything into an SDR display; and the gap between AI shots and BRAW is widest in HDR, where clipping and banding show. If an HDR master is required later, derive it from the same grade with a low ceiling (about 300 nits) so the AI shots do not look dull **[rec]**.

---

## 2. What makes the "iPhone look"

Technical breakdown **[rec, supported by 4, 14]**:

1. **Small-sensor noise**: fine luminance and blotchy chroma in the shadows as soon as light drops.
2. **Aggressive temporal noise reduction**: textures that smear and freeze, waxy flat areas, trails on movement.
3. **Sharpening**: bright halos around edges, artificial micro-contrast. Published iPhone/ALEXA matching tests put most of the gap in sharpness **[pro, 14]**.
4. **Multi-frame HDR and local tone mapping**: lifted shadows, synthetically recovered skies, slightly raised blacks **[pro, 14]**.
5. **HEVC compression**: blocks in gradients, loss of fine detail in motion, 4:2:0 chroma. On *28 Years Later*, Union VFX had to deal with 4:2:0 subsampling and recreated compression artefacts **[pro, 4]**.
6. **Optics**: 24-26 mm equivalent wide angle, software-corrected distortion (stretched edges), nearly infinite depth of field.
7. **Time**: 30 or 60 fps, short shutter in daylight (staccato motion), rolling shutter, electronic stabilisation that "floats".

**Rebuilding it on a clean image (BMD, AI) [rec]**, in this order:

1. Reframing and **distortion** (Resolve Lens Correction in the inspector, or the Lens Distortion tool in Fusion; a slight barrel distortion if you start from a longer lens).
2. **Depth of field**: impossible to restore cleanly; shoot the Blackmagic stopped down (f/8 and beyond) with a short lens. For AI, do not ask for bokeh in the prompt.
3. **"Smart HDR" tone mapping**: a curve that lifts shadows and compresses highlights, plus local contrast (Contrast Pop or positive Midtone Detail).
4. **Smoothing then sharpening**: an exaggerated temporal Noise Reduction pass to reproduce the smearing, then Sharpen with a 1 to 2 pixel radius to create halos.
5. **Digital noise** (luminance plus chroma, stronger in the shadows).
6. **Compression**: an intermediate render in HEVC or H.264 at low bitrate (for instance 8 to 15 Mb/s in 1080p, 4:2:0, long GOP), re-imported into the timeline. It is the only way to get real macroblocks that move.

**Tools, with their status**

- **Resolve Studio**: *Film Grain* (ResolveFX), *Film Look Creator* (grain, blur, halation, vignette; not available in the free version) **[verified, 6]**, temporal and spatial Noise Reduction, Sharpen, Blur, Motion Blur. An effect called "Digital Noise" **was not found**: do not look for it under that name.
- **FilmConvert Nitrate / CineMatch**: Apple Log (iPhone 15 Pro, 2023) and iPhone 12 Pro profiles **[vendor, 15]**. They match colour; they do not make phone noise, and the plug-in aims at film grain.
- **Dehancer**: film emulation (grain, halation) **[vendor]**; no smartphone profile found.
- **Video Village Filmbox**: film emulation **[vendor]**. **LensNode** (Node Mill, distributed by Video Village since 23 July 2026): lens simulation from more than 111 measured profiles (bokeh, aberrations, distortion, vignetting), in ACES, for Resolve, Baselight, Premiere, After Effects and FCP; 149 USD per year or 399 USD perpetual **[vendor and independent review, 24]**. "Scatter" not confirmed.
- **Boris FX Sapphire, Red Giant Universe**: grain, noise and video degradation effects **[vendor, not re-checked for this version]**.
- **Neat Video**: noise profile per camera and per mode, reusable, temporal and spatial filtering **[vendor, 16]**. No "add noise" function confirmed in Neat Video 6.
- **Topaz**: Add noise and Grain settings; Topaz acknowledges that without them the result can look "plastic" in gradients **[vendor, 17]**.

**Profiles extracted from real iPhone rushes [rec, supported by 2, 3]**:

- *Nuke, DasGrain* (free gizmo by Fabian Holtz): three inputs (denoised plate, comp, original plate), analysis on a flat, dark area, then reinjection of the real noise. It does not work in Nuke Indie or Nuke NC, and it requires good denoising **[pro, 2]**. To apply it to a Blackmagic shot, create a "donor plate": a neutral, defocused grey iPhone shot (wall, overcast sky) at the target ISO, from which you extract the noise.
- *onegrain* (sync. labs, announced 7 July 2026): denoising and regraining in one pipeline, command line, API and OFX plug-in for Nuke, Resolve and Baselight; the author calls it "not perfect yet" **[vendor, 3]**.
- *Manual method in Resolve*: shoot a grey chart and a neutral wall on iPhone at several ISOs, subtract the denoised version (Difference or Subtract blend in a Layer Mixer node), keep the residue centred on 50 % grey and overlay it in Soft Light or Overlay on your clean shots. You get real noise with the right structure, and it stays iPhone noise.

---

## 3. Degrain and regrain

The rule of all post-production: "remove the grain, do the work, put the grain back" **[pro, 3]**.

- **Before the AI**: denoise the start images you give the models (frames extracted from the rushes). sync. labs observes that any noise removed before processing improves the output **[pro, 3]**. A diffusion model reads noise as content: it erases it, turns it into patterns, or invents its own that flickers from frame to frame. **Never ask for grain in the prompt**: you would get a "painted" texture that moves with the image and that no one can remove later **[rec]**.
- **Before upscaling**: denoise if needed, otherwise the upscaler sharpens the noise **[vendor, 17]**. A post on the Topaz forum advises running their software last **[unverified statement, 17]**.
- **Before grading**: denoise noisy sources (iPhone at night, IR, high-ISO BMD) in the first node or upstream (Neat Video, Resolve temporal NR), so every source starts from a clean base.
- **After everything**: generate the grain or noise **last, at output resolution, identical on every source**, through a timeline node or an adjustment layer. The same noise over the whole film unifies heterogeneous sources **[vendor, 19]**. Only the final compression comes after.

Point of disagreement: some vendor guides place grain **before** the final grade **[vendor, 18]**. For sensor noise, place it **after** the grade and **before** the simulated compression: a phone's noise appears before HEVC encoding, and the encoding transforms it **[rec]**.

---

## 4. Matching the AI shots

- **Neutral or graded start image?** Give the model an image **already graded in the look's colour, but clean** (no noise, no sharpening). Advantage: the model directly produces the right palette and exposure, so less destructive grading in 8 bits. Risk: models often push saturation and contrast; check the drift on long shots. A neutral image leaves more room in theory, but an 8-bit render has almost none **[rec]**.
- **Style references**: frames from the rushes, denoised. **Style LoRA**: train it on clean images. On grainy images, the LoRA learns the noise as a fixed pattern and reproduces it badly **[rec]**.
- **Upscale** (Topaz Starlight or Proteus, SeedVR2, FlashVSR): **before** the grain, always.
- **Frame rate**: choose a single timeline rate. If the iPhone shot 30 fps and the look wants "phone", a **30 fps** timeline is consistent; then generate the AI at 30 fps or interpolate it. At 24 fps, conform the iPhone shots to 24 (sped up or slowed down as the case requires) and avoid pulldown **[rec]**.
- **Motion blur**: models add little or badly. Resolve (Motion Effects, Motion Blur) or RSMB to add it. The daylight iPhone look wants **little** blur (short shutter), so dose lightly.
- **Rolling shutter**: can be simulated with a per-line vertical offset (Fusion, an expression, or a Sapphire-type plug-in); keep it for fast moves.
- **Wide-angle distortion**: apply it to AI and BMD shots before the noise, never after.

---

## 5. Overall order of the pipeline

| # | Pass | BMD (BRAW) | iPhone Apple Log | iPhone HEVC HLG | IR | AI (Rec.709) | AI (LTX EXR) |
|---|---|---|---|---|---|---|---|
| 1 | Ingest | Native BRAW, backup | ProRes Log | Check DV/HLG metadata | Per camera | Log model, seed, 8 bits | Check the actual space |
| 2 | Conform | Single timeline rate, reframe, distortion | Same | Same | Same | Upscale here, interpolation | Same |
| 3 | Denoise | Light if high ISO | Neat Video / temporal NR | Same | Strong | Rarely | Rarely |
| 4 | Colour management | Gen 5 decode to DWG/Intermediate | CST Apple Log to DWG | HLG to DWG with tone mapping | Monochrome or channel swap | CST Rec.709 to DWG | Linear to DWG |
| 5 | Matching primary | Exposure, balance | Same | Same | Density | Small corrections | Same |
| 6 | Creative look (timeline) | Smart HDR curve, local contrast, palette | Same | Same | Same | Same | Same |
| 7 | Texture | Smearing temporal NR + Sharpen radius 1-2 px | Lighter (already there) | Nothing or almost | Same as BMD | Same as BMD | Same as BMD |
| 8 | Noise | Extracted iPhone noise (DasGrain, onegrain or Resolve residue), same layer everywhere | Same | Same | Same | Same | Same |
| 9 | Simulated compression | Low-bitrate HEVC round trip | Same | Same | Same | Same | Same |
| 10 | Output | Rec.709 Gamma 2.4, ProRes 422 HQ master, then deliverables | | | | | |

Checkpoint **[rec]**: after pass 9, watch the shots on a real phone, side by side with an original iPhone shot. What gives a shot away first is the halos and the depth of field; colour comes after.

---

## 6. Documented examples

- **28 Years Later** (Danny Boyle, Anthony Dod Mantle, 2025): partly shot on modified iPhone 15 Pro Max, with a DJI Inspire 3 drone and GoPro on an FPV drone **[verified, 1, 4]**. At Union VFX, Gascoyne says the iPhone colour pipeline was "fairly good", but 4:2:0 was a problem on bluescreen; the team was "matching the grain structure", adding "it was not really grain", and reproduced what the phone does to the image, compression included; they also had to match the soft, vignetted edges of vintage lenses. Dillan Nicholls cites chroma subsampling, stabilisation artefacts, clipped highlights and focus jumps. The Apple Log to ARRI Log conversion was an obstacle for editing and monitoring. Internal stabilisation was turned off to allow tracking **[pro, 4, befores & afters, 7 August 2026]**. The colourist is not named in the sources read.
- **Tangerine** (Sean Baker, 2015): three iPhone 5s, FiLMiC Pro (control of exposure, focus, white balance, 50 Mb/s encoding in 1080p), Moondog Labs 1.33x anamorphic adapter, around 24 mm. Saturation was deliberately pushed in post in Final Cut Pro **[verified, 20, 21]**. No colourist named.
- **Unsane** (Soderbergh, 2018): three iPhone 7 Plus in 4K, FiLMiC Pro (log or flat curve), Moment 18 mm, 60 mm and fisheye lenses **[verified, 22]**. **High Flying Bird** (2019): iPhone 8, Moondog 1.33x, FiLMiC Pro **[verified, 23]**. No colourist interview found for either film.
- **iPhone / cinema matching (published tests)**: even after colour matching with CineMatch or FilmConvert, noise, clipped whites and artificial sharpening remain; blacks are lifted by dynamic tone mapping; "the iPhone keeps the look of a small sensor" **[pro, 14]**.
- **"Shot on iPhone" ads** and music videos: no colourist interview on matching or grain found in this research. To dig into by post-production house names.

Practical conclusion: on the one well-documented recent case (*28 Years Later*), the professionals did not add "film grain" to VFX shots; they reproduced **the phone's processing** (noise, compression, lens defects). That is the method to follow for the Blackmagic and for the AI.

---

## Sources

1. Definition Magazine, "Production: 28 Years Later", 2025. https://definitionmagazine.com/features/production-28-years-later/
2. Nukepedia, DasGrain v1.8 (Fabian Holtz) and UAL course notes. https://www.nukepedia.com/gizmos/other/dasgrain · https://mngonzalezsanchez.myblog.arts.ac.uk/?p=764
3. sync. labs (Hadi), "The film grain problem", 7 July 2026. https://sync.so/blog/the-film-grain-problem
4. befores & afters (Ian Failes), "What it took to film with iPhones on 28 Years Later", 7 August 2026. https://beforesandafters.com/2026/08/07/what-it-took-to-film-with-iphones-on-28-years-later/
5. Filmmaker Magazine, interview with Anthony Dod Mantle (page returned 403, not read). https://filmmakermagazine.com/132924-interview-cinematographer-anthony-dod-mantle-28-years-later/
6. Blackmagic forum, placing the Film Look Creator in a CST workflow; Mixing Light, Film Look Creator overview. https://forum.blackmagicdesign.com/viewtopic.php?p=1144897 · https://mixinglight.com/color-grading-tutorials/film-look-creator-resolvefx-overview-workflow
7. DaVinci Resolve Club, Film Look Creator. https://davinciresolveclub.com/davinci-resolve-film-look-creator/
8. 4K Shooters, firmware 7.3 and Gen 5 on Pocket 4K/6K, 27 April 2021; BusinessWire, Pocket 6K G2, 23 June 2022. https://4kshooters.net/2021/04/27/blackmagic-camera-7-3-update-adds-gen-5-color-science-to-the-pocket-4k-and-6k-cameras · https://www.businesswire.com/news/home/20220623005759/en
9. Wolfcrow, Pocket 6K Pro. https://wolfcrow.com/important-quirks-and-features-of-the-blackmagic-pocket-cinema-camera-6k-pro-for-cinematography/
10. Blackmagic forum, "Where can I download the Apple Log to Rec709 LUT cube?". https://forum.blackmagicdesign.com/viewtopic.php?p=1052853
11. Gamut, "Apple Log vs Apple Log 2 in DaVinci Resolve". https://gamut.io/apple-log-vs-apple-log-2-in-davinci-resolve-why-color-space-matters/
12. DaVinci Resolve Club, iPhone HDR to SDR; DPReview, iPhone 12 Dolby Vision and Resolve. https://davinciresolveclub.com/iphone-hdr-to-sdr-davinci-resolve/ · https://www.dpreview.com/forums/thread/4591722
13. Lightricks, docs "HDR Video (IC-LoRA) Beta" and "Working with EXR & HDR"; ltx.io, AI video to HDR. https://docs.ltx.io/open-source-model/advanced-workflows/hdr-video-beta · https://docs.ltx.io/open-source-model/usage-guides/working-with-exr-hdr · https://ltx.io/model/capabilities/ai-video-to-hdr
14. No Film School, iPhone 12 Pro with FilmConvert/CineMatch; RedShark, ALEXA vs iPhone; Noam Kroll, iPhone 13 vs ALEXA. https://nofilmschool.com/color-match-your-iphone-12-pro-different-camera-profiles-filmconvert-or-cinematch · https://www.redsharknews.com/alexa-vs-iphone-impressive-results-but-whats-the-catch · https://noamkroll.com/iphone-13-vs-arri-alexa-comparison-why-apples-color-science-is-so-impressive/
15. Newsshooter, FilmConvert Nitrate and CineMatch now support Apple Log, 12 October 2023. https://www.newsshooter.com/2023/10/12/filmconvert-nitrate-and-cinematch-now-support-apple-log/
16. Neat Video, "How does it work". https://www.neatvideo.com/overview/how-does-it-work
17. Topaz Labs, noise, detail and grain settings; Topaz forum "Video AI Workflow?". https://www.topazlabs.com/learn/topaz-video-enhancements-2-noise-detail-focus-grain · https://community.topazlabs.com/t/video-ai-workflow/59211
18. invideo, "Should you upscale AI video before or after colour?" (vendor). https://invideo.io/faq/should-you-upscale-ai-video-before-or-after-colour/
19. Vindral, Film Grain operator. https://composer-docs.vindral.com/operators/operators-film-grain.html
20. American Cinematographer (ASC), "Tangerine: iPhone enables streetwise story". https://theasc.com/articles/tangerine-iphone-enables-streetwise-story
21. Videomaker, "Tangerine dream". https://www.videomaker.com/article/c02/18673-tangerine-dream-how-a-film-shot-on-an-iphone-made-it-to-the-big-screen/
22. Inverse, Unsane shot on iPhone 7 Plus, 2018. https://www.inverse.com/article/42571-unsane-steven-soderbergh-shot-with-iphone-7-plus
23. AppleInsider, High Flying Bird, 28 January 2019; Wikipedia, High Flying Bird. https://appleinsider.com/articles/19/01/28/soderbergh-returns-to-iphone-filmography-with-high-flying-bird · https://en.wikipedia.org/wiki/High_Flying_Bird
24. Newsshooter, "LensNode is now with Video Village", 23 July 2026; postPerspective, LensNode review, March 2026. https://www.newsshooter.com/2026/07/23/lensnode-is-now-with-video-village-alongside-filmbox-scatter/ · https://postperspective.com/review-node-mills-lensnode-lens-simulation-plugin-for-resolve/

---

State verified on 15 October 2026. Text under a [CC BY-SA 4.0](../LICENSE) license.
