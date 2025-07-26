import yaml
import numpy as np
from models.wp6_comms.link_budget import (
    doppler_shift_emitted_to_observed,
    photon_count_rx,
    bits_home_grid,
)


def load_consts():
    import pathlib

    path = pathlib.Path(__file__).resolve().parents[1] / "constants.yaml"
    return yaml.safe_load(path.read_text())


def test_doppler_redshift():
    nu_emit = 1.0e14
    nu_obs = doppler_shift_emitted_to_observed(nu_emit, 0.2)
    assert nu_obs < nu_emit


def test_photon_count_scaling():
    c = load_consts()
    lam = c["comms"]["wavelength_m"]
    D_tx = c["link_budget"]["transmit_aperture_m"]
    p = photon_count_rx(1.0, lam, D_tx, 1.0, 1e6, 1.0)
    p2 = photon_count_rx(1.0, lam, D_tx, 2.0, 1e6, 1.0)
    assert p2 > p


def test_bits_home_with_squeezing():
    c = load_consts()
    dataset_bits = c["comms"]["dataset_bits_nominal"]
    D_rxs = c["comms"]["lunar_receiver_diameters_m"]
    T_ints = c["comms"]["integration_times_hours"]
    sq_gain = c["comms"]["quantum_squeezing_gain_dB_range"][1]
    grid = bits_home_grid(dataset_bits, D_rxs, T_ints, 0.2, 0.0, sq_gain)
    assert np.any(grid >= dataset_bits)


def test_monotonic_bits():
    c = load_consts()
    D_rxs = c["comms"]["lunar_receiver_diameters_m"]
    T_ints = c["comms"]["integration_times_hours"]
    grid = bits_home_grid(int(1e12), D_rxs[:2], [T_ints[0]], 0.2, 0.0, 0.0)
    assert grid[1, 0] > grid[0, 0]
    grid_t = bits_home_grid(int(1e12), [D_rxs[0]], T_ints[:2], 0.2, 0.0, 0.0)
    assert grid_t[0, 1] > grid_t[0, 0]
