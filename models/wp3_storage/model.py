"""WP3 storage trade models."""

from __future__ import annotations

import pandas as pd


def flywheel_specific_energy_MJ_per_kg(tensile_strength_pa: float, density_kg_m3: float) -> float:
    """Ideal specific energy of a rim flywheel."""
    return 0.5 * tensile_strength_pa / density_kg_m3 / 1e6


def total_mass_for_energy(energy_TJ: float, specific_energy_MJ_per_kg: float, efficiency: float = 0.9) -> float:
    """Return required mass (kg) for a given stored energy."""
    energy_MJ = energy_TJ * 1e3
    return energy_MJ / (specific_energy_MJ_per_kg * efficiency)


def compare_storage_options(energies_TJ: list[float]) -> pd.DataFrame:
    """Return mass/efficiency table for several storage technologies."""
    data = []
    for E in energies_TJ:
        fly_se = flywheel_specific_energy_MJ_per_kg(1e9, 7800)
        data.append({
            "option": "flywheel",
            "energy_TJ": E,
            "efficiency": 0.9,
            "mass_kg": total_mass_for_energy(E, fly_se, 0.9),
        })
        data.append({
            "option": "thermal",
            "energy_TJ": E,
            "efficiency": 0.85,
            "mass_kg": total_mass_for_energy(E, 1.5, 0.85),
        })
        data.append({
            "option": "SMES",
            "energy_TJ": E,
            "efficiency": 0.95,
            "mass_kg": total_mass_for_energy(E, 10.0, 0.95),
        })
    return pd.DataFrame(data)


def plot_storage_tradeoff(save_path: str | None = None) -> None:
    """Generate F2-02 storage trade figure."""
    import matplotlib.pyplot as plt

    energies = [10, 20, 30, 40, 50]
    df = compare_storage_options(energies)

    fig, ax = plt.subplots()
    for opt, grp in df.groupby("option"):
        ax.plot(grp["energy_TJ"], grp["mass_kg"], label=f"{opt} (η={grp['efficiency'].iloc[0]})")
    ax.set_xlabel("Stored energy (TJ)")
    ax.set_ylabel("Mass (kg)")
    ax.set_title("Storage trade")
    ax.grid(True, ls="--", alpha=0.4)
    ax.legend()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

