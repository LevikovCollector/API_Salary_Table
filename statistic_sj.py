import time
from dotenv import load_dotenv
import os
from processing_vacancies_from_site import vacancys_processing, draw_table, COMPUTER_LANGUAGE, API_SJ
import requests

def get_vacancys_list_sj(langs_programming, header):
    first_page = 1
    max_page = 101
    town_id = 4
    IT_catalog_id = 48
    data_block = {}
    for lang_programming in langs_programming:
        all_vac = []
        for page in range(first_page, max_page):
            vac_params = {'catalogues': {IT_catalog_id},
                          'town': {town_id},
                          'keywords': 1,
                          'keywords': 'and',
                          'keywords': f'Программист {lang_programming}',
                          'page': page}

            response = requests.get(f'{API_SJ}/vacancies/', headers=header, params=vac_params)
            response.raise_for_status()
            all_vac += [vacancy for vacancy in response.json()['objects']]
            time.sleep(0.5)
        data_block[lang_programming] = all_vac
    return data_block


if __name__ == '__main__':
    load_dotenv(dotenv_path='.env')
    header_sj = {'X-Api-App-Id': os.getenv('SJ_TOKEN')}
    vacancys_sj = get_vacancys_list_sj(COMPUTER_LANGUAGE, header_sj)
    sj_statistic = vacancys_processing(vacancys_sj, 'sj')
    draw_table(sj_statistic, 'SJ Moscow')