from api_requets import post_request, get_request

spotify_api_url = 'spotify23.p.rapidapi.com'
shazam_api_url = 'shazam.p.rapidapi.com'

current_key = 0
keys = [
    "50a30822eamsh5b12b6abf4cb78dp1b77d8jsn0106d78b94a0",
]


def make_header(host):
    global current_key
    header = {
        'X-RapidAPI-Key': keys[current_key],
        'X-RapidAPI-Host': host
    }
    current_key = (current_key + 1) % len(keys)
    return header


def make_url(host, endpoint):
    return f"https://{host}/{endpoint}/"


def search(query):
    url = make_url(spotify_api_url, 'search')
    headers = make_header(spotify_api_url)
    args = {
        'q': query,
        'type': 'multi',
    }
    print('Sending request...')
    data = get_request(url, args, headers)
    print('Got Response!')
    # [i['data'] for i in data['tracks']['items'] + data['albums']['items'] + data['artists']['items']]
    result = data['tracks']['items'] + data['albums']['items'] + data['artists']['items']
    return result
    # result = data['topResults']['items']
    # [result.append(i) for i in data['tracks']['items'] if all(i['data']['uri'] != j['data']['uri'] for j in result)]
    # return [i['data'] for i in result if i['data']['uri'].split(':')[1] in ('artist', 'track', 'album')]


def get_radio(uri):
    return get_request(make_url(spotify_api_url, 'seed_to_playlist'), {'uri': uri}, make_header(spotify_api_url))
