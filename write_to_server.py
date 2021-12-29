import pandas as pd
from upload_access.connection import get_eng

eng = get_eng()

def write_results(df_samples: pd.DataFrame, df_standart: pd.DataFrame, st_receipt: pd.DataFrame):
    uploaded: bool = False
    if len(df_samples) > 0:
        uploaded = check(df_samples['DESPATCH_ID'].values.tolist()[0], df_samples['LAB_JOB_NO'].values.tolist()[0])
    elif len(df_standart) > 0:
        uploaded = check(df_standart['DESPATCH_ID'].values.tolist()[0], df_standart['LAB_JOB_NO'].values.tolist()[0])

    if uploaded: return

    # df_samples.to_sql("BUFFER_ST_RESULT", eng, if_exists='append', index=None)
    # df_standart.to_sql("BUFFER_ST_RESULT_STANDARD", eng, if_exists='append', index=None)
    # st_receipt.to_sql("BUFFER_ST_RECEIPT", eng, if_exists='append', index=None)

def check(despatch_id: str, lab_job_no: str):
    sql = f"""
    select * from ST_RESULT
    where DESPATCH_ID = '{despatch_id}'
    and LAB_JOB_NO = '{lab_job_no}'
    """
    df = pd.read_sql(sql, eng)

    return len(df) != 0