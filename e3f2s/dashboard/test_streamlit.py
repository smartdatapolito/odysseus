import sys
import os
import streamlit as st
import geopandas as gpd


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentparentdir)


from e3f2s.city_data_manager.city_geo_trips.minneapolis_geo_trips import MinneapolisGeoTrips

st.title("Hello world!")





