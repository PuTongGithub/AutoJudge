import requests
from lxml import etree

#get login page
page_url = 'http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp'
page_r = requests.get(page_url)

xml_tree = etree.HTML(page_r.content)
lt = xml_tree.xpath('//input[@name="lt"]/@value')
execution = xml_tree.xpath('//input[@name="execution"]/@value')
_eventId = xml_tree.xpath('//input[@name="_eventId"]/@value')
rmShown = xml_tree.xpath('//input[@name="rmShown"]/@value')

#set username and password
username = '...'
password = '...'

#login, get cookie
log_headers = {
    'Cookie': page_r.headers['Set-Cookie'],
}
formdata = {
    'username': username,
    'password': password,
    'submit': '',
    'lt': lt[0],
    'execution': execution[0],
    '_eventId': _eventId[0],
    'rmShown': rmShown[0]
}
login_times = 3
while login_times > 0:
    log_r = requests.post(page_url, data = formdata, headers = log_headers)
    login_times -= 1
    if(log_r.url == 'http://jwxt.xidian.edu.cn/caslogin.jsp'): break
else:
    print('login fail!')
    import sys
    sys.exit()

#get teachers list
table_url = 'http://jwxt.xidian.edu.cn/jxpgXsAction.do?oper=listWj'
table_headers = {
    'Cookie': log_r.history[1].headers['Set-Cookie'],
}
table_r = requests.get(table_url, headers = table_headers)
xml_tree = etree.HTML(table_r.text)
names = xml_tree.xpath('//img[@src="/img/icon/edit.gif"]/@name')

for name in names:
    data = name.split('#@')
    #get pre judge page
    prep_url = 'http://jwxt.xidian.edu.cn/jxpgXsAction.do'
    formdata = {
        'wjbm': data[0],
        'bpr': data[1],
        'pgnr': data[5],
        'oper': 'wjShow',
        'wjmc': data[3],
        'bprm': data[2],
        'pgnrm': data[4],
        'wjbz': 'null',
        'pageSize': '20',
        'page': '1',
        'currentPage': '1',
        'pageNo': ''
    }
    prep_r = requests.post(prep_url, data = formdata, headers = table_headers)

    #post judge
    post_url = 'http://jwxt.xidian.edu.cn/jxpgXsAction.do?oper=wjpg'
    post_headers = {
        'Cookie': log_r.history[1].headers['Set-Cookie'],
    }
    formdata = {
        'wjbm': data[0],
        'bpr': data[1],
        'pgnr': data[5],
        'xumanyzg': 'zgDA_0000000037',
        'wjbz': '',
        '0000000017': '8_1',
        '0000000019': '6_1',
        '0000000018': '6_1',
        '0000000020': '6_1',
        '0000000021': '7_1',
        '0000000022': '7_1',
        '0000000023': '7_1',
        '0000000025': '7_1',
        '0000000024': '6_1',
        '0000000026': '8_1',
        '0000000027': '8_1',
        '0000000028': '6_1',
        '0000000029': '6_1',
        '0000000030': '6_1',
        '0000000031': '6_1',
        'DA_0000000037': '',
        'zgpj': ''
    }
    post_r = requests.post(post_url, data = formdata, headers = post_headers)
