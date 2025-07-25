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
