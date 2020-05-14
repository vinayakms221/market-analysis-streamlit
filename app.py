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
    html_temp="""
    <div style="align:centre"><p style="color: red; font-size: 50px"><b>MARKET DATA ANALYSIS</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
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
    df=get_data()
    st.header("Data analysis on whole Manufacturing Data")
    st.header("")
    st.subheader("Choose Which Analysis You Want To Make")
    analysis=st.selectbox("",['Categorical Analysis','Product Type Analysis','Payment Mode Analysis','Branch analysis'])
    
    if analysis=="Categorical Analysis":
        st.subheader("Categorical Analysis")
        primary_col = st.selectbox("Primary Columm to GroupBy",['Product line','Payment'])
        selected_columns_names = st.multiselect("Select Columns",['gross income','Quantity'])
        if st.button("Plot"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].sum()
            else:
                vc_plot = df.iloc[:,-1].value_counts()
            st.write(vc_plot.plot(kind='bar'))
            st.pyplot()

    elif analysis=="Product Type Analysis":
        ptype=st.multiselect("Select Product Type",['Electronic accessories','Fashion accessories','Food and beverages','Health and beauty','Home and lifestyle','Sports and travel'])
        l= len(ptype)
        f=df['Invoice ID'].copy()
        if l!=0:
            #dd=dd.drop("Invoice ID",axis=1)
            for i in range(l):
                d=df[df['Product line'] ==ptype[i]]
                dd=pd.concat([f,d],axis=0)
                f=dd.copy()
            abc=dd.groupby('Product line')['gross income'].sum()
            if st.button("Plot"):
                st.write(abc.plot(kind='pie'))
                st.pyplot()
        else:
            html_temp="""<div style="align:centre"><p style="color: red; font-size: 20px">*select any from above</p></div>"""
            st.markdown(html_temp,unsafe_allow_html=True)
    
    elif analysis=="Branch analysis":
        st.subheader("Payment Mode Analysis")
        branch_plot= df.groupby('Branch')['gross income'].sum()
        if st.button("Plot"):
            st.write(branch_plot.plot(kind='pie'))
            st.pyplot()

    else:
        st.subheader("Payment Mode Analysis")
        cust_plot= df['Payment'].value_counts().plot(kind='pie')
        if st.button("Plot"):
            st.write(cust_plot)
            st.pyplot()



def branch():
    #st.sidebar.header("choose branch")
    unit=st.sidebar.selectbox("choose branch",["Branch A","Branch B","Branch C"])
    if unit=="Branch A":
        df=dataA()
    elif unit=="Branch B":
        df=dataB()
    else:
        df=dataC()
    st.header("Data analysis-Branchwise")
    st.header("")
    st.subheader("Choose Which Analysis You Want To Make")
    analysis=st.selectbox("",['Categorical Analysis','Product Type Analysis','Payment Mode Analysis'])

    if analysis=="Categorical Analysis":
        st.subheader("Categorical Analysis")
        primary_col = st.selectbox("Primary Columm to GroupBy",['Product line','Payment'])
        selected_columns_names = st.multiselect("Select Columns",['gross income','Quantity'])
        if st.button("Plot"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].sum()
            else:
                vc_plot = df.iloc[:,-1].value_counts()
            st.write(vc_plot.plot(kind='bar'))
            st.pyplot()

    elif analysis=="Product Type Analysis":
        ptype=st.multiselect("Select Product Type",['Electronic accessories','Fashion accessories','Food and beverages','Health and beauty','Home and lifestyle','Sports and travel'])
        l= len(ptype)
        f=df['Invoice ID'].copy()
        if l!=0:
            #dd=dd.drop("Invoice ID",axis=1)
            for i in range(l):
                d=df[df['Product line'] ==ptype[i]]
                dd=pd.concat([f,d],axis=0)
                f=dd.copy()
            abc=dd.groupby('Product line')['gross income'].sum()
            if st.button("Plot"):
                st.write(abc.plot(kind='pie'))
                st.pyplot()
        else:
            html_temp="""<div style="align:centre"><p style="color: red; font-size: 20px">*select any from above</p></div>"""
            st.markdown(html_temp,unsafe_allow_html=True)


    else:
        st.subheader("Payment Mode Analysis")
        cust_plot= df['Payment'].value_counts().plot(kind='pie')
        if st.button("Plot"):
            st.write(cust_plot)
            st.pyplot()

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
