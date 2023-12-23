import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 

st.set_page_config(
    page_title="Leads Prediction",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

df = pd.read_excel("Silo-Data-Test.xlsx")
role_adjuster = pd.read_excel("Silo-Data-Classifications.xlsx")
states = df["ST"].unique()
silos = df["Silo"].unique()
ap_scale_silos = dict(df[["Silo","AP-Scale"]].values)

role = st.selectbox("Select the job role:",role_adjuster["Role"],4)
input_states = st.multiselect("Select the states:",states)
input_silos = st.multiselect("Select the Silos:",silos)
input_budget = []

def calculate_rating(numbers):
    # Calculate the standard deviation
    std_dev = np.std(numbers)
    
    # Calculate the mean of the numbers
    mean = np.mean(numbers)
    
    # Normalize the standard deviation to a scale of 0 to 1
    normalized_std_dev = std_dev / mean if mean != 0 else 0
    
    # Calculate the rating
    rating = 100 * (1 - normalized_std_dev)
    
    # Make sure the rating is within the scale of 1 to 100
    rating = max(min(rating, 100), 1)
    
    return rating

st.text("Enter the budget for each of the media silos:")
# Calculate the number of rows
num_rows = len(input_silos) // 3
if len(input_silos) % 3 != 0:
    num_rows += 1

# For each row
for i in range(num_rows):
    # Create 9 columns: 3 for options, 3 for dollar signs, and 3 for inputs
    cols = st.columns([0.7, 0.1, 0.9] * 3)  # Repeat the pattern for 3 sets of columns
    
    # For each set of option, dollar sign, and input
    for j in range(3):
        # Calculate the index for the silo
        index = i * 3 + j
        
        # If the index is out of range, break the loop
        if index >= len(input_silos):
            break
        
        # Get the option
        option = input_silos[index]
        
        # Calculate the index for the columns
        col_option = cols[j*3]
        col_dollar = cols[j*3 + 1]
        col_input = cols[j*3 + 2]
        
        # Display the option
        col_option.markdown(f"<div style='text-align: center; color: white; padding-top: 32px; font-size:18px;'>{option}</div>", unsafe_allow_html=True)
        
        # Display the dollar sign
        col_dollar.markdown(f"<div style='text-align: right; color: white; padding-top: 30px; font-size: 20px;'>$</div>", unsafe_allow_html=True)
        
        # Create the text input slot
        text_input_slot = col_input.empty()
        user_input = text_input_slot.text_input('', '', key=f'input_{index}')
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
        leads.append(round(budget/average_CPL,1)) 
    AP_scales = [ap_scale_silos[silo]*lead for silo,lead in zip(input_silos,leads)]
    average_AP_scales = round(sum(AP_scales)/sum(leads),1)

    result = pd.DataFrame({"Silo":input_silos,"Budget":input_budget,"Average CPL":average_CPLs,"Leads":leads})
    result["Budget"] = result["Budget"].apply(lambda a: "$ " + '{:.2f}'.format(a))
    result["Average CPL"] = result["Average CPL"].apply(lambda a: "$ " + '{:.2f}'.format(a))
    result.index = np.arange(1,len(result)+1)
    # st.dataframe(result)
    # Convert the DataFrame to HTML and align all columns to the right
    df_html = result.to_html(classes='table table-striped')
    df_html = df_html.replace('<table ','<table style="text-align:right; margin-bottom:40px; margin-top:50px;" ')

    col_df,col_gauge = st.columns([1.5,1])

    with col_df:
        # Display the DataFrame
        st.markdown(df_html, unsafe_allow_html=True)
        # st.write("AP Scale: "+str(average_AP_scales))
        # st.write("Total Budget: $"+str(sum(input_budget)))
        # st.write("Target Leads: "+str(round(sum(leads))*2))
        # st.write("Min Leads: "+str(round(sum(leads))))
    
        adjuster = role_adjuster[role_adjuster["Role"]==role]["Adjuster"].values[0]
        # Create formatted strings
        st.write(f"""
        Prediction Outcome
        <pre>
        <table style="border: none;">
        <tr><td style="text-align: left; border: none;">AP Scale:</td><td style="text-align: right; border: none;">{int(average_AP_scales*10)}</td></tr>
        <tr><td style="text-align: left; border: none;">Balance:</td><td style="text-align: right; border: none;">{int(calculate_rating(np.log([10000 if i>10000 else i for i in input_budget if i>50])))}</td></tr>
        <tr><td style="text-align: left; border: none;">Total Budget:</td><td style="text-align: right; border: none;">${str(int(sum(input_budget)))}</td></tr>
        <tr><td style="text-align: left; border: none;">Target Leads:</td><td style="text-align: right; border: none;">{round(sum(leads)*adjuster)*2}</td></tr>
        <tr><td style="text-align: left; border: none;">Min Leads:</td><td style="text-align: right; border: none;">{round(sum(leads)*adjuster)}</td></tr>
        </table>
        </pre>
        """, unsafe_allow_html=True)

        with col_gauge:
            # Define your values
            current_price = int(average_AP_scales*10)
            ask_price = 100
            bid_price = 0
            spread = 10
        
            # Create the gauge chart
            fig = go.Figure()        
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    title={'text': "AP Scale"},
                    delta={'reference': ask_price, 'relative': False, 'increasing': {'color': "RebeccaPurple"}, 'decreasing': {'color': "#002b36"}},
                    value=current_price,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'shape': 'angular',
                        'axis': {'range': [bid_price - spread, ask_price + spread]},
                        'bar': {'color': "black", 'thickness': 0.2},
                        'bgcolor': 'black',
                        'borderwidth': 2,
                        'bordercolor': 'black',
                        'steps': [
                            {'range': [80, 100], 'color': 'green'},
                            {'range': [50, 80], 'color': '#30F54B'},
                            {'range': [40, 50], 'color': 'yellow'},
                            {'range': [30, 40], 'color': 'orange'},
                            {'range': [0, 30], 'color': 'red'}
                        ],
                        'threshold': {
                            'line': {'color': 'blue', 'width': 6},
                            'thickness': 0.75,
                            'value': current_price,
                        }
                    }
                )
            )
        
            # Display the chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)

            # Create the gauge chart
            fig2 = go.Figure()        
            fig2.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    title={'text': "Balance"},
                    delta={'reference': ask_price, 'relative': False, 'increasing': {'color': "RebeccaPurple"}, 'decreasing': {'color': "#002b36"}},
                    value=current_price,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'shape': 'angular',
                        'axis': {'range': [bid_price - spread, ask_price + spread]},
                        'bar': {'color': "black", 'thickness': 0.2},
                        'bgcolor': 'black',
                        'borderwidth': 2,
                        'bordercolor': 'black',
                        'steps': [
                            {'range': [80, 100], 'color': 'green'},
                            {'range': [75, 80], 'color': '#30F54B'},
                            {'range': [70, 75], 'color': 'yellow'},
                            {'range': [60, 70], 'color': 'orange'},
                            {'range': [50, 60], 'color': 'red'}
                        ],
                        'threshold': {
                            'line': {'color': 'blue', 'width': 6},
                            'thickness': 0.75,
                            'value': current_price,
                        }
                    }
                )
            )
        
            # Display the chart in Streamlit
            st.plotly_chart(fig2, use_container_width=True)

    























