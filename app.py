import streamlit as st
import datetime as dt
import random
import base64
import io
import math
import wave

st.set_page_config(page_title="💖 For My Valentine", page_icon="💖", layout="wide")

# -----------------------------
# SOUND: generate tiny WAVs (no external files)
# -----------------------------
def _tone_wav_bytes(freq=880, dur=0.10, vol=0.25, sr=44100):
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        for i in range(n):
            t = i / sr
            # soft envelope to avoid clicks
            env = min(1.0, i / (sr * 0.01)) * min(1.0, (n - i) / (sr * 0.02))
            s = math.sin(2 * math.pi * freq * t) * vol * env
            wf.writeframesraw(int(s * 32767).to_bytes(2, "little", signed=True))
    return buf.getvalue()

def _chime_wav_bytes(sr=44100):
    # two-note chime
    a = _tone_wav_bytes(784, 0.11, 0.22, sr)  # G5
    b = _tone_wav_bytes(988, 0.14, 0.22, sr)  # B5
    # concatenate raw wav properly: easiest is re-render as one wav
    # by mixing the two tones with slight overlap:
    dur = 0.28
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        for i in range(n):
            t = i / sr
            s = 0.0
            # first tone 0.00-0.11
            if t <= 0.11:
                env = min(1.0, i / (sr * 0.01)) * min(1.0, (int(sr*0.11) - i) / (sr * 0.02))
                s += math.sin(2 * math.pi * 784 * t) * 0.18 * env
            # second tone starts at 0.07
            t2 = t - 0.07
            if 0.0 <= t2 <= 0.14:
                i2 = int(t2 * sr)
                n2 = int(sr * 0.14)
                env2 = min(1.0, i2 / (sr * 0.01)) * min(1.0, (n2 - i2) / (sr * 0.03))
                s += math.sin(2 * math.pi * 988 * t2) * 0.20 * env2
            # gentle limiter
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

# -----------------------------
# PIXEL HEART SPRITE (generated in-code)
# tries Pillow; if not available, falls back to pure SVG sprite-strip
# -----------------------------
def heart_sprite_data_uri(frames=6, scale=6):
    try:
        from PIL import Image, ImageDraw  # type: ignore
        w, h = 16, 16
        strip = Image.new("RGBA", (w * frames, h), (0, 0, 0, 0))

        # base pixel-heart mask (16x16) as coordinates
        heart_pixels = [
            (5,3),(6,3),(9,3),(10,3),
            (4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),
            (4,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),
            (5,6),(6,6),(7,6),(8,6),(9,6),(10,6),
            (6,7),(7,7),(8,7),(9,7),
            (7,8),(8,8),
            (7,9),(8,9),
        ]

        for f in range(frames):
            img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)

            # animate: pulse + sparkle highlight
            base = (255, 45, 168, 255)      # hot pink
            shadow = (122, 0, 86, 255)      # deep berry
            highlight = (255, 216, 77, 255) # yellow

            # subtle pulse: shift up/down by 0/1 px
            dy = 0 if f % 2 == 0 else 1

            # draw shadow offset
            for (x, y) in heart_pixels:
                d.point((x+1, y+1+dy), fill=shadow)

            # draw body
            for (x, y) in heart_pixels:
                d.point((x, y+dy), fill=base)

            # sparkle highlight: move across
            hx = 4 + f
            for (x, y) in [(hx,5+dy),(hx,4+dy),(hx+1,4+dy)]:
                if 0 <= x < w and 0 <= y < h:
                    d.point((x, y), fill=highlight)

            strip.paste(img, (f*w, 0))

        # upscale (nearest neighbor) for crispy pixels
        strip = strip.resize((strip.size[0]*scale, strip.size[1]*scale), resample=Image.NEAREST)

        buf = io.BytesIO()
        strip.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}", strip.size[0], strip.size[1], frames

    except Exception:
        # SVG fallback: simple strip with frames
        # (still a sprite strip; background-position stepping works)
        w, h = 16, 16
        frames = 6
        rects = [(5,3),(6,3),(9,3),(10,3),
                 (4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),
                 (4,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),
                 (5,6),(6,6),(7,6),(8,6),(9,6),(10,6),
                 (6,7),(7,7),(8,7),(9,7),
                 (7,8),(8,8),
                 (7,9),(8,9)]
        def frame_svg(f):
            dy = 0 if f % 2 == 0 else 1
            hx = 4 + f
            body = []
            for x,y in rects:
                body.append(f"<rect x='{x}' y='{y+dy}' width='1' height='1' fill='#ff2da8'/>")
                body.append(f"<rect x='{x+1}' y='{y+1+dy}' width='1' height='1' fill='#7a0056' opacity='0.9'/>")
            # highlight
            for x,y in [(hx,5+dy),(hx,4+dy),(hx+1,4+dy)]:
                body.append(f"<rect x='{x}' y='{y}' width='1' height='1' fill='#ffd84d'/>")
            return "<g>" + "".join(body) + "</g>"
        frames_svg = "".join([f"<g transform='translate({i*w},0)'>" + frame_svg(i) + "</g>" for i in range(frames)])
        svg = f"""
        <svg xmlns='http://www.w3.org/2000/svg' width='{w*frames}' height='{h}' viewBox='0 0 {w*frames} {h}'>
          {frames_svg}
        </svg>
        """.strip()
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64}", w*frames, h, frames

