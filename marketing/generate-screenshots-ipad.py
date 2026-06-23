#!/usr/bin/env python3
# Generates 4 App Store screenshots for 13-inch iPad (2064x2752).
import random

BASE = """
<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:2064px; height:2752px; overflow:hidden; }}
body {{
  font-family:'Hiragino Maru Gothic ProN','BIZ UDPGothic',sans-serif;
  background: linear-gradient(160deg,#ffe0ec 0%,#fff5cc 50%,#d4f0ff 100%);
  padding:0 110px; display:flex; flex-direction:column; align-items:center;
}}
body.night {{ background: linear-gradient(160deg,#1a1a4e 0%,#2d1b69 50%,#0d2b4e 100%); }}
.status {{ width:100%; height:130px; display:flex; align-items:center; justify-content:space-between; padding:10px 30px 0; }}
.status .time {{ font-size:46px; font-weight:600; color:#111; }}
.status .right {{ display:flex; align-items:center; gap:20px; }}
body.night .status .time {{ color:#fff; }}
.batt {{ width:62px; height:30px; border:4px solid #111; border-radius:8px; position:relative; }}
.batt::after {{ content:''; position:absolute; right:-10px; top:9px; width:6px; height:10px; background:#111; border-radius:0 3px 3px 0; }}
.batt .fill {{ position:absolute; inset:3px; background:#111; border-radius:3px; }}
body.night .batt {{ border-color:#fff; }} body.night .batt::after {{ background:#fff; }} body.night .batt .fill {{ background:#fff; }}
.wifi path {{ fill:#111; }} body.night .wifi path {{ fill:#fff; }}
.caption {{ font-size:96px; font-weight:bold; color:#ff5a87; text-align:center; margin:64px 0 16px; white-space:nowrap; }}
.subcap {{ font-size:48px; color:#b9728a; text-align:center; margin-bottom:48px; }}
body.night .caption {{ color:#c7a8ff; }} body.night .subcap {{ color:#9a8fce; }}
.hero-main {{ font-size:104px; font-weight:bold; color:#ff5a87; text-shadow:5px 7px 0 #fff; white-space:nowrap; }}
body.night .hero-main {{ color:#c7a8ff; text-shadow:4px 5px 0 rgba(0,0,0,.4); }}
.hero-sub {{ font-size:40px; color:#999; margin-top:14px; }}
body.night .hero-sub {{ color:#7a7aaa; }}
.tabs {{ display:flex; gap:20px; background:rgba(255,255,255,.55); padding:16px; border-radius:100px; margin:56px 0; }}
body.night .tabs {{ background:rgba(255,255,255,.12); }}
.tab {{ font-size:50px; font-weight:bold; padding:26px 76px; border-radius:80px; color:#aaa; }}
.tab.active {{ background:#fff; color:#ff5a87; box-shadow:0 6px 16px rgba(255,90,135,.25); }}
body.night .tab.active {{ background:#ff7eb6; color:#fff; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:50px; width:100%; }}
.card {{ height:560px; border-radius:54px; background:#fff; box-shadow:0 16px 40px rgba(0,0,0,.10);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:28px; }}
body.night .card {{ background:#26264f; }}
.card .icon {{ font-size:200px; line-height:1; }}
.card .label {{ font-size:62px; font-weight:bold; color:#444; }}
body.night .card .label {{ color:#c8c8ea; }}
.c1{{border-top:18px solid #ff8aaa;}} .c2{{border-top:18px solid #ffb74d;}} .c3{{border-top:18px solid #4fc3f7;}}
.c4{{border-top:18px solid #81c784;}} .c5{{border-top:18px solid #9575cd;}} .c6{{border-top:18px solid #f06292;}}
.done {{ background:linear-gradient(145deg,#fffde7,#fff59d); border-bottom:16px solid #ffd54f; }}
body.night .done {{ background:linear-gradient(145deg,#2d1b69,#1a1a6e); border-bottom:16px solid #7c4dff; }}
.done .face {{ font-size:250px; line-height:1; }} .done .star {{ font-size:64px; }}
.set-screen {{ width:100%; max-width:1500px; background:#f5f5f7; border-radius:60px; box-shadow:0 16px 48px rgba(0,0,0,.12); overflow:hidden; }}
.set-head {{ display:flex; align-items:center; justify-content:space-between; padding:50px 60px; background:#fff; border-bottom:2px solid #e7e7ec; }}
.set-head .back {{ font-size:48px; font-weight:bold; color:#ff5a87; }}
.set-head .ttl {{ font-size:52px; font-weight:bold; color:#333; }}
.set-head .rst {{ font-size:44px; font-weight:bold; color:#bbb; }}
.set-tabs {{ display:flex; gap:20px; justify-content:center; padding:46px 0 16px; }}
.stab {{ font-size:46px; font-weight:bold; padding:22px 72px; border-radius:70px; border:4px solid #e2e2e2; background:#fff; color:#aaa; }}
.stab.on {{ background:#ff5a87; border-color:#ff5a87; color:#fff; }}
.set-hint {{ text-align:center; color:#bbb; font-size:40px; padding:8px 0 36px; }}
.row {{ display:flex; align-items:center; gap:34px; background:#fff; border-radius:36px; padding:32px 44px; margin:0 50px 32px; box-shadow:0 2px 8px rgba(0,0,0,.06); }}
.row .num {{ font-size:46px; color:#ccc; font-weight:bold; width:40px; }}
.row .emo {{ width:148px; height:148px; border:4px solid #e8e8e8; border-radius:32px; background:#fafafa; display:flex; align-items:center; justify-content:center; font-size:92px; }}
.row .lab {{ flex:1; height:130px; border:4px solid #e8e8e8; border-radius:32px; background:#fafafa; display:flex; align-items:center; padding:0 44px; font-size:62px; font-weight:bold; color:#333; }}
.celeb {{ width:100%; flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:40px; position:relative; }}
.celeb .big {{ font-size:300px; line-height:1; }}
.celeb .txt {{ font-size:130px; font-weight:bold; color:#ff5a87; text-shadow:5px 7px 0 #fff; }}
.celeb .sub {{ font-size:50px; color:#b9728a; }}
.conf {{ position:absolute; width:32px; height:46px; border-radius:6px; }}
</style></head><body class="{bodyclass}">{body}</body></html>
"""

