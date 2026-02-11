import streamlit as st
import datetime
import pandas as pd

# Page Config
st.set_page_config(page_title="For My Valentine", page_icon="❤️")

# Title and Header
st.title("Happy Valentine's Day! ❤️")
st.write("Even though I'm in Buffalo and you're in India, you are always close to my heart.")

# Countdown
target_date = datetime.datetime(2026, 2, 14) # Adjust if needed
today = datetime.datetime.now()
delta = target_date - today

# Image
# st.image("your_photo.jpg", caption="Us") # Uncomment and add a photo of you two

# Interactive "Why I Love You"
st.header("Why I Love You")
reasons = ["Your smile", "How you support my research", "Our FaceTime calls", "Your laugh"]
selected_reason = st.selectbox("Pick a number:", range(1, len(reasons) + 1))
st.success(f"Reason #{selected_reason}: {reasons[selected_reason-1]}")

# Distance Map
st.header("Distance means so little when someone means so much")
data = pd.DataFrame({
    'lat': [42.8864, 19.0760], # Buffalo and Mumbai coordinates
    'lon': [-78.8784, 72.8777]
})
st.map(data)

if st.button("Click for a surprise"):
    st.balloons()
    st.write("I miss you! Happy Valentine's Day!")