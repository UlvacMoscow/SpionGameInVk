import json
import time

import requests
from PackageData.Config import USER_ID, USER_TOKEN, FREEZING


class User:

    def get_friends(self, user_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'count': '1000',
            'v': '5.74'
        }
        return requests.get('https://api.vk.com/method/friends.get', params)

    def get_groups(self, user_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'count': '1000',
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.get', params)

    def get_info_group(self, user_id, group_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'group_ids': group_id,
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getById', params)

    def get_count_members(self, user_id, group_id):

        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'group_id': group_id,
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getMembers', params)

    def check_groups_friends(self, group_friends, groups):
        for friend in group_friends:
            try:
                friend_groups = json.loads(user.get_groups(friend).text)
                time.sleep(FREEZING)
                friend_groups = set(friend_groups['response']['items'])
                groups -= friend_groups
                print('до конца осталось {} секунд'.format(round(full_time - (time.time() - start_time)), 0))
            except KeyError:
                print("Нет доступа к группе пользователя")
        return groups

    def fill_the_json(self, groups):
        for group in groups:
            try:
                name = json.loads(user.get_info_group(USER_ID, group).text)
                time.sleep(FREEZING)
                count = json.loads(user.get_count_members(USER_ID, group).text)
                finish_group_info.append({'name': name['response'][0]['name'],
                                          'gid': group,
                                          'members_count': count['response']['count']})
                time.sleep(FREEZING)
                print('до конца осталось {} секунд'.format(round(full_time - (time.time() - start_time)), 0))
            except KeyError:
                print('нет доступа к информации группы')


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
result_groups = user.check_groups_friends(user_friends['response']['items'], result_groups)
print("Шпионских групп ", len(result_groups))

user.fill_the_json(result_groups)

print(finish_group_info)
with open('spion_game.json', "w", encoding="utf-8") as file:
    json.dump(finish_group_info, file, indent=3, ensure_ascii=False)

print('Время выполнения программы {} секунд'.format(round(time.time() - start_time), 0))
