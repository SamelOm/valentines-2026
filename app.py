import streamlit as st
import datetime as dt
import random
import time

st.set_page_config(page_title="💖 For My Valentine", page_icon="💖", layout="wide")

# ---------- THEME / CSS ----------
st.markdown("""
<style>
/* Full page candy gradient */
.stApp{
  background: radial-gradient(circle at 20% 20%, #fff7a8 0%, #ffd1e8 35%, #ff9fd6 70%, #ffe66d 110%);
}

/* Remove Streamlit chrome spacing */
.block-container{padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px;}
header{visibility:hidden;}
footer{visibility:hidden;}

/* Pixel font fallback chain (no external font) */
.pixel {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  letter-spacing: 0.3px;
}

/* Big title */
.title {
  text-align:center;
  font-weight: 900;
  font-size: 3rem;
  line-height: 1.05;
  color: #7a0056;
  text-shadow: 4px 4px 0 #ffd54a, 8px 8px 0 rgba(0,0,0,0.08);
}

/* Center stage */
.stage{
  display:flex;
  align-items:center;
  justify-content:center;
  min-height: 78vh;
  position: relative;
}

/* Pixel-ish card */
.card{
  width: min(820px, 92vw);
  background: #ffe6f3;
  border: 6px solid #ff58b6;
  border-radius: 0px;               /* blocky */
  box-shadow: 10px 10px 0 #ffd84d;  /* chunky shadow */
  padding: 26px 24px;
  position: relative;
}

/* Yellow accent border inside (Minecraft UI-ish) */
.card:before{
  content:"";
  position:absolute;
  inset:10px;
  border: 4px dashed #ffd84d;
  pointer-events:none;
}

/* Envelope */
.envelope{
  width: 260px;
  height: 170px;
  margin: 10px auto 22px auto;
  background: #fff2fb;
  border: 6px solid #ff58b6;
  box-shadow: 8px 8px 0 #ffd84d;
  position: relative;
  cursor: pointer;
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
  opacity: 0.35;
}
.seal{
  position:absolute;
  width: 44px; height: 44px;
  background:#ff58b6;
  border: 5px solid #7a0056;
  left: 50%; top: 52%;
  transform: translate(-50%,-50%);
  box-shadow: 4px 4px 0 #ffd84d;
}

/* Letter */
.letter{
  background: #fff7a8;
  border: 6px solid #7a0056;
  box-shadow: 10px 10px 0 #ff58b6;
  padding: 18px 18px;
  margin-top: 10px;
}

/* Buttons look blocky */
div.stButton > button{
  background:#ff58b6;
  color:#fff;
  border: 4px solid #7a0056;
  border-radius: 0px;
  padding: 12px 16px;
  font-weight: 900;
  box-shadow: 6px 6px 0 #ffd84d;
}
div.stButton > button:hover{
  background:#ff2da8;
}

/* Pixel hearts floating */
@keyframes floatUp {
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

/* Small captions */
.caption{
  text-align:center;
  font-weight: 800;
  color:#7a0056;
  opacity: .9;
}
</style>
""", unsafe_allow_html=True)

# Floating hearts layer
emojis = ["💖","💗","💕","💛","✨","🌸"]
html = ""
for _ in range(28):
    left = random.randint(0, 100)
    dur = random.uniform(6.0, 12.0)
    delay = random.uniform(0, 4.0)
    emoji = random.choice(emojis)
    html += f"<div class='heart' style='left:{left}vw; animation-duration:{dur}s; animation-delay:{delay}s'>{emoji}</div>"
st.markdown(html, unsafe_allow_html=True)

# ---------- STATE ----------
if "opened" not in st.session_state:
    st.session_state.opened = False
if "secret" not in st.session_state:
    st.session_state.secret = 0

# ---------- CONTENT ----------
st.markdown("<div class='pixel title'>VALENTINE QUEST: BUFFALO ↔ INDIA 💛💗</div>", unsafe_allow_html=True)
st.markdown("<div class='pixel caption'>Pink. Yellow. Pixel vibes. One letter in the middle.</div>", unsafe_allow_html=True)

# Countdown (simple, crisp)
target = dt.datetime(2026, 2, 14, 0, 0, 0)
now = dt.datetime.now()
delta = target - now
if delta.total_seconds() > 0:
    cd = f"{delta.days}d {delta.seconds//3600:02d}h {(delta.seconds%3600)//60:02d}m"
else:
    cd = "TODAY 💖"

st.write("")

st.markdown("<div class='stage'><div class='card pixel'>", unsafe_allow_html=True)

st.markdown(f"### 🧁 Timer till Valentine: **{cd}**")
st.write("")

# Fake clickable envelope vibe + actual button
st.markdown("""
<div class="envelope">
  <div class="seal"></div>
</div>
""", unsafe_allow_html=True)

colA, colB, colC = st.columns([1,1,1])
with colB:
    if not st.session_state.opened:
        if st.button("OPEN THE LETTER 💌"):
            st.session_state.opened = True
            st.balloons()

# Letter
if st.session_state.opened:
    st.markdown("""
    <div class="letter pixel">
      <h2 style="margin:0; color:#7a0056;">Dear you,</h2>
      <p style="font-size:1.1rem; line-height:1.55; margin-top:10px; color:#4b0035; font-weight:800;">
        I know I’m far — Buffalo on my map, India on yours —
        but somehow you still feel like my nearest place.
        <br><br>
        I’m proud of you. I miss you. I choose you.
        <br><br>
        If love was a game, you’re the safe house I always run back to.
      </p>
      <p style="margin-top:14px; color:#7a0056; font-weight:900;">
        Happy Valentine’s Day 💛💗
      </p>
      <p style="margin:0; color:#7a0056; font-weight:900;">
        — from me
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Mini “minecraft quest” interaction
    st.markdown("### 🎮 Mini Quest (Minecraft energy)")
    st.caption("Collect 3 hearts to unlock the final line.")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Mine a 💛"):
            st.session_state.secret += 1
            st.toast("💛 +1", icon="💛")
    with c2:
        if st.button("Mine a 💗"):
            st.session_state.secret += 1
            st.toast("💗 +1", icon="💗")
    with c3:
        if st.button("Mine a 💖"):
            st.session_state.secret += 1
            st.toast("💖 +1", icon="💖")

    progress = min(st.session_state.secret, 3)
    st.progress(progress / 3)

    if progress >= 3:
        st.success("Unlocked ✅")
        st.markdown("""
        <div class="letter pixel" style="background:#ffe6f3;">
          <p style="font-size:1.15rem; margin:0; color:#7a0056; font-weight:950;">
            Final line: I can handle the distance — I can’t handle not having you.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

st.markdown("</div></div>", unsafe_allow_html=True)
