# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, CardFactory, MessageFactory
from botbuilder.schema import AnimationCard,MediaUrl, SigninCard,OAuthCard,ChannelAccount, HeroCard, CardAction, CardImage, ActionTypes, Attachment, Activity, ActivityTypes
from botbuilder.dialogs.choices import Choice
# import requests,socketio
import json,os,requests
import base64
# from app import sio



def create_hero_card() -> Attachment:
    file = os.path.join(os.getcwd(), "cost.jpg")
    image = open(file, 'rb')
    image_read = image.read()
    # image_64_encode = base64.encodebytes(image_read) #encodestring also works aswell as decodestring
    # encodestring also works aswell as decodestring
    image_64_encode = base64.b64encode(image_read).decode()
    # images=[
    #     CardImage(
    #         url="https://ct.yimg.com/xd/api/res/1.2/VhPkyLMc5NAyXyGfjLgA5g--/YXBwaWQ9eXR3YXVjdGlvbnNlcnZpY2U7aD01ODU7cT04NTtyb3RhdGU9YXV0bzt3PTcwMA--/https://s.yimg.com/ob/image/82cbd7d4-5802-4b2b-99bd-690512b34730.jpg"
    #     )],#https://sec.ch9.ms/ch9/7ff5/e07cfef0-aa3b-40bb-9baa-7c9ef8ff7ff5/buildreactionbotframework_960.jpg
    # buttons=[
    #     CardAction(type=ActionTypes.open_url,title="url1",value="https://www.google.com"),
    #     CardAction(type=ActionTypes.open_url,title="url2",value="https://www.yahoo.com"),
    #     ])
                            # name="cost.jpg",
                            # content_type="image/jpg",
    herocard = HeroCard(title="推薦以下兩個選項",
                        images=[CardImage(
                            url=f"data:image/jpg;base64,{image_64_encode}")
                        ],
                        buttons=[
                            CardAction(type=ActionTypes.open_url,
                                       title="url1", value="https://www.google.com"),
                            CardAction(type=ActionTypes.open_url,
                                       title="url2", value="https://www.yahoo.com"),
                        ])
    return CardFactory.hero_card(herocard)


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    contextToReturn = None
    def __init__(self, sio,client_sid=None):
        self.sio=sio
        self.client_sid=client_sid
    async def on_message_activity(self, turn_context: TurnContext):
        print((turn_context.activity))
        # print('activity: ',json.dumps(turn_context.activity, sort_keys=True, indent=4),'\n')
        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        if turn_context.activity.text == 'todo':
            contextToReturn = requests.get(
                'https://jsonplaceholder.typicode.com/todos/1').content.decode('utf-8')
        elif turn_context.activity.text == 'my_ehr':
            contextToReturn = 'https://myehr'
        elif turn_context.activity.text == 'card':
            cardAtt = create_hero_card()
            contextToReturn = MessageFactory.attachment(cardAtt)

        elif turn_context.activity.text == 'getPic':
            contextToReturn ='pic request sent'
            # print('(type)turn_context.activity.channel_data\n',type(turn_context.activity.channel_data))
            # print('turn_context.activity.channel_data\n',turn_context.activity.channel_data['tenant']['id'])
            
            await self.sio.emit('need-pic',{'data': turn_context.activity.channel_data['tenant']['id']}, to=self.sid)#,namespace="/"
        else:
            contextToReturn = f"You said '{ turn_context.activity.text }'"
        await turn_context.send_activity(contextToReturn)
        print()

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
