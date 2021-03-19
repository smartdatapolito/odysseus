import os, sys
import streamlit as st

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(os.path.dirname(currentdir))
p = os.path.join(parentparentdir,'e3f2s')
sys.path.append(p)

from dashboards.sidebar import *
from dashboards.overview.get_plot_data import * 
from dashboards.overview.get_plots_with_menu import *
#from e3f2s.utils.st_html_utils import _max_width_


def load_dashboard():

    # *** LOAD SIDEBAR AND DATA ***
    #TODO
    current_view, city_name, selected_year, selected_month, start_date, stop_date = load_sidebar()
    
    start, stop = load_slider_menu(selected_month, selected_year)
    st.write("Si parte da "+ str(start)+" si arriva a "+str(stop))

    # *** INTRO ***

    st.markdown(
        """
            <style>

            .big-font {
                font-size:80px !important;
            }

            .mid-small-font {
                font-size:40px !important;
            }

            </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="big-font">Città: {}!</p>
        """.format(city_name),
        unsafe_allow_html=True
    )

   
    #bookings_by_hour = get_bookings_count_plot_data(city_name)

    # if bookings_count is not None:

    #     _max_width_()
    #     load_charts_with_menu(bookings_by_hour)


load_dashboard()