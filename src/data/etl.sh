#!/bin/bash

# Activate the virtual environment
source "../../env/bin/activate"

# Pobieranie/Aktualizowanie dnaych historycznych
python get_data.py --site='pse'
python get_data.py --site='pse' --feature='PL_GEN_WIATR' --from_date='2020-01-01'
python get_data.py --site='pse' --feature='PL_GEN_MOC_JW_EPS' --from_date='2020-01-01' --to_date='2023-11-27'
python get_data.py --site='tge'

# Transformacje
python transform_data.py --site='external'
python transform_data.py --site='pse'
python transform_data.py --site='pse' --feature='PL_GEN_WIATR'
python transform_data.py --site='pse' --feature='PL_GEN_MOC_JW_EPS'
python transform_data.py --site='tge'

# Łączenie danych
python combine_data.py --site='pse'
python combine_data.py --site='pse' --feature='PL_GEN_WIATR'
python combine_data.py --site='external'
python combine_data.py --site='tge'

# Outer join
python join_data.py

# Deactivate the virtual environment at the end of the script
deactivate