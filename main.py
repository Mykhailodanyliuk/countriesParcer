import requests
from bs4 import BeautifulSoup
import lxml


def same_letter_count(letter, somelist):
    res = -1
    for country_name in somelist:
        if country_name[0].lower() == letter.lower():
            res += 1
    return res


def get_countries_info():
    page_source = requests.get(
        'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2')
    soup = BeautifulSoup(page_source.text, 'lxml')
    tables = soup.find_all('table', {"class": "wikitable"})

    countries = []
    full_country_names = []
    flag_urls = []

    for table in tables:
        table_body = table.find('tbody')
        countries_html_data = table_body.find_all('tr')[1:]
        for country_html_data in countries_html_data:
            country_fields = country_html_data.find_all('td')[1:] if len(country_html_data.find_all('td')) == 4 \
                else country_html_data.find_all('td')[1:5] if len(country_html_data.find_all('td')) == 5 \
                else country_html_data.find_all('td')
            flag_urls.append('https://uk.wikipedia.org' + country_fields[0].find('a', {"class": "image"}).get('href'))
            countries.append(country_fields[1].text[:-1])
            full_country_names.append(country_fields[2].text[:-1])

    my_list = []
    for i in range(len(countries)):
        my_list.append({'country': countries[i], 'full_country_name': full_country_names[i],
                        'same_letter_count': same_letter_count(countries[i][0], countries), 'flag_url': flag_urls[i]})
    return my_list


def find_country_data(country_name, some_list):
    for country in some_list:
        if country['country'] == country_name:
            print(country)


if __name__ == '__main__':
    find_country_data('Австралия', get_countries_info())
