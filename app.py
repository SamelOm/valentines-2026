import streamlit as st
import random
import base64
import io
import math
import wave
from pathlib import Path

st.set_page_config(page_title="💖 For My Valentine", page_icon="💖", layout="wide")

# =============================
# SOUND (no external files)
# =============================
def _tone_wav_bytes(freq=880, dur=0.10, vol=0.25, sr=44100):
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        for i in range(n):
            t = i / sr
            env = min(1.0, i / (sr * 0.01)) * min(1.0, (n - i) / (sr * 0.02))
            s = math.sin(2 * math.pi * freq * t) * vol * env
            wf.writeframesraw(int(s * 32767).to_bytes(2, "little", signed=True))
    return buf.getvalue()

def _chime_wav_bytes(sr=44100):
    dur = 0.28
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        for i in range(n):
            t = i / sr
            s = 0.0
            if t <= 0.11:
                env = min(1.0, i / (sr * 0.01)) * min(1.0, (int(sr*0.11) - i) / (sr * 0.02))
                s += math.sin(2 * math.pi * 784 * t) * 0.18 * env
            t2 = t - 0.07
            if 0.0 <= t2 <= 0.14:
                i2 = int(t2 * sr)
                n2 = int(sr * 0.14)
                env2 = min(1.0, i2 / (sr * 0.01)) * min(1.0, (n2 - i2) / (sr * 0.03))
                s += math.sin(2 * math.pi * 988 * t2) * 0.20 * env2
            s = max(-0.95, min(0.95, s))
            wf.writeframesraw(int(s * 32767).to_bytes(2, "little", signed=True))
    return buf.getvalue()

