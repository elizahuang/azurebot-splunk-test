# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys,os,json
import traceback
import socketio
from datetime import datetime

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes,ConversationReference

from bot import MyBot,ADAPTER,CONFIG,CONVERSATION_REFERENCES
from generateChart import plotPicAnd2Base64


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error


# Create the Bot

# ## creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins='*')
BOT = MyBot(sio,CONVERSATION_REFERENCES)
APP = web.Application(middlewares=[aiohttp_error_middleware])
BOT.sio.attach(APP) #attach websocket to web app


async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=201)



async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the event we wish to listen out for
@sio.on('message')
async def print_message(sid, message):
    # When we receive a new event of type 'message' through a socket.io connection
    # we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)
    await sio.emit('message', message[::-1])

@sio.on('dbnames')
async def getDbNames(sid, data):
    print('data: ',data)
    await BOT._send_proactive_message(dataToSend=data['dbnames'],type=data['type'],userid=data['userid'])

@sio.on('dbhosts')
async def getDbHosts(sid, data):  
    print('data: ',data)  
    await BOT._send_proactive_message(dataToSend=data,type=data['type'],userid=data['userid'])

@sio.on('img')
async def save_img(sid, data):
    print(data)
    print(type(data))
    await BOT._send_proactive_message(dataToSend=f"data:image/jpg;base64,{plotPicAnd2Base64(data)}",type='base64img',userid=data['userid'])#data is userid
    # await BOT._send_proactive_message(dataToSend=data['img'],type='base64img',userid=data['userid'])#data is userid

@sio.event
def connect(sid, environ, auth):
    BOT.client_sid=sid
    print('connect ', BOT.client_sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

APP.router.add_post("/api/messages", messages)
APP.router.add_get('/', index)



if __name__ == "__main__":
    try:
        # web.run_app(APP, host="localhost", port=CONFIG.PORT)
        port = os.getenv('PORT', default=CONFIG.PORT)
        web.run_app(APP,port=port)
    except Exception as error:
        raise error
