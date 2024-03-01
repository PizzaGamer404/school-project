# https://discordpy.readthedocs.io/en/latest/api.html
import random
import discord
import openai
import json

# Opens openai_key.secret and reads the key
with open('openai_key.secret', 'r') as f:
    ai = openai.AsyncClient(api_key=f.read())

# Opens discord_key.secret and reads the key
with open('discord_key.secret', 'r') as f:
    discord_bot_secret_key = f.read()

# Opens your_examples.json and reads the examples
with open('your_examples.json', 'r') as f:
    prompt = json.load(f)

# Opens the rest of the examples
with open("There.json", "r") as f:
    their_prompt = json.load(f)

with open('shaming_examples.json', 'r') as f:
    shame_examples = json.load(f)

with open('old_timey_examples.json', 'r') as f:
    old_timey_examples = json.load(f)

DISCORD_CHARACTER_LIMIT = 2000

async def used_your_wrong(message: str) -> bool:
    # ChatGPT responds in bits of text called "Tokens", and these corespond to the words "Correct" and "Incorrect"
    # It might actually just be the first few letters, I forget
    correct_token_id = 34192
    incorrect_token_id = 41568
    # Asks AI to determine if it's right or wrong. Provides several examples to get a good answer.
    completion = await ai.chat.completions.create(messages=prompt + [
        {
            'role': 'user',
            'content': message
        }
        # Tells it to use 1 token, use the gpt-3.5-turbo-0125 model (cheapest and most recent),
        # to have no added randomness, and to pick only from the word "Correct" and "Incorrect"
    ], max_tokens=1, model="gpt-3.5-turbo-0125", temperature=0, logit_bias={correct_token_id: 100, incorrect_token_id: 100})
    return completion.choices[0].message.content.lower().startswith('incorrect')

async def used_their_wrong(message: str) -> bool:
    correct_token_id = 34192
    incorrect_token_id = 41568
    # Asks AI to determine if it's right or wrong. Provides several examples to get a good answer.
    completion = await ai.chat.completions.create(messages=their_prompt + [
        {
            'role': 'user',
            'content': "Message: " + message
        }
        # Tells it to use 1 token, use the gpt-3.5-turbo-0125 model (cheapest and most recent),
        # to have no added randomness, and to pick only from the word "Correct" and "Incorrect"
    ], max_tokens=1, model="gpt-3.5-turbo-0125", temperature=0, logit_bias={correct_token_id: 100, incorrect_token_id: 100})
    return completion.choices[0].message.content.lower().startswith('incorrect')


# Creates the bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Misspellings
misspellings_your = {
    "yur", "youre", "yor", "you'r", "ur", "yore", "youre", "yuor", "yoir", 
    "youre'", "yhour", "your'e", "yur", "yours", "yuo", "yout", "yorr",
    "yuur", "yoour", "yuer", "yourr", "yuore",
    "yure", "yuor", "yhur", "youur", "yorr", "yoor", "yowr", "yuour", "yours","yoooour", "you'res"
}
misspellings_youre = {
    "your'e", "youre", "yuore", "yore", "you'r", "yure", "yo're",
    "youre'", "yor'e", "yuo're", "y'oure", "youre", "yu're", "u're", "yur'e",
    "yourre", "your'e", "yorue", "yuoure", "yuo're", "you'are", "youre", "your'e",
    "yow're", "you'er", "yure'", "yuor'e", "yoru'e", "youer"
}
misspellings_there = {"thar","therr", "tharee", "thure"
,"thhere","thire","thareh","ther"}

misspellings_their = {"thier", "thare","thir", "thayr","thur","thiree",}

mispelling_theyre = {"thay're","thare","th'eyre","they'ree"}

# All mispellings as a set
all_there = misspellings_there.union(misspellings_their)
all_there = all_there.union(mispelling_theyre)
# All mispellings as a list
all_wrong_there_list = list(all_there)
# All mispellings as a set
all_yours = misspellings_your.union(misspellings_youre)
# All mispellings as a list
all_wrong_yours_list = list(all_yours)

async def shamer(message: discord.Message):
    # message.reference contains information on who they are replying to (None if not replying)
    if message.reference is None:
        await message.reply('You need to reply to someone to shame. Shame on **you**!')
        return
    try:
        # Gets the message they are replying to
        replied_message = await message.channel.fetch_message(message.reference.message_id)
    # If the message was not found, tell them it wasn't found
    except discord.NotFound:
        if random.randrange(3) > 0:
            await message.reply('Message to shame was not found, but if it was, I am sure it would be very shameful.')
        else:
            await message.reply('Message to shame was not found, but if it was, I am sure it would be absolutely perfect.')
        return
    
    if replied_message.author.bot:
        await message.reply('I **refuse** to shame another bot. How dare you even make me attempt this heinous crime of bot treason? To the dungeon!')
        return
    msg = replied_message.content
    # 
    async with message.channel.typing():
        english_teacher = await ai.chat.completions.create(messages=shame_examples + [
            {
                'role': 'user',
                'content': 'Message: ' + msg
            }
        # ], max_tokens=1024, model="gpt-4-0125-preview", temperature=0)
        ], max_tokens=1024, model="gpt-3.5-turbo-0125", temperature=0.7)
    shame = english_teacher.choices[0].message.content
    try:
        await message.reply(shame[:DISCORD_CHARACTER_LIMIT])
    except Exception:
        await message.channel.send(f'{message.author.mention} {shame}'[:DISCORD_CHARACTER_LIMIT])

