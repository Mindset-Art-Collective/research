.RECIPEPREFIX := >
.PHONY: install test figs

install:
>pip install -r requirements.txt

test:
>pytest -q

figs:
>python scripts/make_figs.py
