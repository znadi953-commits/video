# video

Hub vidéo de **znadi953-commits** — shorts / vidéos sociales générées en local, sans clé API.

## luxora-promo (faceless short · Arabe MSA · 31s)

Premier short faceless de promotion pour la marque **LUXORA** (boutique premium fr/en/ar).
Construit en s'inspirant de la méthodologie du skill
[claude-faceless-shorts-creator](https://github.com/hassancs91/claude-faceless-shorts-creator)
(via la liste [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills)),
**mais adapté pour tourner 100% en local, sans ElevenLabs / Gemini / fal.ai** :

- 🖼 Visuels → génération d'images (outil image local)
- 🗣 Voix Arabe (MSA) → synthèse vocale locale
- 🔤 Captions Arabes → rendu avec reshaping + RTL (Noto Naskh Arabic)
- 🎬 Assemblage → `ffmpeg` (zoom Ken Burns + audio)

### Beat grammar
`HOOK → SETUP → REVEAL → REVEAL → TWIST → LOOP` (frame 0 = thumbnail)

| Beat | Rôle | Caption (AR) |
|---|---|---|
| 1 | HOOK | بوتيك ملكي؟ من بيتك؟ |
| 2 | SETUP | لوكسورا — الأناقة والراحة |
| 3 | REVEAL | بثلاث لغات: فرنسي، إنجليزي، عربي |
| 4 | REVEAL | 20+ تجربة حيّة… ومخزن كامل |
| 5 | TWIST | شوفي قبل ما تشري |
| 6 | LOOP | لوكسورا — ابدئي اليوم |

### Structure (`luxora-promo/`)
- `script.json` — beats (narration + captions + prompts image)
- `images/` — visuels générés (1080×1920)
- `audio/` — narration Arabe par beat
- `captions/` — images + captions brûlées
- `clips/` — clips par beat
- `output/luxora-promo.mp4` — **le short final**
- `poster.jpg` — vignette
- `build.py` — pipeline (captions + zoom + assemblage ffmpeg)
- `NotoNaskhArabic-Regular.ttf` — police Arabe

### Régénérer
```bash
pip install imageio-ffmpeg pillow arabic-reshaper python-bidi
python3 luxora-promo/build.py
```

---
Généré avec l'aide de l'agent Arena (outil image + TTS + ffmpeg).
