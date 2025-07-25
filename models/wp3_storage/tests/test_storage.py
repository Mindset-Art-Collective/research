import pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))
from models.wp3_storage import model as m


def test_flywheel_specific_energy():
    se = m.flywheel_specific_energy_MJ_per_kg(1e9, 7800)
    assert round(se, 2) == round(0.5 * 1e9 / 7800 / 1e6, 2)


def test_storage_acceptance():
    df = m.compare_storage_options([10, 20, 40])
    viable = df[(df["energy_TJ"] >= 30) & (df["efficiency"] >= 0.85) & (df["mass_kg"] < 1e8)]
    assert not viable.empty

