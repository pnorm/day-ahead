### Pobieranie danych
#### Dane historyczne
```bash
cd src/data
python get_data.py --site='pse'
python get_data.py --site='pse' --feature='PL_GEN_WIATR' --from_date='2020-01-01'
python get_data.py --site='pse' --feature='PL_GEN_MOC_JW_EPS' --from_date='2020-01-01' --to_date='2023-11-27'
python get_data.py --site='tge'
```
