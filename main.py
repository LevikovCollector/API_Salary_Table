import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable

API_HH = 'https://api.hh.ru'
API_SJ = '	https://api.superjob.ru/2.0'

def get_vacancys_list_hh(lang_programming):
    all_vac = []
    for page in range(1,101):
        vac_params = {'text': f'Программист {lang_programming}',
                      'area': 1,
                      'only_with_salary':True,
                      'period':30,
                      'vacancy_search_fields': 'name',
                      'per_page': page}

        response = requests.get(f'{API_HH}/vacancies', params=vac_params)
        response.raise_for_status()
        for vacancy in response.json()['items']:
            all_vac.append(vacancy)

    return all_vac

def get_vacancys_list_sj(lang_programming, header):
    all_vac = []
    for page in range(1, 100):
        vac_params = {'catalogues': 48,
                      'town': 4,
                      'keywords': 1,
                      'keywords': 'and',
                      'keywords': f'Программист {lang_programming}',
                      'page': page}

        response = requests.get(f'{API_SJ}/vacancies/', headers=header, params=vac_params)
        response.raise_for_status()
        for vacancy in response.json()['objects']:
            all_vac.append(vacancy)
    return all_vac

def vacancys_processing(lang_programming, resource, header=None):
    vacancys_processed = {}
    average_salary_by_vacancy = []
    for language in lang_programming:
        if resource == 'hh':
            vacancys_by_language = get_vacancys_list_hh(language)
        else:
            vacancys_by_language = get_vacancys_list_sj(language, header)

        for vacancy in vacancys_by_language:
            average_salary_by_vacancy.append(predict_rub_salary(vacancy, resource))
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
        if vac_salary_from is not None and vac_salary_to is not None:
            average_salary = (vac_salary_from+vac_salary_to)/2
        elif vac_salary_from is not None and vac_salary_to is None:
            average_salary = vac_salary_from * 1.2
        elif vac_salary_from is None and vac_salary_to is not None:
            average_salary = vac_salary_to * 0.8
        else:
            return 0
    else:
        return 0

    return int(average_salary)

def draw_table(statistic_dict, title):
    columns = [('Язык программирования', 'Вакансий обработано', 'Средняя зарплата')]

    for key in statistic_dict.keys():
        columns.append((key, statistic_dict[key]['vacancies_processed'], statistic_dict[key]['average_salary']))

    stat_tabele = AsciiTable(columns, title)
    print(stat_tabele.table)
    print()

if __name__=='__main__':
    load_dotenv(dotenv_path='config.env')
    header_sj = {'X-Api-App-Id': os.getenv('SJ_TOKEN')}
    computer_language = ['Swift', 'Scala','Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    hh_statistic = vacancys_processing(computer_language, 'hh')
    sj_statistic = vacancys_processing(computer_language, 'sj', header=header_sj)
    draw_table(hh_statistic, 'HH Moscow')
    draw_table(sj_statistic, 'SJ Moscow')

