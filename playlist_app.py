import streamlit as st

st.title("AI Playlist Generator")

mood = st.text_input("What is your mood?")
st.button("Generate Playlist")
def generate_playlist(mood):
    return "choose playlist"
    