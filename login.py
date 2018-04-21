from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError
from json import loads
from uuid import uuid4

def get_json(url):
    res = urlopen(url)
    b = res.read().decode('utf-8')
    return loads(b)

def get_conf(filename):
    f = open(filename)
    b = f.readlines()
    f.close()
    dic = dict()
    for i in b:
        k, v = i.split('=')
        dic[k] = v[:-1]
    return dic

def generate_state():
    return str(uuid4())

def get_auth(client_id, callback_url, state):
    url = 'https://nid.naver.com/oauth2.0/authorize?%s'
    params = {
                'client_id'     : client_id,
                'redirect_url'  : callback_url,
                'response_type' : 'code',
                'state'         : state
    }
    return url % urlencode(params)

def get_token(client_id, client_secret, state, code):
    url = 'https://nid.naver.com/oauth2.0/token?%s'
    params = {
                'client_id'     : client_id,
                'client_secret' : client_secret,
                'grant_type'    : 'authorization_code',
                'state'         : state,
                'code'          : code
    }
    params = urlencode(params)
    return get_json(url % params)

def refresh_token(client_id, client_secret, refresh_token):
    url = 'https://nid.naver.com/oauth2.0/token?%s'
    params = {
                'grant_type'    : 'refresh_token',
                'client_id'     : client_id,
                'client_secret' : client_secret,
                'refresh_token' : refresh_token
    }
    params = urlencode(params)
    return get_json(url % params)

def delete_token(client_id, client_secret, access_token):
    url = 'https://nid.naver.com/oauth2.0/token?%s'
    params = {
                'grant_type'        : 'delete',
                'client_id'         : client_id,
                'client_secret'     : client_secret,
                'access_token'      : access_token,
                'service_provider'  : 'NAVER'
    }
    params = urlencode(params)
    return get_json(url % params)

def get_profile(token):
    url = 'https://openapi.naver.com/v1/nid/me'
    headers = {'Authorization': 'Bearer ' + token}
    req = Request(url, headers=headers)
    return get_json(req)
