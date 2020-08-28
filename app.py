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
    <div style="align:centre"><p style="color: red; font-size: 50px"><b>RESTAURANT DATA ANALYSIS</p></div>
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

@st.cache
def map_data():
    metadata=pd.read_csv("http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz",nrows=2000)
    return metadata

def graph():
    df=map_data()
    st.header("Graphical Analysis")
    st.header("")
    st.subheader("The map plots the location from where the your restaurant gets order request, the height represents the frequency of requests")
    midpoint = (np.average(df["Lat"]), np.average(df["Lon"]))
    maptype=st.selectbox('select type of graph layer',["ScatterplotLayer","HexagonLayer"])
    if maptype=="ScatterplotLayer":
        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 10.5,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["Lon", "Lat"],
                    #radius=100,
                    elevation_scale=4,
                    get_fill_color=[255, 0, 0, 100],
                    get_radius=100,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        ))
    else:
        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 10.5,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=df,
                    get_position=["Lon", "Lat"],
                    radius=100,
                    elevation_scale=4,
                    get_fill_color=[255, 0, 0, 100],
                    get_radius=100,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        ))


def data():
    #st.sidebar.header("choose analysis")
    unit=st.sidebar.selectbox("",["Whole unit","Branch wise"])
    if unit=="Whole unit":
        fulldata()
    

def fulldata():
    df=get_data()
    st.header("Data analysis on whole Manufacturing Data")
    st.header("")
    st.subheader("Choose Which Analysis You Want To Make")
    analysis=st.selectbox("",['Veg vs Non-Veg','Cuisine Type Analysis','Payment Mode Analysis','Branch analysis'])
    
    
  
    if analysis=="Branch analysis":
        st.subheader("Payment Mode Analysis")
        branch_plot= df.groupby('Branch')['gross income'].sum()
        if st.button("Plot"):
            st.write(branch_plot.plot(kind='pie'))
            st.pyplot()

    elif analysis=="Payment Mode Analysis":
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
