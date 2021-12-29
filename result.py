import pandas as pd
from reader.read_template import read_template


def make_res(despatch_id, lab_job_no, datas, lab_id, template_name):
    template = read_template(lab_id, template_name)

    for i in range(len(datas)):
        datas[i]['despatch_id'] = despatch_id
        datas[i]['value3'] = datas[i]['value2']
        datas[i]['lab_job_no'] = lab_job_no
        datas[i]['lab_method'] = template['ELEMENTS'][datas[i]['element']]['LAB_METHOD']
        datas[i]['gen_method'] = template['ELEMENTS'][datas[i]['element']]['GENERIC_METHOD']
        datas[i]['unit'] = template['ELEMENTS'][datas[i]['element']]['UNIT']

    df = pd.DataFrame(datas)
    df.rename(columns={
        'element':'LAB_ELEMENT',
        'ns':'SAMPLE_TAG',
        'value':'LAB_RESULT_TEXT',
        'value2':'LAB_RESULT_NUMERIC',
        'value3':'RESULT',
        'exlcude':'EXCLUDE',
        'despatch_id':'DESPATCH_ID',
        'lab_job_no':'LAB_JOB_NO',
        'lab_method':'LAB_METHOD',
        'gen_method':'GENERIC_METHOD',
        'unit':'LAB_UNITS'
    }, inplace=True)
    return df

def make_receipt(despatch_id, lab_job_no, receipt_date, del_method):
    d = [{
        'DESPATCH_ID': despatch_id,
        'LAB_JOB_NO': lab_job_no,
        'RECEIPT_DATE': receipt_date,
        'DELIVERY_METHOD': del_method
    }]
    df = pd.DataFrame(d)
    return df

def devide_result(despatch_samples: pd.DataFrame, despatch_standart: pd.DataFrame, result: pd.DataFrame):

    sample_tags = despatch_samples['SAMPLE_TAG'].values.tolist()
    standart_tags = despatch_standart['SAMPLE_TAG'].values.tolist()

    df_samples = result[result['SAMPLE_TAG'].isin(sample_tags)]
    df_standart = result[result['SAMPLE_TAG'].isin(standart_tags)]

    return df_samples, df_standart