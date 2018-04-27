import json
import time

import requests
from PackageData.Config import USER_ID, USER_TOKEN, FREEZING


class User:

    @staticmethod
    def get_friends(user_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'count': '1000',
            'v': '5.74'
        }
        return requests.get('https://api.vk.com/method/friends.get', params)

    @staticmethod
    def get_groups(user_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'count': '1000',
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.get', params)

    @staticmethod
    def get_info_group(user_id, group_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'group_ids': group_id,
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getById', params)

    @staticmethod
    def get_count_members(user_id, group_id):
        params = {
            'access_token': USER_TOKEN,
            'user_id': user_id,
            'group_id': group_id,
            'v': '5.73'
        }
        return requests.get('https://api.vk.com/method/groups.getMembers', params)

    @staticmethod
    def check_groups_friends(group_friends, groups):
        for friend in group_friends:
            try:
                friend_groups = json.loads(user.get_groups(friend).text)
                time.sleep(FREEZING)
                friend_groups = set(friend_groups['response']['items'])
                groups -= friend_groups
                print('до конца осталось {} секунд'.format(round(lead_time - (time.time() - start_time)), 0))
            except KeyError:
                print("Нет доступа к группе пользователя")
        return groups

    @staticmethod
    def fill_the_json(groups):
        for group in groups:
            try:
                name = json.loads(user.get_info_group(USER_ID, group).text)
                time.sleep(FREEZING)
                count = json.loads(user.get_count_members(USER_ID, group).text)
                finish_group_info.append({'name': name['response'][0]['name'],
                                          'gid': group,
                                          'members_count': count['response']['count']})
                time.sleep(FREEZING)
                print('до конца осталось {} секунд'.format(round(lead_time - (time.time() - start_time)), 0))
            except KeyError:
                print('нет доступа к информации группы')

    @staticmethod
    def full_time(amount_friends, amount_groups):
        """
        Нашел примерную закономерность которая позволяет понять сколько групп примерно останется у юзера после проверки,
        точность конечно в минуту, но тем не менее. Сделал выборку из 8 человек, и значение очень даже
         приличное получилось, максимальный промах примерно был 25%, а средний  около 15 %.
        :param amount_friends:
        :param amount_groups:
        :return:
        """
        coefficient = amount_groups / amount_friends
        about_time = amount_friends * FREEZING * 1.5 + amount_groups * coefficient
        return round(about_time, 0)


user = User()
finish_group_info = []
start_time = time.time()
result_groups = json.loads(user.get_groups(USER_ID).text)['response']['items']
result_groups = set(result_groups)
time.sleep(FREEZING)

user_friends = json.loads(user.get_friends(USER_ID).text)
lead_time = user.full_time(len(user_friends['response']['items']), len(result_groups))

print('у данного юзера {} групп и {} друзей'.format(len(result_groups),
                                                    len(user_friends['response']['items'])))

print("Примерное время выполнения программы {} секунд".format(lead_time))
time.sleep(FREEZING)

result_groups = user.check_groups_friends(user_friends['response']['items'], result_groups)
print("Шпионских групп ", len(result_groups))

user.fill_the_json(result_groups)
print('Время выполнения программы {} секунд'.format(round(time.time() - start_time), 0))

with open('spion_game.json', "w", encoding="utf-8") as file:
    json.dump(finish_group_info, file, indent=3, ensure_ascii=False)
