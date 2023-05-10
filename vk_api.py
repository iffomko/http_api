import os

import requests


class VKApi:
    def __init__(self):
        self.__friends_get = 'https://api.vk.com/method/friends.get'
        self.__friends_get_mutual = 'https://api.vk.com/method/friends.getMutual'
        self.__app_id = 51640511
        self.__secret_key = os.environ['SECRET_KEY']
        self.__version = 5.131
        self.__redirect_url = 'https://oauth.vk.com/blank.html'
        self.__token = None

    def __get_access_token(self):
        req_url = f'https://oauth.vk.com/authorize' \
                  f'?client_id={self.__app_id}' \
                  f'&display=page' \
                  f'&scope=friends' \
                  f'&response_type=token' \
                  f'&v={self.__version}' \
                  f'&state=123456'

        print(f'Открой эту ссылку в своем браузере: {req_url}')
        print('И введи query-параметр "access-token", который будет в url адресе: ')
        self.__token = input()

    def __get_all_friends(self, parsed: dict) -> dict:
        url = self.__friends_get + \
              f"?userId={parsed.get('id')}" \
              f"&order=hints" \
              f"&count={10000 if parsed.get('count') is None else parsed.get('count')}" \
              f"&name_case=nom" \
              f"&access_token={self.__token}" \
              f"&fields=first_name" \
              f"&v={self.__version}"

        response = requests.get(url=url).json()

        if response.get('response') is None:
            print('Ошибка')

        return response.get('response')

    def __get_mutual_friends(self, source_id: int, friend_uids: list) -> dict:
        url = self.__friends_get_mutual + \
              f'?source_uid={source_id}' \
              f'&target_uids=' + ",".join(friend_uids) + \
              f'&access_token={self.__token}' \
              f'&v={self.__version}'

        response_body = requests.get(url=url).json()

        return response_body.get('response')

    def get_friends(self, parsed: dict):
        try:
            self.__token = os.environ['ACCESS_TOKEN']
        except KeyError:
            self.__get_access_token()

        if self.__token is None or len(self.__token) == 0:
            print('Мы не смогли получить токен. Попробуйте позже.')
            return None

        response = self.__get_all_friends(parsed)

        if response is None:
            print('Произошла ошибка')
            return

        count_friends = response.get('count')
        friends = response.get('items')

        target_uids = []

        for person in friends:
            target_uids.append(str(person.get('id')))

        mutual_friends = self.__get_mutual_friends(parsed.get('id'), target_uids)

        info_friends = dict()

        for person in friends:
            info_friends[person.get('id')] = {
                'first_name': person.get('first_name'),
                'last_name': person.get('last_name')
            }

        for person in mutual_friends:
            info_friends.get(person.get('id'))['common_friends_count'] = person.get('common_count')

        for person_id in info_friends:
            hasCommon = info_friends.get(person_id).get('common_friends_count') is not None

            if not hasCommon:
                info_friends.get(person_id)['common_friends_count'] = 0

        friends_list = list(info_friends.values())

        friends_list.sort(key=lambda key: key['common_friends_count'], reverse=True)

        return friends_list
