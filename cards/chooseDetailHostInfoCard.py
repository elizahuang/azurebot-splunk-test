import copy
card_template={
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [
        {
            "type": "TextBlock",
            "text": "選擇Host、需要的撈取的時間區間",
            "size": "Large",
            "weight": "Bolder"
        },
        {
            "type": "TextBlock",
            "text": "選定的DB及項目: ",
            "wrap": True
        },
        {
            "type": "Input.ChoiceSet",
            "choices": [
                {
                    "title": "all",
                    "value": "all"
                }
            ],
            "placeholder": "選擇一台或全部Host",
            "label": "Host",
            "id": "choose_host"
        },
        {
            "type": "Input.ChoiceSet",
            "choices": [
                {
                    "title": "sum",
                    "value": "sum"
                },
                {
                    "title": "max",
                    "value": "max"
                },
                {
                    "title": "avg",
                    "value": "avg"
                }
            ],
            "placeholder": "請選擇Aggregation type",
            "id": "aggregation_type",
            "label": "Aggregation"
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "Input.Date",
                            "label": "開始日期",
                            "id": "start_date"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "Input.ChoiceSet",
                            "id": "choose_start_hour",
                            "label": "開始時間",
                            "choices": [
                                {
                                    "title": "凌晨12:00",
                                    "value": "00:00:00"
                                },
                                {
                                    "title": "上午 01:00",
                                    "value": "01:00:00"
                                },
                                {
                                    "title": "上午 02:00",
                                    "value": "02:00:00"
                                },
                                {
                                    "title": "上午 03:00",
                                    "value": "03:00:00"
                                },
                                {
                                    "title": "上午 04:00",
                                    "value": "04:00:00"
                                },
                                {
                                    "title": "上午 05:00",
                                    "value": "05:00:00"
                                },
                                {
                                    "title": "上午 06:00",
                                    "value": "06:00:00"
                                },
                                {
                                    "title": "上午 07:00",
                                    "value": "07:00:00"
                                },
                                {
                                    "title": "上午 08:00",
                                    "value": "08:00:00"
                                },
                                {
                                    "title": "上午 09:00",
                                    "value": "09:00:00"
                                },
                                {
                                    "title": "上午 10:00",
                                    "value": "10:00:00"
                                },
                                {
                                    "title": "上午 11:00",
                                    "value": "11:00:00"
                                },
                                {
                                    "title": "中午 12:00",
                                    "value": "12:00:00"
                                },
                                {
                                    "title": "下午 01:00",
                                    "value": "13:00:00"
                                },
                                {
                                    "title": "下午 02:00",
                                    "value": "14:00:00"
                                },
                                {
                                    "title": "下午 03:00",
                                    "value": "15:00:00"
                                },
                                {
                                    "title": "下午 04:00",
                                    "value": "16:00:00"
                                },
                                {
                                    "title": "下午 05:00",
                                    "value": "17:00:00"
                                },
                                {
                                    "title": "下午 06:00",
                                    "value": "18:00:00"
                                },
                                {
                                    "title": "下午 07:00",
                                    "value": "19:00:00"
                                },
                                {
                                    "title": "下午 08:00",
                                    "value": "20:00:00"
                                },
                                {
                                    "title": "下午 09:00",
                                    "value": "21:00:00"
                                },
                                {
                                    "title": "下午 10:00",
                                    "value": "22:00:00"
                                },
                                {
                                    "title": "下午 11:00",
                                    "value": "23:00:00"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "Input.Date",
                            "label": "結束日期",
                            "id": "end_date"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "Input.ChoiceSet",
                            "id": "choose_end_hour",
                            "label": "結束時間",
                            "choices": [
                                {
                                    "title": "凌晨12:00",
                                    "value": "00:00:00"
                                },
                                {
                                    "title": "上午 01:00",
                                    "value": "01:00:00"
                                },
                                {
                                    "title": "上午 02:00",
                                    "value": "02:00:00"
                                },
                                {
                                    "title": "上午 03:00",
                                    "value": "03:00:00"
                                },
                                {
                                    "title": "上午 04:00",
                                    "value": "04:00:00"
                                },
                                {
                                    "title": "上午 05:00",
                                    "value": "05:00:00"
                                },
                                {
                                    "title": "上午 06:00",
                                    "value": "06:00:00"
                                },
                                {
                                    "title": "上午 07:00",
                                    "value": "07:00:00"
                                },
                                {
                                    "title": "上午 08:00",
                                    "value": "08:00:00"
                                },
                                {
                                    "title": "上午 09:00",
                                    "value": "09:00:00"
                                },
                                {
                                    "title": "上午 10:00",
                                    "value": "10:00:00"
                                },
                                {
                                    "title": "上午 11:00",
                                    "value": "11:00:00"
                                },
                                {
                                    "title": "中午 12:00",
                                    "value": "12:00:00"
                                },
                                {
                                    "title": "下午 01:00",
                                    "value": "13:00:00"
                                },
                                {
                                    "title": "下午 02:00",
                                    "value": "14:00:00"
                                },
                                {
                                    "title": "下午 03:00",
                                    "value": "15:00:00"
                                },
                                {
                                    "title": "下午 04:00",
                                    "value": "16:00:00"
                                },
                                {
                                    "title": "下午 05:00",
                                    "value": "17:00:00"
                                },
                                {
                                    "title": "下午 06:00",
                                    "value": "18:00:00"
                                },
                                {
                                    "title": "下午 07:00",
                                    "value": "19:00:00"
                                },
                                {
                                    "title": "下午 08:00",
                                    "value": "20:00:00"
                                },
                                {
                                    "title": "下午 09:00",
                                    "value": "21:00:00"
                                },
                                {
                                    "title": "下午 10:00",
                                    "value": "22:00:00"
                                },
                                {
                                    "title": "下午 11:00",
                                    "value": "23:00:00"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "送出",
            "data": {
                "submit_type": "chooseDetail_HostInfo"
            }
        }
    ]
}

choice_template= {
                    "title": "Choice 1",
                    "value": "Choice 1"
                }

def prepareHostDetailCard(sio,client_id,db_specifications):
    cardToReturn=copy.deepcopy(card_template)
    cardToReturn["body"][1]["text"]="選定查看的項目: "
    for key in db_specifications:
        cardToReturn["body"][1]["text"]+=" "
        cardToReturn["body"][1]["text"]+=db_specifications.get(key)
    ##問Host, sockerio
    hosts=[{'name':'host1111'},{'name':'host2222'},{'name':'host3333'},{'name':'host4444'}]
    for host in hosts:
        choice=copy.deepcopy(choice_template) 
        choice['title']=host['name']
        choice['value']=host['name']
        cardToReturn["body"][2]["choices"]+=[choice]
    


    return cardToReturn