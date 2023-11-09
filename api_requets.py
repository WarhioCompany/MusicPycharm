# import requests
# import json
#
#
#
#
# def auth(username, password):
#     global auth_key
#     body = {
#         'username': username,
#         'password': password
#     }
#     data = requests.post(url=f'{url}users/auth', json=body).text
#     print(data)
#     auth_key = json.loads(data)['activkey']
#     print(auth_key)
#
#
# def request(url, auth_key, **params_data):
#     params = list()
#     for key, value in params_data:
#         if type(value) is list:
#             params.append(f'{key}={",".join(value)})')
#         else:
#             params.append(f'{key}={value})')
#
#     headers = {'Authorization': f'Bearer {auth_key}', 'Content-Type': 'application/json'}
#     if params:
#         request_url = f'{url}?{"&".join(params)}'
#     else:
#         request_url = f'{url}'
#     print(request_url)
#     print(headers)
#     print(requests.get(request_url, headers=headers).text)
#
#
# auth('matvey.i.zakharov@gmail.com', 'WhyAreYouLookingAtMyPassw0rd')
# input()
# request('trends/nodes')


import requests
import json


base_header = {'Content-Type': 'application/json'}


def make_header(headers=None):
    new_header = base_header
    if headers:
        new_header = {**headers, **base_header}
    return new_header


def get_request(url, params, headers=None):
    data = requests.get(url=url, params=params, headers=headers)#make_header(headers))
    return json.loads(data.text)


def post_request(url, body, headers=None):
    data = requests.get(url=url, data=body, headers=make_header(headers))
    return json.loads(data.text)

#https://spotify23.p.rapidapi.com/search/
#print(get_request('https://spotify23.p.rapidapi.com/search/', {'q': 'Porter Robinson', 'type': 'multi'}, {'X-RapidAPI-Key': '50a30822eamsh5b12b6abf4cb78dp1b77d8jsn0106d78b94a0', 'X-RapidAPI-Host': 'spotify23.p.rapidapi.com'}))