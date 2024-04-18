import agile_pile_calculator as ap

def test_get_pile_group_properties():
    testsec, testgeom = ap.create_pile_group([0,5000,5000,0], [0,0,5000,5000], 4, 600)

    assert ap.get_pile_group_properties(testsec) == [("Area" , 1129157.4566), 
                                            ("Ixx_c", 7082599367488.3955), 
                                            ("Iyy_c", 7082599367488.438),
                                            ("Izz_c", 14165198734976.834),
                                            ]
    

def test_get_pile_group_loads():
    testsec, testgeom = ap.create_pile_group([0,5000,5000,0], [0,0,5000,5000], 4, 600)

    testloadcase = {"n": 1000*1000,
                "mxx": 1000*1000000,
                "myy": 1000*1000000,
                #  "mzz": 0.,
                #  "vx": 0.,
                #  "vy": 0.,
                }
    
    assert ap.get_pile_group_loads(600, testsec,testloadcase, [(0,0), (5000,0), (5000,5000), (0,5000)]) == [("P1", 250), ("P2", 51),("P3", 250),("P4",450)]


def test_pile_group_shear_loads():
    testsec, testgeom = ap.create_pile_group([0,5000,5000,0], [0,0,5000,5000], 4, 600)
    pile_prop_data = ap.get_pile_group_properties(testsec)
    testv_x = 1000.
    testv_y = 1000.
    testm_zz = 1000.
    list_of_coords = [(0,0), (5000,0), (5000,5000), (0,5000)]

    assert ap.get_pile_group_shear_loads(testsec, testv_x, testv_y, list_of_coords,pile_prop_data,600, testm_zz) == [("P1", 361), ("P2", 424),("P3", 361),("P4",283)]