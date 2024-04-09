from sectionproperties.pre.library import circular_section
from sectionproperties.pre import Material, CompoundGeometry
from sectionproperties.analysis import Section
import matplotlib.pyplot as plt
import pandas as pd
import math as m

def create_pile_group(x_coord_acc = [], y_coord_acc = [], no_of_piles = int, pile_dia = int):

    list_of_coord = list(zip(x_coord_acc, y_coord_acc))

    pile_list = []
    for coord in list_of_coord:
        pile = circular_section(d=pile_dia , n=64).align_center((coord))
        pile_list.append(pile)

    pile_group = pile_list[0]
    for pile in pile_list[1:]:
        pile_group +=pile

    geom = pile_group
    geom.create_mesh(mesh_sizes=[2000])
    sec = Section(geometry = geom)
    sec.calculate_geometric_properties()
    return sec, geom


def get_pile_group_properties(sec):

    pile_group_area = sec.get_area()
    pile_group_ixxc ,pile_group_iyyc, pile_group_ixyc = sec.get_ic()
    
    pile_prop_data = [("Area" , pile_group_area), 
                      ("Ixx_c", pile_group_ixxc), 
                      ("Iyy_c", pile_group_iyyc),
                      ("Izz_c", pile_group_ixxc+pile_group_iyyc),
                      ]
    
    return pile_prop_data


def get_pile_group_loads(pile_dia, sec, load_case = {},  list_of_coords = []):

    sec.calculate_geometric_properties()
    stress = sec.calculate_stress(**load_case)
    sig = sec.get_stress_at_points(pts=list_of_coords, **load_case)
    area = (m.pi * pile_dia**2)*0.25

    pile_load_data = []
    for pile_number, stress in enumerate(sig):
        pile_load = (f"P{pile_number+1}" , round(stress[0] * area/1000))
        pile_load_data.append(pile_load)

    return pile_load_data


def get_pile_group_shear_loads(sec, v_x: float, v_y : float, list_of_coords : [], pile_prop_data :[], pile_dia : float, m_zz = float):

    area = (m.pi * pile_dia**2)*0.25
    Izz_c = pile_prop_data[3][1]
    J = Izz_c/area
    no_of_piles = len(list_of_coords)
    x_c, y_c = sec.get_c()
    # Get shear loads per pile##
    shear_load_acc = []
    for pile_number, coord in enumerate(list_of_coords):
        shear_load_pile = (f"P{pile_number+1}", (round((((v_x/no_of_piles)+((m_zz*(coord[0] - x_c)*10**3)/J))**2 + ((v_y/no_of_piles)-((m_zz*(coord[1] - y_c)*10**3)/J))**2)**0.5)))
        shear_load_acc.append(shear_load_pile)
    return shear_load_acc
 
    
