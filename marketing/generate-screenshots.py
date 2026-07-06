#!/usr/bin/env python3
# Generates 6 App Store screenshot HTML files (1320x2868) for できた！.
import os
import base64
import re
import unicodedata

BASE = """
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1320px; height:2868px; overflow:hidden; }}
body {{
  font-family:'Hiragino Maru Gothic ProN','BIZ UDPGothic',sans-serif;
  background: linear-gradient(160deg,#ffe0ec 0%,#fff5cc 50%,#d4f0ff 100%);
  padding:96px 70px 0; display:flex; flex-direction:column; align-items:center;
}}
body.night {{ background: linear-gradient(160deg,#1a1a4e 0%,#2d1b69 50%,#0d2b4e 100%); }}
/* status bar */
.status {{ width:100%; height:120px; display:flex; align-items:center; justify-content:space-between; padding:6px 26px 0; }}
.status .time {{ font-size:44px; font-weight:600; color:#111; }}
.status .right {{ display:flex; align-items:center; gap:18px; }}
body.night .status .time {{ color:#fff; }}
.batt {{ width:58px; height:28px; border:4px solid #111; border-radius:8px; position:relative; }}
.batt::after {{ content:''; position:absolute; right:-10px; top:8px; width:6px; height:10px; background:#111; border-radius:0 3px 3px 0; }}
.batt .fill {{ position:absolute; inset:3px; background:#111; border-radius:3px; }}
body.night .batt {{ border-color:#fff; }} body.night .batt::after {{ background:#fff; }} body.night .batt .fill {{ background:#fff; }}
.wifi path {{ fill:#111; }} body.night .wifi path {{ fill:#fff; }}
/* caption */
.caption {{ font-family:'Hiragino Sans','Hiragino Kaku Gothic ProN','BIZ UDPGothic',sans-serif;
  font-size:70px; font-weight:800; color:#ff5a87; text-align:center; margin:46px 0 34px; white-space:nowrap; }}
.subcap {{ font-size:38px; color:#b9728a; text-align:center; margin-bottom:38px; }}
body.night .caption {{ color:#c7a8ff; }} body.night .subcap {{ color:#9a8fce; }}
/* ss-1: "no ads" badge at the top-left of the canvas, above the caption */
.adfree-badge {{ position:absolute; top:56px; left:56px; z-index:2;
  font-family:'Hiragino Sans','Hiragino Kaku Gothic ProN','BIZ UDPGothic',sans-serif;
  font-size:58px; font-weight:800; color:#fff; background:#ff5a87;
  padding:28px 56px; border-radius:80px; white-space:nowrap;
  box-shadow:0 10px 26px rgba(255,90,135,.45); transform:rotate(-5deg); }}
/* ss-1: frame the app screenshot so it reads separately from the caption/bg */
body.framed {{ background:#edeef3; }}
.appshot {{ position:relative; width:100%; margin-top:40px; padding:70px 0 56px;
  background:linear-gradient(160deg,#ffe0ec 0%,#fff5cc 50%,#d4f0ff 100%);
  border-radius:60px; box-shadow:0 18px 48px rgba(0,0,0,.16);
  display:flex; flex-direction:column; align-items:center; }}
/* ss-1 only: slightly taller cards so the frame fills the canvas */
.appshot .card {{ height:500px; }}
/* hero */
.hero-main {{ font-size:88px; font-weight:bold; color:#ff5a87; text-shadow:4px 6px 0 #fff; white-space:nowrap; }}
body.night .hero-main {{ color:#c7a8ff; text-shadow:3px 4px 0 rgba(0,0,0,.4); }}
.hero-sub {{ font-size:34px; color:#999; margin-top:12px; }}
body.night .hero-sub {{ color:#7a7aaa; }}
/* tabs */
.tabs {{ display:flex; gap:16px; background:rgba(255,255,255,.55); padding:14px; border-radius:90px; margin:46px 0; }}
body.night .tabs {{ background:rgba(255,255,255,.12); }}
.tab {{ font-size:44px; font-weight:bold; padding:22px 60px; border-radius:70px; color:#aaa; }}
.tab.active {{ background:#fff; color:#ff5a87; box-shadow:0 6px 16px rgba(255,90,135,.25); }}
body.night .tab.active {{ background:#ff7eb6; color:#fff; }}
/* grid */
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:42px; width:100%; }}
.card {{ height:420px; border-radius:46px; background:#fff; box-shadow:0 14px 34px rgba(0,0,0,.10);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px; }}
body.night .card {{ background:#26264f; }}
.card .icon {{ font-size:146px; line-height:1; }}
.card .label {{ font-size:50px; font-weight:bold; color:#444; }}
body.night .card .label {{ color:#c8c8ea; }}
.c1{{border-top:15px solid #ff8aaa;}} .c2{{border-top:15px solid #ffb74d;}} .c3{{border-top:15px solid #4fc3f7;}}
.c4{{border-top:15px solid #81c784;}} .c5{{border-top:15px solid #9575cd;}} .c6{{border-top:15px solid #f06292;}}
.done {{ background:linear-gradient(145deg,#fffde7,#fff59d); border-bottom:13px solid #ffd54f; }}
body.night .done {{ background:linear-gradient(145deg,#2d1b69,#1a1a6e); border-bottom:13px solid #7c4dff; }}
.done .face {{ font-size:190px; line-height:1; }} .done .star {{ font-size:54px; }}
.card.mosaic {{ background-repeat:no-repeat; border-bottom:none; overflow:hidden; }}
/* settings */
.set-screen {{ width:100%; background:#f5f5f7; border-radius:50px; box-shadow:0 14px 40px rgba(0,0,0,.12); overflow:hidden; }}
.set-head {{ display:flex; align-items:center; justify-content:space-between; padding:44px 50px; background:#fff; border-bottom:2px solid #e7e7ec; }}
.set-head .back {{ font-size:42px; font-weight:bold; color:#ff5a87; }}
.set-head .ttl {{ font-size:46px; font-weight:bold; color:#333; }}
.set-head .rst {{ font-size:38px; font-weight:bold; color:#bbb; }}
.set-tabs {{ display:flex; gap:16px; justify-content:center; padding:40px 0 36px; }}
.stab {{ font-size:40px; font-weight:bold; padding:18px 60px; border-radius:60px; border:4px solid #e2e2e2; background:#fff; color:#aaa; }}
.stab.on {{ background:#ff5a87; border-color:#ff5a87; color:#fff; }}
.set-hint {{ text-align:center; color:#bbb; font-size:34px; padding:6px 0 30px; }}
.row {{ display:flex; align-items:center; gap:28px; background:#fff; border-radius:30px; padding:26px 34px; margin:0 36px 26px; box-shadow:0 2px 8px rgba(0,0,0,.06); }}
.row .num {{ font-size:38px; color:#ccc; font-weight:bold; width:30px; }}
.row .emo {{ width:118px; height:118px; border:4px solid #e8e8e8; border-radius:26px; background:#fafafa; display:flex; align-items:center; justify-content:center; font-size:74px; }}
.row .lab {{ flex:1; height:104px; border:4px solid #e8e8e8; border-radius:26px; background:#fafafa; display:flex; align-items:center; padding:0 34px; font-size:50px; font-weight:bold; color:#333; }}
/* celebration */
.celeb {{ width:100%; flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:30px; position:relative; }}
.celeb .big {{ font-size:240px; line-height:1; }}
.celeb .txt {{ font-size:96px; font-weight:bold; color:#ff5a87; text-shadow:4px 6px 0 #fff; }}
.celeb .sub {{ font-size:40px; color:#b9728a; }}
.conf {{ position:absolute; width:26px; height:38px; border-radius:5px; }}
/* photo on the card back (v1.1) */
.photo {{ position:relative; width:100%; height:100%; border-radius:46px; overflow:hidden; }}
.photo svg {{ position:absolute; inset:0; width:100%; height:100%; display:block; }}
.photo .subj {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:188px; line-height:1; filter:drop-shadow(0 6px 10px rgba(0,0,0,.18)); }}
.photo .star {{ position:absolute; top:20px; right:24px; font-size:54px; filter:drop-shadow(0 2px 4px rgba(0,0,0,.35)); z-index:2; }}
.sceneA {{ background:
  radial-gradient(circle at 24% 28%, rgba(255,255,255,.55) 0 5%, transparent 6%),
  radial-gradient(circle at 72% 18%, rgba(255,255,255,.4) 0 4%, transparent 5%),
  radial-gradient(circle at 82% 62%, rgba(255,244,210,.6) 0 7%, transparent 8%),
  radial-gradient(circle at 38% 78%, rgba(255,255,255,.35) 0 6%, transparent 7%),
  linear-gradient(150deg,#ffd9a8 0%,#ff9fb6 58%,#c89cff 100%); }}
.sceneB {{ background:
  radial-gradient(circle at 28% 24%, rgba(255,255,255,.5) 0 5%, transparent 6%),
  radial-gradient(circle at 76% 30%, rgba(255,255,255,.38) 0 4%, transparent 5%),
  radial-gradient(circle at 66% 74%, rgba(255,255,255,.34) 0 7%, transparent 8%),
  radial-gradient(circle at 30% 70%, rgba(220,255,210,.5) 0 6%, transparent 7%),
  linear-gradient(150deg,#a6e3a1 0%,#74c7ec 60%,#89b4fa 100%); }}
/* photo shot (v1.1) — a real photo of a kid's drawing being snapped */
.photoshot {{ width:100%; display:flex; flex-direction:column; align-items:center; }}
.photoshot img {{ width:1000px; border-radius:56px; box-shadow:0 34px 70px rgba(0,0,0,.28); }}
.photoshot .tag {{ margin-top:70px; font-size:46px; font-weight:bold; color:#3f8f5f;
  background:rgba(255,255,255,.78); padding:30px 56px; border-radius:80px;
  box-shadow:0 8px 22px rgba(0,0,0,.10); }}
/* full-screen clear photo (v1.1) — the user's own picture fills the screen */
.celeb.photobg {{ overflow:hidden; border-radius:60px; margin-bottom:44px; }}
.celeb .photoback.shot {{ background-size:auto 152%; background-position:center; }}
.celeb .photoback {{ position:absolute; inset:0; z-index:0; overflow:hidden;
  background:linear-gradient(#37286b 0%,#7a3f86 26%,#e9744f 60%,#ffc987 100%); }}
.celeb .photoback::after {{ content:''; position:absolute; inset:0; z-index:3;
  background:linear-gradient(rgba(0,0,0,.26),rgba(0,0,0,.46)); }}
.celeb .photoback .sun {{ position:absolute; left:50%; top:52%; transform:translate(-50%,-50%);
  width:300px; height:300px; border-radius:50%;
  background:radial-gradient(circle,#fff7e0 0%,#ffd884 52%,rgba(255,190,120,0) 72%); }}
.celeb .photoback .hill {{ position:absolute; left:-6%; right:-6%; bottom:0; z-index:2;
  border-radius:50% 50% 0 0 / 100% 100% 0 0; }}
.celeb .photoback .hill.back {{ height:30%; background:#5a3a6e; }}
.celeb .photoback .hill.front {{ height:20%; background:#2e2350; left:-12%; right:-12%; }}
.celeb.photobg .big {{ position:relative; z-index:2; text-shadow:0 4px 14px rgba(0,0,0,.45); }}
.celeb.photobg .txt {{ position:relative; color:#fff; text-shadow:0 4px 14px rgba(0,0,0,.5); z-index:2; }}
.celeb.photobg .sub {{ position:relative; color:#fff; opacity:.9; z-index:2; }}
.celeb.photobg .conf {{ z-index:2; }}
</style></head><body class="{bodyclass}">{body}</body></html>
"""

