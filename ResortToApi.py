from pprint import pprint

import chardet
import requests
import json
import time
from PackageData.Config import USER_ID, USER_TOKEN, FREEZING



class User:
    def get_friends(self, user_id):

        params = {
            'access_token' : USER_TOKEN,
            'user_id' : user_id,
            'count' : '1000',
            'v' : '5.74'
        }
        return requests.get('https://api.vk.com/method/friends.get', params)


    def get_groups(self, user_id):
        params = {
            'access_token' : USER_TOKEN,
            'user_id' : user_id,
            'count' : '1000',
            'v' : '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.get', params)


    def get_info_group(self, user_id, group_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'group_ids' : group_id,
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getById', params)


    def get_count_members(self, user_id, group_id):

        params = {
            'access_token':  USER_TOKEN,
            'user_id': user_id,
            'group_id': group_id,
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getMembers', params)


user = User()
finish_group_info = []
start_time = time.time()
result_groups = json.loads(user.get_groups(USER_ID).text)['response']['items']
result_groups = set(result_groups)
time.sleep(FREEZING)
user_friends = json.loads(user.get_friends(USER_ID).text)
full_time = len(user_friends['response']['items']) * \
            FREEZING * 1.5 + len(result_groups) * 0.9
print('у данного юзера {} групп и {} друзей'.format(len(result_groups),
                                                    len(user_friends['response']['items'])))
print("Примерное время выполнения программы {} секунд".format(round(full_time, 0)))
time.sleep(FREEZING)


for friend in user_friends['response']['items']:
    try:
        friend_groups = json.loads(user.get_groups(friend).text)
        time.sleep(FREEZING)
        # print(friend_groups)
        friend_groups = set(friend_groups['response']['items'])
        result_groups = result_groups - friend_groups
        print('до конца осталось {} секунд'.format(round(full_time - (time.time() - start_time)), 0))
    except KeyError:
        print("Нет доступа к группе пользователя")


print("Шпионских групп ", len(result_groups))

# result_groups_json = {'gid' : list(result_groups)}
# result_groups_json = json.dumps(result_groups_json)
# pprint(result_groups_json)

# name = json.loads(user.get_info_group(USER_ID).text)
#
# print('here', name)
#
# print(name['response'][0]['name'])
# time.sleep(FREEZING)
# count = json.loads(user.get_count_members(USER_ID).text)
# print(count['response']['count'])
#
# print(count)


for group in result_groups:
    try:
        name = json.loads(user.get_info_group(USER_ID, group).text)
        time.sleep(FREEZING)
        count = json.loads(user.get_count_members(USER_ID, group).text)
        finish_group_info.append({'name' : name['response'][0]['name'],
                                  'gid' : group,
                                  'members_count' : count['response']['count']})
        time.sleep(FREEZING)
        print('до конца осталось {} секунд'.format(round(full_time - (time.time() - start_time)), 0))
    except KeyError:
        print('нет доступа к информации группы')


print(finish_group_info)
finish_group_info = json.dumps(finish_group_info)
pprint(finish_group_info)


print('Время выполнения программы {} секунд'.format(round(time.time() - start_time), 0))











