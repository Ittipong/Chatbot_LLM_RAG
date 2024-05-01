#!/bin/env python3
import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF
import asyncio
from streamlit_extras.app_logo import add_logo



def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def read_and_save_file():
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)


def page():
    
    custom_html = """
    <div class="banner">
    <img src="https://cdn-apac.onetrust.com/logos/1a47fb42-48b0-45a2-9952-28a06e552348/5ddf9705-9e61-4f91-be2b-d71c729f655f/dc5fb890-4450-4fff-848d-41b34f439bf7/Lotus's_Logo.svg.png" alt="Banner Image">
    
    </div>
    <style>
        .banner {
            width: 100%;
            height: 200px;
            overflow: hidden;
    }
    .banner img {
        width: 100%;
        object-fit: fill;
    }
    </style>
    """
# Display the custom HTML
    st.components.v1.html(custom_html)

    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()

    st.header("Chatbot Customer service")
    
    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

if __name__ == "__main__":
    page()
