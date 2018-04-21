#!/usr/bin/python3

from bottle import route, post, redirect, run, request, response, template

import login
import cafe

@route('/')
def index():
    redirect(login_url)

@route('/callback')
def callback():
    new_state = request.GET.state

    if new_state != state:
        response.status = 401
        return 'error'
    
    global code
    code = request.GET.code
    redirect('/get_token')

@route('/get_token')
def get_token():
    json = login.get_token(client_id, client_secret, state, code)
    global access_token, refresh_token
    access_token = json['access_token']
    refresh_token = json['refresh_token']
    redirect('/write')

@route('/refresh_token')
def refresh_token_():
    refresh_token = conf['refresh_token']
    json = login.refresh_token(client_id, client_secret, refresh_token)
    global access_token
    access_token = json['access_token']
    return json

@route('/get_profile')
def get_profile():
    return login.get_profile(access_token)

@route('/write')
def write():
    return template('write.html')

@post('/action')
def action():
    clubid = request.forms.clubid
    menuid = request.forms.menuid
    subject = request.forms.subject
    content = request.forms.content
    return cafe.write(access_token, clubid, menuid, subject, content)

conf = login.get_conf('naver.conf')
client_id = conf['client_id']
client_secret = conf['client_secret']
callback_url = conf['callback_url']
state = login.generate_state()

login_url = login.get_auth(client_id, callback_url, state)

run(host='0.0.0.0')
