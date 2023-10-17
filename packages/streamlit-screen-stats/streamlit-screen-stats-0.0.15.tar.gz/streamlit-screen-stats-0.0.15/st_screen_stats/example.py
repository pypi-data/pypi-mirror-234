import streamlit as st
# from __init__ import my_component
# from __init__ import SizeRange #ScreenData, StreamlitNativeWidgetScreen
from st_screen_stats import SizeRange # ScreenData, StreamlitNativeWidgetScreen

st.set_page_config(layout="wide")

# st.subheader("Component with constant args")

# screenD = ScreenData()
# screen_d = screenD.st_screen_data_window_top()

# st.write(screen_d)


# st.subheader("native widget method")
# screenDN = StreamlitNativeWidgetScreen()
# screenDN.st_screen_data_window_top()
# stats_ = screenDN.get_window_screen_stats(key="get_item")
# st.write(stats_)

screenRange = SizeRange()
val_ = screenRange.WidthRange(upperRange=1000)
st.write(val_)

# upperScreenWidth = 1000

# js_el = f'''
#             <script>

            
#                 function test (e) {{
#                     if (window.innerWidth <= {upperScreen} ){{
#                         console.log("present")
#                     }}
#                 }}
                
#                 window.addEventListener("resize", test)
                
#             </script>

#         '''
# # st.components.v1.html(js_el)

# # my_component()


