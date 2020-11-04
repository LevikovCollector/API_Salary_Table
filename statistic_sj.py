from dotenv import load_dotenv
import os
from common import vacancys_processing, draw_table, COMPUTER_LANGUAGE

if __name__ == '__main__':
    load_dotenv(dotenv_path='.env')
    header_sj = {'X-Api-App-Id': os.getenv('SJ_TOKEN')}
    sj_statistic = vacancys_processing(COMPUTER_LANGUAGE, 'sj', header=header_sj)
    draw_table(sj_statistic, 'SJ Moscow')