import streamlit as st
import os
import openai

st.title("Login OpenAI")


api_key = st.text_input(
    label="APIKEY",
    placeholder="Input OpenAI APIKEY",
    type="password",
    label_visibility="hidden",
    help="check your api key in https://beta.openai.com/account/api-keys",
)

api_submit = st.button("Submit API KEY", key="submit_apikey")
st.session_state["api_key"] = api_key
if "api_key" not in st.session_state.keys() or not api_submit:
    st.stop()

if st.session_state["api_key"]:
    openai.api_key = st.session_state["api_key"]
    try:
        with st.spinner("logining..."):
            openai.Model.list()
        st.success("login success")
        st.session_state["logined"] = True
    except:
        st.error("login failed, check your api key in https://beta.openai.com/account/api-keys")
        st.session_state["logined"] = False
else:
    st.error("Please input your OpenAI APIKEY")
    st.stop()