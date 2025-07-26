import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from models.wp6_comms.earth_moon_windows import coherent_integration_time


def test_integration_output_lengths():
    res = coherent_integration_time(
        site="earth",
        beta=0.2,
        flyby_date="2038-04-03",
        target_ra_dec=(180.0, 0.0),
        duration_days=7,
    )
    assert len(res["days"]) == 7
    assert len(res["integration_seconds"]) == 7
    assert len(res["duty_cycle"]) == 7
    assert all(0 <= s <= 86400 for s in res["integration_seconds"])


def test_earth_vs_moon_contrast():
    earth = coherent_integration_time(
        site="earth",
        beta=0.2,
        flyby_date="2038-04-03",
        target_ra_dec=(180.0, 0.0),
        duration_days=7,
    )
    moon = coherent_integration_time(
        site="moon",
        beta=0.2,
        flyby_date="2038-04-03",
        target_ra_dec=(180.0, 0.0),
        duration_days=7,
    )
    avg_earth = sum(earth["duty_cycle"]) / len(earth["duty_cycle"])
    avg_moon = sum(moon["duty_cycle"]) / len(moon["duty_cycle"])
    assert avg_moon > avg_earth
    assert all(
        abs(d - s / 86400.0) < 1e-6
        for d, s in zip(earth["duty_cycle"], earth["integration_seconds"])
    )
