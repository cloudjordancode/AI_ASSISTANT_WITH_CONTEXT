# AI Chat Interface

**Module:** 6 — Web Essentials & Streamlit
**Estimated time:** 45 minutes

## Objective

Build a Streamlit chat interface with streaming responses, session-based chat history, and sidebar controls.

## What You'll Build

A chat application that maintains conversation history using `st.session_state`. The sidebar includes an API key input (password field), a system prompt text area, a model selector, a Clear button, and a message count display. The main area renders the full chat history with `st.chat_message()` and accepts new input via `st.chat_input()`. A mock response generator provides streaming output for students without an API key, displayed with `st.write_stream()`.

## Reference Code

The starter file (`starter.py`) provides a scaffold with TODOs — fill in each section, then compare with the solution.

## Running

```bash
streamlit run starter.py
```

## Deliverable

A working Streamlit chat app with sidebar controls, persistent chat history, and streaming responses.
