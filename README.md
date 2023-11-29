#### Pobieranie dnaych historycznych
```bash
cd src/data
python get_data.py --site='pse'
python get_data.py --site='pse' --feature='PL_GEN_WIATR' --from_date='2020-01-01'
python get_data.py --site='pse' --feature='PL_GEN_MOC_JW_EPS' --from_date='2020-01-01' --to_date='2023-11-27'
python get_data.py --site='tge'
```

#### Transformacje
```bash
cd src/data
python transform_data.py --site='external'
python transform_data.py --site='pse'
python transform_data.py --site='pse' --feature='PL_GEN_WIATR'
python transform_data.py --site='pse' --feature='PL_GEN_MOC_JW_EPS'
python transform_data.py --site='tge'
```

#### Łączenie danych
```bash
cd src/data
...
```