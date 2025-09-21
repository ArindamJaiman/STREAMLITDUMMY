import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Dummy Page", page_icon="✅", layout="centered")

st.title("Hello from Streamlit 👋")
st.write(
    "This is a **dummy page**. "
    "If you can read this on a public URL, your deploy worked!"
)

col1, col2 = st.columns(2)
col1.metric("Status", "✅ Online")
col2.write(f"Deployed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

with st.expander("What is this?"):
    st.markdown(
        "- A minimal Streamlit app\n"
        "- No database, no auth, just a page\n"
        "- Edit this file and push to redeploy"
    )

if st.button("Say hi"):
    st.success("Hi Sidhanth! 👋")
