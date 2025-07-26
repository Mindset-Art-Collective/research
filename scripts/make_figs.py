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

Path('figures/wp2_phasing').mkdir(parents=True, exist_ok=True)
Path('figures/wp3_storage').mkdir(parents=True, exist_ok=True)
Path('figures/wp6_comms').mkdir(parents=True, exist_ok=True)

plot_phase_error_frontier('figures/wp2_phasing/F2-01_phase_error_frontier.png')
plot_closed_loop_walkoff('figures/wp2_phasing/F2-01b_walkoff_timeseries.png')
plot_storage_tradeoff('figures/wp3_storage/F2-02_storage_trade.png')
plot_bits_home_grid(0.2, 'figures/wp6_comms/F2-03_bits_home.png')

