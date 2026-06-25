#!/usr/bin/env python3
# Generates 6 App Store screenshot HTML files (1320x2868) for できた！.
import os
import math

BASE = """
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1320px; height:2868px; overflow:hidden; }}
body {{
  font-family:'Hiragino Maru Gothic ProN','BIZ UDPGothic',sans-serif;
  background: linear-gradient(160deg,#ffe0ec 0%,#fff5cc 50%,#d4f0ff 100%);
  padding:0 70px; display:flex; flex-direction:column; align-items:center;
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
.caption {{ font-size:70px; font-weight:bold; color:#ff5a87; text-align:center; margin:46px 0 12px; white-space:nowrap; }}
.subcap {{ font-size:38px; color:#b9728a; text-align:center; margin-bottom:38px; }}
body.night .caption {{ color:#c7a8ff; }} body.night .subcap {{ color:#9a8fce; }}
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
/* settings */
.set-screen {{ width:100%; background:#f5f5f7; border-radius:50px; box-shadow:0 14px 40px rgba(0,0,0,.12); overflow:hidden; }}
.set-head {{ display:flex; align-items:center; justify-content:space-between; padding:44px 50px; background:#fff; border-bottom:2px solid #e7e7ec; }}
.set-head .back {{ font-size:42px; font-weight:bold; color:#ff5a87; }}
.set-head .ttl {{ font-size:46px; font-weight:bold; color:#333; }}
.set-head .rst {{ font-size:38px; font-weight:bold; color:#bbb; }}
.set-tabs {{ display:flex; gap:16px; justify-content:center; padding:40px 0 14px; }}
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
/* full-screen clear photo (v1.1) — a CSS sunset landscape standing in for the user's photo */
.celeb.photobg {{ overflow:hidden; }}
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

STATUS = """<div class="status"><div class="time">{time}</div><div class="right">
<svg class="wifi" width="56" height="40" viewBox="0 0 56 40"><path d="M28 8C17 8 7.6 12.6 1 19.7l5.2 5.4C11.8 19.3 19.4 15.6 28 15.6s16.2 3.7 21.8 9.5l5.2-5.4C48.4 12.6 39 8 28 8zm0 14c-5.5 0-10.4 2.4-13.8 6.1l5.4 5.6C21.4 31.5 24.5 30 28 30s6.6 1.5 8.4 3.7l5.4-5.6C38.4 24.4 33.5 22 28 22zm0 13.6l6.2-6.4c-1.6-1.7-3.8-2.6-6.2-2.6s-4.6.9-6.2 2.6L28 35.6z"/></svg>
<div class="batt"><div class="fill"></div></div></div></div>"""

def grid(cards):
    return '<div class="grid">' + ''.join(cards) + '</div>'

def done(face, star):
    return f'<div class="card done"><div class="face">{face}</div><div class="star">{star}</div></div>'

def task(cls, icon, label):
    return f'<div class="card {cls}"><div class="icon">{icon}</div><div class="label">{label}</div></div>'

def photo_card(scene, subj, star):
    return (f'<div class="card done"><div class="photo {scene}">'
            f'<div class="subj">{subj}</div><div class="star">{star}</div></div></div>')

def kid_drawing(body, ear, cheek, accent, paper, seed, extra=""):
    """An ORIGINAL kawaii mascot in a child's crayon style (no real-world IP).
    Stands in for a user-uploaded photo/drawing in the v1.1 card-back shot."""
    fid = f"cr{seed}"
    rays = "".join(
        f'<line x1="58" y1="52" x2="{58+38*math.cos(a):.1f}" y2="{52+38*math.sin(a):.1f}"/>'
        for a in [i*0.7854 for i in range(8)])
    grass = 'M-10 300 Q 25 278 60 300 T 130 300 T 200 300 T 270 300 T 340 300 T 410 300'
    return f'''<svg viewBox="0 0 400 320" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
<defs><filter id="{fid}" x="-15%" y="-15%" width="130%" height="130%">
<feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="{seed}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter></defs>
<rect x="0" y="0" width="400" height="320" fill="{paper}"/>
<g filter="url(#{fid})">
  <g fill="none" stroke="#f0b93b" stroke-width="4" stroke-linecap="round">{rays}</g>
  <circle cx="58" cy="52" r="22" fill="#ffe08a" stroke="#e8a92e" stroke-width="4"/>
  <path d="{grass}" fill="none" stroke="#7cc04a" stroke-width="7" stroke-linecap="round"/>
  <g stroke="{accent}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M152 118 L132 74 L182 108 Z" fill="{ear}"/>
    <path d="M248 118 L268 74 L218 108 Z" fill="{ear}"/>
    <ellipse cx="200" cy="188" rx="80" ry="84" fill="{body}"/>
    <circle cx="171" cy="172" r="16" fill="#fff"/>
    <circle cx="229" cy="172" r="16" fill="#fff"/>
    <circle cx="173" cy="175" r="7.5" fill="{accent}" stroke="none"/>
    <circle cx="231" cy="175" r="7.5" fill="{accent}" stroke="none"/>
    <path d="M179 206 Q200 232 221 206" fill="none"/>
    <path d="M120 198 Q100 206 96 226" fill="none"/>
    <path d="M280 198 Q300 206 304 226" fill="none"/>
    {extra}
  </g>
  <circle cx="156" cy="202" r="11" fill="{cheek}"/>
  <circle cx="244" cy="202" r="11" fill="{cheek}"/>
</g></svg>'''

def kid_card(svg, star="⭐"):
    return (f'<div class="card done"><div class="photo">{svg}'
            f'<div class="star">{star}</div></div></div>')

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
<div class="caption">よるのしたくも、たのしく 🌙</div>
<div class="subcap">ねるまえのルーティンを、わくわくに。</div>
<div class="hero-main">できたら　おしてみよう！</div>
<div class="hero-sub">よるのしたくを、やさしくサポート</div>
<div class="tabs"><div class="tab">☀️ あさ</div><div class="tab active">🌙 よる</div></div>
""" + grid([
    done("😴","🌙"), done("😴","🌙"),
    task("c3","🪥","はみがき"), task("c4","🚽","といれ"),
    task("c5","📚","えほん"), task("c6","💤","ねる"),
])

