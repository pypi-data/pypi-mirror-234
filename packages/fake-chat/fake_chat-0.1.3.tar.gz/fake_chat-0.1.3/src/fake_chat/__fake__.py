import json
import os
import random
import string
import time
from os import path

import requests
from pandora.openai.auth import Auth0


class fake:
    files_dir: str = os.getcwd()
    proxy: str = None
    is_get_token: bool = True
    is_get_share_token: bool = True
    share_token_expires_in: int = 0
    is_get_pool_token: bool = True
    pool_token: str = ''
    login_wait_time: int = 20

    @staticmethod
    def get_credentials(_credentials_file: str = None):
        if _credentials_file is None:
            _credentials_file = path.join(fake.files_dir, 'credentials.txt')
        try:
            if not path.exists(_credentials_file):
                # 创建文件
                with open(_credentials_file, 'w', encoding='utf-8'):
                    pass
            with open(_credentials_file, 'r', encoding='utf-8') as f_:
                print('credentials_file: {}'.format(_credentials_file))
                credentials_ = f_.read().split('\n')
            credentials_ = [credential.split(',', 1) for credential in credentials_]
            return credentials_
        except Exception as e:
            print('get credentials failed: {}'.format(e))
            return []

    # 登录账号，获取token
    @staticmethod
    def login_get_token(_username: str, _password: str, _proxy: str = None):
        token_info_ = {
            'username': _username,
            'token': 'None'
        }
        try:
            token = Auth0(_username, _password, _proxy).auth(False)
            print('Login success: {}'.format(_username))
            token_info_['token'] = token
        except Exception as e_:
            err_str = str(e_).replace('\n', '').replace('\r', '').strip()
            print('Login failed: {}, {}'.format(_username, err_str))
            token_info_['token'] = 'None'
        return token_info_

    # 使用token 生成share token
    @staticmethod
    def generate_share_token(_unique_name: str = ''.join(random.sample(string.ascii_letters + string.digits, 8)),
                             _token=None,
                             _expires_in: int = 0, _show_conversations: bool = True, _show_userinfo: bool = True,
                             _site_limit: str = '',
                             _proxy: str = None):
        post_data = {
            'unique_name': _unique_name,
            'show_conversations': _show_conversations,
            'show_userinfo': _show_userinfo,
            'site_limit': _site_limit,
            'access_token': _token,
            'expires_in': _expires_in,
        }
        resp = requests.post('https://ai.fakeopen.com/token/register', data=post_data, proxies={
            'http': _proxy,
            'https': _proxy,
        })
        share_token_info_ = {'expire_at': 0, 'show_conversations': _show_conversations, 'show_userinfo': _show_userinfo,
                             'site_limit': _site_limit,
                             'token_key': 'None',
                             'unique_name': 'None'}
        if resp.status_code == 200:
            share_token_info_ = resp.json()
            print('share token: {}'.format(share_token_info_['token_key']))
        else:
            err_str = resp.text.replace('\n', '').replace('\r', '').strip()
            print('share token failed: {}'.format(err_str))
            share_token_info_['token_key'] = 'None'
        return share_token_info_

    # 使用share tokens 生成pool token
    @staticmethod
    def generate_pool_token(_pool_token: str = None, _share_tokens: list = None, _proxy: str = None):
        if not _share_tokens or len(_share_tokens) == 0:
            print('no share token!')
            return None
        post_data = {
            'share_tokens': '\n'.join(_share_tokens),
        }
        if _pool_token and _pool_token != 'None' and len(_pool_token) > 0 and _pool_token != '':
            post_data['pool_token'] = _pool_token
        resp = requests.post('https://ai.fakeopen.com/pool/update', data=post_data, proxies={
            'http': _proxy,
            'https': _proxy
        })
        pool_token_info_ = {
            "count": 0,
            "pool_token": 'None',
        }
        if resp.status_code == 200:
            pool_token_info_ = resp.json()
            print(f'pool token: {pool_token_info_["pool_token"]}')
        else:
            err_str = resp.text.replace('\n', '').replace('\r', '').strip()
            print('generate pool token failed: {}'.format(err_str))
            pool_token_info_['pool_token'] = 'None'
        return pool_token_info_

    @classmethod
    def get_file_path(cls, _file_name):
        return path.join(cls.files_dir, _file_name)

    @classmethod
    def auto_pool_token(cls):
        credentials_file = cls.get_file_path('credentials.txt')
        credentials = fake.get_credentials(_credentials_file=credentials_file)
        token_keys = []
        for credential in credentials:
            if not credential or len(credential) != 2:
                continue

            username, password = credential[0].strip(), credential[1].strip()

            token_info = dict()
            if cls.is_get_token:
                # 显示进度
                progress = '{}/{}'.format(credentials.index(credential) + 1, len(credentials))
                print('Login begin: {}, {}'.format(username, progress))
                # 登录账号，获取token
                token_info = fake.login_get_token(username, password, cls.proxy)
                token_keys.append(token_info)

            if cls.is_get_share_token:
                # 生成share token
                share_token_info = fake.generate_share_token(username, token_info['token'],
                                                             cls.share_token_expires_in,
                                                             _show_conversations=False,
                                                             _show_userinfo=False,
                                                             _proxy=cls.proxy)
                token_info['share_token'] = share_token_info['token_key']
            # 判断是否是最后一个
            if credentials.index(credential) == len(credentials) - 1:
                break
            time.sleep(fake.login_wait_time)

        if cls.is_get_token:
            tokens_file = cls.get_file_path('tokens.txt')
            with open(tokens_file, 'w', encoding='utf-8') as f_:
                for token_info in token_keys:
                    f_.write('{}, {}\n'.format(token_info['username'], token_info['token']))
        if cls.is_get_share_token:
            share_tokens_file = cls.get_file_path('share_tokens.txt')
            with open(share_tokens_file, 'w', encoding='utf-8') as f_:
                for token_info in token_keys:
                    f_.write('{}, {}\n'.format(token_info['username'], token_info['share_token']))

        if cls.is_get_pool_token:
            pool_token_file = cls.get_file_path('pool_token.json')
            if path.exists(pool_token_file) and pool_token_file != '':
                try:
                    with open(pool_token_file, 'r', encoding='utf-8') as f:
                        json_ = json.load(f)
                        cls.pool_token = json_['pool_token']
                except Exception:
                    cls.pool_token = ''
            # 生成pool token
            pool_token_info = fake.generate_pool_token(_pool_token=cls.pool_token,
                                                       _share_tokens=[token_info['share_token'] for token_info in
                                                                      token_keys
                                                                      if
                                                                      token_info['share_token'] != 'None'],
                                                       _proxy=cls.proxy)
            # 输出json格式
            if pool_token_info:
                with open(pool_token_file, 'w', encoding='utf-8') as f_:
                    f_.write(json.dumps(pool_token_info, indent=4, ensure_ascii=False))
