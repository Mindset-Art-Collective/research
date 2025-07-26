from pathlib import Path
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from models.wp2_phasing.model import plot_phase_error_frontier
from models.wp2_phasing.control_loop import plot_closed_loop_walkoff
from models.wp3_storage.model import plot_storage_tradeoff
# WP6 communications figure uses squeezing parameters grounded in
# LIGO-grade implementations (~6 dB max, 10% loss)
from models.wp6_comms.link_budget import plot_bits_home_grid
from models.wp6_comms.earth_moon_windows import coherent_integration_time

Path('figures/wp2_phasing').mkdir(parents=True, exist_ok=True)
Path('figures/wp3_storage').mkdir(parents=True, exist_ok=True)
Path('figures/wp6_comms').mkdir(parents=True, exist_ok=True)

plot_phase_error_frontier('figures/wp2_phasing/F2-01_phase_error_frontier.png')
plot_closed_loop_walkoff('figures/wp2_phasing/F2-01b_walkoff_timeseries.png')
plot_storage_tradeoff('figures/wp3_storage/F2-02_storage_trade.png')
plot_bits_home_grid(0.2, 'figures/wp6_comms/F2-03_bits_home.png')


def plot_wp6b_integration_window(
    save_path: str | None = None,
    days: int = 30,
    min_elevation_deg: float = 20.0,
):
    """Generate F2-05 showing Earth vs Moon integration duty cycle."""
    import matplotlib.pyplot as plt

    res_earth = coherent_integration_time(
        site="earth",
        beta=0.2,
        flyby_date="2038-04-03",
        target_ra_dec=(180.0, 0.0),
        duration_days=days,
        min_elevation_deg=min_elevation_deg,
    )
    res_moon = coherent_integration_time(
        site="moon",
        beta=0.2,
        flyby_date="2038-04-03",
        target_ra_dec=(180.0, 0.0),
        duration_days=days,
        min_elevation_deg=min_elevation_deg,
    )

    fig, ax = plt.subplots()
    ax.plot(res_earth["days"], [s / 3600 for s in res_earth["integration_seconds"]], label="Earth")
    ax.plot(res_moon["days"], [s / 3600 for s in res_moon["integration_seconds"]], label="Moon")
    ax.set_ylabel("Integration hours/day")
    ax.set_xlabel("Date (UTC)")
    ax.set_title("Integration duty cycle")
    ax.legend()
    ax.grid(True, ls="--", alpha=0.4)
    fig.autofmt_xdate(rotation=45)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig, ax


plot_wp6b_integration_window('figures/wp6_comms/F2-05_integration_duty_cycle.png')

