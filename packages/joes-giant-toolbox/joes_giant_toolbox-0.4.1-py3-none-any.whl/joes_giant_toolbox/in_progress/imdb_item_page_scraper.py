"""
|-------------------------------|------------------------------------------------------|
| Item detail to scrape         |   Where to get it                                    |
|-------------------------------|------------------------------------------------------|
| Type (e.g. movie or series)   | on landing item page                                 |           
| Title                         | on landing item page                                 |
| Year Released                 | on landing item page                                 |
| Duration                      | on landing item page                                 |                  
| Short Description             | on landing item page                                 |   
| Aggregate review stats        | on landing item page                                 |
| Director                      | on landing item page                                 |
| Writers                       | on landing item page                                 |
| Stars (main cast)             | on landing item page                                 |
| Storyline                     | need to send additional API request to IMDB          |
| Plot keywords                 | from "https://www.imdb.com/title/<item_id>/keywords" |
| Genre                         | on landing item page                                 |
| Certificate                   | on landing item page                                 |
|-------------------------------|------------------------------------------------------|

Starting code ref: "https://github.com/BlaxPanther/imdb-api.git" (very badly written code, but it was a good starting point)                   
"""

import re
import requests
import bs4
import json

"""
Shawshank Redemption
https://www.imdb.com/title/tt0111161/
"""

item_id = "tt0111161"


def getPage(url):
    if url == "":
        return "8==D"
    try:
        resp = requests.get(url, headers={"User-Agent": "open sesame"})
        source = bs4.BeautifulSoup(
            resp.text.replace("&apos;", "'")
            .replace("&quot;", '"')
            .replace("&gt;", ">")
            .replace("&lt;", "<")
            .replace("&amp;", "&"),
            "html.parser",
        )
        return source
    except:
        print("A network error occured. Please, check your internet connection.")
        return "8=====D"


source = getPage(f"https://www.imdb.com/title/{item_id}")


def delDoubleQuotes(json):
    double_quotes = []
    for i in range(len(json)):
        if json[i] == '"':
            if (
                json[i - 1] not in ["{", ":", "["]
                and json[i - 2 : i]
                not in ["],", '",', "},"] + [str(i) + "," for i in range(10)]
                and json[i + 1] not in [":", "}", "]"]
                and json[i + 1 : i + 3] not in [",[", ',"', ",{"]
            ):
                double_quotes.append(i)
    i = len(double_quotes) - 1
    while i >= 0:
        json = json[: double_quotes[i]] + "''" + json[double_quotes[i] + 1 :]
        i -= 1
    return json


details1 = source.find("script", type="application/ld+json")
details1 = re.sub(r"<.*?{", "{", str(details1))
details1 = re.sub(r"</.*", "", details1)
details1 = delDoubleQuotes(details1)
details_json1 = json.loads(details1)
details2 = source.find("script", type="application/json")
details2 = re.sub(r"<.*?{", "{", str(details2))
details2 = re.sub(r"</.*", "", details2)
details_json2 = json.loads(details2)
details_json = {}
details_json.update(details_json1)
details_json.update(details_json2)