# ---------- SETTINGS ----------
settings = STATUS.format(time="7:05") + """
<div class="caption">アイコンも なまえも 自由に</div>
<div class="subcap">わが家のしたくに、ぴったり合わせて。</div>
<div class="set-screen">
  <div class="set-head"><div class="back">‹ もどる</div><div class="ttl">⚙️ せってい</div><div class="rst">リセット</div></div>
  <div class="set-tabs"><div class="stab on">☀️ あさ</div><div class="stab">🌙 よる</div></div>
  <div class="set-hint">アイコンとなまえをかえられます</div>
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

# ---------- CARD BACK IMAGE (v1.1) — lead screenshot ----------
# Done cards show ORIGINAL child's-crayon mascots (stand-ins for a user's photo/drawing).
kid_a = kid_drawing(body="#8fd9c4", ear="#8fd9c4", cheek="#ff9bb0", accent="#3a4a55", paper="#fdf3df", seed=4)
kid_b = kid_drawing(body="#ffb27a", ear="#ffb27a", cheek="#ff7e8f", accent="#5a3a2a", paper="#eaf6ff", seed=9,
                    extra='<path d="M200 200 q-12 -16 -24 -2 q-2 14 24 28 q26 -14 24 -28 q-12 -14 -24 2 Z" fill="#fff3c4"/>')
cardback = STATUS.format(time="7:08") + """
<div class="caption">できたカードに、おうちの写真</div>
<div class="subcap">お気に入りの1枚で、もっとうれしい「できた！」</div>
<div class="hero-main">できた　を　もっと自分ごとに</div>
<div class="hero-sub">設定した写真は、端末のなかだけに保存されます</div>
<div class="tabs"><div class="tab active">☀️ あさ</div><div class="tab">🌙 よる</div></div>
""" + grid([
    kid_card(kid_a), kid_card(kid_b),
    task("c3","🧦","くつした"), task("c4","🍚","あさごはん"),
    task("c5","🪥","はみがき"), task("c6","🚽","といれ"),
])

# ---------- CLEAR IMAGE (v1.1) ----------
random.seed(11)
conf2 = ''.join(
    f'<div class="conf" style="left:{random.randint(0,100)}%; top:{random.randint(2,95)}%; '
    f'background:{random.choice(colors)}; transform:rotate({random.randint(0,360)}deg);"></div>'
    for _ in range(70))
clearimg = STATUS.format(time="7:12") + """
<div class="caption">クリア画面も、自分だけの1枚に</div>
<div class="subcap">ぜんぶできたごほうびに、お気に入りの写真を。</div>
<div class="celeb photobg">
  <div class="photoback"><div class="sun"></div><div class="hill back"></div><div class="hill front"></div></div>
""" + conf2 + """
  <div class="big">🌟</div>
  <div class="txt">がんばったね！</div>
  <div class="sub">タップしてもどる</div>
</div>
"""

# ss-1 is the card-back image shot (v1.1 headline); the plain あさ board
# (`asa`, still defined above) was retired in favour of it.
out = {
    'ss-1-cardback.html': BASE.format(bodyclass='', body=cardback),
    'ss-2-yoru.html': BASE.format(bodyclass='night', body=yoru),
    'ss-3-settings.html': BASE.format(bodyclass='', body=settings),
    'ss-4-celebration.html': BASE.format(bodyclass='', body=celebration),
    'ss-5-clearimage.html': BASE.format(bodyclass='', body=clearimg),
}
for name, html in out.items():
    with open('/tmp/' + name, 'w') as f:
        f.write(html)
    print('wrote', name)
