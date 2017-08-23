import requests
from fake_useragent import UserAgent
import csv
import sys
from bs4 import BeautifulSoup
import config
from Parser_HTML import parser_map
import time
import random


def file_reader():
    with open("inputfile.csv", "rU") as csv_file:
        reader = csv.reader(csv_file)

        input_data = [one_line for one_line in reader]

    return input_data


def file_wirter(str_list):
    with open("output_file.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(str_list)


def requestHTMLPage(url):
    status = False
    times = 0
    html_page = ""
    while not status and times < 5:
        try:
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random
            }
            print "the url is : %s " % url
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
    return config.url_base + tanent_name


def has_no_result(soup):
    element = parser_map[config.search_no_result[0]](soup, config.search_no_result[1][0], config.search_no_result[1][1])
    if not element:
        return False

    tags = config.search_no_result[2]
    for eachTag in tags:
        element = parser_map[eachTag](element)
        if not element:
            return False

    if element.strip() == "No businesses found under current search term":
        print "no this company"
        return True
    else:
        print element.strip()
        sys.exit(1)


def parser_specific_company(link, tenant_name, zip):
    url_base = "http://siccode.com"
    link = url_base + link
    specific_html_page = requestHTMLPage(link)
    soup = BeautifulSoup(specific_html_page, "html.parser")
    company_name_rule = config.specific_company.get("company_name")
    company_name_tag = parser_map[company_name_rule[0]](soup, company_name_rule[1][0], company_name_rule[1][1])
    company_name = parser_map[company_name_rule[2]](company_name_tag).string.strip()
    if tenant_name != company_name:
        print "company name is %s " % company_name
        sys.exit(1)

    zip_rule = config.specific_company.get("zip")
    zip_code = parser_map[zip_rule[0]](soup, zip_rule[1][0], zip_rule[1][1]).string.strip()
    if zip_code != zip:
        return False

    NAICS_code_rule = config.specific_company.get("NAICS")
    NAICS_code = parser_map[NAICS_code_rule[0]](soup, NAICS_code_rule[1][0], NAICS_code_rule[1][1]).string.strip()
    NAICS_code = NAICS_code.split(" - ")[0].strip()
    print "the code is: %s " % NAICS_code

    return NAICS_code


def parse_search_table(soup, tenant_name, city_state, zip):
    elements_property = config.search_table[0]
    elements = parser_map[elements_property[0]](soup, elements_property[1][0], elements_property[1][1])
    name_property = config.search_table[1].get("name")
    state_city = config.search_table[1].get("state_city")
    for each_element in elements:
        company_name_tag = parser_map[name_property[0]](each_element, name_property[1][0], name_property[1][1])
        company_name = parser_map[name_property[2]](company_name_tag).strip()
        if company_name != tenant_name:
            continue

        company_state_city_tag = parser_map[state_city[0]](each_element, state_city[1][0], state_city[1][1])
        company_state_city = parser_map[state_city[2]](company_state_city_tag).strip()
        if company_state_city != city_state:
            continue

        link_property = config.search_table[1].get("link")
        link_tag = parser_map[link_property[2]](each_element)
        link = parser_map[link_property[3]](link_tag)
        if link:
            return parser_specific_company(link, tenant_name, zip)

        else:
            print "company matched, however website does not provide no link"
            sys.exit(1)

    return False


def main():
    inputData = file_reader()

    for i in range(config.counter, len(inputData)):
        this_row = inputData[i][0]

        city = this_row.split('\t')[0]
        state = this_row.split('\t')[1]
        zip = this_row.split('\t')[2]
        tenant_name = this_row.split('\t')[3]
        city_state = city + ", " + state

        print "Current matched number is %s, unmatched number is %s" % (config.matched, config.unmatched)
        print "NO. %s company, the tenant name is %s" % (config.counter, tenant_name)
        html_page = requestHTMLPage(composite_url(tenant_name))

        soup = BeautifulSoup(html_page, 'html.parser')
        if has_no_result(soup):
            config.unmatched = config.unmatched + 1
            config.counter = config.counter + 1
            continue

        code = parse_search_table(soup, tenant_name, city_state, zip)
        if code:
            config.matched = config.matched + 1
            result = [city, state, zip, tenant_name, code]
            file_wirter(result)
        else:
            config.unmatched = config.unmatched + 1

        config.counter = config.counter + 1
        time.sleep(random.randint(1, 3))

if __name__ == "__main__":
    main()
