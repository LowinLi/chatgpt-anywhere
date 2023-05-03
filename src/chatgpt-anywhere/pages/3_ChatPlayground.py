import streamlit as st
import openai
from streamlit_tags import st_tags
import extra_streamlit_components as stx
import random
from streamlit_chat import message
import copy

st.set_page_config(
    page_title="Chat",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

st.title("OpenAI Chat Playground")



if "logined" not in st.session_state.keys() or not st.session_state["logined"]:
    st.error("Please login first")
    st.stop()

if st.session_state["api_type"] == "open_ai":
    models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"]
    models = [model for model in models if model in st.session_state["model_list"]]

if st.session_state["api_type"] == "azure":
    models = ["gpt-35-turbo", "gpt-4", "gpt-4-32k"]
    models = [
        model
        for model in models
        if model in st.session_state["model2deployment"].keys()
    ]

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

ce, c1, ce, c2, c3 = st.columns([0.07, 2, 0.07, 6, 0.07])
with c1:
    st.subheader("configuration", anchor=None)
    background_prompt = st.text_area(
        "background information",
        disabled=False,
        height=200,
        key="background_prompt",
    )
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
    stop = st_tags(label="stop words", text="", value=[], maxtags=10, key="stop")
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
    st.subheader("Chat", anchor=None)
    running = False
    user_input = st.text_input("Input and Enter","", key="input", disabled=running)
    if user_input:
        messages = [{"role": "system", "content": background_prompt}]
        for i in range(len(st.session_state["generated"])):
            messages.append({"role": "user", "content": st.session_state["past"][i]})
            messages.append({"role": "assistant", "content": st.session_state["generated"][i]})
        messages.append({"role": "user", "content": user_input})

        running = True

        if st.session_state["api_type"] == "azure":
            res = openai.ChatCompletion.create(
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=stop or None,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                stream=True,
                messages=messages,
                engine=st.session_state["model2deployment"][model_option],
            )
        elif st.session_state["api_type"] == "open_ai":
            res = openai.ChatCompletion.create(
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop=stop or None,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                stream=True,
                messages=messages,
                model=model_option
            )
        
        result = ""
        with st.empty():
            # key = len(st.session_state["generated"])
            # message(user_input, avatar_style="pixel-art", key=str(key) + "_user", is_user=True)
            for x in res:
                if "content" in x.choices[0].delta.keys():
                    result += x.choices[0].delta.content
            # message(result, avatar_style="pixel-art", key=str(key))

                

        

        st.session_state.past.append(user_input)
        st.session_state.generated.append(result)

    if st.session_state["generated"]:
        
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], avatar_style="icons", key=str(i))
            message(st.session_state["past"][i], avatar_style="fun-emoji", is_user=True, key=str(i) + "_user")
