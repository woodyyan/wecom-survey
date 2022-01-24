# -*- coding: utf8 -*-
import json

import requests


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

    template = '''
            {
                "msgtype": "markdown",
                "markdown": {
                    "content": "**方案咨询问卷有新数据了** \n 姓名：%s \n 微信：%s \n 电话：%s \n 邮箱：%s \n 公司：%s \n 职位：%s \n 需求：%s \n 方案：%s \n 渠道：%s"
                }
            }
            '''
    content = template % (name, wechat, phone, email, company, title, requirement, solution, channel)
    r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=81ef7bfa-0ff4-4850-86df-a8e272c8cafe',
                      data=content.encode('utf-8'))
    print(r.status_code)
    print(r.content)
    return r.status_code
