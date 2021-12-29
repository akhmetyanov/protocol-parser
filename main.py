from ws_reader.order_prot_data import find_order_prot_data
from ws_reader.element_sample import find_element_sample_adress
from ws_reader.sample_data import read, rules
from result import make_res, make_receipt, devide_result
from despath import find_despatch
from write_to_server import write_results


paths = [
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 88-21 ц СЯХТМ к заказу 02 СЯХТМ0511.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 89-21 ц СЯХТМ к заказу 02 СЯХТМ0519.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 90-21 ц СЯХТМ к заказу 02 СЯХТМ0523.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 91-21 ц СЯХТМ к заказу 02 СЯХТМ0483.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 92-21 ц СЯХТМ к заказу 02 СЯХТМ0516.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 94-21 ц СЯХТМ к заказу 02 СЯХТМ0515.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 95-21 ц СЯХТМ к заказу 02 СЯХТМ0513.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 96-21 ц СЯХТМ к заказу 02 СЯХТМ0525.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 97-21 ц СЯХТМ к заказу 02 СЯХТМ0551.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 98-21 ц СЯХТМ к заказу 02 СЯХТМ0517.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 99-21 ц СЯХТМ к заказу 02 СЯХТМ0518.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 100-21 ц СЯХТМ к заказу 02 СЯХТМ0485.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 102-21 ц СЯХТМ к заказу 02 СЯХТМ0502.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 103-21 ц СЯХТМ к заказу 02 СЯХТМ0492.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 104-21 ц СЯХТМ к заказу 02 СЯХТМ0490.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 105-21 ц СЯХТМ к заказу 02 СЯХТМ0491.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 106-21 ц СЯХТМ к заказу 02 СЯХТМ0510.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 107-21 ц СЯХТМ к заказу 02 СЯХТМ0493.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 108-21 ц СЯХТМ к заказу 02 СЯХТМ0490.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 109-21 ц СЯХТМ к заказу 02 СЯХТМ0491.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\Protocols\Отчет 110-21 ц СЯХТМ к заказу 02 СЯХТМ0489.xlsx"
]

lab = 'LB40'
# template_name = 'LB_40_PACY'
template_name = 't'

def main():
    for path in paths:
        # читаем протокол находим номер и даны протокола и наряз-заказа
        prot_num, prot_date, order_num, order_date = find_order_prot_data(path, lab, template_name)

        # читаем протокол находи заголовки колонок элементов, колонку с номерами проб и по пересечению определем адреса значений элементов по пробам
        element_sample_adress = find_element_sample_adress(path, lab, template_name)

        # на основе полученных адресов читаем зачения по пробам из протокола
        datas = read(element_sample_adress, path)
        
        # согласно шаблону, для значений применяем правила: это или замена '**' на пустыне или зачнение < нпо делить на 2
        rules(datas, lab, template_name)

        # после того, как прочитали всю аналитику, нужно разобюраться с номером наряд заказа
        # бывает, что в протоколе при записи наряд-заказа вида "02-СЯХТМ0516" пропускают тире и пишут в виде "02 СЯХТМ0516"
        # нужно сначала поискать оригинальный вид, после если не нашелся оригинальный, то заменить пробелы в номеры тире 
        # и повторить поиск. Если же тут уже не нашлось, то выполнить поиск по пробно в GB_SAMPLE, GB_SAMPLE_CHECK, GB_SAMPLE_QAQC
        # если поиск проб в этих таблицах возвращает результаты, то составить новый наряд заказ на основе этих проб. 
        df_samples, df_standart, despatch_id = find_despatch(order_num)

        if df_samples is None and df_standart is None:
            raise Exception(f"Наряд-азказа {order_num} не найден")

        # составляем датафреймы на основе данных
        result_df = make_res(despatch_id, prot_num, datas, lab, template_name)
        receipt_df = make_receipt(despatch_id, prot_num, prot_date,result_df['GENERIC_METHOD'][0])

        result_samples, result_standart = devide_result(df_samples, df_standart, result_df)
        write_results(result_samples, result_standart)
        
main()