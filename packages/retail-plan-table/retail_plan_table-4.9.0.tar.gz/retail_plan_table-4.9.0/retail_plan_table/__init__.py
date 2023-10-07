import os

import streamlit as st  
import pandas as pd

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True
if not _RELEASE:
    _retail_plan_table = components.declare_component(
        "retail_plan_table",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _retail_plan_table = components.declare_component("retail_plan_table", path=build_dir)


def retail_plan_table(key=None,data=None,shape=None,price_multiple=None,invoice_prices=None):
    data = data.to_dict(orient='records') 
    return _retail_plan_table(key=key, data=data ,shape=shape,price_multiple=price_multiple,invoice_prices=invoice_prices)

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
#if True:
    shape = {
        "width": "100%",
        "height": "300px"
    }
    price_multiple=[
             "",
             "10 for",
             "15 for",
             "2 for",
            "3 for",
            "4 for",
           "5 for",
           "6 for",
           "7 for",
          "B1G1",
         "B2G1",
         "B2G2",
        "B2G3",
        "B2S2",
        "B3G2",
       "B3S2",
       "B3S3",
      "B5S5",
       "ea. wyb 2",
       "ea. wyb 3",
      "ea. wyb 4",
      "ea. wyb 5"
   ]
    #data={'Category': ['White Tag', 'Retail Multiple', 'Price', 'Multiple', 'Take Rate', 'Discount vs EDV', 'Effective Retail', 'Volume / Event (Cases)', 'Event Frequency (Wks)', 'Invoice', 'Allowances (All/Promo)', 'Trade Allowance per case', 'Other', 'Net Invoice Cost', 'Net Cost (Unit)', 'Invoice Cost @ 100% Take Rate', 'Customer Margin ($/Unit)', 'Customer Margin %'], 'edv': [2.99, 0, 0, '', 0, '', 2.99, 0, 52, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P1_A': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P1_B': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P1_C': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P1_D': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P2_A': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P2_B': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P2_C': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'P2_D': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'Holiday': [2.99, 0, 0, '', 0, '0.00%', 2.99, 0, 0, 20.64, '', 0, 0, 20.64, 1.72, 20.64, 1.2700000000000002, '42.47%'], 'Total': ['', '', '', '', '', '', 0, 0, 52, '', '', 0, 0, 0, 0, 0, '', '0.00%']}
    #data={'Category': ['White Tag', 'Retail Multiple', 'Price', 'Multiple', 'Take Rate', 'Discount vs EDV', 'Effective Retail', 'Volume / Event (Cases)', 'Event Frequency (Wks)', 'Invoice', 'Allowances (All/Promo)', 'Trade Allowance per case', 'Other', 'Net Invoice Cost', 'Net Cost (Unit)', 'Invoice Cost @ 100% Take Rate', 'Customer Margin ($/Unit)', 'Customer Margin %'], 'edv': ['2.99', '0', '0', '', '0', '', '2.99', '0', '52', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P1_A': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P1_B': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P1_C': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P1_D': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P2_A': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P2_B': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P2_C': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'P2_D': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'Holiday': ['2.99', '0', '0', '', '0', '0.00%', '2.99', '0', '0', '20.64', '', '0', '0', '20.64', '1.72', '20.64', '1.2700000000000002', '42.47%'], 'Total': ['', '', '', '', '', '', '0', '0', '52', '', '', '0', '0', '0', '0', '0', '', '0.00%']}
    st.session_state.check=False
    # view_changes=st.button("button")
    # if view_changes:
    #     st.session_state.check=True
    # st.write("view_changes",st.session_state.check)
    invoice_prices={"0":26.88,"1":27.88}
    data=[{'Category': 'White Tag', 'edv': 2.99, 'P1_A': 2.99, 'P1_B': 2.99, 'P1_C': 2.99, 'P1_D': 2.99, 'P2_A': 2.99, 'P2_B': 2.99, 'P2_C': 2.99, 'P2_D': 2.99, 'Holiday': 2.99, 'Total': '12'}, {'Category': 'Retail Multiple', 'edv': 0, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': ''}, {'Category': 'Price', 'edv': 0, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': ''}, {'Category': 'Multiple', 'edv': '', 'P1_A': '', 'P1_B': '', 'P1_C': '', 'P1_D': '', 'P2_A': '', 'P2_B': '', 'P2_C': '', 'P2_D': '', 'Holiday': '', 'Total': '55'}, {'Category': 'Take Rate', 'edv': 0, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': ''}, {'Category': 'Discount vs EDV', 'edv': '', 'P1_A': '0.00%', 'P1_B': '0.00%', 'P1_C': '0.00%', 'P1_D': '0.00%', 'P2_A': '0.00%', 'P2_B': '0.00%', 'P2_C': '0.00%', 'P2_D': '0.00%', 'Holiday': '0.00%', 'Total': ''}, {'Category': 'Effective Retail', 'edv': 2.99, 'P1_A': 2.99, 'P1_B': 2.99, 'P1_C': 2.99, 'P1_D': 2.99, 'P2_A': 2.99, 'P2_B': 2.99, 'P2_C': 2.99, 'P2_D': 2.99, 'Holiday': 2.99, 'Total': 0}, {'Category': 'Volume / Event (Cases)', 'edv': 0, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': 0}, {'Category': 'Event Frequency (Wks)', 'edv': 52, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': 52}, {'Category': 'Invoice', 'edv': 23.0, 'P1_A': 23.0, 'P1_B': 23.0, 'P1_C': 23.0, 'P1_D': 23.0, 'P2_A': 23.0, 'P2_B': 23.0, 'P2_C': 23.0, 'P2_D': 23.0, 'Holiday': 23.0, 'Total': ''}, {'Category': 'Allowances (All/Promo)', 'edv': 'All', 'P1_A': 'All', 'P1_B': 'All', 'P1_C': 'All', 'P1_D': 'All', 'P2_A': 'All', 'P2_B': 'All', 'P2_C': 'All', 'P2_D': 'All', 'Holiday': 'A11', 'Total': ''}, {'Category': 'Trade Allowance per case', 'edv': 0, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': 0}, {'Category': 'Other', 'edv': 0, 'P1_A': 0, 'P1_B': 0, 'P1_C': 0, 'P1_D': 0, 'P2_A': 0, 'P2_B': 0, 'P2_C': 0, 'P2_D': 0, 'Holiday': 0, 'Total': 0}, {'Category': 'EDV', 'edv': 'false', 'P1_A': 'false', 'P1_B': 'false', 'P1_C': 'false', 'P1_D': 'false', 'P2_A': 'false', 'P2_B': 'false', 'P2_C': 'false', 'P2_D': 'false', 'Holiday': 'false', 'Total': ''}, {'Category': 'Net Invoice Cost', 'edv': 23.0, 'P1_A': 23.0, 'P1_B': 23.0, 'P1_C': 23.0, 'P1_D': 23.0, 'P2_A': 23.0, 'P2_B': 23.0, 'P2_C': 23.0, 'P2_D': 23.0, 'Holiday': 23.0, 'Total': 0}, {'Category': 'Net Cost (Unit)', 'edv': 1.9166666666666667, 'P1_A': 1.9166666666666667, 'P1_B': 1.9166666666666667, 'P1_C': 1.9166666666666667, 'P1_D': 1.9166666666666667, 'P2_A': 1.9166666666666667, 'P2_B': 1.9166666666666667, 'P2_C': 1.9166666666666667, 'P2_D': 1.9166666666666667, 'Holiday': 1.9166666666666667, 'Total': 0}, {'Category': 'Invoice Cost @ 100% Take Rate', 'edv': 23.0, 'P1_A': 23.0, 'P1_B': 23.0, 'P1_C': 23.0, 'P1_D': 23.0, 'P2_A': 23.0, 'P2_B': 23.0, 'P2_C': 23.0, 'P2_D': 23.0, 'Holiday': 23.0, 'Total': 0}, {'Category': 'Customer Margin ($/Unit)', 'edv': 1.0733333333333335, 'P1_A': 1.0733333333333335, 'P1_B': 1.0733333333333335, 'P1_C': 1.0733333333333335, 'P1_D': 1.0733333333333335, 'P2_A': 1.0733333333333335, 'P2_B': 1.0733333333333335, 'P2_C': 1.0733333333333335, 'P2_D': 1.0733333333333335, 'Holiday': 1.0733333333333335, 'Total': ''}, {'Category': 'Customer Margin %', 'edv': '35.90%', 'P1_A': '35.90%', 'P1_B': '35.90%', 'P1_C': '35.90%', 'P1_D': '35.90%', 'P2_A': '35.90%', 'P2_B': '35.90%', 'P2_C': '35.90%', 'P2_D': '35.90%', 'Holiday': '35.90%', 'Total': '0.00%'}, {'Category': 'Current', 'edv': 'false', 'P1_A': 'false', 'P1_B': 'false', 'P1_C': 'false', 'P1_D': 'false', 'P2_A': 'false', 'P2_B': 'false', 'P2_C': 'false', 'P2_D': 'false', 'Holiday': 'false', 'Total': ''}, {'Category': 'New', 'edv': 'false', 'P1_A': 'false', 'P1_B': 'false', 'P1_C': 'false', 'P1_D': 'false', 'P2_A': 'false', 'P2_B': 'false', 'P2_C': 'false', 'P2_D': 'true', 'Holiday': 'false', 'Total': ''}]
    if "data" not in st.session_state:
        st.session_state.data=data
    # if "message" not in st.session_state:
    #     st.session_state.message=message
    df = retail_plan_table(data=pd.DataFrame(data),shape= shape,price_multiple=price_multiple,invoice_prices=invoice_prices)
    # if df!=None :
    #     st.session_state["data"]=df
    st.write(df)
    # if "condition" not in st.session_state:
    #     st.session_state.condition=df
    # if df != None and not are_dicts_equal(df,st.session_state.condition):
    #     st.write(df)
    #     data =[]
    #     st.session_state.condition=df
    #     st.session_state.data=data
    #     st.session_state.message="scenario is updated/created"
    #     st.experimental_rerun()
