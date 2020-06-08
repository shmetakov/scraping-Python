# 1) Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#
#     *Наименование вакансии
#     *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
#     *Ссылку на саму вакансию
#     *Сайт откуда собрана вакансия
#
# По своему желанию можно добавить еще работодателя и расположение.
# Данная структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

from pprint import pprint

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

main_link = 'https://hh.ru/'
job_title_search = input('Введите название вакансии: ')

current_page = 0

params = {
    'text': job_title_search
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36',
    'Accept': '*/*'
}

vacancies = pd.DataFrame(dict(
    name=[],
    link=[],
    address=[],
    company_name=[],
    site=[],
    compensation_min=[],
    compensation_max=[],
    compensation_cur=[]
))


def get_link(tag):
    result = tag.find('a', {
        'class': 'bloko-link',
        'data-qa': 'vacancy-serp__vacancy-title'
    })

    if not result:
        return None

    return result['href']


def get_name(tag):
    return tag.find('a', {
        'class': 'bloko-link',
        'data-qa': 'vacancy-serp__vacancy-title'
    }).text


def get_company_name(tag):
    return tag.find('a', {
        'class': 'bloko-link',
        'data-qa': 'vacancy-serp__vacancy-employer'
    }).text


def get_address(tag):
    result = tag.find('span', {
        'class': 'vacancy-serp-item__meta-info',
        'data-qa': 'vacancy-serp__vacancy-address'
    })

    if result:
        return result.text

    return None


def get_compensation(tag):
    tag_link = item.find('span', {
        'class': 'bloko-section-header-3 bloko-section-header-3_lite',
        'data-qa': 'vacancy-serp__vacancy-compensation'
    })

    comp_min = None
    comp_max = None
    comp_cur = None

    def split_compensation(comp_str):
        comp, currency = comp_str.split(' ')
        comp = int(comp.replace('\xa0', ''))

        return comp, currency

    if tag_link:
        compensation = tag_link.text
        compensation = compensation.split('-')

        if len(compensation) == 2:
            comp_min = int(compensation[0].replace('\xa0', ''))
            comp_max, comp_cur = split_compensation(compensation[1])

        elif len(compensation) == 1:
            if compensation[0].startswith('от'):
                comp_min, comp_cur = split_compensation(compensation[0].replace('от ', ''))
            elif compensation[0].startswith('до'):
                comp_max, comp_cur = split_compensation(compensation[0].replace('до ', ''))

    return comp_min, comp_max, comp_cur


def has_next_page():
    button_next = soup.find('a', {
        'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control',
        'data-qa': 'pager-next'
    })

    return bool(button_next)


while True:
    params['page'] = current_page

    response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'lxml')

    vacancies_block = soup.find('div', {'data-qa': 'vacancy-serp__results'})
    vacancies_list = vacancies_block.find('div', {
            'class': 'vacancy-serp'
        }).findChildren(recursive=False)

    for item in vacancies_list:
        link = get_link(item)

        if not link:
            continue

        name = get_name(item)
        company_name = get_company_name(item)
        address = get_address(item)
        compensation_min, compensation_max, compensation_cur = get_compensation(item)

        vacancies = vacancies.append({
            'name': name,
            'link': link,
            'address': address,
            'company_name': company_name,
            'site': main_link,
            'compensation_min': compensation_min,
            'compensation_max': compensation_max,
            'compensation_cur': compensation_cur
        }, ignore_index=True)

    if not has_next_page():
        break

    current_page += 1


pd.options.display.max_rows = 10
pd.options.display.max_columns = vacancies.shape[1]

pprint(vacancies)


