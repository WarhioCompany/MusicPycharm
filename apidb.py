import api
import db
import threading


def search(query):
    db.create_db()
    result = db.search_by_query(query)

    if any(i[1] for i in result.items()):
        print('getting result from the database')
        return result

    print('getting result from the api')

    api_data = api.search(query)
    result = filter_api_results(api_data)

    t = threading.Thread(target=db.add_search_results, args=(query, result))
    t.start()

    return result


def filter_api_results(api_data):
    results = {
        'track': [],
        'album': [],
        'artist': []
    }
    for element in api_data:
        obj = parse_element(element['data'])
        if obj:
            results[obj['type']].append(obj)
    return results


def parse_element(data):
    elem_type = data['uri'].split(':')[1]

    result = {
        'uri': data['uri'],
        'type': elem_type,
        'name': '',
        'artist': '',
        'cover': '',
        'duration': ''
    }
    try:
        if elem_type == 'artist':
            result['name'] = data['profile']['name']
            result['cover'] = data['visuals']['avatarImage']['sources'][1]['url']
        else:
            result['name'] = data['name']
            result['artist'] = parse_artists(data)

            if elem_type == 'track':
                result['duration'] = calculate_duration(data)
                result['cover'] = data['albumOfTrack']['coverArt']['sources'][0]['url']
            else:
                result['cover'] = data['coverArt']['sources'][0]['url']
        return result
    except TypeError as e:
        print(f'Skipping element because of {e}')
        return None


def parse_artists(data):
    artist_list = [i['profile']['name'] for i in data['artists']['items']]
    artists = ', '.join(artist_list)
    return artists


def calculate_duration(data):
    seconds = round(data['duration']['totalMilliseconds'] / 1000)
    duration = f'{seconds // 60}:{seconds % 60:02}'
    return duration
