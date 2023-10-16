import os

import streamlit as st  
import pandas as pd

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _custom_dataframe = components.declare_component(
        "custom_dataframe",
        url="http://localhost:3002",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_dataframe = components.declare_component("custom_dataframe", path=build_dir)


def custom_dataframe(data=None, key=None,editable_cell=None,shape=None,colorable_cells=None,colorable_text=None,firstColumnWide=None,issequencingPage=None,label=None):
    data = data.to_dict(orient='list') 
    return _custom_dataframe(data=data, key=key, editable_cells=editable_cell,  colorable_cells=colorable_cells, shape=shape, colorable_text=colorable_text,firstColumnWide=firstColumnWide,issequencingPage=issequencingPage,label=label)



# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_dataframe/__init__.py`
if not _RELEASE:
    data = {
        "Category": ["CCF Regional Accrual", "CTM Local Accrual", "Flex", "Other", "DNNSI"],
        "P1_A": [1, 0, 0, 0, 0],
        "New Pricing": [0, 2, 0, 1, 0],
        "Change $": [0, 0, 4, 0, 0],
        "Change%": [0, 0, 9, 0, 0]
    }
    editable_cell = {
        "New Pricing":[0,1,2,3],
        }
    shape = {
        "no_rows": 5,
        "no_cols": 5,
        "width": "70%",
        "height": "200px",
        "landscape":"false"
    }
    colorable_cells  = {
    "Category": ["", "", "", "", ""],
    "Current": ["", "", "", "", ""],
    "New Pricing": ["rgb(255,229,180)", "rgb(255,229,180)", "rgb(255,229,180)", "rgb(255,229,180)", ""],
    "Change $": ["", "", "", "", ""],
    "Change%": ["", "", "", "", ""]
    }
    firstColumnWide={"isTrue":False,"width":"40%"}
    issequencingPage=False
    label="accruals2"
    df2 = pd.DataFrame(data)
    df = custom_dataframe(df2,key=2,editable_cell=editable_cell,shape= shape,colorable_cells=colorable_cells, colorable_text={},firstColumnWide=firstColumnWide,issequencingPage=issequencingPage,label=label)
    st.dataframe(df)