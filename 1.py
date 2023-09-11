import requests


def get_updates(offset: int = 0, timeout: int = 60):
    """
    The get_updates function defines a class method. Accepts offset and timeout as parameters with certain
    values by omission. Produces a telegram API request for sent messages. Returns the API response
    as a GetUpdatesResponse object.
    """
    url: str = "https://api.telegram.org/bot5950361070:AAFTCM6xOs6FFzi0yJrftQZgERfeIAKI5Ww/getUpdates"
    response = requests.get(url, params={"offset": 0, "timeout": 10})
    return response.json()

if __name__ == '__main__':
    result = get_updates()
    # for i in result['result']:
    #     print(i)
    print(result)