from common import vacancys_processing, draw_table, COMPUTER_LANGUAGE

if __name__ == '__main__':
    hh_statistic = vacancys_processing(COMPUTER_LANGUAGE, 'hh')
    draw_table(hh_statistic, 'HH Moscow')