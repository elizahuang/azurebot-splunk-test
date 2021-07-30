# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, CardFactory, MessageFactory, BotFrameworkAdapterSettings,BotFrameworkAdapter
from botbuilder.schema import AnimationCard,MediaUrl, SigninCard,OAuthCard,ChannelAccount, HeroCard, CardAction, CardImage, ActionTypes, Attachment, Activity, ActivityTypes,ConversationReference, SuggestedActions,ThumbnailCard
from botbuilder.dialogs.choices import Choice
# import requests,socketio
import json,os,requests
import base64
# from app import sio
from typing import Dict
from config import DefaultConfig

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
# Create a shared dictionary.  The Bot will add conversation references when users
# join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()

adapCard={
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.0",
  "body": [
    {
      "type": "Container",
      "items": [
        {
          "type": "TextBlock",
          "text": "Publish Adaptive Card schema",
          "weight": "bolder",
          "size": "medium"
        },
        {
          "type": "ColumnSet",
          "columns": [
            {
              "type": "Column",
              "width": "auto",
              "items": [
                {
                  "type": "Image",
                  "url": "https://pbs.twimg.com/profile_images/3647943215/d7f12830b3c17a5a9e4afcc370e3a37e_400x400.jpeg",
                  "size": "small",
                  "style": "person"
                }
              ]
            },
            {
              "type": "Column",
              "width": "stretch",
              "items": [
                {
                  "type": "TextBlock",
                  "text": "Matt Hidinger",
                  "weight": "bolder",
                  "wrap": True
                },
                {
                  "type": "TextBlock",
                  "spacing": "none",
                  "text": "Created {{DATE(2017-02-14T06:08:39Z, SHORT)}}",
                  "isSubtle": True,
                  "wrap": True
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "Container",
      "items": [
        {
          "type": "TextBlock",
          "text": "Now that we have defined the main rules and features of the format, we need to produce a schema and publish it to GitHub. The schema will be the starting point of our reference documentation.",
          "wrap": True
        },
        {
          "type": "FactSet",
          "facts": [
            {
              "title": "Board:",
              "value": "Adaptive Card"
            },
            {
              "title": "List:",
              "value": "Backlog"
            },
            {
              "title": "Assigned to:",
              "value": "Matt Hidinger"
            },
            {
              "title": "Due date:",
              "value": "Not set"
            }
          ]
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.ShowCard",
      "title": "Comment",
      "card": {
        "type": "AdaptiveCard",
        "body": [
          {
            "type": "Input.Text",
            "id": "comment",
            "isMultiline": True,
            "placeholder": "Enter your comment"
          }
        ],
        "actions": [
          {
            "type": "Action.Submit",
            "title": "OK"
          }
        ]
      }
    },
    {
      "type": "Action.OpenUrl",
      "title": "View",
      "url": "https://adaptivecards.io"
    }
  ]
}


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
    def __init__(self, sio,conversation_references: Dict[str, ConversationReference],client_sid=None):
        self.sio=sio
        self.conversation_references = conversation_references
        self.client_sid=client_sid
    async def on_message_activity(self, turn_context: TurnContext):
        print('***********dealing with msg event**********')  ## submit btn is also msg activity
        print((turn_context.activity))
        # print('activity: ',json.dumps(turn_context.activity, sort_keys=True, indent=4),'\n')
        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        if turn_context.activity.text == 'proactive':
            userid=self._add_conversation_reference(turn_context.activity)
            await self._send_proactive_message(userid=userid)
            
        if turn_context.activity.text == 'todo':
            contextToReturn = requests.get(
                'https://jsonplaceholder.typicode.com/todos/1').content.decode('utf-8')
        elif turn_context.activity.text == 'my_ehr':
            contextToReturn = 'https://myehr'
        elif turn_context.activity.text == 'card':
            cardAtt = create_hero_card()
            contextToReturn = MessageFactory.attachment(cardAtt)
        elif turn_context.activity.text=='adaptive':
            contextToReturn =MessageFactory.attachment(Attachment(content_type='application/vnd.microsoft.card.adaptive',
                                      content=adapCard))
        elif turn_context.activity.text == 'getPic':
            contextToReturn ='pic request sent'
            # print('(type)turn_context.activity.channel_data\n',type(turn_context.activity.channel_data))
            # print('turn_context.activity.channel_data\n',turn_context.activity.channel_data['tenant']['id'])
            userid=self._add_conversation_reference(turn_context.activity)
            # turn_context.activity.channel_data['tenant']['id']
            await self.sio.emit('need-pic',{'data': userid}, to=self.client_sid)#,namespace="/"
        else:
            contextToReturn = f"You said '{ turn_context.activity.text }'"
        await turn_context.send_activity(contextToReturn)
        return await self._send_suggested_actions(turn_context)
        print()
    # # Send a message to all conversation members.
    # # This uses the shared Dictionary that the Bot adds conversation references to.
    async def _send_proactive_message(self,dataToSend=None,type=None,userid=None):
        contextToReturn=None
        # print('***********tenant_id**********',turn_context.activity.channel_data['tenant']['id'])
        print('****userid****',userid)
        if type=='base64img':
            herocard = HeroCard(title="yourPic",
                        images=[CardImage(
                            url=dataToSend)
                        ])
            contextToReturn=MessageFactory.attachment(CardFactory.hero_card(herocard))
        else: 
            contextToReturn = "Testing proactive msg"
        print('CONVERSATION_REFERENCES.values\n',CONVERSATION_REFERENCES)
        
        # for conversation_reference in CONVERSATION_REFERENCES.values():
        #     print('proactive event type: ',type)
        #     await ADAPTER.continue_conversation(
        #         conversation_reference,
        #         lambda turn_context: turn_context.send_activity(contextToReturn),
        #         CONFIG.APP_ID,
        #     )
        conversation_reference=CONVERSATION_REFERENCES[userid]
        await ADAPTER.continue_conversation(
            conversation_reference,
            lambda turn_context: turn_context.send_activity(contextToReturn),
            CONFIG.APP_ID,
        )
        return await self._send_suggested_actions(conversation_reference)

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
        return await self._send_suggested_actions(turn_context)

    def _add_conversation_reference(self, activity: Activity):
        """
        This populates the shared Dictionary that holds conversation references. In this sample,
        this dictionary is used to send a message to members when /api/notify is hit.
        :param activity:
        :return:
        """
        conversation_reference = TurnContext.get_conversation_reference(activity)
        # print('*************conversation_ref to json************\n',json.dumps(conversation_reference.__dict__))
        # print('*************conversation_ref to json************')
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference
        return conversation_reference.user.id

    async def _send_suggested_actions(self, turn_context: TurnContext):
        reply = ThumbnailCard(
            title="option list",
            text="Welcome for using the services",
            buttons=[
                CardAction(
                    displayText="CPU Info for Host",
                    title="CPU Info for Host",
                    type=ActionTypes.im_back,
                    value="cpu_info",
                    image="https://ct.yimg.com/xd/api/res/1.2/VhPkyLMc5NAyXyGfjLgA5g--/YXBwaWQ9eXR3YXVjdGlvbnNlcnZpY2U7aD01ODU7cT04NTtyb3RhdGU9YXV0bzt3PTcwMA--/https://s.yimg.com/ob/image/82cbd7d4-5802-4b2b-99bd-690512b34730.jpg",
                    # image_alt_text="CPU Info for Host",
                ),
                CardAction(
                    displayText="Mem Info for Host",
                    title="Mem Info for Host",
                    type=ActionTypes.im_back,
                    value="mem_info",
                    image="https://ct.yimg.com/xd/api/res/1.2/VhPkyLMc5NAyXyGfjLgA5g--/YXBwaWQ9eXR3YXVjdGlvbnNlcnZpY2U7aD01ODU7cT04NTtyb3RhdGU9YXV0bzt3PTcwMA--/https://s.yimg.com/ob/image/82cbd7d4-5802-4b2b-99bd-690512b34730.jpg",
                    # image_alt_text="Mem Info for Host",
                )])         
        
        await turn_context.send_activity(MessageFactory.attachment(CardFactory.thumbnail_card(reply)))