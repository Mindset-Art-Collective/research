"""Closed-loop phasing control simulation for WP2."""

from __future__ import annotations

import numpy as np
from scipy.signal import lfilter


def closed_loop_walkoff(
    psd_f: np.ndarray,
    psd_mag: np.ndarray,
    controller_bw_hz: float,
    accel_time_s: float,
    baseline_m: float,
    distance_m: float,
    r_sail_m: float,
    n_runs: int = 1000,
    seed: int | None = None,
) -> dict:
    """Simulate phase noise rejection by a 1-pole controller.

    Parameters mirror the simple frequency-domain model used in WP2. `psd_f`
    and `psd_mag` describe the path length jitter power spectral density. The
    controller is modeled as a single pole low-pass with 3 dB bandwidth
    ``controller_bw_hz``.  The output dictionary contains the RMS and five sigma
    lateral walk-off (in meters) as well as the simulated walk-off time series
    for all Monte Carlo runs.
    """
    rng = np.random.default_rng(seed)
    max_f = float(np.max(psd_f))
    dt = 1.0 / (2 * max_f)
    n = int(accel_time_s / dt)

    # approximate white noise std from PSD magnitude and bandwidth
    bandwidth = float(np.max(psd_f) - np.min(psd_f))
    # PSD has units m^2/Hz, integrate over equivalent bandwidth for variance
    noise_std = float(np.sqrt(np.mean(psd_mag) * bandwidth))

    alpha = np.exp(-2 * np.pi * controller_bw_hz * dt)

    series = np.empty((n_runs, n))
    for j in range(n_runs):
        noise = rng.normal(scale=noise_std, size=n)
        lowpassed = lfilter([1 - alpha], [1, -alpha], noise)
        residual = noise - lowpassed
        delta_theta = residual / baseline_m
        series[j] = delta_theta * distance_m

    rms = float(np.sqrt(np.mean(series**2)))
    return {
        "rms": rms,
        "five_sigma": 5 * rms,
        "walkoff_time_series": series,
    }


def plot_closed_loop_walkoff(save_path: str | None = None) -> None:
    """Generate an example closed-loop walk-off time series."""
    f = np.linspace(1, 1000, 100)
    psd = np.ones_like(f) * 1e-9
    out = closed_loop_walkoff(
        f,
        psd,
        controller_bw_hz=200,
        accel_time_s=10.0,
        baseline_m=10e3,
        distance_m=1e8,
        r_sail_m=1.0,
        n_runs=1,
        seed=42,
    )
    t = np.arange(out["walkoff_time_series"].shape[1]) * (1 / (2 * f.max()))
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(t, out["walkoff_time_series"][0])
    plt.xlabel("Time (s)")
    plt.ylabel("Spot walk-off (m)")
    plt.title("Example closed-loop walk-off")
    plt.grid(True, ls="--", alpha=0.4)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

