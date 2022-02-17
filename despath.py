import pandas as pd
from upload_access.connection import get_eng

eng = get_eng()

def find_despatch(despatch_id:str):
    # первый раз ищем по оригинальному номеру из протокола
    df_sample, df_standart = _find(despatch_id)

    # если по оригинальному ничего не нашли, то заменяем пробелы на тире и снова повторяем. 
    # иногда, по цианированию они могут доавить лишний 0 - тоже момент за которым надо следить
    if len(df_sample) == 0 and len(df_standart) == 0:
        despatch_id = despatch_id.replace(' ', '-')
        df_sample, df_standart = _find(despatch_id)
    else:
        return df_sample, df_standart, despatch_id

    if len(df_sample) != 0 or len(df_standart) != 0:
        return df_sample, df_standart, despatch_id

    return None, None, None

def _find(despatch_id:str):
    if despatch_id is None: raise Exception("despatch_id is None")
    sql_sample = f"""
    select * from ST_DESPATCH_SAMPLE
    where DESPATCH_ID like '%{despatch_id.strip()}%'
    """
    df_sample = pd.read_sql(sql_sample, eng)

    sql_standart = f"""
    select * from ST_DESPATCH_STANDARD
    where DESPATCH_ID like '%{despatch_id.strip()}%'
    """

    df_standart = pd.read_sql(sql_standart, eng)
    return df_sample, df_standart
