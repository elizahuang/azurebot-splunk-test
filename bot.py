
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, CardFactory, MessageFactory, BotFrameworkAdapterSettings,BotFrameworkAdapter
from botbuilder.schema import AnimationCard,MediaUrl, SigninCard,OAuthCard,ChannelAccount, HeroCard, CardAction, CardImage, ActionTypes, Attachment, Activity, ActivityTypes,ConversationReference, SuggestedActions,ThumbnailCard
from botbuilder.dialogs.choices import Choice
import json,os,requests
import base64
from typing import Dict
from config import DefaultConfig
from cards.chooseDB_info_card import *
from cards.chooseDetailHostInfoCard import *

CONFIG = DefaultConfig()
# Create adapter.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD) #creating a setting object with app_id, app_password
ADAPTER = BotFrameworkAdapter(SETTINGS) # creating adapter with the setting object
# Create a shared dictionary.  The Bot will add conversation references when users
# join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()

# create a hero card for testing, azure provides multiple kinds of cards, 
# however the most often used card in this small project is adaptive card, which supports input box, buttons, and other components. 
def create_hero_card() -> Attachment:
    file = os.path.join(os.getcwd(), "cost.jpg")
    image = open(file, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read).decode()
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


# MyBot class handles the bot logic, and inherited the ActivityHandler class provided by the bot framework
# Currently, the 'MyBot' class distinguish activities with different activity types and handle them with different handler functions
# Activities of the same type got differnt responses to send to users, according to the contents in the activity, 
# such as, the 'text' or 'value' in message activities 
class MyBot(ActivityHandler):
    contextToReturn = None #the content that eventually send to the channel that user uses, may be a string or a card 
    def __init__(self, sio,conversation_references: Dict[str, ConversationReference],client_sid=None):
        self.sio=sio # the socket server object
        self.conversation_references = conversation_references # dictionary used to save users' conversation reference
        self.client_sid=client_sid #whenever socket server connected to socket client, record the id of the socket client for later use to emit contents
    async def on_message_activity(self, turn_context: TurnContext):
        ## activity triggered by a btn is also msg activity
        print('***********dealing with msg event**********')  
        print((turn_context.activity)) # contents infos of the incoming activity
        #azure's as_dict() function, enables attributes in objects be showed
        print('turn_context_from_property: \n',turn_context.activity.from_property.as_dict()) #print where the activity is from        
        print('turn_context_conversation: \n',turn_context.activity.conversation.as_dict()) #print infos about the conversation, tenant id is also listed here
        print('turn_context_recipient: \n',turn_context.activity.recipient.as_dict()) #print who the recipient of the activity is 

        if turn_context.activity.text != None:
          if 'proactive' in turn_context.activity.text : # testing sending proactive msg
              userid=self._add_conversation_reference(turn_context.activity) #add the conversation reference to dict for later use
              await self._send_proactive_message(userid=userid) # send 'Testing proactive msg' to user
              return

          elif 'card' in turn_context.activity.text :
              cardAtt = create_hero_card()
              contextToReturn = MessageFactory.attachment(cardAtt)

          elif 'dbInfo' in turn_context.activity.text:
              userid=self._add_conversation_reference(turn_context.activity)
              print({'userid': userid,'type':'dbnames_for_dbcards'})
              print('self.client_sid:',self.client_sid)
              await self.sio.emit('dbnames',{'userid': userid,'type':'dbnames_for_dbcards'}, to=self.client_sid) #ask socket client to send dbnames
              contextToReturn ='dbname request sent'       
          else:
              contextToReturn = f"You said '{ turn_context.activity.text }'" #echo the msg
        elif turn_context.activity.value != None:
          userid=self._add_conversation_reference(turn_context.activity) 
          if turn_context.activity.value['submit_type']!=None:
            if turn_context.activity.value['submit_type']=='chooseDB_info':
              
              variableToPass={'choose_db':turn_context.activity.value['choose_db'],
                              'choose_info_type': turn_context.activity.value['choose_info_type'],
                              'userid':userid,
                              'type':'hostname_for_dbcards'
                              }     
              print(variableToPass)
              await self.sio.emit('dbhosts',variableToPass, to=self.client_sid) #ask socket client to send dbhosts
              contextToReturn='dbhost request sent' 

            elif turn_context.activity.value['submit_type']=='chooseDetail_HostInfo':
                print('*************chooseDetail_HostInfo***********',turn_context.activity.value)
                variableToPass=turn_context.activity.value
                variableToPass["start_time"]=variableToPass["start_date"]+"T"+variableToPass["choose_start_hour"]
                variableToPass["end_time"]=variableToPass["end_date"]+"T"+variableToPass["choose_end_hour"]
                from datetime import datetime
                if datetime.strptime(variableToPass["start_time"],"%Y-%m-%dT%H:%M:%S")<=datetime.strptime(variableToPass["end_time"],"%Y-%m-%dT%H:%M:%S"):
                    variableToPass["userid"]=userid
                    variableToPass['choose_host']=json.loads(variableToPass['choose_host'])['choose_host']
                    del variableToPass["start_date"]
                    del variableToPass["end_date"]
                    del variableToPass["choose_start_hour"]
                    del variableToPass["choose_end_hour"]
                    del variableToPass["submit_type"]
                    print('variableToPass_needPic',variableToPass)
                    await self.sio.emit('need-pic',variableToPass, to=self.client_sid) #send what the user chose and ask socket client to send info of the data points
                    contextToReturn='dbpic request sent'
                else:
                    contextToReturn='Start datetime should be earlier than end datetime.\nPlease retry.'
  
        await turn_context.send_activity(contextToReturn)
        print()

    # send proactive msg to certain user
    # uses the shared Dictionary that the Bot adds conversation references to.
    async def _send_proactive_message(self,dataToSend=None,type=None,userid=None):
        contextToReturn=None
        # print('***********tenant_id**********',turn_context.activity.channel_data['tenant']['id'])
        print('****userid****',userid)
        if type=='base64img':
            herocard = HeroCard(images=[CardImage(url=dataToSend)])
            contextToReturn=MessageFactory.attachment(CardFactory.hero_card(herocard))
        elif type=='dbnames_for_dbcards':
            contextToReturn=MessageFactory.attachment(Attachment(
                    content_type='application/vnd.microsoft.card.adaptive', content=prepareChooseDBCard(dataToSend)))
        elif type=='hostname_for_dbcards':
            contextToReturn=MessageFactory.attachment(Attachment(
                    content_type='application/vnd.microsoft.card.adaptive', content=prepareHostDetailCard(dataToSend)))            
        else: 
            contextToReturn = "Testing proactive msg"
        print('CONVERSATION_REFERENCES.values\n',CONVERSATION_REFERENCES)

        # # Send a message to all conversation members.
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
        return #await self._send_suggested_actions(conversation_reference)

    # act when there is member added
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
        return # await self._send_suggested_actions(turn_context)

    # add conversation reference to the dict
    def _add_conversation_reference(self, activity: Activity):
        """
        This populates the shared Dictionary that holds conversation references. In this sample,
        this dictionary is used to send a message to members when /api/notify is hit.
        :param activity:
        :return:
        """
        conversation_reference = TurnContext.get_conversation_reference(activity)
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference
        return conversation_reference.user.id

    # send suggested action whenever after every response activity sent
    '''
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
    '''