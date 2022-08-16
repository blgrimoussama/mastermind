import random
import time
import json
import re
import os.path
from func import get_user

language = 'en'

players = []
started = False
closed = False
balls = ['🔴', '🟢', '🟤', '🟡', '🔵', '🟣']  # , '⚫']
hex_balls = {
    '🔴': '#F8312F',
    '🟢': '#00D26A',
    '🟤': '#6D4534',
    '🟡': '#FCD53F',
    '🔵': '#0074BA',
    '🟣': '#8D65C5'
}
check_balls = ['⚪', '🟠']
hex_check_balls = {'⚪': '#fff', '🟠': '#FF6723'}
versus = []
rounds = []
combination = []
first_start = ''
rem_rounds = 8
all_combinations = []
# json_path = os.path.join('json', "mastermind.json")

# print(leaderboard)

# def add_to_json():
# with open(json_path, 'w') as data:
# pass


def Mastermind(message, leaderboard_path, mastermind_json):
    # global json_path
    global language
    global players, started, closed, balls, hex_balls, check_balls, hex_check_balls
    global rem_rounds, versus, rounds, combination, first_start
    global all_combinations
    # json_path = mastermind_json
    author = message.author
    msg = message.content.lower()
    s = msg.split()
    mod = author.is_mod
    name = author.mention.replace('@', '')
    with open(leaderboard_path, "r") as data:
        leaderboard = json.load(data)
    with open(mastermind_json, "r") as data:
        mastermind_data = json.load(data)
    try:
        if msg == '!colors':
            return ['The available colors are:' + ''.join(balls)]
        if msg == 'check colors':
            return [
                check_balls[0] +
                "means it's in the combination but not in the right place",
                check_balls[1] +
                "means it's in the combination and in the right place"
            ]
        if msg == '!master' and not started and (mod or name
                                                 in ['0US5AMA', '0us5ama']):
            started = True
            closed = False
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
            with open(mastermind_json, 'w') as f:
                json.dump(mastermind_data, f, indent=4)
            return ['Mastermind game has just started ! Type "!Play" to join']

        if msg == 'master leaderboard':
            return [leaderboard]
        if started:
            if not closed:
                if msg == '!play':
                    if name not in players:
                        players.append(name)
                        time.sleep(0.5)
                        return ['You joined the game ! ' + name]
                    else:
                        time.sleep(0.5)
                        return ["You've already joined the game ! " + name]
                '''if msg == 'open' and mod:
                    closed = False
                    versus = random.sample(players, 2)'''
                if msg == '!close' and (mod or name in ['0us5ama', '0US5AMA']):
                    if len(players) >= 2:
                        closed = True
                        versus = random.sample(players, 2)
                        random.shuffle(versus)

                        versus_with_url = [{
                            'name':
                            player,
                            'url':
                            get_user(player)["profile_image_url"]
                        } for player in versus]

                        # with open(mastermind_json, "r") as data:
                        #     mastermind_data = json.load(data)
                        mastermind_data['players'] = {
                            "versus": versus_with_url,
                            "next": versus[0]
                        }
                        with open(mastermind_json, "w") as f:
                            json.dump(mastermind_data, f, indent=4)
                        rounds = versus * 4
                        combination = random.sample(balls, 4)
                        random.shuffle(combination)
                        return [
                            'Round has started !',
                            'It is ' + versus[0] + ' vs ' + versus[1] +
                            '. The first to start is : {}.'.format(versus[0])
                        ]
                    else:
                        return [
                            'Need a minimum of 2 players to start the game !'
                        ]
            if msg == '!answer' and (mod or name in ['0us5ama', '0US5AMA']):
                return ['The answer is : ' + ''.join(combination)]
            if msg == '!rounds':
                return [
                    'There is ' + str(rem_rounds) + ' rounds left. ' + name
                ]
            if rem_rounds <= 7:
                if msg == '!last':
                    return [all_combinations[-1]]
                if msg == '!all_previous':
                    return [all_combinations]
            if s[0] == '!guess' and name in versus:
                if name != rounds[0]:
                    return ['It is not your turn !']
                else:
                    '''if s[1] == 'random':
                        guess = random.sample(balls, 4)
                        random.shuffle(guess)
                        return ['Your random guess is: ' + ''.join(guess),]'''
                    guess = list(re.sub('(\w| )', '', msg))
                    guess = [c for c in guess if c in balls][:4]
                    # print(name + "'s Guess for the " + str(8 - rem_rounds) + "round is " + str(guess) + "at " + str(message.timestamp.strftime("%H:%M:%S")))
                    if len(guess) == 0:
                        return ['Wrong Syntax !']
                    if len(guess) < 4:
                        return ['Your guess must have 4 colors !']
                    if guess == combination:
                        players = []
                        started = False
                        previous_rem_rounds = rem_rounds
                        rem_rounds = 8
                        output = 'Good Job ' + name + '.' + \
                            ' You guessed the combination "{}" !'.format(
                                ''.join(combination))
                        leaderboard[name] = leaderboard.get(name, 0) + 1
                        with open(leaderboard_path, 'w') as f:
                            json.dump(leaderboard, f, indent=4)
                        lst = combination
                        dictt = {}
                        sub_dict = {}
                        for ind, ele in enumerate(lst):
                            dictt[ind] = hex_balls[ele]
                            sub_dict[ind] = '#FF6723'
                        # Before adding the matches cuz the last column should not contain matches
                        dictt['matches'] = sub_dict
                        mastermind_data['guesses']['8'] = dictt
                        mastermind_data['guesses'][str(
                            8 - previous_rem_rounds)] = dictt
                        with open(mastermind_json, 'w') as f:
                            json.dump(mastermind_data, f, indent=4)
                        combination = []
                        all_combinations = []
                        return [
                            output, 'The game is ending soon !',
                            'The leaderboard is : ' + str(leaderboard)
                        ]
                    else:
                        outcome = ''
                        for i in guess:
                            if i in combination:
                                if guess.index(i) == combination.index(i):
                                    outcome += '1'
                                else:
                                    outcome += '0'
                        # print(outcome)
                        output = ''.join(
                            outcome.count('1') * [check_balls[1]] +
                            outcome.count('0') * [check_balls[0]])
                        # print(output)
                        rounds.remove(name)
                        mastermind_data['players']['next'] = rounds[0]
                        with open(mastermind_json, "w") as f:
                            json.dump(mastermind_data, f, indent=4)
                        rem_rounds -= 1
                        all_combinations.append(''.join(guess) + ' ==> ' +
                                                output)
                        # mastermind_data['guesses'][8 - rem_rounds] = [guess, output]
                        lst = guess
                        dictt = {}
                        sub_dict = {}
                        for ind, ele in enumerate(lst):
                            dictt[ind] = hex_balls[ele]
                            try:
                                sub_dict[ind] = hex_check_balls[output[ind]]
                            except IndexError:
                                sub_dict[ind] = '#aaa'
                        dictt['matches'] = sub_dict
                        mastermind_data['guesses'][str(7 - rem_rounds)] = dictt
                        with open(mastermind_json, 'w') as f:
                            json.dump(mastermind_data, f, indent=4)
                        if rem_rounds == 0:
                            players = []
                            started = False
                            rem_rounds = 8
                            comb_copy = combination
                            combination = []
                            all_combinations = []
                            # print(comb_copy)
                            if ''.join(comb_copy):
                                dictt = {}
                                sub_dict = {}
                                for ind, ele in enumerate(comb_copy):
                                    dictt[ind] = hex_balls[ele]
                                    sub_dict[ind] = '#aaa'
                                dictt['matches'] = sub_dict
                                mastermind_data['guesses']['8'] = dictt
                                with open(mastermind_json, 'w') as f:
                                    json.dump(mastermind_data, f, indent=4)
                                return [
                                    name + ' your matches are : ' + output,
                                    'The round has ended ! the answer is :' +
                                    ''.join(comb_copy)
                                ]
                        else:
                            return [name + ' your matches are : ' + output]
            if (msg == '!end' and
                (mod or name in ['0us5ama', '0US5AMA'])) or rem_rounds == 0:
                players = []
                started = False
                rem_rounds = 8
                comb_copy = combination
                combination = []
                all_combinations = []
                # print(comb_copy)
                if ''.join(comb_copy):
                    dictt = {}
                    sub_dict = {}
                    for ind, ele in enumerate(comb_copy):
                        dictt[ind] = hex_balls[ele]
                        sub_dict[ind] = '#aaa'
                    dictt['matches'] = sub_dict
                    mastermind_data['guesses']['8'] = dictt
                    with open(mastermind_json, 'w') as f:
                        json.dump(mastermind_data, f, indent=4)
                    return [
                        'The round has ended ! the answer is :' +
                        ''.join(comb_copy)
                    ]
                else:
                    return ['The round has ended !']
            else:
                return [0]
        else:
            return [0]
    except IndexError:
        return [0]
