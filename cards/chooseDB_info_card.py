import copy
card_template={
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [
        {
            "type": "TextBlock",
            "text": "選擇DB、需要的資訊類型",
            "size": "Large",
            "weight": "Bolder"
        },
        {
            "type": "Input.ChoiceSet",
            "id": "choose_db",
            "label": "Choose_DB",
            "value": "",
            "choices": []
        },
        {
            "type": "Input.ChoiceSet",
            "id": "choose_info_type",
            "label": "Choose_Info_Type",
            "value": "",
            "choices": [
                {
                    "title": "cpu",
                    "value": "cpu"
                },
                {
                    "title": "mem",
                    "value": "mem"
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "送出",
            "data": {
                "submit_type": "chooseDB_info"
            }
        }
    ]
}

choices_template= {
                    "title": "test_title",
                    "value": "test_value"
                }

def prepareChooseDBCard(dbnames):    
    cardToReturn=copy.deepcopy(card_template)
    for items in dbnames:
        choiceItem=copy.deepcopy(choices_template)
        choiceItem["title"]=items
        choiceItem["value"]=items
        cardToReturn["body"][1]["choices"]+=[choiceItem]
    # infoOptions=[{'name':'cpu'},{'name':'mem'}]
    # for items in infoOptions:
    #     choiceItem=copy.deepcopy(choices_template)
    #     choiceItem["title"],choiceItem["value"]=items["name"]
    #     cardToReturn["body"][1]["choices"]+=[choiceItem]
    return cardToReturn