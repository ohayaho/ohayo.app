#!/usr/bin/env python3
# Generates 5 App Store screenshots for 13-inch iPad (2064x2752), matching the
# v1.2 iPhone set (gothic captions, no status bar/subcaps, dino mosaic, firetruck
# clear image, photo shot). The app UI is shown as a centered portrait panel.
import os, base64, re, unicodedata

W, H = 2064, 2752
APPW = 1500          # width of the centered app panel
COLS, ROWS = 2, 3
GAP = 44
CARDW = (APPW - (COLS - 1) * GAP) / COLS   # 728
CARDH = 486
GW = APPW
GH = ROWS * CARDH + (ROWS - 1) * GAP       # 1948

def _datauri(name):
    p = os.path.join(os.path.dirname(__file__), 'assets', name)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

_DINO_URI = _datauri('dino.jpg'); DINO_W, DINO_H = 644, 951
_FIRETRUCK_URI = _datauri('firetruck.jpg')
_PHOTO_URI = _datauri('dino-photo.jpg')

BASE = """
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:2064px; height:2752px; overflow:hidden; }}
body {{
  font-family:'Hiragino Maru Gothic ProN','BIZ UDPGothic',sans-serif;
  background: linear-gradient(160deg,#ffe0ec 0%,#fff5cc 50%,#d4f0ff 100%);
  padding:90px 120px 0; display:flex; flex-direction:column; align-items:center;
}}
body.night {{ background: linear-gradient(160deg,#1a1a4e 0%,#2d1b69 50%,#0d2b4e 100%); }}
body.framed {{ background:#edeef3; }}
/* caption (gothic, sized inline by enrich) */
.caption {{ font-family:'Hiragino Sans','Hiragino Kaku Gothic ProN','BIZ UDPGothic',sans-serif;
  font-size:120px; font-weight:800; color:#ff5a87; text-align:center; margin:0 0 40px; white-space:nowrap; }}
body.night .caption {{ color:#c7a8ff; }}
.adfree {{ font-family:'Hiragino Sans','Hiragino Kaku Gothic ProN','BIZ UDPGothic',sans-serif;
  font-size:160px; font-weight:800; color:#ff5a87; text-align:center; white-space:nowrap; margin:0 0 -24px; }}
/* app panel */
.app {{ width:1500px; display:flex; flex-direction:column; align-items:center; }}
.appshot {{ width:1500px; padding:50px 0 56px; border-radius:80px;
  background:linear-gradient(160deg,#ffe0ec 0%,#fff5cc 50%,#d4f0ff 100%);
  box-shadow:0 26px 66px rgba(0,0,0,.16); display:flex; flex-direction:column; align-items:center; }}
.hero-main {{ font-size:104px; font-weight:bold; color:#ff5a87; text-shadow:5px 7px 0 #fff; white-space:nowrap; }}
body.night .hero-main {{ color:#c7a8ff; text-shadow:4px 5px 0 rgba(0,0,0,.4); }}
.hero-sub {{ font-size:46px; color:#999; margin-top:16px; }}
body.night .hero-sub {{ color:#7a7aaa; }}
.tabs {{ display:flex; gap:20px; background:rgba(255,255,255,.55); padding:16px; border-radius:100px; margin:44px 0; }}
body.night .tabs {{ background:rgba(255,255,255,.12); }}
.tab {{ font-size:54px; font-weight:bold; padding:26px 78px; border-radius:80px; color:#aaa; }}
.tab.active {{ background:#fff; color:#ff5a87; box-shadow:0 6px 16px rgba(255,90,135,.25); }}
body.night .tab.active {{ background:#ff7eb6; color:#fff; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:44px; width:1500px; }}
.card {{ height:486px; border-radius:54px; background:#fff; box-shadow:0 16px 40px rgba(0,0,0,.10);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:26px; overflow:hidden; }}
body.night .card {{ background:#26264f; }}
.card .icon {{ font-size:200px; line-height:1; }}
.card .label {{ font-size:70px; font-weight:bold; color:#444; }}
body.night .card .label {{ color:#c8c8ea; }}
.c1{{border-top:18px solid #ff8aaa;}} .c2{{border-top:18px solid #ffb74d;}} .c3{{border-top:18px solid #4fc3f7;}}
.c4{{border-top:18px solid #81c784;}} .c5{{border-top:18px solid #9575cd;}} .c6{{border-top:18px solid #f06292;}}
.card.mosaic {{ background-repeat:no-repeat; }}
/* settings */
.set-screen {{ width:1500px; background:#f5f5f7; border-radius:60px; box-shadow:0 16px 48px rgba(0,0,0,.12); overflow:hidden; }}
.set-head {{ display:flex; align-items:center; justify-content:space-between; padding:50px 60px; background:#fff; border-bottom:2px solid #e7e7ec; }}
.set-head .back {{ font-size:48px; font-weight:bold; color:#ff5a87; }}
.set-head .ttl {{ font-size:52px; font-weight:bold; color:#333; }}
.set-head .sp {{ width:120px; }}
.set-tabs {{ display:flex; gap:20px; justify-content:center; padding:46px 0 16px; }}
.stab {{ font-size:46px; font-weight:bold; padding:22px 72px; border-radius:70px; border:4px solid #e2e2e2; background:#fff; color:#aaa; }}
.stab.on {{ background:#ff5a87; border-color:#ff5a87; color:#fff; }}
.set-hint {{ text-align:center; color:#bbb; font-size:40px; padding:8px 0 36px; }}
.row {{ display:flex; align-items:center; gap:34px; background:#fff; border-radius:36px; padding:32px 44px; margin:0 50px 32px; box-shadow:0 2px 8px rgba(0,0,0,.06); }}
.row .num {{ font-size:46px; color:#ccc; font-weight:bold; width:40px; }}
.row .emo {{ width:148px; height:148px; border:4px solid #e8e8e8; border-radius:32px; background:#fafafa; display:flex; align-items:center; justify-content:center; font-size:92px; }}
.row .lab {{ flex:1; height:130px; border:4px solid #e8e8e8; border-radius:32px; background:#fafafa; display:flex; align-items:center; padding:0 44px; font-size:66px; font-weight:bold; color:#333; }}
/* photo shot */
.photoshot {{ display:flex; flex-direction:column; align-items:center; }}
.photoshot img {{ height:1850px; width:auto; border-radius:70px; box-shadow:0 40px 90px rgba(0,0,0,.28); }}
.photoshot .tag {{ margin-top:80px; font-size:60px; font-weight:bold; color:#2e8b57;
  background:rgba(255,255,255,.82); padding:34px 66px; border-radius:90px; box-shadow:0 10px 26px rgba(0,0,0,.10); white-space:nowrap; }}
/* clear image (firetruck), rounded panel */
.clearimg {{ width:1360px; height:1900px; border-radius:80px; overflow:hidden; position:relative;
  box-shadow:0 26px 66px rgba(0,0,0,.2); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:44px; }}
.clearimg .photoback {{ position:absolute; inset:0; z-index:0; background-position:center; background-size:auto 152%; }}
.clearimg .photoback::after {{ content:''; position:absolute; inset:0; background:linear-gradient(rgba(0,0,0,.26),rgba(0,0,0,.46)); }}
.clearimg .big {{ position:relative; z-index:2; font-size:280px; line-height:1; text-shadow:0 6px 18px rgba(0,0,0,.45); }}
.clearimg .txt {{ position:relative; z-index:2; font-size:150px; font-weight:bold; color:#fff; text-shadow:0 6px 18px rgba(0,0,0,.5); }}
.clearimg .sub {{ position:relative; z-index:2; font-size:54px; color:#fff; opacity:.9; }}
.conf {{ position:absolute; width:34px; height:48px; border-radius:6px; z-index:2; }}
</style></head><body class="{bodyclass}">{body}</body></html>
"""

