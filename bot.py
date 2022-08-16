from twitchio.ext import commands
from mastermind import Mastermind
import json
import time
import os.path
import re

class Bot(commands.Bot):

    def __init__(self, connect_as, connect_to):
        self.connect_as = connect_as.lower()
        self.connect_to = connect_to.lower()
        self.messages = []
        self.message_id = 1
        self.mastermind_data = {}
        self.path = 'json/' + connect_to
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        # new_channel = input("New channel : ")
        super().__init__(token=self.connect_as, prefix='!', initial_channels=[
            self.connect_to])  # new_channel

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in to {self.connect_to} as | {self.nick}')

    async def event_message(self, message):
        # global channel_name
        if message.echo:
            return

        channel_name = re.search(".+: (.+)>", str(message.channel)).group(1)

        self.path = 'json/' + channel_name
        
        messages_path = os.path.join(self.path, "messages.json")
        mastermind_path = os.path.join(self.path, "mastermind.json")
        mastermind_leaderboard = os.path.join(self.path, "mastermind_leaderboard.json")
        s = message.content.split()
        msg = message.content.lower()
        # dir(message.author)
        try:
            self.messages.append({'id': self.message_id, 'author': message.author.display_name, 'message': message.content,
                             'time': message.timestamp.strftime("%H:%M:%S")})
            self.message_id += 1
        except AttributeError:
            pass
        with open(messages_path, "w") as data:
            json.dump({"messages": self.messages, "message_id": self.message_id}, data)
            # print(self.message_id)
        # try:
        if msg == 'test':
            await message.channel.send("It's a test")
        if msg == 'clear' and (message.author.display_name.lower() == '0us5ama' or message.author.display_name.lower() == 'hussain149'):
            self.messages = []
            self.message_id = 1
            await message.channel.send("Message list cleared!")
            with open(messages_path, "w") as data:
                json.dump({"messages": self.messages, "message_id": self.message_id}, data)
        # except IndexError:
            # pass
        # try:
        ma_game = Mastermind(
            message, mastermind_leaderboard, mastermind_path)
        if ma_game[0]:
            for out in ma_game:
                time.sleep(1)
                await message.channel.send(out)
        # except AttributeError:
        #     pass
