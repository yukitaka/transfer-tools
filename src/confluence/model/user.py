from src.utils import store

class User:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_user_by_id(user_id):
        user = store.load_json(f'data/confluence/users/{user_id}.json')

        return User(str.strip(user['displayName'].replace('(Unlicensed)', '')))



