import requests
import time
import json

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class User:
    def __init__(self, TOKEN, user_id):
        self.token = TOKEN
        if isinstance(user_id, int) or user_id.isdigit():
            self.user_id = int(user_id)
        else:
            self.user_id = self.get_ids(user_id)

    def get_params(self):
        return {
            'access_token': self.token,
            'v': 5.91
        }
      
    def get_ids(self, user):
        params = self.get_params()
        params['user_ids'] = user
        response = requests.get('https://api.vk.com/method/users.get', params)
        json_doc = response.json()
        user_id = json_doc['response'][0]['id']
        return user_id
 
    def get_user_groups(self):
        groups_ids_list = []
        params = self.get_params()
        params['user_id'] = self.user_id
        params['extended'] = '1'
        params['fields'] = 'name', 'members_count'
        URL = 'https://api.vk.com/method/groups.get'
        response = requests.get(URL, params)
        
        for group_item in response.json()['response']['items']:
            if not group_item.get('deactivated') == 'banned':
                groups_ids_list.append(
                    {'group_id': group_item['id'],
                     'members_count': group_item['members_count'],
                     'name': group_item['name']
                     }
                )
            else:
                print(f'Ошибка при добавлении в список. Группа {group_item["id"]} деактивирована.')
        return groups_ids_list
    
    def get_group_members(self, group_info):
        params = self.get_params()
        params['group_id'] = group_info['group_id']
        params['filter'] = 'friends'    
        URL = 'https://api.vk.com/method/groups.getMembers'
        response = requests.get(URL, params)
        

        if response.json()['response']['count'] == 0:
            groups_dict = {
                "group_id": group_info['group_id'],
                "group_name": group_info['name'],
                'members_count': group_info['members_count']
            }
            return groups_dict
        else:
            return None             
        
if __name__ == '__main__':
    
    Evgen = User(TOKEN, 'eshmargunov')
    
    with open('groups.json', 'w', encoding='utf-8') as output:
        json_file = []
        groups = Evgen.get_user_groups()
        for group_info in groups:
            print('...processing...')
            data = Evgen.get_group_members(group_info)
            time.sleep(0.4)
            if data:
                json_file.append(data)
        json.dump(json_file, output, ensure_ascii=False, indent=4)
        print('Готово. Проверьте json файл.')