def autoplay_wav(wav_bytes: bytes):
    b64 = base64.b64encode(wav_bytes).decode("utf-8")
    st.markdown(
        f"""
        <audio autoplay="true">
          <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True,
    )

CLICK_WAV = _tone_wav_bytes(980, 0.08, 0.22)
OPEN_WAV  = _tone_wav_bytes(660, 0.10, 0.22)
CHIME_WAV = _chime_wav_bytes()

# =============================
# Pixel scene SVG (small boy+girl+cat)
# =============================
def pixel_scene_svg(scale=16):
    W, H = 64, 40

    def r(x, y, w=1, h=1, c="#000"):
        return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{c}'/>"

    pink = "#ff2da8"
    yellow = "#ffd84d"
    berry = "#7a0056"
    cream = "#fff7a8"
    skin1 = "#f6c7a8"
    skin2 = "#eab08f"
    hair1 = "#3b1d2b"
    hair2 = "#1f0f18"
    shirt1 = "#ff58b6"
    shirt2 = "#ffd84d"
    pants = "#7a0056"

    cat_white = "#ffffff"
    cat_spot  = "#b57a4a"

    px = []

    # sparkles
    for (x,y) in [(6,5),(10,8),(52,7),(56,10),(46,4),(18,6)]:
        px += [r(x,y,1,1,yellow), r(x+1,y,1,1,cream)]

    # heart (small)
    heart_pixels = [
        (30,6),(31,6),(34,6),(35,6),
        (29,7),(30,7),(31,7),(32,7),(33,7),(34,7),(35,7),(36,7),
        (29,8),(30,8),(31,8),(32,8),(33,8),(34,8),(35,8),(36,8),
        (30,9),(31,9),(32,9),(33,9),(34,9),(35,9),
        (31,10),(32,10),(33,10),(34,10),
        (32,11),(33,11),
        (32,12),(33,12)
    ]
    for x,y in heart_pixels:
        px.append(r(x+1,y+1,1,1,berry))
    for x,y in heart_pixels:
        px.append(r(x,y,1,1,pink))
    for x,y in [(31,7),(32,7),(31,8)]:
        px.append(r(x,y,1,1,yellow))

    # ground strip
    px.append(r(0, 34, 64, 4, "#ffe6f3"))
    px.append(r(0, 33, 64, 1, "#ff9fd6"))

    # Girl (left)
    px += [r(12,18,8,1,hair2), r(11,19,10,2,hair1), r(12,21,8,1,hair1)]
    px += [r(13,20,6,3,skin1), r(13,23,6,1,skin2)]
    px += [r(15,21,1,1,berry), r(17,21,1,1,berry)]
    px += [r(12,24,8,5,shirt1), r(13,25,6,1,yellow)]
    px += [r(13,29,3,4,pants), r(17,29,3,4,pants)]
    px += [r(13,33,3,1,berry), r(17,33,3,1,berry)]

    # Guy (right)
    px += [r(44,18,8,1,hair2), r(43,19,10,2,hair1), r(44,21,8,1,hair1)]
    px += [r(45,20,6,3,skin1), r(45,23,6,1,skin2)]
    px += [r(47,21,1,1,berry), r(49,21,1,1,berry)]
    px += [r(44,24,8,5,shirt2), r(45,25,6,1,pink)]
    px += [r(45,29,3,4,pants), r(49,29,3,4,pants)]
    px += [r(45,33,3,1,berry), r(49,33,3,1,berry)]

    # Cat (middle) white + brown spots
    px += [
        r(29,27,7,4,cat_white),
        r(31,24,3,2,cat_white),
        r(31,24,1,1,berry),
        r(33,24,1,1,berry),
        r(32,25,1,1,berry),
        r(28,28,2,1,cat_white),
        r(27,27,1,2,cat_white),
        r(30,30,5,1,berry)
    ]
    px += [
        r(30,28,1,1,cat_spot),
        r(33,28,1,1,cat_spot),
        r(31,29,1,1,cat_spot),
        r(34,29,1,1,cat_spot),
    ]

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
      <rect x="0" y="0" width="{W}" height="{H}" fill="transparent"/>
      {''.join(px)}
    </svg>
    """.strip()

    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"""
    <div style="display:flex; justify-content:center; margin: 4px 0 12px 0;">
      <img src="data:image/svg+xml;base64,{b64}"
           style="width:{W*scale}px; height:{H*scale}px; image-rendering: pixelated;" />
    </div>
    """

# =============================
# CSS (the "bar" is the .card)
# =============================
st.markdown("""
<style>
.stApp{
  background:
    linear-gradient(90deg, rgba(255,216,77,0.28) 0 12px, rgba(255,45,168,0.18) 12px 24px),
    radial-gradient(circle at 20% 20%, #fff7a8 0%, #ffd1e8 35%, #ff9fd6 80%);
  background-size: 24px 24px, auto;
}
header, footer{visibility:hidden;}
.block-container{padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px;}

.pixel{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  letter-spacing: 0.4px;
}
.title{
  text-align:center;
  font-weight: 950;
  font-size: 3.2rem;
  color: #7a0056;
  text-shadow: 4px 4px 0 #ffd84d;
  margin-bottom: .6rem;
}
.stage{
  display:flex;
  align-items:center;
  justify-content:center;
}
.card{
  width: min(1100px, 96vw);
  background: #ffe6f3;
  border: 10px solid #ff58b6;
  border-radius: 0px;
  box-shadow: 14px 14px 0 #ffd84d;
  padding: 18px;
}

/* Photo area inside the same card */
.photo-frame{
  margin-top: 10px;
  border: 8px solid #7a0056;
  box-shadow: 12px 12px 0 #ff58b6;
  background: #fff7a8;
  padding: 10px;
}
.photo-frame img{
  border-radius: 0px !important;
}

/* Envelope + letter */
.envelope{
  width: 320px;
  height: 200px;
  margin: 10px auto 18px auto;
  background: #fff2fb;
  border: 10px solid #ff58b6;
  box-shadow: 12px 12px 0 #ffd84d;
  position: relative;
}
.envelope:before{
  content:"";
  position:absolute;
  left:0; right:0; top:0; bottom:0;
  background:
    linear-gradient(135deg, transparent 50%, #ffd84d 50%) left,
    linear-gradient(225deg, transparent 50%, #ffd84d 50%) right;
  background-size: 50% 100%;
  background-repeat: no-repeat;
  opacity: 0.25;
}
.seal{
  position:absolute;
  width: 64px; height: 64px;
  background:#ff58b6;
  border: 8px solid #7a0056;
  left: 50%; top: 54%;
  transform: translate(-50%,-50%);
  box-shadow: 8px 8px 0 #ffd84d;
}
.letter{
  background: #fff7a8;
  border: 10px solid #7a0056;
  box-shadow: 14px 14px 0 #ff58b6;
  padding: 18px;
  margin-top: 10px;
}
div.stButton > button{
  background:#ff58b6;
  color:#fff;
  border: 8px solid #7a0056;
  border-radius: 0px;
  padding: 14px 18px;
  font-weight: 950;
  box-shadow: 10px 10px 0 #ffd84d;
}
div.stButton > button:hover{ background:#ff2da8; }
</style>
""", unsafe_allow_html=True)

# Floating hearts layer
emojis = ["💖","💗","💕","💛","✨","🌸"]
html = ""
for _ in range(26):
    left = random.randint(0, 100)
    dur = random.uniform(6.0, 12.0)
    delay = random.uniform(0, 4.0)
    emoji = random.choice(emojis)
    html += f"<div class='heart' style='left:{left}vw; animation-duration:{dur}s; animation-delay:{delay}s'>{emoji}</div>"

st.markdown("""
<style>
@keyframes floatUp{
  0% { transform: translateY(0) scale(1); opacity: 0; }
  10% { opacity: 0.95; }
  100% { transform: translateY(-105vh) scale(1.6); opacity: 0; }
}
.heart{
  position: fixed;
  bottom: -24px;
  font-size: 18px;
  animation: floatUp linear infinite;
  z-index: 0;
  pointer-events:none;
  filter: drop-shadow(0 0 10px rgba(255, 45, 168, .35));
}
</style>
""", unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)

# =============================
# STATE
# =============================
if "opened" not in st.session_state:
    st.session_state.opened = False
if "hearts" not in st.session_state:
    st.session_state.hearts = 0
if "play" not in st.session_state:
    st.session_state.play = None  # "click" | "open" | "chime"

# Trigger sounds
if st.session_state.play == "click":
    autoplay_wav(CLICK_WAV); st.session_state.play = None
elif st.session_state.play == "open":
    autoplay_wav(OPEN_WAV); st.session_state.play = None
elif st.session_state.play == "chime":
    autoplay_wav(CHIME_WAV); st.session_state.play = None

# =============================
# UI
# =============================
st.markdown("<div class='pixel title'>VALENTINE LETTER 💖</div>", unsafe_allow_html=True)

st.markdown("<div class='stage'><div class='card pixel'>", unsafe_allow_html=True)

# 1) Pixel scene inside the card (this is inside the "bar")
st.markdown(pixel_scene_svg(scale=16), unsafe_allow_html=True)

# 2) Big photo INSIDE the same card
# Put your uploaded image next to app.py and name it: us.jpg (recommended)
PHOTO_PATHS = ["us.jpg", "IMG_6276.jpg", "IMG_6276.jpeg", "IMG_6276.png"]

found = None
for p in PHOTO_PATHS:
    if Path(p).exists():
        found = p
        break

st.markdown("<div class='photo-frame'>", unsafe_allow_html=True)
st.markdown("### Our photo 📸", unsafe_allow_html=True)

if found:
    st.image(found, use_container_width=True)
else:
    st.info("Put your photo in the same folder as app.py and name it **us.jpg** (or IMG_6276.jpg).")
    # fallback uploader (optional)
    up = st.file_uploader("Or upload here:", type=["jpg","jpeg","png"])
    if up:
        st.image(up, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# 3) Envelope + letter
st.markdown("""
<div class="envelope">
  <div class="seal"></div>
</div>
""", unsafe_allow_html=True)

center = st.columns([1,1,1])[1]
with center:
    if not st.session_state.opened:
        if st.button("OPEN 💌"):
            st.session_state.opened = True
            st.session_state.play = "open"
            st.balloons()

if st.session_state.opened:
    st.markdown("""
    <div class="letter pixel">
      <h2 style="margin:0; color:#7a0056;">Dear you,</h2>
      <p style="font-size:1.18rem; line-height:1.6; margin-top:10px; color:#4b0035; font-weight:900;">
        Even when the map says “far,” you still feel like my closest place.
        <br><br>
        I’m proud of you. I miss you. I choose you.
      </p>
      <p style="margin-top:14px; color:#7a0056; font-weight:950;">
        Happy Valentine’s Day 💛💗
      </p>
      <p style="margin:0; color:#7a0056; font-weight:950;">— me</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    a, b, c = st.columns(3)
    with a:
        if st.button("💛"):
            st.session_state.hearts += 1
            st.session_state.play = "click"
    with b:
        if st.button("💗"):
            st.session_state.hearts += 1
            st.session_state.play = "click"
    with c:
        if st.button("💖"):
            st.session_state.hearts += 1
            st.session_state.play = "click"

    progress = min(st.session_state.hearts, 3)
    st.progress(progress / 3)

    if progress >= 3:
        st.session_state.play = "chime"
        st.success("unlocked ✅")
        st.markdown("""
        <div class="letter pixel" style="background:#ffe6f3;">
          <p style="font-size:1.2rem; margin:0; color:#7a0056; font-weight:980;">
            Final line: The distance is hard — but not having you would be harder.
          </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
