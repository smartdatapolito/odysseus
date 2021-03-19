import pandas as pd
import streamlit as st

import os, sys
import streamlit as st
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.append(parentparentdir)

from e3f2s.dashboards.load_data import *
from e3f2s.dashboards.overview.get_widgets import *



from e3f2s.city_data_manager.data_transormer_cdm import *

@st.cache(allow_output_mutation=True)
def load_bookings_by_hour(citta,sorgente,anno,mese):
    # get inputs from streamlit for city, data_source, year, month
    st.write(citta,sorgente,anno,mese)
    gigi = Loader(city=citta, source=sorgente, year=anno, month=mese)
    bookings_df =  gigi.read_data()
    df_busy = df.filter(["start_hour"], axis=1)
    df_busy["occurance"] = 1
    most_busy_hour = df_busy.groupby(by="start_hour").sum(["occurance"]).sort_values(by=["occurance"], ascending=[True])
    most_busy_hour = most_busy_hour.reset_index()

    return most_busy_hour


# @st.cache(allow_output_mutation=True)
# def load_deleted_bookings_by_hour(club_id, start, end):
#     conn = connect()
#     # execute_sql_scripts("db_management/sql_scripts/stored_function", conn)

#     bookings_deleted_by_hour = pd.read_sql(
#         """
#             select * from booking_deleted_per_hour(
#                 {}, {}, {}
#             )
#         """.format(
#             "'" + club_id + "'",
#             "'" + str(start) + "'",
#             "'" + str(end) + "'"
#         ),
#         conn
#     )
#     bookings_deleted_by_hour["datetime"] = pd.to_datetime(bookings_deleted_by_hour["date_hour"], utc=True)
#     bookings_deleted_by_hour["bookings_count"] = bookings_deleted_by_hour.bookings_count.astype(float)

#     bookings_deleted_by_hour["age_unknown"] = bookings_deleted_by_hour.bookings_count - bookings_deleted_by_hour[age_bin_cols].sum(
#         axis=1
#     ).values
#     bookings_deleted_by_hour["sex_unknown"] = bookings_deleted_by_hour.bookings_count - bookings_deleted_by_hour[["male", "female"]].sum(
#         axis=1
#     ).values

#     return bookings_deleted_by_hour


# @st.cache(allow_output_mutation=True)
# def load_club_name():
#     conn = connect()
#     # execute_sql_scripts("db_management/sql_scripts/stored_function", conn)

#     club_names = pd.read_sql(
#         """
#             select club_name,club_id,club_city,club_email from clubs_with_data()
#             where has_booking = true
#         """,
#         conn
#     )

#     return club_names


# @st.cache(allow_output_mutation=True)
# def load_club_by_id(club_id):
#     conn = connect()
#     # execute_sql_scripts("db_management/sql_scripts/stored_function", conn)

#     club = pd.read_sql(
#         """
#             select * from clubs
#             where clubs.club_id = {}
#         """.format(
#             "'" + club_id + "'",
#         ),
#         conn
#     )

#     return club


# @st.cache(allow_output_mutation=True)
# def load_club_by_name(club_name):
#     conn = connect()
#     # execute_sql_scripts("db_management/sql_scripts/stored_function", conn)

#     club = pd.read_sql(
#         """
#             select * from clubs
#             where clubs.club_name = {}
#         """.format(
#             "'" + club_name + "'",
#         ),
#         conn
#     )

#     return club
