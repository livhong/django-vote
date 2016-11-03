import json

from poll.models import User

class UserSerializer():
    @staticmethod
    def parse(userStr):
        data = json.loads(userStr)
        user_data = {
            'nickname': data['nickname'],
            'openid': data['openid'],
            'headimgurl': data['headimgurl'],
            'sex': data['sex'],
            'city': data['city'],
            'country': data['country'],
            'id': data['id']
        }
        if 'unionid' in data:
            user_data.update('unionid', data.unionid)
        user = User(**user_data)
        return user

    @staticmethod
    def toString(user):
        user_data = {
            'nickname': user.nickname,
            'openid': user.openid,
            'headimgurl': user.headimgurl,
            'sex': user.sex,
            'city': user.city,
            'country': user.country,
            'unionid': user.unionid,
            'id': user.id
        }
        userStr = json.dumps(user_data)
        return str(userStr)