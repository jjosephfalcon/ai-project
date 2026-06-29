import streamlit as st

st.title("Learning session_state")

# -------------------------------------------------------
# THE PROBLEM: Streamlit reruns the whole file on every
# click. So a normal variable resets to 0 every time.
# -------------------------------------------------------

normal_count = 0  # this resets to 0 on EVERY rerun

st.header("Normal variable (broken)")
st.write(f"Count: {normal_count}")  # will always show 0
if st.button("Add 1 (broken)"):
    normal_count += 1  # pointless — resets next rerun
    st.write(f"Tried to set it to {normal_count} but it won't stick!")

st.divider()

# -------------------------------------------------------
# THE FIX: session_state survives reruns.
# Think of it as a save file for your variables.
# -------------------------------------------------------

st.header("session_state (works)")

# Step 1: Create the variable ONCE (only runs on first load)
if "count" not in st.session_state:
    st.session_state.count = 0

# Step 2: Use it like a normal variable
st.write(f"Count: {st.session_state.count}")

# Step 3: Change it — the change STICKS across reruns
if st.button("Add 1 (works)"):
    st.session_state.count += 1

if st.button("Reset"):
    st.session_state.count = 0

st.divider()

# -------------------------------------------------------
# WHY THIS MATTERS FOR YOUR CHATBOT:
# Messages are stored in session_state.messages (a list).
# Every time you send a message, it gets appended to that list.
# Because it's in session_state, the list survives reruns
# and all your messages stay on screen.
# -------------------------------------------------------

st.header("Mini chatbot (same idea)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all stored messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Add a new message to the list
if user_input := st.chat_input("Type something..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": f"You said: {user_input}"})
    st.rerun()
