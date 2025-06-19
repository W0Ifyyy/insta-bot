import requests
api_url = 'http://api.forismatic.com/api/1.0/'

def get_quote():
    response = requests.post(api_url, data={
    'method': 'getQuote',
    'format': 'json',
    'lang': 'en',
    'key': 'random'
    } )
    if response.status_code == requests.codes.ok:
        return {
            'quote': response.json()['quoteText'],
            'author': response.json()['quoteAuthor']
        }
    else:
        print("Error:", response.status_code, response.text)
