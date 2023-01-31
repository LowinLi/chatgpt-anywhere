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


with st.empty():
    with st.form(key="my_form"):
        ce, c1, ce, c2, c3 = st.columns([0.07, 2, 0.07, 6, 0.07])
        with c1:
            st.subheader("configuration", anchor=None)
            # tts_option = st.checkbox("是否开启自动TTS朗读", value=False)
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
                label_visibility="hidden"
                
            )
            running=False
            submitted = st.form_submit_button("Submit", disabled=running)

            if not submitted:
                st.stop()
            if stop == []:
                stop = None
            running=True
            res = openai.Completion.create(
                model="text-davinci-003",
                prompt=text_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                stop=stop,
                top_p=top_p,
                stream=True
            )
            result = ""
            with st.empty():
                for x in res:
                    result += x.choices[0].text
                    st.markdown("#### Output:\n"+result)
            running=False
                
                    
            
            