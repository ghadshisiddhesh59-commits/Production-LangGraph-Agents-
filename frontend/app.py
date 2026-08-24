import uuid

import streamlit as st

from frontend.api import ask_question


st.set_page_config(
    page_title="Production AI Agent",
    page_icon="🤖",
    layout="wide"
)


# Session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# Messages
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:

    st.title("Conversation")

    if st.button("🗑️ New Conversation"):

        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.session_state.messages = []

        st.rerun()


# Header
st.title("🤖 Production LangGraph AI Agent")

st.caption(
    "LangGraph + FastAPI + LLM Tools + Persistent Memory"
)

st.divider()


# Existing messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# Chat
question = st.chat_input(
    "Ask the AI agent anything..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = ask_question(
                    question,
                    st.session_state.session_id
                )

                answer = result["answer"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"Request failed: {e}"
                )