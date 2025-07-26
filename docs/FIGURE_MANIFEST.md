| Fig ID | WP   | Title                                                      | Script / Notebook                                              | Inputs            | Acceptance it supports |
| ------ | ---- | ---------------------------------------------------------- | ------------------------------------------------------------- | --------------------------- | ---------------------- |
| F2-01  | WP2  | **Phase error & spot walk-off vs array size**              | `models/wp2_phasing/model.py::plot_phase_error_frontier()`     | D, λ, t_accel, R_sail     | WP2                    |
| F2-01b | WP2  | **Closed-loop walkoff time series**                        | `models/wp2_phasing/control_loop.py::plot_closed_loop_walkoff()` | PSD, controller BW | WP2 |
| F2-02  | WP3  | **Storage mass/η vs energy (flywheel vs thermal vs SMES)** | `models/wp3_storage/model.py::compare_storage_options()`       | energies_TJ, η ranges      | WP3                    |
| F2-03  | WP6  | **Bits home vs aperture & integration (Earth vs Moon)**    | `models/wp6_comms/link_budget.py::plot_bits_home_grid()`       | D_rx, T_int, β, squeezing | WP6                    |
| F2-04  | WP6R | **SNR coherent vs incoherent vs array size**               | `models/wp6_receive_array/coherent_sum.py::snr_scaling_plot()` | N_tiles, phase noise       | WP6 (receiver)         |
| F2-05  | WP6B | **Earth vs Moon integration duty cycle**                   | `scripts/make_figs.py::plot_wp6b_integration_window()`         | geometry, dates           | WP6B                   |
