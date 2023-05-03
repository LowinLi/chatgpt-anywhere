import streamlit as st
import requests
from streamlit_tags import st_tags
import random
import copy
import openai


st.set_page_config(
    page_title="ChatGPT-PlayGround",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

st.title("OpenAI Playground")


if "logined" not in st.session_state.keys() or not st.session_state["logined"]:
    st.error("Please login first")
    st.stop()

if st.session_state["api_type"] == "open_ai":
    models = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4", "gpt-4-32k", "code-davinci-002"]
    models = [model for model in models if model in st.session_state["model_list"]]

if st.session_state["api_type"] == "azure":
    models = ["text-davinci-003", "gpt-35-turbo", "gpt-4", "gpt-4-32k", "code-davinci-002"]
    models = [
        model
        for model in models
        if model in st.session_state["model2deployment"].keys()
    ]


with st.empty():
    with st.form(key="my_form"):
        ce, c1, ce, c2, c3 = st.columns([0.07, 2, 0.07, 6, 0.07])
        with c1:
            st.subheader("configuration", anchor=None)
            # tts_option = st.checkbox("是否开启自动TTS朗读", value=False)
            model_option = st.selectbox("Select Model", models)
            max_tokens = st.slider(
                "max words",
                min_value=5,
                max_value=4000,
                value=100,
                step=1,
                label_visibility="visible",
            )
            temperature = st.slider(
                "temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.5,
                step=0.1,
                label_visibility="visible",
            )
            top_p = st.slider(
                "top_p",
                min_value=0.1,
                max_value=1.0,
                step=0.1,
                value=1.0,
                label_visibility="visible",
            )
            stop = st_tags(label="stop words", text="", value=[], maxtags=10, key="2")
            presence_penalty = st.slider(
                "presence_penalty",
                min_value=-2.0,
                max_value=2.0,
                value=0.0,
                step=0.1,
                label_visibility="visible",
            )
            frequency_penalty = st.slider(
                "frequency_penalty",
                min_value=-2.0,
                max_value=2.0,
                value=0.0,
                step=0.1,
                label_visibility="visible",
            )

        with c2:
            runtime_parameters = {}
            st.subheader("type your input here", anchor=None)
            text_prompt = st.text_area(
                label="a",
                help="The prompt or prompts to guide the text generation",
                disabled=False,
                height=500,
                max_chars=4000,
                label_visibility="hidden",
            )
            running = False
            submitted = st.form_submit_button("Submit", disabled=running)

            if not submitted:
                st.stop()
            if stop == []:
                stop = None
            running = True
            runtime_parameters["max_tokens"] = max_tokens
            runtime_parameters["temperature"] = temperature
            runtime_parameters["top_p"] = top_p
            runtime_parameters["stop"] = stop
            runtime_parameters["presence_penalty"] = presence_penalty
            runtime_parameters["frequency_penalty"] = frequency_penalty
            runtime_parameters["stream"] = True

            if st.session_state["api_type"] == "azure":
                runtime_parameters["engine"] = st.session_state["model2deployment"][model_option]
            elif st.session_state["api_type"] == "open_ai":
                runtime_parameters["model"] = model_option
            if model_option in ["text-davinci-003", "code-davinci-002"]:
                runtime_parameters["prompt"] = text_prompt
                res = openai.Completion.create(**runtime_parameters)
                result = ""
                with st.empty():
                    for x in res:
                        result += x.choices[0].text
                        print(result)
                        st.markdown("#### Output:\n" + result)
                running = False

            else:
                messages = [
                    {"role": "system", "content": ""}, 
                    {"role": "user", "content": text_prompt},
                ]
                runtime_parameters["messages"] = messages
                res = openai.ChatCompletion.create(**runtime_parameters)
                result = ""
                with st.empty():
                    for x in res:
                        if "content" in x.choices[0].delta.keys():
                            result += x.choices[0].delta.content
                        st.markdown("#### Output:\n" + result)
                running = False

