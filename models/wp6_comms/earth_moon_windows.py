"""Integration window models for WP6B."""

from __future__ import annotations

import numpy as np
from astropy.coordinates import EarthLocation, SkyCoord, AltAz, get_sun, solar_system_ephemeris
from astropy.time import Time
from astropy.utils import iers
import astropy.units as u

iers.conf.auto_download = False


def coherent_integration_time(
    site: str,
    beta: float,
    flyby_date: str,
    target_ra_dec: tuple[float, float],
    duration_days: int,
    min_elevation_deg: float = 20.0,
) -> dict:
    """Return daily integration windows (seconds) over the flyby duration."""

    site = site.lower()
    if site not in {"earth", "moon"}:
        raise ValueError("site must be 'earth' or 'moon'")

    location = EarthLocation(lat=0.0 * u.deg, lon=0.0 * u.deg, height=0.0 * u.m)

    start = Time(flyby_date)
    step = 10 * u.minute
    n_steps = int((duration_days * 24 * u.hour / step).decompose())
    times = start + np.arange(n_steps) * step

    target = SkyCoord(ra=target_ra_dec[0] * u.deg, dec=target_ra_dec[1] * u.deg)
    solar_system_ephemeris.set("builtin")
    if site == "moon":
        frame0 = AltAz(obstime=start, location=location)
        alt = target.transform_to(frame0).alt
        visible = np.ones_like(times.value, dtype=bool) & (alt >= min_elevation_deg * u.deg)
    else:
        frame = AltAz(obstime=times, location=location)
        alt = target.transform_to(frame).alt
        visible = alt >= min_elevation_deg * u.deg
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
            int_sec *= 0.9
        days.append(day_start.iso.split()[0])
        integration_seconds.append(int_sec)

    duty = [sec / 86400.0 for sec in integration_seconds]

    return {
        "days": days,
        "integration_seconds": integration_seconds,
        "duty_cycle": duty,
    }
