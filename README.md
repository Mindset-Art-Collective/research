# Lunar Lightsail Modeling Repo

This repository implements reproducible physics models, figures, and tests that underpin **Paper v2**: *A Lunar Laser Architecture for Relativistic Lightsails*.

See `docs/` for the acceptance matrix, figure manifest, and outline.

## Setup

```bash
make install
```

## Running tests

```bash
make test
```

## Generating figures

Figures are **not tracked** in Git. Regenerate them with:

```bash
make figs
```

Generated PNGs will appear under `figures/` and are uploaded by CI as artifacts.

The WP6 communications models incorporate optional quantum squeezing, capped at
6&nbsp;dB with a 10% loss factor, reflecting LIGO-grade performance (see
PhysRevX.13.041021). Figure F2-03 illustrates the bits returned vs aperture and
integration time for various β.