SPRITE_URI, SPRITE_W, SPRITE_H, SPRITE_FRAMES = heart_sprite_data_uri()

# -----------------------------
# CSS (more pixel + sprite + audio-ready)
# -----------------------------
st.markdown(f"""
<style>
.stApp{{
  /* Candy pixels */
  background:
    linear-gradient(90deg, rgba(255,216,77,0.28) 0 12px, rgba(255,45,168,0.18) 12px 24px),
    linear-gradient(0deg, rgba(255,255,255,0.10) 0 12px, rgba(255,255,255,0.0) 12px 24px),
    radial-gradient(circle at 20% 20%, #fff7a8 0%, #ffd1e8 35%, #ff9fd6 70%, #ffe66d 110%);
  background-size: 24px 24px, 24px 24px, auto;
}}
header, footer{{visibility:hidden;}}
.block-container{{padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1120px;}}

.pixel{{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  letter-spacing: 0.4px;
}}

.title{{
  text-align:center;
  font-weight: 950;
  font-size: 3.1rem;
  line-height: 1.05;
  color: #7a0056;
  text-shadow:
    4px 4px 0 #ffd84d,
    8px 8px 0 rgba(0,0,0,0.10);
}}

.caption{{
  text-align:center;
  font-weight: 900;
  color:#7a0056;
  opacity: .92;
}}

.stage{{
  display:flex;
  align-items:center;
  justify-content:center;
  min-height: 78vh;
}}

.card{{
  width: min(860px, 94vw);
  background: #ffe6f3;
  border: 8px solid #ff58b6;
  border-radius: 0px;
  box-shadow: 12px 12px 0 #ffd84d;
  padding: 26px 24px;
  position: relative;
}}

.card:before{{
  content:"";
  position:absolute;
  inset:10px;
  border: 4px dotted #ffd84d;
  pointer-events:none;
}}

.envelope{{
  width: 280px;
  height: 180px;
  margin: 10px auto 20px auto;
  background: #fff2fb;
  border: 8px solid #ff58b6;
  box-shadow: 10px 10px 0 #ffd84d;
  position: relative;
}}
.envelope:before{{
  content:"";
  position:absolute;
  left:0; right:0; top:0; bottom:0;
  background:
    linear-gradient(135deg, transparent 50%, #ffd84d 50%) left,
    linear-gradient(225deg, transparent 50%, #ffd84d 50%) right;
  background-size: 50% 100%;
  background-repeat: no-repeat;
  opacity: 0.28;
}}
.seal{{
  position:absolute;
  width: 52px; height: 52px;
  background:#ff58b6;
  border: 6px solid #7a0056;
  left: 50%; top: 54%;
  transform: translate(-50%,-50%);
  box-shadow: 6px 6px 0 #ffd84d;
}}

.letter{{
  background: #fff7a8;
  border: 8px solid #7a0056;
  box-shadow: 12px 12px 0 #ff58b6;
  padding: 18px 18px;
}}

div.stButton > button{{
  background:#ff58b6;
  color:#fff;
  border: 6px solid #7a0056;
  border-radius: 0px;
  padding: 12px 16px;
  font-weight: 950;
  box-shadow: 8px 8px 0 #ffd84d;
}}
div.stButton > button:hover{{
  background:#ff2da8;
}}

/* Sprite heart animation */
.sprite-heart {{
  width: {SPRITE_W // SPRITE_FRAMES}px;
  height: {SPRITE_H}px;
  background-image: url("{SPRITE_URI}");
  background-repeat: no-repeat;
  background-size: {SPRITE_W}px {SPRITE_H}px;
  image-rendering: pixelated;
  margin: 0 auto 10px auto;
  animation: heartSteps 0.65s steps({SPRITE_FRAMES}) infinite;
}}
@keyframes heartSteps {{
  from {{ background-position: 0px 0px; }}
  to   {{ background-position: -{SPRITE_W}px 0px; }}
}}

/* Floating pixel hearts */
@keyframes floatUp {{
  0% {{ transform: translateY(0) scale(1); opacity: 0; }}
  10% {{ opacity: 0.95; }}
  100% {{ transform: translateY(-105vh) scale(1.6); opacity: 0; }}
}}
.heart {{
  position: fixed;
  bottom: -24px;
  font-size: 18px;
  animation: floatUp linear infinite;
  z-index: 0;
  pointer-events:none;
  filter: drop-shadow(0 0 10px rgba(255, 45, 168, .35));
}}
</style>
""", unsafe_allow_html=True)

