import streamlit as st
import base64

st.set_page_config(page_title="💖 For My Valentine", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
.stApp {
    background:
      linear-gradient(90deg, rgba(255,216,77,0.25) 0 18px, rgba(255,45,168,0.15) 18px 36px),
      radial-gradient(circle at 30% 30%, #fff7a8 0%, #ffd1e8 40%, #ff9fd6 80%);
    background-size: 36px 36px, auto;
}

header, footer {visibility:hidden;}
.block-container {padding: 0;}

.title {
    text-align:center;
    font-size:4rem;
    font-weight:900;
    color:#7a0056;
    text-shadow:6px 6px 0 #ffd84d;
    margin-top:20px;
}

.scene-wrapper {
    display:flex;
    justify-content:center;
    align-items:center;
    height:85vh;
}
</style>
""", unsafe_allow_html=True)

# ------------------ PIXEL SCENE ------------------
def pixel_scene(scale=18):
    W, H = 80, 70

    def r(x,y,w=1,h=1,c="#000"):
        return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{c}'/>"

    pink = "#ff2da8"
    pink2 = "#ff58b6"
    berry = "#7a0056"
    yellow = "#ffd84d"
    cream = "#fff7a8"
    skin = "#f6c7a8"
    hair = "#2b0d18"
    pants = "#7a0056"

    cat_white = "#ffffff"
    cat_spot = "#b57a4a"

    px = []

    # ---------------- BIG HEART ----------------
    fill = set()
    for y in range(5, 45):
        for x in range(10, 70):
            dx = abs(x - 40)
            if y < 22:
                if dx + (22 - y) < 30:
                    fill.add((x,y))
            else:
                if dx * 1.3 + (y - 22) * 1.5 < 40:
                    fill.add((x,y))

    # carve top dip
    for y in range(5,18):
        for x in range(34,47):
            if y < 14:
                if (x,y) in fill:
                    fill.remove((x,y))

    outline = set()
    for (x,y) in fill:
        for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if (nx,ny) not in fill:
                outline.add((x,y))

    for (x,y) in fill:
        px.append(r(x,y,1,1,cream))
    for (x,y) in outline:
        px.append(r(x,y,1,1,pink2))
        px.append(r(x+1,y,1,1,pink2))

    # ---------------- GROUND ----------------
    px.append(r(20,45,40,3,"#ffe6f3"))

    # ---------------- GIRL ----------------
    px += [
        r(20,28,14,4,hair),
        r(22,32,10,10,skin),
        r(22,42,10,10,pink2),
        r(24,52,4,12,pants),
        r(30,52,4,12,pants)
    ]

    # ---------------- GUY ----------------
    px += [
        r(46,28,14,4,hair),
        r(48,32,10,10,skin),
        r(48,42,10,10,yellow),
        r(50,52,4,12,pants),
        r(56,52,4,12,pants)
    ]

    # ---------------- CAT (WHITE + BROWN SPOTS) ----------------
    px += [
        r(36,46,8,6,cat_white),
        r(38,42,4,4,cat_white),
        r(34,50,3,2,cat_white),
    ]

    # brown spots
    px += [
        r(38,48,2,2,cat_spot),
        r(41,49,2,2,cat_spot),
        r(39,44,1,1,cat_spot)
    ]

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    {''.join(px)}
    </svg>
    """

    b64 = base64.b64encode(svg.encode()).decode()
    return f"""
    <div class='scene-wrapper'>
        <img src="data:image/svg+xml;base64,{b64}"
             style="width:{W*scale}px; height:{H*scale}px; image-rendering: pixelated;" />
    </div>
    """

# ------------------ UI ------------------
st.markdown("<div class='title'>VALENTINE 💖</div>", unsafe_allow_html=True)
st.markdown(pixel_scene(scale=18), unsafe_allow_html=True)