# No fake status bar (time/wifi/battery). Each screen still calls
# STATUS.format(time=...) for backwards-compat; an empty template yields "".
STATUS = ""

# ---- caption auto-sizing + trust badge ----------------------------------
# Captions are the big promo lines. We size each one to fill (almost) the whole
# content width on a single line, so short captions get much larger.
_CONTENT_W = 1120   # 1320 − padding, with safety margin (caption is nowrap)

def _text_units(s):
    u = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x1F000 or 0x2600 <= o <= 0x27BF:   # emoji / pictographs
            u += 1.15
        elif ch == ' ':
            u += 0.4
        elif unicodedata.east_asian_width(ch) in ('F', 'W', 'A'):
            u += 1.0
        else:
            u += 0.55
    return u

def _cap_size(text, cap=140, floor=80):
    u = _text_units(text)
    return int(max(floor, min(cap, _CONTENT_W / u))) if u else cap

def enrich(body):
    """Size each caption to fill (almost) one line."""
    def _size_cap(m):
        text  = m.group(1)
        plain = re.sub(r'<[^>]+>', '', text)
        return f'<div class="caption" style="font-size:{_cap_size(plain)}px">{text}</div>'
    return re.sub(r'<div class="caption">(.*?)</div>', _size_cap, body, flags=re.S)