async def old_timey(message: discord.Message):
    # message.reference contains information on who they are replying to (None if not replying)
    if message.reference is None:
        await message.reply('You need to reply to someone.')
        return
    try:
        # Gets the message they are replying to
        replied_message = await message.channel.fetch_message(message.reference.message_id)
    # If the message was not found, tell them it wasn't found
    except discord.NotFound:
        await message.reply('Message not found.')
        return
    if replied_message.author.bot:
        await message.reply('I **refuse** to reprase another bot. How dare you even make me attempt this heinous crime of bot treason? To the dungeon!')
        return
    msg = replied_message.content
    async with message.channel.typing():
        english_teacher = await ai.chat.completions.create(messages=old_timey_examples + [
            {
                'role': 'user',
                'content': msg
            }
        # ], max_tokens=1024, model="gpt-4-0125-preview", temperature=0.7)
        ], max_tokens=1024, model="gpt-3.5-turbo-0125", temperature=0.7)
    shame = english_teacher.choices[0].message.content
    try:
        await message.reply(shame[:DISCORD_CHARACTER_LIMIT])
    except Exception:
        await message.channel.send(f'{message.author.mention} {shame}'[:DISCORD_CHARACTER_LIMIT])


# On message event
@bot.event
async def on_message(message: discord.Message):
    # Ignore bot messages
    if message.author.bot:
        return
    
    if message.content == '!shame':
        await shamer(message)
        return
    if message.content == '!oldtimey':
        await old_timey(message)
        return
    # Splits the text into words
    words = message.content.split()
    # Removes punctuation from each word
    words = [word.strip('.,!?') for word in words]
    # Tracks if they have said "your" / "you're" / "yours" or if they have spelled it wrong
    said_your = False
    bad_your_spelling = False
    # Tracks if they have said "there" / "their" / "they're" or if they have spelled it wrong
    said_there = False
    bad_there_spelling = False
    # Loops over words
    for word in words:
        # Makes the word lowercase
        word = word.lower()
        # Checks if they said an incorrect version of `your`, `you're` or `yours`
        if word in all_yours:
            bad_your_spelling = True
            said_your = True
        # Checks if they said an incorrect version of `there`, `their` or `they're`
        if word in all_there:
            bad_there_spelling = True
            said_there = True
        # Checks if they said a correct version of any of the words
        if word in { 'your', 'you\'re', 'yours' }:
            said_your = True
        if word in {'there','there\'s', 'they\'re', 'their','their\'s' }:
            said_there = True
    if not said_your and not said_there:
        return
    # Uses AI to see if they said either word in the wrong context
    # The and statement is a nice way to first check if they said the word. If false, it automatically stops before asking the AI since it already knows it will be false.
    bad_your_usage = said_your and await used_your_wrong(message.content)
    bad_their_usage = said_there and await used_their_wrong(message.content)
    # If they spelled and used `your/you're` wrong
    if bad_your_usage and bad_your_spelling:
        await message.reply('HOW DO YOU MESS UP ***SO*** BADLY AS TO SPELL '+ random.choice(all_wrong_yours_list).upper()+' WRONG?!?! AND YOU USED IT IN THE WRONG CONTEXT?!?!!!! GRAHHHHHHH')
    # If they spelled and used `their` wrong
    elif bad_their_usage and bad_there_spelling:
        await message.reply('HOW DO YOU MESS UP ***SO*** BADLY AS TO SPELL '+ random.choice(all_wrong_there_list).upper()+' WRONG ' + random.choice(all_wrong_yours_list).upper() + '?!?! AND YOU USED IT IN THE WRONG CONTEXT?!?!!!! GRAHHHHHHH')
    # If they used `your` wrong
    elif bad_your_usage:
        await message.reply('You used the wrong ' + random.choice(all_wrong_yours_list) + '!!!!! (╯°□°)╯︵ ┻━┻')
    # If either were spelled wrong
    elif bad_your_spelling or bad_there_spelling:
        await message.reply('AAAAAAAAAAAAAAAAAAAA WRONG SPELLING!!!! (╯°□°)╯︵ ┻━┻')


# Runs the bot
bot.run(discord_bot_secret_key)