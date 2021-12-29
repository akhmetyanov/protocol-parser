import pandas as pd
from upload_access.connection import get_eng

eng = get_eng()

def write_results(df_samples: pd.DataFrame, df_standart: pd.DataFrame, st_receipt: pd.DataFrame):
    df_samples.to_sql("BUFFER_ST_RESULT", eng, if_exists='append', index=None)
    df_standart.to_sql("BUFFER_ST_RESULT_STANDARD", eng, if_exists='append', index=None)
    st_receipt.to_sql("BUFFER_ST_RECEIPT", eng, if_exists='append', index=None)