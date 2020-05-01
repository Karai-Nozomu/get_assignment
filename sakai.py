import requests
import json
from bs4 import BeautifulSoup

def ses_get_login_data(ses, url):
    re = ses.get(url)
    soup = BeautifulSoup(re.content, 'html.parser')
    lt = soup.find_all('input')[3]['value']
    res_url = re.url
    return lt, res_url

def ses_get_json(ses, url):
    headers = {'content-type' : 'application/json'}
    re = ses.get(url)
    return re.json()

def ses_login(ses, userid, password):
    login_url = 'https://cas.ecs.kyoto-u.ac.jp/cas/login'
    lt, res_url = ses_get_login_data(ses, login_url)
    login_data = {
        'username' : userid,
        'password' : password,
        'lt' : lt,
        'execution' : 'e1s1',
        '_eventId' : 'submit',
        'submit' : '%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3',
    }
    login = ses.post(res_url, data=login_data)

def ses_get_ass_list(ses):
    ass_list = []
    ass_url = 'https://panda.ecs.kyoto-u.ac.jp/direct/assignment/my.json'
    class_url = 'https://panda.ecs.kyoto-u.ac.jp/direct/site.json'
    ass_data = ses_get_json(ses, ass_url)
    class_data = ses_get_json(ses, class_url)
    ass_dict = ass_data['assignment_collection']
    class_dict = class_data['site_collection']
    for i in range(len(ass_dict)):
        if(ass_dict[i]['status'] == '公開'):
            ass_list.append(ass_dict[i]['context'] + '  ' + ass_dict[i]['dropDeadTimeString'])
    ass_str = ','.join(ass_list)
    for i in range(len(class_dict)):
        ass_str = ass_str.replace(class_dict[i]['id'], class_dict[i]['title'])
    return ass_str.split(',')
