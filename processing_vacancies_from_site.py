from terminaltables import AsciiTable

API_HH = 'https://api.hh.ru'
API_SJ = 'https://api.superjob.ru/2.0'
COMPUTER_LANGUAGE = ['Swift', 'Scala','Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']


def vacancys_processing(vacancys_by_language, resource):
    vacancys_processed = {}
    for language in vacancys_by_language.keys():
        average_salary_by_vacancy = [predict_rub_salary(vacancy, resource) for vacancy in vacancys_by_language[language]]
        if average_salary_by_vacancy:
            total_average_salary_by_vacancy = int(sum(average_salary_by_vacancy) / len(average_salary_by_vacancy))
            vacancys_processed[language] = {
                'vacancies_processed': len(vacancys_by_language[language]),
                'average_salary': total_average_salary_by_vacancy
            }
        else:
            vacancys_processed[language] = {
                'vacancies_processed': len(vacancys_by_language[language]),
                'average_salary': 0
            }
    return vacancys_processed

def predict_rub_salary(vacancy, resource):
    if resource == 'hh':
        vac_salary_from = vacancy['salary']['from']
        vac_salary_to = vacancy['salary']['to']
        vac_salary_currency = vacancy['salary']['currency']
    elif resource == 'sj' :
        vac_salary_from = vacancy['payment_from']
        vac_salary_to = vacancy['payment_to']
        vac_salary_currency = vacancy['currency']
    average_salary = 0

    if vac_salary_currency in ['RUR','rub']:
        if vac_salary_from and vac_salary_to:
            average_salary = (vac_salary_from+vac_salary_to)/2
        elif vac_salary_from  and not vac_salary_to:
            average_salary = vac_salary_from * 1.2
        elif not vac_salary_from and vac_salary_to:
            average_salary = vac_salary_to * 0.8

    return int(average_salary)

def draw_table(statistic_dict, title):
    columns = [(key, statistic_dict[key]['vacancies_processed'], statistic_dict[key]['average_salary']) for key in statistic_dict.keys()]
    columns.insert(0, ('Язык программирования', 'Вакансий обработано', 'Средняя зарплата'))

    stat_tabele = AsciiTable(columns, title)
    print(stat_tabele.table)
    print()
