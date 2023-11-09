import sqlite3

db_name = 'db.db'


def get_cursor():
    conn = sqlite3.connect(db_name)
    return conn.cursor()


def create_db():
    c = get_cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS search ( 
    id integer PRIMARY KEY,
    query text NOT NULL,
    uri text NOT NULL UNIQUE,
    type text NOT NULL,
    name text NOT NULL,
    artist text,
    cover text NON NULL,
    duration text
    ); """)


def add_search_results(query, new_data):#, to_update):
    cursor = get_cursor()
    query = query.replace(' ', '_')

    add_data(cursor, query, new_data['track'] + new_data['album'] + new_data['artist'])
    #update_data(cursor, query, to_update)

    cursor.connection.commit()

    # for element in data:
    #     uri = element['uri']
    #     elem_type = uri.split(':')[1]
    #
    #     name, artist, cover, duration = '', '', '', ''
    #     try:
    #         if elem_type == 'artist':
    #             name = element['profile']['name']
    #             cover = element['visuals']['avatarImage']['sources'][1]['url']
    #         else:
    #             name = element['name']
    #
    #             artist = parse_artists(element)
    #
    #             if elem_type == 'track':
    #                 duration = calculate_duration(element)
    #
    #                 cover = element['albumOfTrack']['coverArt']['sources'][0]['url']
    #             else:
    #                 cover = element['coverArt']['sources'][0]['url']
    #     except TypeError as e:
    #         print(f'Skipping element because of {e}')
    #         continue
    #     insert_or_update(query, uri, elem_type, name, artist, cover, duration)


def add_data(cursor, query, data):
    for element in data:
        insert(cursor, query, element['uri'], element['type'], element['name'],
               element['artist'], element['cover'], element['duration'])


def update_data(cursor, query, data):
    for element in data:
        update(cursor, query, element['uri'])


# def parse_artists(data):
#     artist_list = [i['profile']['name'] for i in data['artists']['items']]
#     artists = ', '.join(artist_list)
#     return artists
#
#
# def calculate_duration(data):
#     seconds = round(data['duration']['totalMilliseconds'] / 1000)
#     duration = f'{seconds // 60}:{seconds % 60:02}'
#     return duration


def insert(cursor, query, uri, elem_type, name, artist, cover, duration):
    try:
        cursor.execute(f"INSERT INTO search (query, uri, type, name, artist, cover, duration) "
                       f"VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (query, uri, elem_type, name, f'"{artist}"', cover, duration))
    except sqlite3.IntegrityError:
        update(cursor, query, uri)


def update(cursor, query, uri):
    res = cursor.execute(f"SELECT query, uri FROM search WHERE uri = ?", (uri,)).fetchone()
    queries = set(res[0].split() + [query])
    cursor.execute("UPDATE search SET query = ? WHERE uri = ?", (' '.join(queries), res[1]))


# def insert_or_update(query, uri, elem_type, name, artist, cover, duration):
#     c = get_cursor()
#
#     try:
#         c.execute(f"INSERT INTO search (query, uri, type, name, artist, cover, duration) "
#                   f"VALUES (?, ?, ?, ?, ?, ?, ?)",
#                   (query, uri, elem_type, name, f'"{artist}"', cover, duration))
#     except sqlite3.IntegrityError:
#         res = c.execute(f"SELECT query, uri FROM search WHERE uri = ?", (uri,)).fetchone()
#         queries = set(res[0].split() + [query])
#         c.execute("UPDATE search SET query = ? WHERE uri = ?", (' '.join(queries), res[1]))
#
#     c.connection.commit()


def print_table():
    c = get_cursor()
    res = c.execute("SELECT * FROM search")
    [print(i) for i in res]


def search_by_query(query):
    c = get_cursor()
    res = {
        'track': [],
        'album': [],
        'artist': []
    }

    query_res = c.execute("SELECT * FROM search ORDER BY type").fetchall()
    search_res = [i for i in query_res if query.replace(' ', '_') in i[1].split()]

    columns = ['query', 'uri', 'type', 'name', 'artist', 'cover', 'duration']
    for element in search_res:
        data = {}
        for i in range(len(columns)):
            data[columns[i]] = element[i + 1]
        data['artist'] = data['artist'][1:-1]
        res[data['type']].append(data)

    return res