STATUS = """<div class="status"><div class="time">{time}</div><div class="right">
<svg class="wifi" width="60" height="42" viewBox="0 0 56 40"><path d="M28 8C17 8 7.6 12.6 1 19.7l5.2 5.4C11.8 19.3 19.4 15.6 28 15.6s16.2 3.7 21.8 9.5l5.2-5.4C48.4 12.6 39 8 28 8zm0 14c-5.5 0-10.4 2.4-13.8 6.1l5.4 5.6C21.4 31.5 24.5 30 28 30s6.6 1.5 8.4 3.7l5.4-5.6C38.4 24.4 33.5 22 28 22zm0 13.6l6.2-6.4c-1.6-1.7-3.8-2.6-6.2-2.6s-4.6.9-6.2 2.6L28 35.6z"/></svg>
<div class="batt"><div class="fill"></div></div></div></div>"""

def grid(cards): return '<div class="grid">' + ''.join(cards) + '</div>'
def done(face, star): return f'<div class="card done"><div class="face">{face}</div><div class="star">{star}</div></div>'
def task(cls, icon, label): return f'<div class="card {cls}"><div class="icon">{icon}</div><div class="label">{label}</div></div>'

asa = STATUS.format(time="7:00") + """
<div class="caption">あさのしたく、じぶんで！</div>
<div class="subcap">タップするだけ。平日の朝がちょっとラクに。</div>
<div class="hero-main">できたら　おしてみよう！</div>
<div class="hero-sub">平日の朝をちょっとラクにする、したくサポート</div>
<div class="tabs"><div class="tab active">☀️ あさ</div><div class="tab">🌙 よる</div></div>
""" + grid([
    done("😊","⭐"), done("😊","⭐"), task("c3","🧦","くつした"),
    task("c4","🍚","あさごはん"), task("c5","🪥","はみがき"), task("c6","🚽","といれ"),
])

yoru = STATUS.format(time="20:30") + """
<div class="caption">よるのしたくも、たのしく 🌙</div>
<div class="subcap">ねるまえのルーティンを、わくわくに。</div>
<div class="hero-main">できたら　おしてみよう！</div>
<div class="hero-sub">よるのしたくを、やさしくサポート</div>
<div class="tabs"><div class="tab">☀️ あさ</div><div class="tab active">🌙 よる</div></div>
""" + grid([
    done("😴","🌙"), done("😴","🌙"), task("c3","🪥","はみがき"),
    task("c4","🚽","といれ"), task("c5","📚","えほん"), task("c6","💤","ねる"),
])

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
</div>
"""

random.seed(7)
colors = ['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#ff922b','#cc5de8','#f06595','#3bc9db']
conf = ''.join(
    f'<div class="conf" style="left:{random.randint(0,100)}%; top:{random.randint(2,95)}%; '
    f'background:{random.choice(colors)}; transform:rotate({random.randint(0,360)}deg);"></div>'
    for _ in range(90))
celebration = STATUS.format(time="7:12") + """
<div class="caption">ぜんぶできたら 大かんせい！</div>
<div class="subcap">がんばりを、おもいっきりおいわい。</div>
<div class="celeb">""" + conf + """
  <div class="big">🌟</div><div class="txt">がんばったね！</div>
  <div class="big">🎉</div><div class="sub">タップしてもどる</div>
</div>
"""

out = {
    'ipad-1-asa.html': BASE.format(bodyclass='', body=asa),
    'ipad-2-yoru.html': BASE.format(bodyclass='night', body=yoru),
    'ipad-3-settings.html': BASE.format(bodyclass='', body=settings),
    'ipad-4-celebration.html': BASE.format(bodyclass='', body=celebration),
}
for name, html in out.items():
    open('/tmp/' + name, 'w').write(html); print('wrote', name)