# Floating hearts layer
emojis = ["💖","💗","💕","💛","✨","🌸"]
html = ""
for _ in range(30):
    left = random.randint(0, 100)
    dur = random.uniform(6.0, 12.0)
    delay = random.uniform(0, 4.0)
    emoji = random.choice(emojis)
    html += f"<div class='heart' style='left:{left}vw; animation-duration:{dur}s; animation-delay:{delay}s'>{emoji}</div>"
st.markdown(html, unsafe_allow_html=True)

# -----------------------------
# STATE
# -----------------------------
if "opened" not in st.session_state:
    st.session_state.opened = False
if "hearts" not in st.session_state:
    st.session_state.hearts = 0
if "play" not in st.session_state:
    st.session_state.play = None  # "click" | "open" | "chime"

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='pixel title'>VALENTINE LETTER 💛💗</div>", unsafe_allow_html=True)
st.markdown("<div class='pixel caption'>pink + yellow • pixel vibes • one letter in the middle</div>", unsafe_allow_html=True)

# Countdown
target = dt.datetime(2026, 2, 14, 0, 0, 0)
now = dt.datetime.now()
delta = target - now
cd = f"{delta.days}d {delta.seconds//3600:02d}h {(delta.seconds%3600)//60:02d}m" if delta.total_seconds() > 0 else "TODAY 💖"
st.write("")
st.markdown(f"<div class='pixel caption'>timer: <b>{cd}</b></div>", unsafe_allow_html=True)
st.write("")

# Autoplay sounds when triggered
if st.session_state.play == "click":
    autoplay_wav(CLICK_WAV)
    st.session_state.play = None
elif st.session_state.play == "open":
    autoplay_wav(OPEN_WAV)
    st.session_state.play = None
elif st.session_state.play == "chime":
    autoplay_wav(CHIME_WAV)
    st.session_state.play = None

# -----------------------------
# CENTER STAGE
# -----------------------------
st.markdown("<div class='stage'><div class='card pixel'>", unsafe_allow_html=True)

# sprite heart
st.markdown("<div class='sprite-heart'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="envelope">
  <div class="seal"></div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if not st.session_state.opened:
        if st.button("OPEN 💌"):
            st.session_state.opened = True
            st.session_state.play = "open"
            st.balloons()

if st.session_state.opened:
    st.markdown("""
    <div class="letter pixel">
      <h2 style="margin:0; color:#7a0056;">Dear you,</h2>
      <p style="font-size:1.12rem; line-height:1.58; margin-top:10px; color:#4b0035; font-weight:900;">
        Even when the map says “far,” you still feel like my closest place.
        <br><br>
        I love how you show up for me — the kind that calms me down and lights me up at the same time.
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
    st.markdown("### 💖 little unlock (3 hearts)")
    st.caption("tap 3 times. each tap makes a sound.")

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
          <p style="font-size:1.18rem; margin:0; color:#7a0056; font-weight:980;">
            Final line: The distance is hard — but not having you would be harder.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

st.markdown("</div></div>", unsafe_allow_html=True)
