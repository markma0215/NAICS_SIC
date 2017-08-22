import requests
from fake_useragent import UserAgent
import csv
import sys
from bs4 import BeautifulSoup
import config
from Parser_HTML import parser_map

matched = 0
unmatched = 0
counter = 1
url_base = "http://siccode.com/en/search/"


def file_reader():
    with open("inputfile.csv", "rU") as csvfile:
        reader = csv.reader(csvfile)

        input_data = [oneline for oneline in reader]

    return input_data


def requestHTMLPage(url):
    status = False
    times = 0
    html_page = ""
    while not status and times < 5:
        try:
            ua = UserAgent()
            print ua.random
            headers = {
                'User-Agent': ua.random
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                html_page = response.text
                status = True
            else:
                print response.status_code
                times = times + 1
        except Exception, e:
            print e.message
            print "try again"
            times = times + 1

    if not html_page:
        sys.exit(1)

    return html_page


def composite_url(tanent_name):
    tanent_name = tanent_name.strip()
    tanent_name = tanent_name.replace(" ", "%20")
    return url_base + tanent_name


def has_no_result(soup):

    element = parser_map[config.search_no_result[0]](soup, config.search_no_result[1][0], config.search_no_result[1][1])
    if not element:
        return False

    tags = config.search_no_result[1]()
    for eachTag in tags:
        element = parser_map[config.search_no_result[1][0]]
        if not element:
            return False

    if element.strip() == "No businesses found under current search term":
        return True
    else:
        print element.strip()
        return False


def parse_search_table(soup):
    elements_property = config.search_table[0]
    elements = parser_map[elements_property[0]](soup, elements_property[1][0], elements_property[1][1])
    name_property = config.search_table[1].get("name")
    state_city = config.search_table[1].get("state_city")
    for each_element in elements:
        each_element = parser_map[name_property[0]](each_element, name_property[1][0], name_property[1][1])
        each_element = parser_map[name_property[2]](each_element)


def main():
    inputData = file_reader()

    global counter
    for i in range(counter, len(inputData)):
        this_row = inputData[i][0]

        city = this_row.split('\t')[0]
        state = this_row.split('\t')[1]
        zip = this_row.split('\t')[2]
        tanent_name = this_row.split('\t')[3]
        html_page = requestHTMLPage(composite_url(tanent_name))

        # html_page = requestHTMLPage("http://siccode.com/en/search/Faith%20Christian%20Academy%20Inc")
        soup = BeautifulSoup(html_page, 'html.parser')

        if has_no_result(soup):
            unmatched = unmatched + 1
            counter = counter + 1
            continue






if __name__ == "__main__":
    main()
    # url = "http://siccode.com/en/search/Al%20Rounds%20Studio"
