### Pobieranie danych
#### Dane historyczne
```bash
cd src/data
# Dla argumentów domyślnych tj --site='pse' --feature='PL_GEN_WIATR' --from_date='2020-01-01' --to_date=<DZISIAJ>
python get_data.py historical
# Możemy pominąć argumenty i wtedu zostaje przypisana wartość domyślna --to_date=<DZISIAJ>
python get_data.py historical --site='pse' --feature='PL_GEN_WIATR' --from_date='2020-01-01'
python get_data.py historical --site='pse' --feature='PL_GEN_MOC_JW_EPS' --from_date='2020-01-01' --to_date='2023-11-27'
python get_data.py historical --site='tge'
```

#### Backfills - uzupełnienie brakujących danych
```bash
cd src/data
python get_data.py backfill --site='pse' --feature='PL_GEN_WIATR'
python get_data.py backfill --site='pse' --feature='PL_GEN_MOC_JW_EPS'
python get_data.py backfill --site='tge'
```