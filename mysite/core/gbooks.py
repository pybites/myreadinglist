import requests
import requests_cache

requests_cache.install_cache('book_cache', backend='sqlite', expire_after=86400)

BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
SEARCH_URL = BASE_URL + '?q={}'
BOOK_URL = BASE_URL + '/{}'


def get_book_info(book_id):
    query = BOOK_URL.format(book_id)
    return requests.get(query).json()


def search_books(term):
    query = SEARCH_URL.format(term)
    return requests.get(query).json()


if __name__ == '__main__':
    from pprint import pprint as pp
    #pp(get_book_info('PvwDFlJUYHcC'))
    term = 'python for finance'
    #pp(search_books(term))
    for item in search_books(term)['items']:
        try:
            id_ = item['id']
            title = item['volumeInfo']['title']
        except KeyError:
            continue
        print(id_, title)
