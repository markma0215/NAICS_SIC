
# search_result
search_no_result = [
    "find", ["div", "span8 business-results"], ["h2", "small", "string"]
]

search_table = [[
        "find_all", ["div", "row-fluid result-row company-list businesses"]
    ],
    {
        "name": ["find", ["h5", "business-name"], "string"],
        "state_city": ["find", ["span", "province bc-float-left"], "string"]
    }
]