def grid(cards):
    return '<div class="grid">' + ''.join(cards) + '</div>'

def done(face, star):
    return f'<div class="card done"><div class="face">{face}</div><div class="star">{star}</div></div>'

def task(cls, icon, label):
    return f'<div class="card {cls}"><div class="icon">{icon}</div><div class="label">{label}</div></div>'

# A real child's crayon drawing, used as the single picture that spans the whole
# grid in the v1.1 card-back shot (アタック25-style mosaic — one image, six cards).
_DINO_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'dino.jpg')
_DINO_URI  = 'data:image/jpeg;base64,' + base64.b64encode(open(_DINO_PATH, 'rb').read()).decode()
DINO_W, DINO_H = 644, 951

def _datauri(name):
    p = os.path.join(os.path.dirname(__file__), 'assets', name)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

# A real photo of a child's drawing being snapped with a phone (authenticity:
# "this is your own photo"), and a fire-truck crayon drawing used full-screen
# as the clear-screen background.
_PHOTO_URI     = _datauri('dino-photo.jpg')
_FIRETRUCK_URI = _datauri('firetruck.jpg')

# The asa board sitting behind the (partial) mosaic reveal.
_ASA_TASKS = [
    ("c1", "😴", "おきる"),     ("c2", "👕", "きがえ"),
    ("c3", "🧦", "くつした"),   ("c4", "🍚", "あさごはん"),
    ("c5", "🪥", "はみがき"),   ("c6", "🚽", "といれ"),
]

