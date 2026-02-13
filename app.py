import streamlit as st
import datetime as dt
import pandas as pd
import time
import random

st.set_page_config(page_title="For My Valentine", page_icon="❤️", layout="centered")

# -----------------------------
# CSS: floating hearts + glow + pulse
# -----------------------------
st.markdown("""
<style>
@keyframes floatUp {
  0% { transform: translateY(0) translateX(0) scale(0.8); opacity: 0; }
  10% { opacity: .9; }
  100% { transform: translateY(-120vh) translateX(30px) scale(1.4); opacity: 0; }
}
.heart {
  position: fixed;
  bottom: -40px;
  font-size: 22px;
  animation: floatUp linear infinite;
  z-index: 0;
  filter: drop-shadow(0 0 10px rgba(255, 0, 100, .35));
  pointer-events: none;
}
.glow-title {
  font-size: 3rem;
  font-weight: 800;
  text-align: center;
  margin-top: .2rem;
  text-shadow: 0 0 14px rgba(255, 0, 90, .35);
}
.soft {
  text-align:center;
  font-size:1.05rem;
  opacity:.92;
}
.card {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
  padding: 18px 18px;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,.08);
}
.pulse-btn button {
  border-radius: 999px !important;
  padding: .6rem 1.2rem !important;
  font-weight: 700 !important;
  animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 0, 100, .35); }
  70% { transform: scale(1.03); box-shadow: 0 0 0 16px rgba(255, 0, 100, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 0, 100, 0); }
}
.small-note {
  font-size: .95rem;
  opacity: .85;
}
</style>
""", unsafe_allow_html=True)

# Floating hearts layer (HTML)
hearts = ["❤️", "💖", "💘", "💗", "💕", "💞", "🌹", "✨"]
floating_html = ""
for i in range(22):
    left = random.randint(0, 100)
    size = random.randint(18, 34)
    dur = random.uniform(6.5, 12.0)
    delay = random.uniform(0, 4.0)
    emoji = random.choice(hearts)
    floating_html += f"""
    <div class="heart" style="left:{left}vw;font-size:{size}px;
         animation-duration:{dur}s;animation-delay:{delay}s">{emoji}</div>
    """
st.markdown(floating_html, unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def typewriter(text: str, speed: float = 0.03):
    box = st.empty()
    out = ""
    for ch in text:
        out += ch
        box.markdown(f"<div class='soft'>{out}</div>", unsafe_allow_html=True)
        time.sleep(speed)

def countdown(target: dt.datetime):
    now = dt.datetime.now()
    delta = target - now
    if delta.total_seconds() <= 0:
        return "It’s today ❤️"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    mins, secs = divmod(rem, 60)
    return f"{days} days • {hours:02d}:{mins:02d}:{secs:02d}"

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='glow-title'>Happy Valentine’s Day ❤️</div>", unsafe_allow_html=True)
typewriter("Even though I’m in Buffalo and you’re in India, you’re always right here with me. 💞", 0.02)
st.write("")

# Countdown (live-ish: refresh button)
target_date = dt.datetime(2026, 2, 14, 0, 0, 0)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Countdown to us 🕯️")
    st.markdown(f"**{countdown(target_date)}**")
    st.markdown("<div class='small-note'>Every second is one step closer to the next hug.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.button("Refresh ⏳")

st.write("")

# -----------------------------
# Romantic “Reasons” reveal
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("Why I love you")
reasons = [
    "Your smile (it resets my whole day).",
    "How you support me—even when I’m deep in research mode.",
    "Our FaceTime calls—my favorite part of the day.",
    "Your laugh. Instant peace.",
    "The way you believe in me when I doubt myself.",
    "How you make distance feel temporary."
]
choice = st.slider("Pick a reason number", 1, len(reasons), 1)

if st.button("Tell me ❤️"):
    st.success(f"Reason #{choice}: {reasons[choice-1]}")
    st.balloons()
st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Love meter (animated progress)
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("Love meter")
st.caption("Scientifically measured. Completely unbiased. 😌")
meter = st.empty()
for p in range(0, 101, 5):
    meter.progress(p)
    time.sleep(0.02)
st.success("Result: 100% you. Always.")
st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Map + romantic line
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("Distance means so little…")
st.caption("…when someone means so much.")
data = pd.DataFrame({
    "lat": [42.8864, 19.0760],   # Buffalo, Mumbai
    "lon": [-78.8784, 72.8777]
})
st.map(data)
st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Surprise section
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header("One more thing…")
st.caption("Press it when you’re ready.")

st.markdown("<div class='pulse-btn'>", unsafe_allow_html=True)
surprise = st.button("Click for a surprise 💌")
st.markdown("</div>", unsafe_allow_html=True)

if surprise:
    st.balloons()
    st.toast("💖", icon="❤️")
    st.markdown("### I miss you.")
    typewriter("If I could, I’d teleport to you right now—just to hold your hand for a minute.", 0.02)
    st.write("")
    st.markdown("**Happy Valentine’s Day, my love.** 🌹✨")

st.markdown("</div>", unsafe_allow_html=True)
