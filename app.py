import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import altair as alt
import pydeck as pdk
import seaborn as sns


DATE_TIME = "date/time"
DATA_URL = ("https://github.com/vinayakms221/market-analysis-streamlit/blob/master/supermarket_sales%20-%20Sheet1.csv"
)

def main():
    st.title("MARKET DATA ANALYSIS")
    st.sidebar.title("Analysis type")
    app_mode = st.sidebar.selectbox("Choose the analysis type",["Data Analysis", "Geographical Analysis"])
    if app_mode=="Data Analysis":
        data()
    else:
        graph()

@st.cache
def get_data():
    metadata=pd.read_csv("./datasets/supermarket_sales.csv")
    return metadata

def data():
    #st.sidebar.header("choose analysis")
    unit=st.sidebar.selectbox("",["Whole unit","Branch wise"])
    if unit=="Whole unit":
        fulldata()
    else:
        branch()

def fulldata():
    st.subheader("Data analysis on whole Manufacturing Data")
    html_temp="""
    <div style="background-color:tomato; border-radius:1em"><p style="color: white; font-size: 50px">Streamlit is awesome</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

def branch():
    #st.sidebar.header("choose branch")
    unit=st.sidebar.selectbox("choose branch",["Branch A","Branch B","Branch C"])
    if unit=="Branch A":
        df=dataA()
    elif unit=="Branch B":
        df=dataB()
    else:
        df=dataC()
    
    primary_col = st.selectbox("Primary Columm to GroupBy",['Product line'])
    selected_columns_names = st.multiselect("Select Columns",['gross income','Quantity'])
    if st.button("Plot"):
        st.text("Generate Plot")
        if selected_columns_names:
            vc_plot = df.groupby(primary_col)[selected_columns_names].sum()
        else:
            vc_plot = df.iloc[:,-1].value_counts()
        st.write(vc_plot.plot(kind='bar'))
        st.pyplot()
    #cust_plot= df['Payment'].value_counts().plot(kind='bar')
    #st.write(cust_plot)
    #st.pyplot()
    
    #cust_plot= df.groupby('Product line')['gross income'].sum()
    #st.write(cust_plot.plot(kind='pie'))
    #st.pyplot()

@st.cache
def dataA():
    data=get_data()
    metadata=data[data['Branch']=="A"]
    return metadata
@st.cache
def dataB():
    data=get_data()
    metadata=data[data['Branch']=="B"]
    return metadata
@st.cache
def dataC():
    data=get_data()
    metadata=data[data['Branch']=="C"]
    return metadata


    

if __name__=='__main__':
    main()