# ---- caption auto-sizing (fill one line) ----
_CONTENT_W = 1740
def _text_units(s):
    u = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x1F000 or 0x2600 <= o <= 0x27BF: u += 1.15
        elif ch == ' ': u += 0.4
        elif unicodedata.east_asian_width(ch) in ('F','W','A'): u += 1.0
        else: u += 0.55
    return u
def _cap_size(text, cap=196, floor=120):
    lines = re.split(r'<br\s*/?>', text)
    widest = max((_text_units(re.sub(r'<[^>]+>', '', ln)) for ln in lines), default=1) or 1
    return int(max(floor, min(cap, _CONTENT_W / widest)))
def enrich(body):
    def rep(m):
        text = m.group(1); plain = re.sub(r'<[^>]+>', '', text)
        return f'<div class="caption" style="font-size:{_cap_size(text)}px">{text}</div>'
    return re.sub(r'<div class="caption">(.*?)</div>', rep, body, flags=re.S)

def task(cls, icon, label): return f'<div class="card {cls}"><div class="icon">{icon}</div><div class="label">{label}</div></div>'

def dino_mosaic(flipped):
    cover = max(GW / DINO_W, GH / DINO_H)
    iw, ih = DINO_W * cover, DINO_H * cover
    offX, offY = (GW - iw) / 2, (GH - ih) / 2
    tasks = [("c1","😴","おきる"),("c2","👕","きがえ"),("c3","🧦","くつした"),
             ("c4","🍚","あさごはん"),("c5","🪥","はみがき"),("c6","🚽","といれ")]
    cells = []
    for i in range(COLS * ROWS):
        if i in flipped:
            c, r = i % COLS, i // COLS
            x = offX - c * (CARDW + GAP); y = offY - r * (CARDH + GAP)
            cells.append(f'<div class="card mosaic" style="background-image:url(\'{_DINO_URI}\');'
                         f'background-size:{iw:.0f}px {ih:.0f}px;background-position:{x:.0f}px {y:.0f}px;"></div>')
        else:
            cls, icon, label = tasks[i]; cells.append(task(cls, icon, label))
    return '<div class="grid">' + ''.join(cells) + '</div>'

