import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Leads Prediction",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

df = pd.read_excel("Silo-Data-Test.xlsx")
states = df["ST"].unique()
silos = df["Silo"].unique()
ap_scale_silos = dict(df[["Silo","AP-Scale"]].values)

input_states = st.multiselect("Select the states:",states)
input_silos = st.multiselect("Select the Silos:",silos)
input_budget = []

# For each selected option, display a row with the option and a text input
for i, option in enumerate(input_silos):
    col1, col2, _ = st.columns([1,3,2])  # Adjust the ratio as needed
    col1.markdown(f"<div style='text-align: center; color: white; padding-top: 30px; font-size:18px;'>{option}</div>", unsafe_allow_html=True)
    text_input_slot = col2.empty()
    user_input = text_input_slot.text_input('', '', key=f'input_{i}')
    input_budget.append(user_input)

if st.button("Predict"):
    leads = []
    average_CPLs = []
    input_budget = [float(i) for i in input_budget]
    for silo,budget in zip(input_silos,input_budget):
        CPLs = []
        for state in input_states:
            CPLs.append(df[(df["Silo"]==silo) & (df["ST"]==state)]["CPL"])
        CPLs = pd.Series([CPL.values[0] if len(CPL)>0 else None for CPL in CPLs]).dropna()
        average_CPL = CPLs.sum()/len(CPLs)
        average_CPLs.append(average_CPL)
        leads.append(int(budget//average_CPL)) 
    AP_scales = [ap_scale_silos[silo] for silo in input_silos]
    average_AP_scales = round(sum(AP_scales)/len(input_silos),1)

    result = pd.DataFrame({"Silo":input_silos,"Budget":input_budget,"Average CPL":average_CPLs,"Leads":leads})
    result["Budget"] = result["Budget"].apply(lambda a: "$ " + str(round(a,2)))
    result["Average CPL"] = "$ " + str(round(result["Average CPL"],2))
    st.dataframe(result)
    st.write("AP Scale: "+str(average_AP_scales))
    st.write("Total leads: "+str(sum(leads)))



















