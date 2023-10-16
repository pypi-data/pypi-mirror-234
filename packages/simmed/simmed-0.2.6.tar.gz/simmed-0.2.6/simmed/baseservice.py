import json
from flask import request
from simmed.simmed_jsonrpc import SimMedError


class BaseService(object):

    def __init__(self, flask_app):
        '''初始化'''
        self.app = flask_app

    def current_user(self):
        """
           获取当前登录的用户信息
        Returns:
            _type_: user
        """
        weAppAuthorization = request.headers['weappauthorization'] if request.headers and 'weappauthorization' in request.headers else ''
        user_str = self.app.config['REDIS_STORE'].get(weAppAuthorization)
        if not user_str:
            raise SimMedError("尚未登录!")

        user = json.loads(user_str)
        if 'SessionKey' not in user:
            raise SimMedError("尚未登录!")

        self.app.config['REDIS_STORE'].expire(
            user['SessionKey'], 60*300)
        return user
