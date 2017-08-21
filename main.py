import urllib2
import requests
from fake_useragent import UserAgent

def main():
    url = "http://siccode.com/en/search/Al%20Rounds%20Studio"
    ua = UserAgent()
    print ua.random
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    # }
    headers = {
        'User-Agent': ua.random
    }
    response = requests.get(url, headers=headers)
    # response = urllib2.urlopen(url)
    # if response.get_code() == 200:
    if response.status_code == 200:
        print response.text
    else:
        print response.status_code


if __name__ == "__main__":
    main()
