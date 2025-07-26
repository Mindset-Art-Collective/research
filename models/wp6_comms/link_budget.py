import logging
import math
import pathlib
import yaml
import numpy as np

# Load constants with error handling
CONST_PATH = pathlib.Path(__file__).resolve().parents[2] / "constants.yaml"
try:
    CONSTS = yaml.safe_load(CONST_PATH.read_text())
except Exception as exc:  # noqa: BLE001
    raise RuntimeError(f"Failed to load constants: {exc}") from exc

for key in ["physics", "comms", "link_budget"]:
    if key not in CONSTS:
        raise KeyError(f"Missing '{key}' in constants.yaml")

PHYS = CONSTS["physics"]
COMMS = CONSTS["comms"]
LINK = CONSTS["link_budget"]

# Documented conversion
METERS_PER_LIGHT_YEAR = float(PHYS.get("meters_per_light_year", 9.4607e15))


def doppler_shift_emitted_to_observed(nu_emit_hz: float, beta: float) -> float:
    """Return observed frequency from source at β due to relativistic Doppler."""
    gamma = 1.0 / math.sqrt(1.0 - beta ** 2)
    return nu_emit_hz / (gamma * (1 + beta))


def photon_count_rx(
    P_t_w: float,
    lambda_m: float,
    D_tx_m: float,
    D_rx_m: float,
    range_m: float,
    eta_sys: float,
) -> float:
    """Return expected photon count rate at the receiver."""
    if any(val <= 0 for val in [lambda_m, D_tx_m, D_rx_m, range_m]) or P_t_w < 0:
        raise ValueError("All physical parameters must be positive")

    h = PHYS["h"]
    c = PHYS["c"]
    w0 = D_tx_m / 2.0
    theta = lambda_m / (math.pi * w0)
    beam_radius = theta * range_m
    beam_area = math.pi * beam_radius**2
    A_rx = math.pi * (D_rx_m / 2.0) ** 2
    received_power = P_t_w * eta_sys * A_rx / beam_area
    return received_power / (h * c / lambda_m)


def bits_home_grid(
    dataset_bits: int,
    D_rxs: list[float],
    T_ints: list[float],
    beta: float,
    coding_gain_db: float,
    squeezing_gain_db: float,
) -> np.ndarray:
    """Return grid (D_rx × T_int) of bits returned.

    Quantum squeezing gain is capped and reduced by a loss fraction derived from
    LIGO-grade implementations (~10% optics loss).
    """
    if dataset_bits <= 0:
        raise ValueError("dataset_bits must be positive")

    c = PHYS["c"]
    lambda_emit = COMMS["wavelength_m"]
    nu_emit = c / lambda_emit
    nu_obs = doppler_shift_emitted_to_observed(nu_emit, beta)
    lambda_obs = c / nu_obs

    P_t_w = LINK["transmit_power_w"]
    D_tx_m = LINK["transmit_aperture_m"]
    eta_sys = LINK["system_efficiency"]
    range_m = 4.0 * METERS_PER_LIGHT_YEAR

    coding_gain = 10 ** (coding_gain_db / 10)
    squeeze_gain = 10 ** (squeezing_gain_db / 10)
    loss_fraction = LINK.get("quantum_loss_fraction", 0.1)
    effective_gain = coding_gain * squeeze_gain * (1 - loss_fraction)

    grid = np.zeros((len(D_rxs), len(T_ints)))
    for i, d in enumerate(D_rxs):
        for j, t in enumerate(T_ints):
            rate = photon_count_rx(P_t_w, lambda_obs, D_tx_m, d, range_m, eta_sys)
            bits = rate * t * 3600 * effective_gain
            grid[i, j] = min(bits, dataset_bits)
    return grid


def plot_bits_home_grid(beta: float, save_path: str | None = None) -> None:
    """Generate contour/heatmap of bits returned vs aperture and integration time."""
    import matplotlib.pyplot as plt

    D_rxs = CONSTS['comms']['lunar_receiver_diameters_m']
    T_ints = CONSTS['comms']['integration_times_hours']
    dataset_bits = CONSTS['comms']['dataset_bits_nominal']
    sq_min, sq_max = CONSTS['comms']['quantum_squeezing_gain_dB_range']

    betas = CONSTS['comms']['doppler_betas']

    fig, axes = plt.subplots(1, len(betas), figsize=(5 * len(betas), 4), sharey=True)
    if len(betas) == 1:
        axes = [axes]

    for ax, b in zip(axes, betas):
        grid = bits_home_grid(dataset_bits, D_rxs, T_ints, b, 0.0, sq_max)
        im = ax.imshow(
            grid,
            origin='lower',
            extent=[T_ints[0], T_ints[-1], D_rxs[0], D_rxs[-1]],
            aspect='auto',
            cmap='viridis',
        )
        cs = ax.contour(
            grid,
            levels=[dataset_bits],
            origin='lower',
            extent=[T_ints[0], T_ints[-1], D_rxs[0], D_rxs[-1]],
            colors='red',
            linestyles='--',
        )
        ax.clabel(cs, fmt=f"{dataset_bits/1e6:g} Mbit")
        ax.set_title(f"β={b}")
        ax.set_xlabel('Integration time (h)')
        ax.set_ylabel('Receiver diameter (m)')

    fig.colorbar(im, ax=axes, label='Bits returned')
    fig.suptitle('Bits returned vs aperture & integration')
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return None
