"""
L12 — AI Chat Interface  (STARTER)
=====================================
Run with:
    streamlit run starter.py

Your goal: build a Streamlit chat interface with streaming responses.

Required features:
    1. Sidebar: API key input (type="password"), system prompt text area,
       model selector, Clear button, message count
    2. Chat history in session state (list of {"role": ..., "content": ...})
    3. Full chat display using st.chat_message() for each message
    4. st.chat_input() for user messages
    5. Mock response generator for students without an API key
    6. st.write_stream() to display the streaming response

Key concepts:
    Chat history pattern:
        Store messages as a list in session state:
            [{"role": "user", "content": "Hello"},
             {"role": "assistant", "content": "Hi!"}]
        On every re-run, iterate through ALL messages and re-render them.
        This is why history appears to persist — it's stored in session_state
        and re-drawn each time from scratch.

    st.chat_message(role):
        Context manager that renders a styled chat bubble.
        `with st.chat_message("user"): st.markdown(text)`

    st.chat_input(placeholder):
        Fixed-to-bottom input; returns submitted text or None.

    st.write_stream(generator):
        Renders text from a generator token by token (typewriter effect).
        Returns the complete assembled string when done.
"""

import streamlit as st
import time

# ── Page config ────────────────────────────────────────────────────────────
# TODO: 
# 
st.set_page_config(page_title="AI CHAT ASSISTANT", page_icon="💁🏼", layout="centered")

# ── Session state ──────────────────────────────────────────────────────────
# TODO: Initialise "messages" to [] — a list of {"role": ..., "content": ...} dicts
# TODO: Initialise "api_key" to ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""

# ── Sidebar ────────────────────────────────────────────────────────────────
# TODO: with st.sidebar:
#   - st.header("Settings")
#   - API key: st.text_input("OpenAI API Key", type="password")
#     Store in st.session_state.api_key
#   - System prompt: st.text_area with a default value
#   - Model: st.selectbox with ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
#   - st.divider()
#   - Clear button: if clicked, set messages = [] and st.rerun()
#   - Caption showing message count

# — Sidebar —
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "OpenAI API Key (optional)",
        type="password",
        placeholder="sk-..."
    )
    st.session_state["api_key"] = api_key

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant who explains concepts clearly and patiently.",
        help="Customize the AI's personality, tone, and behavior. For example: 'You are a friendly Python tutor who explains coding concepts to beginners.'",
        height=120
    )

    st.subheader("Context")
    python_context = st.checkbox("Include Python expertise")
    web_context = st.checkbox("Include web development context")
    ai_context = st.checkbox("Include AI/ML context")

    contexts = []

    if python_context:
        contexts.append("Python programming")

    if web_context:
        contexts.append("Web development")

    if ai_context:
        contexts.append("Artificial Intelligence and Machine Learning")

    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()

    st.caption(f"Messages: {len(st.session_state['messages'])}")


    # — Conversation Export —
    if st.button("📋 Copy Conversation"):
        if st.session_state["messages"]:
            export_text = ""

            for msg in st.session_state["messages"]:
                role = "You" if msg["role"] == "user" else "AI"
                export_text += f"{role}: {msg['content']}\n\n"

            st.code(export_text, language=None)

            st.download_button(
                "💾 Download Chat",
                data=export_text,
                file_name="chat_export.txt",
                mime="text/plain"
            )

        else:
            st.info("No messages to export yet.")

# ── Page title ─────────────────────────────────────────────────────────────
# TODO: st.title and info banner if no API key

st.title("💁🏼 AI Chat Assistant")

if not st.session_state["api_key"]:
    st.info("No API key provided — using mock AI responses.")

# ══════════════════════════════════════════════════════════════════════════
# RENDER CHAT HISTORY
# ──────────────────────────────────────────────────────────────────────────
# TODO: Loop through st.session_state.messages
#       For each message, use `with st.chat_message(message["role"]):`
#       and display the content with st.markdown()
#
# IMPORTANT: This loop re-renders ALL messages on every re-run.
# Messages appear to persist because they're stored in session_state.

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ── Mock response generator ────────────────────────────────────────────────
# TODO: Implement mock_stream(user_message) as a generator function.
#   - Map keywords to responses (e.g. "python", "streamlit", "fastapi")
#   - yield one word at a time with time.sleep(0.04) between each
#   - This simulates streaming without needing an API key

def mock_stream(user_message: str):
    question = user_message.lower()

    if "python" in question:
        response = "Python is a versatile programming language."
    elif "streamlit" in question:
        response = "Streamlit helps you build interactive Python web applications."
    elif "fastapi" in question:
        response = "FastAPI is a Python framework for building APIs."
    else:
        response = f"You asked: '{user_message}'. Here's a general explanation."

    if contexts:
        response += f"\n\nSelected context: {', '.join(contexts)}."

    response += f"\n\nAssistant instructions: {system_prompt}"

    for word in response.split():
        yield word + " "
        time.sleep(0.04)
    


# ── Chat input ─────────────────────────────────────────────────────────────
# TODO: Use `if prompt := st.chat_input("Ask me anything…"):`
#   Inside:
#   1. Append {"role": "user", "content": prompt} to st.session_state.messages
#   2. Render the user message with st.chat_message("user")
#   3. Render the assistant response with st.chat_message("assistant"):
#      - Use mock_stream(prompt) as the generator
#      - Call `full_response = st.write_stream(generator)`
#        st.write_stream renders the generator output token by token
#        and returns the complete string
#   4. Append {"role": "assistant", "content": full_response} to messages
if prompt := st.chat_input("Ask me anything..."):

    # 1. Save the user's message
    st.session_state["messages"].append({
        "role": "user",
        "content": prompt
    })

    # 2. Display the user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Generate and display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = st.write_stream(
                mock_stream(prompt)
            )

    # 4. Save the assistant's response
    st.session_state["messages"].append({
        "role": "assistant",
        "content": full_response
    })