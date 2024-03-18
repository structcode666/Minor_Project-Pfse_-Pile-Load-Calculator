import streamlit as st
from sectionproperties.pre.library import circular_section
from sectionproperties.analysis import Section
from sectionproperties.pre import Material, CompoundGeometry
import matplotlib.pyplot as plt
import pandas as pd
import agile_pile_calculator as ap


##Pile Calcualtor Layout##
st.set_page_config(page_title="Agile Pile", layout="wide")

st.header("PILE LOAD CALCULATOR")
st.write("This application helps visualize the locations of piles under a raft and calculate the loads")

with st.sidebar:
    st.header("PILE INFORMATION")
    no_of_piles = st.text_input("Number of piles under the raft", " ")
    pile_dia = st.number_input("Pile Diameter", min_value=0)
st.subheader("Pile Coordinates")

with st.sidebar:
    st.header("LOAD INFORMATION")
    axial_load = st.text_input("Axial Load (N)", " ")
    m_xx = st.text_input("Mxx (N.m)", " ")
    m_yy = st.text_input("Myy (N.m)", " ")
    # m_zz = st.text_input("Mzz", " ")
    # v_x = st.text_input("Vx", " ")
    # v_y = st.text_input("Vy", " ")

## Set up Pile Data Table##
pile_data = []
for i in range(0, int(no_of_piles)):
    x = None 
    y = None
    pile_coord = (f"P{i+1}" , x , y)
    pile_data.append(pile_coord)

pile_df = pd.DataFrame(pile_data, columns = ["Pile Number" , "X Coord", "Y Coord"])
final_pile_df = st.data_editor(pile_df,hide_index=True, num_rows="dynamic")

## Plot Pile Layout##
st.subheader("Pile Layout")  
x_coord_acc = []
for x in final_pile_df["X Coord"]:
    x_coord_acc.append(int(x))
y_coord_acc = []
for y in final_pile_df["Y Coord"]:
    y_coord_acc.append(int(y))

sec, geom = ap.create_pile_group(x_coord_acc, y_coord_acc, int(no_of_piles), int(pile_dia))

ax = geom.plot_geometry(
    labels=[],
    nrows=1,
    ncols=1,
    figsize=(10, 5),
    render=False,
)

##get the figure object from the first plot##
fig = ax.get_figure()

# plot the centroids
sec.plot_centroids(ax=fig.axes[0])
st.pyplot(fig)

##Show pile group properties as a table##
st.subheader("Pile Group Properties")
pile_prop_data = ap.get_pile_group_properties(sec)
pile_prop_df = pd.DataFrame(pile_prop_data, columns = ["Pile Group Property" , "Value"])
pile_prop_table = st.data_editor(pile_prop_df,hide_index=True, num_rows="static")

##Get Pile Group Loads##

st.subheader("Pile Loads")

load_case = {"n": int(axial_load),
             "mxx": int(m_xx),
             "myy": int(m_yy),
             "mzz": 0.,
             "vx": 0.,
             "vy": 0.,
             }

pile_load_data = ap.get_pile_group_loads(int(pile_dia), sec, load_case, list(zip(x_coord_acc, y_coord_acc)))

pile_load_df = pd.DataFrame(pile_load_data, columns = ["Pile Vert Reactions" , "Value"])

final_pile_load_df = st.data_editor(pile_load_df, hide_index=True, num_rows="dynamic")



             
        








   






