import json, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
for d in ('captions','clips','output'):
    os.makedirs(d, exist_ok=True)
script = json.load(open('script.json'))

import re
def get_dur(path):
    out = subprocess.run([FF,'-i',path], capture_output=True, text=True).stderr
    m = re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)', out)
    if not m: return 3.0
    h,mi,s = map(float, m.groups())
    return h*3600+mi*60+s
FONT = 'NotoNaskhArabic-Regular.ttf'
W, H = 1242, 2208   # 1.15x of 1080x1920 for zoom headroom
FPS = 25
OUTW, OUTH = 1080, 1920

def cover(img, w, h):
    iw, ih = img.size
    r = max(w/iw, h/ih)
    img = img.resize((math.ceil(iw*r), math.ceil(ih*r)), Image.LANCZOS)
    x = (img.width - w)//2; y = (img.height - h)//2
    return img.crop((x, y, x+w, y+h))

def fit_font(draw, text, maxw, start=70):
    f = start
    while f > 30:
        font = ImageFont.truetype(FONT, f)
        if draw.textlength(text, font=font) <= maxw:
            return font
        f -= 4
    return ImageFont.truetype(FONT, 30)

clips = []
for i, b in enumerate(script['beats'], 1):
    im = cover(Image.open(f'images/{b["id"]}.png').convert('RGB'), W, H)
    d = ImageDraw.Draw(im)
    disp = get_display(arabic_reshaper.reshape(b['caption']))
    font = fit_font(d, disp, W-120, 70)
    tw = d.textlength(disp, font=font)
    # rounded translucent bar
    pad = 34
    bx, by = int((W-tw)/2)-pad, H-300
    bw, bh = int(tw)+2*pad, int(font.size*1.9)
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=28, fill=(8,12,28,178))
    d.text((W/2, by+bh/2), disp, font=font, fill=(255,221,128), anchor='mm')
    cap = f'captions/{b["id"]}.png'
    im.save(cap)

    # audio duration
    adur = get_dur(f'audio/{b["id"]}.mp3')
    frames = max(2, int(round(adur*FPS)))
    clip = f'clips/beat{i}.mp4'
    os.makedirs('clips', exist_ok=True)
    vf = (f"[0:v]zoompan=z='min(1.0+0.15*(on/{frames}),1.15)':d={frames}:s={OUTW}x{OUTH}:fps={FPS},"
          f"trim=duration={adur:.3f},setpts=PTS-STARTPTS,format=yuv420p[v]")
    subprocess.run([FF,'-y','-loop','1','-i',cap,'-i',f'audio/{b["id"]}.mp3',
        '-filter_complex',vf,'-map','[v]','-map','1:a','-r',str(FPS),'-c:a','aac','-b:a','128k','-shortest',clip],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clips.append(clip)
    print(f'{b["id"]}: audio {adur:.2f}s -> {clip}')

with open('clips.txt','w') as f:
    for c in clips:
        f.write(f"file '{os.path.abspath(c)}'\n")
subprocess.run([FF,'-y','-f','concat','-safe','0','-i','clips.txt','-c','copy','output/luxora-promo.mp4'],
    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
dur = get_dur('output/luxora-promo.mp4')
print('FINAL output/luxora-promo.mp4  duration=%.2fs  size=%d bytes' % (dur, os.path.getsize('output/luxora-promo.mp4')))
