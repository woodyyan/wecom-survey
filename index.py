# -*- coding: utf8 -*-
import json
import requests


def main_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))

    event_json = json.loads(json.dumps(event, indent=2))
    survey_json = json.loads(event_json["body"])

    answers = survey_json['payload']['answer']
    content = ''
    for answer in answers:
        content += str(answer)
    r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=81ef7bfa-0ff4-4850-86df-a8e272c8cafe',
                      data=content.encode('utf-8'))
    print(r.status_code)
    print(r.content)
    return r.status_code
