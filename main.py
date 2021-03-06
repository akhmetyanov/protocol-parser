from ws_reader.order_prot_data import find_order_prot_data
from ws_reader.element_sample import find_element_sample_adress
from ws_reader.sample_data import read, rules
from result import make_res, make_receipt, devide_result
from despath import find_despatch
from write_to_server import write_results

paths = [
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 7-22ПЕЩ.ИК к заказу № 11-ПЕЩ000279.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 6-22ПЕЩ.ИК к заказу № 11-ПЕЩ000278.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 5-22ПЕЩ.ИК к заказу № 11-ПЕЩ000281.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 1-22ПЕЩ.ИК к заказу № 11-ПЕЩ000267.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 2-22ПЕЩ.ИК к заказу № 11-ПЕЩ000268.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 3-22ПЕЩ.ИК к заказу № 11-ПЕЩ000271.xlsx",
    r"C:\Users\AkhmetyanovIR\Desktop\PE_протокол\Сера, мышьяк\ААА\Протокол № 4-22ПЕЩ.ИК к заказу № 11-ПЕЩ000272.xlsx"
]

lab = 'LB40'
template_name = 'LB40_MPAL'

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
            print(f"Наряд-заказа {order_num} не найден")
            print(f"Содать нз {order_num} на основе протокола?")
            
            def get_user_choice():
                user_input = input("Y - создать, N - пропустить: ")
                if str(user_input).lower() not in ["y", "n"]: user_input = get_user_choice()
                return user_input

            user_input = get_user_choice()

            if user_input == 'y':
                from find_project import find_project
                

                def get_user_project():
                    user_input = str(input("Введите код проекта: "))
                    project = find_project(user_input)

                    if project is None:
                        print(f"Проект {user_input} не найдет в таблице GB_PROJECT")
                        get_user_project()

                    return user_input
            
                user_input = str(get_user_project()).upper()

                samples_list = [d['ns'] for d in datas]
                samples_list = list(set(samples_list))

                from create_despath import create_despath
                create_despath(user_input, order_num, order_date, prot_num, lab, samples_list)

                df_samples, df_standart, despatch_id = find_despatch(order_num)

            else:        
                continue

        # составляем датафреймы на основе данных
        result_df = make_res(despatch_id, prot_num, datas, lab, template_name)
        receipt_df = make_receipt(despatch_id, prot_num, prot_date,result_df['GENERIC_METHOD'][0])

        result_samples, result_standart = devide_result(df_samples, df_standart, result_df)
        result_samples['TEXT_RULE'] = [''] * len(result_samples)
        result_standart['TEXT_RULE'] = [''] * len(result_standart)
        write_results(result_samples, result_standart, receipt_df)
        
main()