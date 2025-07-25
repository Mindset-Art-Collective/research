"""WP2 – Phasing & pointing control models."""

import yaml, math, pathlib
import numpy as np
import matplotlib.pyplot as plt

# Load constants.yaml from repo root (2 levels up: wp2_phasing → models → repo root)
CONST_PATH = pathlib.Path(__file__).resolve().parents[2] / 'constants.yaml'
CONSTS = yaml.safe_load(CONST_PATH.read_text())

def required_path_length_stability(lambda_m: float,
                                   R_sail_m: float,
                                   distance_m: float,
                                   baseline_m: float) -> float:
    """Return required RMS path‑length stability (meters).

    Derivation:
        angular error δθ ≈ δL / baseline
        spot displacement δx = δθ * distance
        Requirement: δx ≤ 0.5 R_sail
        ⇒ δL ≤ 0.5 R_sail * baseline / distance
    """
    return 0.5 * R_sail_m * baseline_m / distance_m

def plot_phase_error_frontier(save_path=None):
    c = CONSTS
    distance_m = 1e8  # 0.1 million km
    R_sail = c['mission']['sail_radii_m'][0]  # use smallest
    lambda_m = c['mission']['wavelengths_nm'][0] * 1e-9

    baselines_km = c['mission']['array_diameters_km']
    baselines_m = np.array(baselines_km) * 1e3

    req_pm = np.array([required_path_length_stability(lambda_m, R_sail, distance_m, b)*1e12
                       for b in baselines_m])

    fig, ax = plt.subplots()
    ax.plot(baselines_km, req_pm, marker='o')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Array diameter (km)')
    ax.set_ylabel('Required RMS path stability (pm)')
    ax.set_title('Phase error frontier (1 m sail, 0.1 Mkm)')
    ax.grid(True, which='both', ls='--', alpha=0.4)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax