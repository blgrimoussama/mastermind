from quart import Quart
from quart import render_template, jsonify
from bot import Bot
from hypercorn.config import Config
from hypercorn.asyncio import serve
from requests import Request
import asyncio
import json
import os.path
import time
import requests

import nest_asyncio

nest_asyncio.apply()

TOKEN = os.environ['paperrocker']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
SCOPE = 'user_read'

app = Quart(__name__)
channel = 'nightousama'
bot = Bot(TOKEN, channel)

# The chat page variables
messages = []
message_id = 1
messages_path = os.path.join('json/' + channel, "messages.json")
# Mastermind variables
mastermind_path = os.path.join('json/' + channel, "mastermind.json")
mastermind_leaderboard = os.path.join('json/' + channel,
                                      "mastermind_leaderboard.json")
mastermind_data = {}


def reset_json():
    default_url = "https://static-cdn.jtvnw.net/user-default-pictures-uv/ebb84563-db81-4b9c-8940-64ed33ccfc7b-profile_image-300x300.png"
    mastermind_data = {}
    mastermind_data['guesses'] = {}
    mastermind_data['players'] = {
        "versus": [{
            "name": "",
            "url": default_url
        }, {
            "name": "",
            "url": default_url
        }],
        "next":
        None
    }
    dictt = {}
    sub_dict = {}
    for ind in range(4):
        dictt[ind] = '#fff'
        sub_dict[ind] = '#aaa'
    for i in range(9):
        dictt['matches'] = sub_dict
        mastermind_data['guesses'][i] = dictt
    with open(mastermind_path, 'w') as f:
        json.dump(mastermind_data, f, indent=4)


reset_json()


def prepare_url(URL, RESPONSE_TYPE, CLIENT_ID, REDIRECT_URI, SCOPE):
    request_parameters = {
        "response_type": RESPONSE_TYPE,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    p = Request('GET', URL, params=request_parameters).prepare()
    return p.url


user_authorization_url = prepare_url('https://id.twitch.tv/oauth2/authorize',
                                     'code', CLIENT_ID, REDIRECT_URI, SCOPE)


@app.route("/")
async def main():
    return "Hello World!"


@app.route("/<user>/message_json")
async def message_json(user):
    messages_path = os.path.join('json/' + user, "messages.json")
    # Mastermind variables
    with open(messages_path, "r") as data:
        message_data = json.load(data)
        messages = message_data['messages']
        message_id = message_data['message_id']
    return jsonify(messages)


@app.route("/<user>/mastermind_json")
async def mastermind_json(user):
    mastermind_path = os.path.join('json/' + user, "mastermind.json")
    with open(mastermind_path, "r") as data:
        mastermind_data = json.load(data)
    return jsonify(mastermind_data)


@app.route("/iframe")
async def iframe():
    return '<iframe id="myframe" width="100%" height="100%" src="https://c4arena.com/embed" frameborder="0"></iframe>'


@app.route("/c4arena")
async def c4():
    return await render_template('c4arena.html')


@app.route("/index")
async def index():
    return await render_template('index.html',
                                 authorization_url=user_authorization_url)


@app.route("/<user>/chat")
async def chat(user):
    # print("Loading data...", await data_json())
    data = await message_json(user)
    # print(await data.json)
    return await render_template('chat.html',
                                 messages=await data.json,
                                 user=user)


@app.route("/<user>/mastermind")
async def mastermind(user):
    # print("Loading data...", await data_json())
    data = await mastermind_json(user)
    # print(await data.json)
    return await render_template('mastermind.html',
                                 colors=await data.json,
                                 user=user)


@app.route('/<string:user>/add')
async def add(user):
    await bot.join_channels([user])
    return await render_template('login.html')


loop = asyncio.get_event_loop()
config = Config()
config.bind = ['0.0.0.0:8080']
loop.create_task(serve(app, config))
bot.run()