def dino_mosaic(flipped, uri=_DINO_URI, nw=DINO_W, nh=DINO_H, tasks=_ASA_TASKS):
    """One picture covering the whole grid; only the flipped cards show their
    window into it, the rest stay as ordinary task cards (アタック25 mid-reveal).
    Mirrors the app's applyRewardSizing(): cover the grid, then offset per cell."""
    cols, rows = 2, 3            # iPhone mock grid (see BASE .grid; ss-1 cards are 470px tall)
    cardW, cardH, gap = 569, 500, 42
    GW, GH = cols * cardW + (cols - 1) * gap, rows * cardH + (rows - 1) * gap
    cover  = max(GW / nw, GH / nh)
    iw, ih = nw * cover, nh * cover
    offX, offY = (GW - iw) / 2, (GH - ih) / 2
    cells = []
    for i in range(cols * rows):
        if i in flipped:
            c, r = i % cols, i // cols
            x = offX - c * (cardW + gap)
            y = offY - r * (cardH + gap)
            cells.append(
                f'<div class="card done mosaic" style="background-image:url(\'{uri}\');'
                f'background-size:{iw:.0f}px {ih:.0f}px;'
                f'background-position:{x:.0f}px {y:.0f}px;"></div>')
        else:
            cls, icon, label = tasks[i]
            cells.append(task(cls, icon, label))
    return '<div class="grid">' + ''.join(cells) + '</div>'

# ---------- ASA ----------
asa = STATUS.format(time="7:00") + """
<div class="caption">あさのしたく、じぶんで！</div>
<div class="subcap">タップするだけ。平日の朝がちょっとラクに。</div>
<div class="hero-main">できたら　おしてみよう！</div>
<div class="hero-sub">平日の朝をちょっとラクにする、したくサポート</div>
<div class="tabs"><div class="tab active">☀️ あさ</div><div class="tab">🌙 よる</div></div>
""" + grid([
    done("😊","⭐"), done("😊","⭐"),
    task("c3","🧦","くつした"), task("c4","🍚","あさごはん"),
    task("c5","🪥","はみがき"), task("c6","🚽","といれ"),
])

# ---------- YORU ----------
yoru = STATUS.format(time="20:30") + """
<div class="caption">おやすみの準備も</div>
<div class="tabs"><div class="tab">☀️ あさ</div><div class="tab active">🌙 よる</div></div>
""" + grid([
    task("c1","🛁","おふろ"),   task("c2","👕","パジャマ"),
    task("c3","🪥","はみがき"), task("c4","🚽","といれ"),
    task("c5","📚","えほん"),   task("c6","💤","ねる"),
])