import random
random.seed(7)
colors = ['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#ff922b','#cc5de8','#f06595','#3bc9db']
def confetti(n=90):
    return ''.join(f'<div class="conf" style="left:{random.randint(0,100)}%; top:{random.randint(2,95)}%; '
        f'background:{random.choice(colors)}; transform:rotate({random.randint(0,360)}deg);"></div>' for _ in range(n))

# ---------- 1. ASA (dino mosaic) ----------
asa = """
<div class="adfree">広告なし！</div>
<div class="caption">朝のしたくを楽しくすすめる</div>
<div class="appshot">
<div class="hero-main">できたら　おしてみよう！</div>
<div class="hero-sub">平日の朝をちょっとラクにする、したくサポート</div>
<div class="tabs"><div class="tab active">☀️ あさ</div><div class="tab">🌙 よる</div></div>
""" + dino_mosaic({0, 3}) + """
</div>
"""

# ---------- 2. PHOTO ----------
photo = """
<div class="caption">好きな画像を使える！</div>
<div class="photoshot">
  <img src=\"""" + _PHOTO_URI + """\">
  <div class="tag">🔒 画像はサーバに送られないから安心</div>
</div>
"""

# ---------- 3. CLEAR (firetruck) ----------
clearimg = """
<div class="caption">子どものやる気アップ</div>
<div class="clearimg">
  <div class="photoback" style="background-image:url('""" + _FIRETRUCK_URI + """');"></div>
""" + confetti(90) + """
  <div class="big">🌟</div>
  <div class="txt">がんばったね！</div>
  <div class="sub">タップしてもどる</div>
</div>
"""

# ---------- 4. YORU (all fronts) ----------
yoru = """
<div class="caption">おやすみの準備も</div>
<div class="app">
<div class="tabs"><div class="tab">☀️ あさ</div><div class="tab active">🌙 よる</div></div>
<div class="grid">""" + ''.join([
    task("c1","🛁","おふろ"), task("c2","👕","パジャマ"),
    task("c3","🪥","はみがき"), task("c4","🚽","といれ"),
    task("c5","📚","えほん"), task("c6","💤","ねる"),
]) + """</div>
</div>
"""

# ---------- 5. SETTINGS ----------
settings = """
<div class="caption">わが家のしたくに<br>カスタマイズ</div>
<div class="set-screen">
  <div class="set-head"><div class="back">‹ もどる</div><div class="ttl">🃏 カード（表）</div><div class="sp"></div></div>
  <div class="set-tabs"><div class="stab on">☀️ 朝</div><div class="stab">🌙 夜</div></div>
  <div class="set-hint">アイコンと名前を変えられます</div>
  <div class="row"><div class="num">1</div><div class="emo">😴</div><div class="lab">ぱじゃまをぬぐ</div></div>
  <div class="row"><div class="num">2</div><div class="emo">👕</div><div class="lab">きがえ</div></div>
  <div class="row"><div class="num">3</div><div class="emo">🧦</div><div class="lab">くつした</div></div>
  <div class="row"><div class="num">4</div><div class="emo">🍚</div><div class="lab">あさごはん</div></div>
</div>
"""

out = {
    'ipad-1-asa.html': BASE.format(bodyclass='framed', body=enrich(asa)),
    'ipad-2-photo.html': BASE.format(bodyclass='', body=enrich(photo)),
    'ipad-3-clearimage.html': BASE.format(bodyclass='', body=enrich(clearimg)),
    'ipad-4-yoru.html': BASE.format(bodyclass='night', body=enrich(yoru)),
    'ipad-5-settings.html': BASE.format(bodyclass='', body=enrich(settings)),
}
for name, html in out.items():
    open('/tmp/' + name, 'w').write(html); print('wrote', name)
