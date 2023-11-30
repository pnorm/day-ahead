Ze względu na niewystarczające dane predykcje są na 3 dni wstecz, tj. 2023-11-30 daje predykcje z 2023-11-27.


```bash
git clone https://github.com/pnorm/day-ahead.git
cd day-ahead
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Pobieranie i przetwarzanie danych.
Aby pobierać i aktualizować automatycznie możemy ustawic cronjob.
```bash
cd src/data
# Pobieranie lub aktualizowanie danych
./etl.sh
```

Uruchamianie api
```bash
cd api
uvicorn main:app --reload
```


Struktura folderów projektu
```
├── api
│   └── utils
├── data
│   ├── external
│   ├── interim
│   │   ├── PL_GEN_MOC_JW_EPS
│   │   ├── PL_GEN_WIATR
│   │   └── TGE
│   ├── processed
│   └── raw
│       ├── PL_GEN_MOC_JW_EPS
│       ├── PL_GEN_WIATR
│       └── TGE
├── notebooks
└── src
    ├── data
    │   ├── logs
    │   ├── tests
    │   └── utils
    ├── features
    ├── models
    └── visualization
```