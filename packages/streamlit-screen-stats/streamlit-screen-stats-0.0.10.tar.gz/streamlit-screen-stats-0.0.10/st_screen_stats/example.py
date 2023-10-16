import streamlit as st
from __init__ import ScreenData, StreamlitNativeWidgetScreen
# from st_screen_stats import ScreenData, StreamlitNativeWidgetScreen

st.set_page_config(layout="wide")

st.subheader("Component with constant args")

screenD = ScreenData()
screen_d = screenD.st_screen_data_window_top()

st.write(screen_d)


st.subheader("native widget method")
screenDN = StreamlitNativeWidgetScreen()
screenDN.st_screen_data_window_top()
stats_ = screenDN.get_window_screen_stats(key="get_item")
st.write(stats_)

# st.write(num_clicks["innerWidth"])

# num_clicks_ = screenD.st_screen_data_window_top()
# st.write(num_clicks_)
# st.write(num_clicks_["innerWidth"])


# if "count_" not in st.session_state:
#     st.session_state["count_"] = 0

# st.session_state["count_"] += 1
# st.write(st.session_state["count_"])

# st.write("Hi - jme") 

