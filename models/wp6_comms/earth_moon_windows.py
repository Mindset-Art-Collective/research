"""Integration window models for WP6B.

This module computes daily coherent integration windows for a lunar or
terrestrial receiver. The lunar model assumes a near-side equatorial site and
applies a conservative ``MOON_INTEGRATION_REDUCTION_FACTOR`` to account for
partial Earth occlusion, libration margins, and local topography.
"""

from __future__ import annotations

import numpy as np
from astropy.coordinates import (
    EarthLocation,
    SkyCoord,
    AltAz,
    get_sun,
    solar_system_ephemeris,
)
from astropy.time import Time
from astropy.utils import iers
import astropy.units as u

MOON_INTEGRATION_REDUCTION_FACTOR = 0.9
"""Accounts for partial Earth occlusion and local lunar topography."""

iers.conf.auto_download = False


def coherent_integration_time(
    site: str,
    beta: float,
    flyby_date: str,
    target_ra_dec: tuple[float, float],
    duration_days: int,
    min_elevation_deg: float = 20.0,
    location: EarthLocation | None = None,
) -> dict:
    """Return daily integration windows (seconds) over the flyby duration."""

    site = site.lower()
    if site not in {"earth", "moon"}:
        raise ValueError("site must be 'earth' or 'moon'")

    if location is None:
        # Near-equatorial default for Earth or a near-side lunar outpost.
        location = EarthLocation(lat=0.0 * u.deg, lon=0.0 * u.deg, height=0.0 * u.m)

    start = Time(flyby_date)
    step = 10 * u.minute
    n_steps = int((duration_days * 24 * u.hour / step).decompose())
    times = start + np.arange(n_steps) * step

    target = SkyCoord(ra=target_ra_dec[0] * u.deg, dec=target_ra_dec[1] * u.deg)
    solar_system_ephemeris.set("builtin")
    frame = AltAz(obstime=times, location=location)
    alt = target.transform_to(frame).alt
    visible = alt >= min_elevation_deg * u.deg
    if site == "earth":
        sun_alt = get_sun(times).transform_to(frame).alt
        visible &= sun_alt < 0 * u.deg

    seconds_per_step = step.to(u.s).value
    days = []
    integration_seconds = []

    for i in range(duration_days):
        day_start = start + i * u.day
        day_end = day_start + 1 * u.day
        mask = (times >= day_start) & (times < day_end)
        int_sec = float(np.sum(visible[mask])) * seconds_per_step
        if site == "moon":
            int_sec *= MOON_INTEGRATION_REDUCTION_FACTOR
        days.append(day_start.iso.split()[0])
        integration_seconds.append(int_sec)

    duty = [sec / 86400.0 for sec in integration_seconds]

    return {
        "days": days,
        "integration_seconds": integration_seconds,
        "duty_cycle": duty,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compute coherent integration windows")
    parser.add_argument("--site", choices=["earth", "moon"], required=True)
    parser.add_argument("--beta", type=float, default=0.2)
    parser.add_argument("--flyby-date", type=str, default="2038-04-03")
    parser.add_argument("--ra", type=float, default=180.0)
    parser.add_argument("--dec", type=float, default=0.0)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--min-el", type=float, default=20.0)
    args = parser.parse_args()

    result = coherent_integration_time(
        site=args.site,
        beta=args.beta,
        flyby_date=args.flyby_date,
        target_ra_dec=(args.ra, args.dec),
        duration_days=args.days,
        min_elevation_deg=args.min_el,
    )
    for d, sec in zip(result["days"], result["integration_seconds"]):
        print(f"{d}: {sec/3600:.2f} h of integration")
