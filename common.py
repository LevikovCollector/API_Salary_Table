import requests
from terminaltables import AsciiTable

API_HH = 'https://api.hh.ru'
API_SJ = '	https://api.superjob.ru/2.0'
#COMPUTER_LANGUAGE = ['Swift', 'Scala','Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
COMPUTER_LANGUAGE = ['Swift']
def get_vacancys_list_hh(lang_programming):
    town_id = 1
    first_page = 1
    max_page = 101
    for page in range(first_page, max_page):
        vac_params = {'text': f'Программист {lang_programming}',
                      'area': {town_id},
                      'only_with_salary':True,
                      'period':30,
                      'vacancy_search_fields': 'name',
                      'per_page': page}

        response = requests.get(f'{API_HH}/vacancies', params=vac_params)
        response.raise_for_status()

        all_vac = [vacancy for vacancy in response.json()['items']]

    return all_vac

def get_vacancys_list_sj(lang_programming, header):
    first_page = 1
    max_page = 101
    town_id = 4
    IT_catalog_id = 48
    for page in range(first_page, max_page):
        vac_params = {'catalogues': {IT_catalog_id},
                      'town': {town_id},
                      'keywords': 1,
                      'keywords': 'and',
                      'keywords': f'Программист {lang_programming}',
                      'page': page}

        response = requests.get(f'{API_SJ}/vacancies/', headers=header, params=vac_params)
        response.raise_for_status()
        all_vac = [vacancy for vacancy in response.json()['objects']]

    return all_vac

def vacancys_processing(lang_programming, resource, header=None):
    vacancys_processed = {}
    average_salary_by_vacancy = []
    for language in lang_programming:
        if resource == 'hh':
            vacancys_by_language = get_vacancys_list_hh(language)
        else:
            vacancys_by_language = get_vacancys_list_sj(language, header)
        average_salary_by_vacancy = [predict_rub_salary(vacancy, resource) for vacancy in vacancys_by_language]

        total_average_salary_by_vacancy = int(sum(average_salary_by_vacancy) / len(average_salary_by_vacancy))
        vacancys_processed[language] = {
            'vacancies_processed': len(vacancys_by_language),
            'average_salary': total_average_salary_by_vacancy
        }
    return vacancys_processed

def predict_rub_salary(vacancy, resource):
    if resource == 'hh':
        vac_salary_from = vacancy['salary']['from']
        vac_salary_to = vacancy['salary']['to']
        vac_salary_currency = vacancy['salary']['currency']
    elif resource == 'sj' :
        vac_salary_from = vacancy['payment_from']
        if vac_salary_from == 0:
            vac_salary_from = None
        vac_salary_to = vacancy['payment_to']
        if vac_salary_to == 0:
            vac_salary_to = None
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
