import streamlit as st
import os
import openai

st.title("Login")
import streamlit as st

tab1, tab2 = st.tabs(["Login from OpenAI", "Login from Azure OpenAI"])
st.session_state["logined"] = False
with tab1:
    api_key = st.text_input(
        label="APIKEY",
        placeholder="Input OpenAI APIKEY",
        type="password",
        label_visibility="hidden",
        help="check your api key in https://beta.openai.com/account/api-keys",
    )
    api_submit = st.button("Submit API KEY", key="submit_apikey")

with tab2:
    api_key2 = st.text_input(
        label="APIKEY",
        placeholder="Input Azure OpenAI APIKEY",
        type="password",
        help="check your api key in https://portal.azure.com"
    )
    api_base2 = st.text_input(
        label="API BASE",
        placeholder="Input Azure OpenAI API BASE",
        type="password",
        help="check your api base in https://portal.azure.com"
    )

    api_submit2 = st.button("Submit API KEY", key="submit_apikey2")


if api_submit:
    st.session_state["api_type"] = "open_ai"
    st.session_state["api_key"] = api_key
    st.session_state["api_base"] = "https://api.openai.com/v1"
    st.session_state["api_version"] = None

    openai.api_key = st.session_state["api_key"]
    openai.api_base = st.session_state["api_base"]
    openai.api_version = st.session_state["api_version"]
    openai.api_type = st.session_state["api_type"]

    openai.api_key = st.session_state["api_key"]
    openai.api_type = st.session_state["api_type"]
    openai.api_version = st.session_state["api_version"]
    openai.api_base = st.session_state["api_base"]
    try:
        with st.spinner("logining..."):
            st.session_state["model_list"] = [x.id for x in openai.Model.list().data]
        st.success("login success")
        st.session_state["logined"] = True
    except:
        st.error(
            "login failed, check your api key in https://beta.openai.com/account/api-keys"
        )
        st.session_state["logined"] = False

elif api_submit2:
    st.session_state["api_type"] = "azure"
    st.session_state["api_key"] = api_key2
    st.session_state["api_base"] = api_base2
    st.session_state["api_version"] = "2023-03-15-preview"

    openai.api_key = st.session_state["api_key"]
    openai.api_base = st.session_state["api_base"]
    openai.api_version = st.session_state["api_version"]
    openai.api_type = st.session_state["api_type"]

    try:
        with st.spinner("logining..."):
            st.session_state["model2deployment"] = {}
            for x in openai.Deployment.list().data:
                st.session_state["model2deployment"][x.model] = x.id
        st.success("login success")
        st.session_state["logined"] = True
    except Exception as e:
        st.error(str(e))
        st.error(
            "login failed, check your api key in https://beta.openai.com/account/api-keys"
        )
        st.session_state["logined"] = False
