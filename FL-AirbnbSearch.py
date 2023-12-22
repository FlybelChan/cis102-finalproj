######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import numpy as np
import folium
from streamlit_folium import folium_static
######################
# Page Title
######################

st.title("Welcome to FL-Airbnb Search App")
st.markdown("Here to help you search for most loved homes on Airbnb!!")

# PIL.Image
image_logo = "airbnb_logo_detail.jpg"
st.image(image_logo, caption='image_logo', use_column_width=True)

st.header("Ready to find your suitable place?")

# PIL.Image
image_webshot = "airbnb_webshot.png"
st.image(image_webshot, caption='image_webshot', use_column_width=True)

@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.header('AirBnB Data NYC (2019-09-12)')
st.dataframe(df.head(10))

st.subheader("Choose your NYC boroughs, neighbourhoods, and price range:")

boroughs=df['neighbourhood_group'].unique()
st_boroughs=st.multiselect("Select Boroughs",df['neighbourhood_group'].unique(), default=boroughs)

filtered_df = df.loc[df['neighbourhood_group'].isin(st_boroughs)]

st_neighbourhood = st.multiselect("Select neighbourhoods", filtered_df['neighbourhood'].unique(), default=filtered_df['neighbourhood'].unique())
filtered_df2 = filtered_df.loc[filtered_df['neighbourhood'].isin(st_neighbourhood)]

cols=["name", "host_name", "room_type", "price"]
st_ms = st.multiselect("Columns to show:", filtered_df2.columns.tolist(), default=cols)

st.dataframe(filtered_df2[st_ms].head(20)) #can treat [st_ms] as a list and the inside as columns

st.write("---")

# Display the filtered DataFrame
#st.dataframe(filtered_df)
choose_price = st.slider('Your price range:', float(df.price.min()), 1000., (50., 300.))
filtered_df3 = filtered_df2[(filtered_df2["price"] >= choose_price[0]) & (filtered_df2["price"] <= choose_price[1])]

cols=["name", "host_name", "room_type", "price"]
st_ms = st.multiselect("Columns to show:", filtered_df3.columns.tolist(), default=cols, key = 1)

st.dataframe(filtered_df3[st_ms].head(20))

num_rows = filtered_df3.shape[0]
st.write(f'Total {num_rows} housing rental are found in {",".join(st_boroughs)} with price between {choose_price[0]} and {choose_price[1]}')

st.write("---")

st.header("Here are the location(s) of the your preferred housing rentals:")


# Get "latitude", "longitude", "price" 
listings = filtered_df3.query("(price>=@choose_price[0]) & (price<= @choose_price[1])")[["name", "latitude", "longitude", "neighbourhood","host_name","room_type","price"]]

#listings = listings.head(50)
pref_list = listings.values[0,:]
#pref_list_50 = pref_list[:50]
#pref_list = listings.head(50).values
#pref_list = listings.values[0:50,:]
m = folium.Map(location=pref_list[1:3], zoom_start=16)

tooltip = "listings"
for j in range(len(listings)):
    name, lat, lon, nbh, hostn, rmtype, price = listings.values[j,:]
    folium.Marker(
            (lat,lon), popup=f"Name:{name}\nNeighbourhood:{nbh}\nHost name:{hostn}\nRoom type:{rmtype}" , tooltip=f"Price:${price}"
        ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)


st.write("---")
