from pprint import pprint
import requests
import json
import time
from PackageData.Config import USER_ID, USER_TOKEN, FREEZING



class User:
    def get_friends(self, user_token, user_id):

        params = {
            'access_token' : user_token,
            'user_id' : user_id,
            'count' : '1000',
            'v' : '5.74'
        }
        return requests.get('https://api.vk.com/method/friends.get', params)


    def get_groups(self, user_token, user_id):
        params = {
            'access_token' : user_token,
            'user_id' : user_id,
            'count' : '1000',
            'v' : '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.get', params)


    def get_info_group(self, user_token, user_id):
        params = {
            'access_token': user_token,
            'user_id': user_id,
            'group_ids' : '51766355',
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getById', params)


    def get_count_members(self, user_token, user_id):
        params = {
            'access_token':  user_token,
            'user_id': user_id,
            'group_id': '51766355',
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getMembers', params)


user = User()
start_time = time.time()
result_groups = json.loads(user.get_groups(USER_TOKEN, USER_ID).text)['response']['items']
result_groups = set(result_groups)
time.sleep(FREEZING)
user_friends = json.loads(user.get_friends(USER_TOKEN, USER_ID).text)
full_time = len(user_friends['response']['items']) * FREEZING * 1.5
print('у данного юзера {} групп и {} друзей'.format(len(result_groups),len(user_friends['response']['items'])))
print("Примерное время выполнения программы {} секунд".format(round(full_time, 0)))
time.sleep(FREEZING)


for friend in user_friends['response']['items']:
    try:
        friend_groups = json.loads(user.get_groups(USER_TOKEN, friend).text)
        time.sleep(FREEZING)
        # print(friend_groups)
        friend_groups = set(friend_groups['response']['items'])
        result_groups = result_groups - friend_groups
        print('до конца осталось {} секунд'.format(round(full_time - (time.time() - start_time)), 0))
    except KeyError:
        print("Нет доступа к группе пользователя")


print("Шпионских групп ", len(result_groups))
result_groups_json = {'gid' : list(result_groups)}
result_groups_json = json.dumps(result_groups_json)
pprint(result_groups_json)
print('Время выполнения программы {} секунд'.format(round(time.time() - start_time), 0))

# print(user.get_info_group(USER_TOKEN, USER_ID).text)
# print(user.get_count_members(USER_TOKEN, USER_ID).text)












