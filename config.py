#Shadow Lake Towne Center - Management …

matched = 19
unmatched = 245
counter = 265
url_base = "http://siccode.com/en/search/"

# search_result
search_no_result = [
    "find", ["div", "span8 business-results"], ["h2", "small", "string"]
]

search_table = [[
        "find_all", ["div", "row-fluid result-row company-list businesses"]
    ],
    {
        "name": ["find", ["h5", "business-name"], "string"],
        "state_city": ["find", ["span", "province bc-float-left"], "string"],
        "link": ["", "", "a", "attri_href"]
    }
]

specific_company = {
    "company_name": ["find", ["h1", "span12"], "span"],
    "zip": ["find_itemprop", ["span", "postalCode"]],
    "NAICS": ["find", ["span", "naics-item"]]
}