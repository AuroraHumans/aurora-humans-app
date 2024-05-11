import streamlit as st
from langchain.llms import OpenAI
import json

st.title("💚💚🥰 Aurora Humans Worldwide Upload Dataset")

'''with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"'''


def insert_feelings(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:", "What did you feel when you saw the sky alive?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        insert_feelings(text)