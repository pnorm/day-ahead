import pandas as pd


def join():
    df1 = pd.read_csv("../../data/processed/pl_gen_moc_jw_eps.csv", index_col='date')
    df2 = pd.read_csv("../../data/processed/pl_gen_wiatr.csv", index_col='date')
    df3 = pd.read_csv("../../data/processed/fixing.csv", index_col='date')

    result_outer = pd.merge(df1, df2, on='date', how='outer')
    final_outer = pd.merge(result_outer, df3, on='date', how='outer')
    final_outer.sort_index(inplace=True)

    final_df = final_outer[final_outer.index >= '2020-04-20'].copy()
    final_df.fillna(0.0, inplace=True)
    
    final_df.to_csv("../../data/processed/electricity.csv")


if __name__ == "__main__":
    join()