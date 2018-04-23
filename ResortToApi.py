from urllib.parse import urlencode
from pprint import pprint
import requests

USER_NAME = 'tim_leary'
USER_ID = '5030613'
USER_TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'

AUTH_URL ='https://oauth.vk.com/authorize'
APP_ID = '6417385'
API_VK = 'https://api.vk.com/method/friends.get'

def get_token():
    auth_data ={
        'client_id' : APP_ID,
        'display' : 'mobile',
        'scope' : 'friends, groups',
        'response_type' : 'token',
        'v' : '5.73',
    }

    print('?'.join((AUTH_URL, urlencode(auth_data))))


# MY_TOKEN = '081932010981455846063c4fa7738184c4355b36ca81be6c778e5633c2e118c9a373ef648d07f01506d87'
# MY_ID = '135282071'
def get_friends():

    params = {
        'access_token' : '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099',
        'client_id' : '135282071',
        'count' : '1000',
        'v' : '5.74'
    }

    response = requests.get('https://api.vk.com/method/friends.get', params)
    pprint(response.text)

def get_groups():
        # 'access_token' : '081932010981455846063c4fa7738184c4355b36ca81be6c778e5633c2e118c9a373ef648d07f01506d87',
        # 'client_id' : '135282071',

    params = {
        'access_token': USER_TOKEN,
        'user_id': USER_ID,
        'count' : '1000',
        'v': '5.73'
    }

    response = requests.get('https://api.vk.com/method/groups.get', params)
    pprint(response.text)

get_groups()
# get_friends()

group_id = [51766355,164800385,87389803,35486626,8564,4100014,151498735,41771674,124656670,30314549]
group_friends = [15628,23059,45857,65668,88364,157312,187268,212696,239216,252651,256433,301147,321229,325712,326136]

# params = {
#     'access_token': USER_TOKEN,
#     'client_id': USER_ID,
#     'group_id' : '51766355',
#     'extended': '0',
#     'count': '1000',
#     'v': '5.73'
# }
#
# response = requests.get('https://api.vk.com/method/groups.getById', params)
# pprint(response.text)