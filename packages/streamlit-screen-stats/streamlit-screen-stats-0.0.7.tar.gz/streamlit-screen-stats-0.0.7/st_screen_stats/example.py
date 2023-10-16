import streamlit as st
from __init__ import ScreenData
# from st_screen_stats import st_screen_data


st.subheader("Component with constant args")

screenD = ScreenData()
screen_d = screenD.st_screen_data_window()

st.write(screen_d)
# st.write(num_clicks["innerWidth"])

# num_clicks_ = screenD.st_screen_data_window_top()
# st.write(num_clicks_)
# st.write(num_clicks_["innerWidth"])


# if "count_" not in st.session_state:
#     st.session_state["count_"] = 0

# st.session_state["count_"] += 1
# st.write(st.session_state["count_"])

# st.write("Hi - jme") 

