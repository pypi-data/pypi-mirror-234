import os

import streamlit as st  
import pandas as pd

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True
if not _RELEASE:
    _streamlit_card_component = components.declare_component(
        "streamlit_card_component",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_card_component = components.declare_component("streamlit_card_component", path=build_dir)


def streamlit_card_component(key=None,shape=None ,data=None,label=None):
    return _streamlit_card_component(key=key,shape=shape,data=data,label=label)

def are_dicts_equal(dict1, dict2):
    # Check if both dictionaries have the same keys
    if type(dict2) != dict:
        return False
    if set(dict1.keys()) != set(dict2.keys()):
        return False
    
    # Check if the values for each key are equal
    for key in dict1:
        if dict1[key] != dict2[key]:
            return False
    return True

# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_dataframe/__init__.py`
if not _RELEASE:
    shape = {
        "width": "100%",
        "height": "60px",
        "is_horizontal":"false"
    }
    data=["4.56","12.34","8.98","7.67","4.56","12.34","8.98","7.67","4.56","12.34"]
    label=["dnnsi","rate needed","fyi new target","planned to target difference","predicted volume","predicted_volume(unit)","predicted_customer_margin","current fy volume","current fy volume(unit)","current fy customer margin"]
    df = streamlit_card_component(shape=shape,data=data,label=label)
    st.write(df)