# ---------- SETTINGS ----------
settings = STATUS.format(time="7:05") + """
<div class="caption" style="font-size:112px">わが家のしたくに<br>カスタマイズ</div>
<div class="set-screen">
  <div class="set-head"><div class="back" style="font-size:54px">‹</div><div class="ttl">カード（表）</div><div class="back">保存</div></div>
  <div class="set-tabs"><div class="stab on">☀️ あさ</div><div class="stab">🌙 よる</div></div>
  <div class="row"><div class="num">1</div><div class="emo">😴</div><div class="lab">ぱじゃまをぬぐ</div></div>
  <div class="row"><div class="num">2</div><div class="emo">👕</div><div class="lab">きがえ</div></div>
  <div class="row"><div class="num">3</div><div class="emo">🧦</div><div class="lab">くつした</div></div>
  <div class="row"><div class="num">4</div><div class="emo">🍚</div><div class="lab">あさごはん</div></div>
  <div class="row"><div class="num">5</div><div class="emo">🪥</div><div class="lab">はみがき</div></div>
</div>
"""

# ---------- CELEBRATION ----------
import random
random.seed(7)
colors = ['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#ff922b','#cc5de8','#f06595','#3bc9db']
conf = ''.join(
    f'<div class="conf" style="left:{random.randint(0,100)}%; top:{random.randint(2,95)}%; '
    f'background:{random.choice(colors)}; transform:rotate({random.randint(0,360)}deg);"></div>'
    for _ in range(70))
celebration = STATUS.format(time="7:12") + """
<div class="caption">ぜんぶできたら 大かんせい！</div>
<div class="subcap">がんばりを、おもいっきりおいわい。</div>
<div class="celeb">""" + conf + """
  <div class="big">🌟</div>
  <div class="txt">がんばったね！</div>
  <div class="big">🎉</div>
  <div class="sub">タップしてもどる</div>
</div>
"""

# ---------- CARD BACK IMAGE — lead screenshot (v1.2.1) ----------
# One picture (a real child's crayon drawing) spans all six cards; flipping
# each completed card reveals its slice, アタック25-style.
# Headline is the emotional hook; "no ads" moved to a corner badge.
cardback = STATUS.format(time="7:08") + """
<div class="adfree-badge">広告なし</div>
<div class="caption" style="font-size:112px; line-height:1.35; margin:140px 0 40px">「はやくして！」と<br>言わない朝へ</div>
<div class="appshot">
<div class="hero-main">できたら　おしてみよう！</div>
<div class="tabs"><div class="tab active">☀️ あさ</div><div class="tab">🌙 よる</div></div>
""" + dino_mosaic({0, 3}) + """
</div>
"""

# ---------- CLEAR IMAGE (v1.1) ----------
random.seed(11)
conf2 = ''.join(
    f'<div class="conf" style="left:{random.randint(0,100)}%; top:{random.randint(2,95)}%; '
    f'background:{random.choice(colors)}; transform:rotate({random.randint(0,360)}deg);"></div>'
    for _ in range(70))
clearimg = STATUS.format(time="7:12") + """
<div class="caption">子どものやる気アップ</div>
<div class="celeb photobg">
  <div class="photoback shot" style="background-image:url('""" + _FIRETRUCK_URI + """');"></div>
""" + conf2 + """
  <div class="big">🌟</div>
  <div class="txt">がんばったね！</div>
  <div class="sub">タップしてもどる</div>
</div>
"""

# ---------- PHOTO (v1.1) — "use your child's own drawing/photo" + privacy ----------
photo_shot = STATUS.format(time="7:06") + """
<div class="caption">好きな画像を使える！</div>
<div class="photoshot">
  <img src=\"""" + _PHOTO_URI + """\">
  <div class="tag">🔒 画像はサーバに送られないから安心</div>
</div>
"""

# ss-1 is the card-back image shot (v1.1 headline); the plain あさ board
# (`asa`, still defined above) was retired in favour of it.
out = {
    'ss-1-cardback.html': BASE.format(bodyclass='framed', body=enrich(cardback)),
    'ss-2-photo.html': BASE.format(bodyclass='', body=enrich(photo_shot)),
    'ss-3-clearimage.html': BASE.format(bodyclass='', body=enrich(clearimg)),
    'ss-4-yoru.html': BASE.format(bodyclass='night', body=enrich(yoru)),
    'ss-5-settings.html': BASE.format(bodyclass='', body=enrich(settings)),
    'ss-6-celebration.html': BASE.format(bodyclass='', body=enrich(celebration)),
}
for name, html in out.items():
    with open('/tmp/' + name, 'w') as f:
        f.write(html)
    print('wrote', name)
