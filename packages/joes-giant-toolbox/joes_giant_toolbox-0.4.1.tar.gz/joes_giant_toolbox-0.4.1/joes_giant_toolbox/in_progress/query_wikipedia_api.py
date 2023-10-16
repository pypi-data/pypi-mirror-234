import requests


def query_wikipedia_api(query_str):
    """documentation TODO"""
    wikipedia_api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": query_str,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
    }

    response = requests.get(wikipedia_api_url, params=params)
    json_data = response.json()

    return json_data
