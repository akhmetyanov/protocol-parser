import re
import pandas as pd

from upload_access.connection import get_eng

def create_despath(project: str, despath_id: str, despath_date, prot_num:str, lab_id: str, samples: list):
    eng = get_eng()
    __create_destah(project, despath_id, despath_date, eng, lab_id, prot_num)
    __create_sample(project, despath_id, samples, eng)
    __create_standart(project, despath_id, samples, eng)

def __create_destah(project: str, despath_id: str, despath_date, eng, lab_id: str, prot_num:str):
    df = pd.DataFrame([{
        'DESPATCH_ID': str(despath_id),
        'DESCRIPTION': 'buffer_uf',
        'LAB_ID': lab_id,
        'MULTI_LAB': 0,
        'STATUS': 'NEW',
        'SEND_DATE': despath_date,
        'REMARKS': f'Добавлено 2020-06-02 17:04:17 из протокола {prot_num}',
        'PROJECT': project
    }])
    __write(df, eng, 'ST_DESPATCH')

def __create_sample(project: str, despath_id: str, samples: list, eng):
    s_samples = "','".join([s for s in samples])
    samples = pd.read_sql(f"""
    --sql
    select 
        SAMPLE_ID AS SAMPLE_TAG
        ,PROJECT
        ,SITE_ID
        , SAMPLE_ID
        , 'X' AS FRACTION
        , QC_TYPE
        , 'k' as QC_SOURCE
    from GB_SAMPLE_CHECK
    where PROJECT = '{project}' and SAMPLE_ID in
    (
        '{s_samples}'
    )

    union

    select 
        SAMPLE_ID AS SAMPLE_TAG
        ,PROJECT
        ,SITE_ID
        , SAMPLE_ID
        , 'X' AS FRACTION
        , QC_TYPE
        , 'k' as QC_SOURCE
    from GB_SAMPLE
    where PROJECT = '{project}' and SAMPLE_ID in
    (
        '{s_samples}'
    )
    ;
    """, eng)

    if len(samples) == 0:
        print("Пробы не найдены")
        return

    samples['DESPATCH_ID'] = [despath_id] * len(samples)
    __write(samples, eng, 'ST_DESPATCH_SAMPLE')


def __create_standart(project: str, despath_id: str, samples: list, eng):
    s_samples = "','".join([s for s in samples])

    samples = pd.read_sql(f"""
    --sql
    select 
        SAMPLE_ID AS SAMPLE_TAG
        , NULL as STANDARD_ID
        , QC_TYPE
        , CASE QC_TYPE 
            WHEN 'F_BLANK' THEN 'k'
            WHEN 'STANDARD' THEN 'F'
            WHEN 'BLANK' THEN 'B'
        END AS QC_SOURCE
        , SAMPLE_ID
        ,PROJECT
        ,SITE_ID
        from GB_SAMPLE_QAQC
    where PROJECT = '{project}' and SAMPLE_ID in
    (
        '{s_samples}'
    )
    ;
    """, eng)

    samples['DESPATCH_ID'] = [despath_id] * len(samples)

    if len(samples) == 0:
        print("Пробы не найдены")
        return
    
    __write(samples, eng, 'ST_DESPATCH_STANDARD')
    
def __write(df: pd.DataFrame, eng, table):
    df.to_sql(table, eng, index=False, if_exists='append')