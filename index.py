# -*- coding: utf8 -*-
import json

import requests
from config import AUTHORIZATION


# list_id = "61ae07345439df8afcbb15f2"  # "name": "商机线索池 -切入点待验证"
# label: 'id': '61a9f4ef33ccc35e9209fc75', 'name': '新商机',
# label: 'id': '61f14b9893957c737f7e8d8e', 'name': '来源：方案咨询问卷',


def main_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))

    event_json = json.loads(json.dumps(event, indent=2))
    survey_json = json.loads(event_json["body"])

    answers = survey_json['payload']['answer']
    name = ''
    wechat = ''
    phone = ''
    email = ''
    company = ''
    title = ''
    requirement = ''
    solution = ''
    channel = ''
    for question in answers[0]['questions']:
        if 'q-1-sD5N' == question['id']:
            name = question['text']
        elif 'q-2-vkU8' == question['id']:
            wechat = question['text']
        elif 'q-3-iuZ8' == question['id']:
            phone = question['text']
        elif 'q-4-54Wm' == question['id']:
            email = question['text']
        elif 'q-5-ko1N' == question['id']:
            company = question['text']
        elif 'q-6-Uz4g' == question['id']:
            title = question['text']
        elif 'q-8-VSB9' == question['id']:
            requirement = question['text']
        elif 'q-9-ZT1V' == question['id']:
            for option in question['options']:
                solution += option['text'] + ';'
        elif 'q-10-Gukp' == question['id']:
            for option in question['options']:
                channel += option['text'] + ';'

    survey = '姓名：%s \n 微信：%s \n 电话：%s \n 邮箱：%s \n 公司：%s \n 职位：%s \n 需求：%s \n 方案：%s \n 渠道：%s' % (
        name, wechat, phone, email, company, title, requirement, solution, channel)
    template = '''
            {
                "msgtype": "markdown",
                "markdown": {
                    "content": "**方案咨询问卷有新数据了** \n %s"
                }
            }
            '''
    content = template % survey
    r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=81ef7bfa-0ff4-4850-86df-a8e272c8cafe',
                      data=content.encode('utf-8'))
    print(r.status_code)
    print(r.content)
    create_trello_card(survey, name)
    return r.status_code


def create_trello_card(survey, name):
    headers = {'Authorization': AUTHORIZATION, 'Accept': 'application/json'}
    template = '''{
      "desc": "%s",
      "idBoard": "61a9f4eff4d82d5399d26e70",
      "idList": "61ae07345439df8afcbb15f2",
      "idLabels": [
        "61a9f4ef33ccc35e9209fc75",
        "61f14b9893957c737f7e8d8e"
      ],
      "name": "方案咨询 - %s"
    }'''
    content = template % (survey, name)
    r = requests.post('https://api.trello.com/1/cards?idList=61ae07345439df8afcbb15f2',
                      headers=headers, data=content.encode('utf-8'))
    print(r.status_code)
    print(r.content)
