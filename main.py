
import os
from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.title("Simple Chatbot")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
if "messages" not in st.session_state:
    st.session_state.messages = []

for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)

question = st.chat_input("Ask something...")

if question:

    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append(("user", question))

    history = ""

    for role, message in st.session_state.messages:
        if role == "user":
            history += f"User: {message}\n"
        else:
            history += f"Assistant: {message}\n"

    prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Conversation History:
{history}

User: {question}

Assistant:
""")

    chain = prompt | model

    response = chain.invoke({
        "history": history,
        "question": question
    })

    with st.chat_message("assistant"):
        st.write(response.content)

    # Save AI response
    st.session_state.messages.append(("assistant", response.content)) 