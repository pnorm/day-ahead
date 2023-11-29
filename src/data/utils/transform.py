import csv
from datetime import date, datetime, timedelta
from io import StringIO

from bs4 import BeautifulSoup
from loguru import logger
import numpy as np
import pandas as pd


class DataProcessor:
    @staticmethod
    def combine():
        pass


    @staticmethod
    def process_wind(df):
        # Rename columns
        df.rename(columns={
            "Data": "date",
            "Godzina": "hour",
            "Generacja źródeł wiatrowych": "wind",
            "Generacja źródeł fotowoltaicznych": "solar"
        }, inplace=True)

        # Create a copy to avoid SettingWithCopyWarning
        df_copy = df.copy()

        # Convert and clean columns with .loc
        df_copy.loc[:, 'solar'] = df_copy['solar'].astype(str).str.replace(',', '.').replace('-', np.nan).astype(float)
        df_copy.loc[:, 'wind'] = df_copy['wind'].astype(str).str.replace(',', '.').replace('-', np.nan).astype(float)
        df_copy = df_copy[df_copy['hour'] != '2A']

        # Convert 'hour' column to Timedelta
        hour_timedelta = pd.to_timedelta(df_copy['hour'].astype(int), unit='h')

        # Add Timedelta to 'date' column
        df_copy['date'] = pd.to_datetime(df_copy['date'], format='%Y-%m-%d') + hour_timedelta
        df_copy.index = df_copy['date'] - pd.to_timedelta('1H')

        df_copy = df_copy.drop(columns=['date', 'hour'])
        df_copy.fillna(0, inplace=True)

        return df_copy

    @staticmethod
    def safe_float_convert(x):
        x = str(x).replace(',', '.').replace('\xa0', '')
        try:
            return float(x)
        except ValueError:
            return 0.0 

    @staticmethod
    def process_power(df):
        # Drop unnecessary columns
        df.drop(['Data publikacji', 'Tryb pracy', 'Nazwa'], axis=1, inplace=True)
        df["Kod"] = df['Kod'].str[:3]
        df['Doba'] = pd.to_datetime(df['Doba'], format='%Y%m%d')

        # Convert columns 1 to 24 to float after replacing commas
        df.iloc[:, 2:] = df.iloc[:, 2:].map(DataProcessor.safe_float_convert)

        grouped_data = df.groupby(['Doba', 'Kod']).sum().reset_index()
        grouped_data.iloc[:, 2:] = grouped_data.iloc[:, 2:].map(lambda x: round(x, 3) if pd.notna(x) else x)

        # Pivot the DataFrame to get the desired format
        df_pivot = grouped_data.melt(id_vars=['Doba', 'Kod'], var_name='Hour', value_name='Value')
        result = df_pivot.pivot_table(index=['Doba', 'Hour'], columns='Kod', values='Value', aggfunc='first').reset_index()
        result = result[result['Hour'] != '2A']

        result['Hour'] = result['Hour'].astype(int)
        result['Datetime'] = result['Doba'] + pd.to_timedelta(result['Hour'], unit='h')
        result.index = result['Datetime'] - pd.to_timedelta('1H')

        result = result.drop(columns=['Doba', 'Hour', 'Datetime'])
        result = result.sort_index()
        result.fillna(0, inplace=True)
        result.index.name = 'date'
        return result
    
    @staticmethod
    def process_external(df):
        df.index = pd.to_datetime(df.index, format="%d.%m.%Y %H:%M")
        df.drop(columns=['fixing_ii_price', 'fixing_ii_volume'], inplace=True)

        df_copy = df.copy()
        df_copy.rename(columns={f'fixing_i_price': 'OT'}, inplace=True)
        df_copy = df_copy[['fixing_i_volume', 'OT']]

        return df_copy
    
    @staticmethod
    def parse_tge(html_code) -> pd.DataFrame:
        # Parse the HTML code
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find the table
        table = soup.find('table', {'id': 'footable_kontrakty_godzinowe'})

        # Extract data from the table
        data = []
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            data.append(cols)

        # Create a DataFrame from the scraped data
        df = pd.DataFrame(data[2:-3], columns=data[1])

        return df
    
    @staticmethod
    def process_tge(df, current_date):
        df = df.iloc[:, :3]
        df_copy = df.copy()

        df_copy.rename(columns={
            "Czas": "hour", 
            "Kurs (PLN/MWh)": "OT",
            "Wolumen (MWh)": "fixing_i_volume",
        }, inplace=True)

        df_copy['date'] = [datetime.fromisoformat(current_date) + timedelta(hours=i) for i in range(len(df_copy))]
        df_copy.index = df_copy['date']
        df_copy.drop(['hour', 'date'], axis=1, inplace=True)

        df_copy.fillna(0, inplace=True)
        df_copy.loc[:, 'OT'] = df_copy['OT'].astype(str).str.replace(',', '.').replace('-', np.nan).replace('', np.nan).astype(float)
        df_copy.loc[:, 'fixing_i_volume'] = df_copy['fixing_i_volume'].astype(str).str.replace(',', '.').replace('-', np.nan).replace('', np.nan).astype(float)

        df_copy = df_copy[['fixing_i_volume', 'OT']]

        return df_copy

    @staticmethod
    def decode(data):
        if data is not None:
            try:
                decoded_data = data.decode('windows-1250')
                data_io = StringIO(decoded_data)
            except Exception as e:
                logger.debug(f"Problem with decoding data: {e}")
            try:
                csv_reader = csv.reader(data_io, delimiter=';')
                rows = list(csv_reader)
                
                # Check if the row has exactly 30 columns before removing the last element
                rows = [row[:-1] if len(row) == 30 else row for row in rows]
                
                df = pd.DataFrame(rows[1:], columns=rows[0])
                logger.debug(f"Data decoded and transformed to DataFrame. Shape {df.shape}")
                return df
            except csv.Error as e:
                logger.error(f"Error parsing CSV data: {e}")
                return None
        logger.error("DataFrame is empty")
        