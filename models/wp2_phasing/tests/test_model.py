import math, pathlib, sys
sys.path.append(str(pathlib.Path(__file__).parents[3]))
from models.wp2_phasing import model as m

def test_required_path_length():
    # simple sanity: larger baseline → larger δL tolerable
    delta_small = m.required_path_length_stability(1e-6, 1, 1e8, 1e3)
    delta_large = m.required_path_length_stability(1e-6, 1, 1e8, 1e4)
    assert delta_large > delta_small