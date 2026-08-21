import uuid

import streamlit as st

from api import (
    ask_question,
    stream_answer
)


st.set_page_config(
    page_title="Production AI Agent",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Session ID
# --------------------------------------------------

if "session_id" not in st.session_state:

    st.session_state.session_id = str(
        uuid.uuid4()
    )

# -------------------------------------------------
# Clear Chat
# -------------------------------------------------

if st.sidebar.button("🗑️ New Conversation"):
    st.session_state.session_id = str(
        uuid.uuid4()
    )

    st.session_state.message = []

    st.rerun()

# --------------------------------------------------
# Chat history
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 Production LangGraph AI Agent")

st.caption(
    "LangGraph + FastAPI + Ollama + Persistent Memory"
)

st.divider()


# --------------------------------------------------
# Display previous messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# Chat input
# --------------------------------------------------

question = st.chat_input(
    "Ask the AI agent anything..."
)


if question:

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Assistant response

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        try:

            for chunk in stream_answer(
                question,
                st.session_state.session_id
            ):

                full_response += chunk

                response_placeholder.markdown(
                    full_response + "|"
                )

                response_placeholder.markdown(
                    full_response 
                )

        except Exception as e:


            response_placeholder.error(
                f"{full_response}\n\n{e}"
            )


    # Save assistant response

    if full_response:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )