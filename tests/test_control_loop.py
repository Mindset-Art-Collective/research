import numpy as np
from models.wp2_phasing.control_loop import closed_loop_walkoff


def test_bandwidth_reduces_walkoff():
    f = np.linspace(1, 1000, 100)
    psd = np.ones_like(f) * 1e-9
    low_bw = closed_loop_walkoff(
        f, psd, controller_bw_hz=50, accel_time_s=5.0,
        baseline_m=1000.0, distance_m=1e8, r_sail_m=1.0,
        n_runs=10, seed=1
    )
    high_bw = closed_loop_walkoff(
        f, psd, controller_bw_hz=500, accel_time_s=5.0,
        baseline_m=1000.0, distance_m=1e8, r_sail_m=1.0,
        n_runs=10, seed=1
    )
    assert high_bw["five_sigma"] < low_bw["five_sigma"]

