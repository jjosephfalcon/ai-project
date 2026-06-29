# ============================================================
# CHATBOT UI — Built with Streamlit + Groq
# ============================================================
# HOW TO RUN:
#   1. Set your API key:   $env:GROQ_API_KEY = "your-key-here"
#   2. Launch the UI:      streamlit run chatbot_ui.py
#   3. Your browser opens automatically at http://localhost:8501
# ============================================================

import os
import streamlit as st
from groq import Groq

# ── CONCEPT 1: Streamlit's Rerun Model ───────────────────────
# Every time the user does ANYTHING (types, clicks, etc.),
# Streamlit reruns this entire script from top to bottom.
# That means variables reset to their defaults on every rerun.
# This is very different from normal Python programs!
# The fix is session_state (see CONCEPT 2 below).
# ─────────────────────────────────────────────────────────────

# Page configuration — must be the first Streamlit call
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ── CONCEPT 2: st.session_state ──────────────────────────────
# session_state is a dictionary that PERSISTS across reruns.
# It lives for the duration of the browser session.
# We use it to store the chat history so messages don't vanish.
#
# Pattern:  if "key" not in st.session_state:
#               st.session_state["key"] = default_value
# This initializes only once, then keeps the value on reruns.
# ─────────────────────────────────────────────────────────────

# Initialize chat history as an empty list on first load
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the selected persona (we support switching personas)
if "persona" not in st.session_state:
    st.session_state.persona = "SpongeBob"


# ── GROQ CLIENT SETUP ────────────────────────────────────────
# We read the API key from the environment (same as your original
# script). @st.cache_resource tells Streamlit to create the client
# ONCE and reuse it — not rebuild it on every rerun.
# ─────────────────────────────────────────────────────────────

@st.cache_resource
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY environment variable not set. Please set it and restart.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()


# ── PERSONA DEFINITIONS ───────────────────────────────────────
# Each persona is a "system prompt" — a hidden instruction that
# tells the AI how to behave before any user message is sent.
# System prompts are the #1 tool for shaping AI personality.
# ─────────────────────────────────────────────────────────────

PERSONAS = {
    "SpongeBob": {
        "icon": "🧽",
        "system": (
            "You are SpongeBob SquarePants — enthusiastic, funny, optimistic, and a little goofy. "
            "You live in Bikini Bottom, work at the Krusty Krab, and love your best friend Patrick. "
            "Answer in SpongeBob's voice, sneak in SpongeBob-style jokes or references when it fits, "
            "and always stay cheerful and encouraging."
        ),
    },
    "Helpful Assistant": {
        "icon": "🤖",
        "system": (
            "You are a helpful, concise, and friendly AI assistant. "
            "Give clear, accurate answers. When unsure, say so."
        ),
    },
    "Pirate": {
        "icon": "🏴‍☠️",
        "system": (
            "You are a friendly pirate named Captain Code. Speak like a pirate (arrr, matey, ye, etc.) "
            "but give genuinely helpful answers. Throw in nautical references when they fit."
        ),
    },
}


# ── UI LAYOUT ────────────────────────────────────────────────

st.title("💬 AI Chatbot")
st.caption("Powered by Groq · llama-3.3-70b-versatile")

# Sidebar: persona picker and clear button
with st.sidebar:
    st.header("Settings")

    # st.selectbox returns the selected value each rerun.
    # We store it in session_state so the choice persists.
    chosen_persona = st.selectbox(
        "Choose a persona",
        options=list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona),
    )

    # If the user switches persona, clear chat history and update
    if chosen_persona != st.session_state.persona:
        st.session_state.persona = chosen_persona
        st.session_state.messages = []
        st.rerun()  # Immediately rerun to reflect the change

    persona = PERSONAS[st.session_state.persona]
    st.info(f"Current persona: {persona['icon']} {st.session_state.persona}")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**How it works:**")
    st.markdown(
        "1. Your message → sent to Groq API\n"
        "2. Groq runs llama-3.3-70b\n"
        "3. Response streams back word-by-word\n"
        "4. History kept in `session_state`"
    )


# ── CONCEPT 3: Displaying Chat History ───────────────────────
# st.chat_message("role") creates a chat bubble.
# role is "user" or "assistant" — Streamlit styles them differently.
# We loop through session_state.messages and render all previous
# messages so they appear after a rerun.
# ─────────────────────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── CONCEPT 4: The Chat Input ────────────────────────────────
# st.chat_input() renders the input box pinned to the bottom.
# It returns the user's text when they press Enter, else None.
# The `if prompt:` block only runs when the user submits a message.
# ─────────────────────────────────────────────────────────────

if prompt := st.chat_input(f"Message {persona['icon']} {st.session_state.persona}..."):

    # Add user message to history and display it immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ── CONCEPT 5: Streaming Responses ───────────────────────
    # Instead of waiting for the full reply, we stream it.
    # stream=True makes Groq send tokens as they're generated.
    # st.write_stream() displays each chunk as it arrives,
    # giving the "AI is typing" effect you see in ChatGPT.
    #
    # We also build the system message list here:
    #   [system prompt] + [all past messages] + [new user message]
    # This gives the model full conversation context every call.
    # ─────────────────────────────────────────────────────────

    # Build the messages list: system prompt first, then history
    api_messages = [{"role": "system", "content": persona["system"]}]
    api_messages += st.session_state.messages  # includes the new user msg

    with st.chat_message("assistant"):
        # stream=True returns a generator of chunks
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages,
            stream=True,
        )

        # st.write_stream iterates the generator and displays each chunk
        # It also returns the full assembled text when done
        full_response = st.write_stream(
            chunk.choices[0].delta.content or ""
            for chunk in stream
            if chunk.choices[0].delta.content
        )

    # Save the completed assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
