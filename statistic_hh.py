from processing_vacancies_from_site import vacancys_processing, draw_table, COMPUTER_LANGUAGE, API_HH
import requests
import time

def get_vacancys_list_hh(langs_programming):
    town_id = 1
    first_page = 1
    max_page = 101
    lang_with_vacancys = {}
    for lang_programming in langs_programming:
        all_vac = []
        for page in range(first_page, max_page):
            vac_params = {'text': f'Программист {lang_programming}',
                          'area': {town_id},
                          'only_with_salary':True,
                          'period':30,
                          'vacancy_search_fields': 'name',
                          'per_page': page}

            response = requests.get(f'{API_HH}/vacancies', params=vac_params)
            response.raise_for_status()

            all_vac += [vacancy for vacancy in response.json()['items']]
            time.sleep(0.5)
        lang_with_vacancys[lang_programming] = all_vac
    return lang_with_vacancys

if __name__ == '__main__':
    vacancys_hh = get_vacancys_list_hh(COMPUTER_LANGUAGE)
    hh_statistic = vacancys_processing(vacancys_hh, 'hh')
    draw_table(hh_statistic, 'HH Moscow')