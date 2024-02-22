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

with open('shaming_examples.json', 'r') as f:
    shame_examples = json.load(f)

async def used_your_wrong(message: str) -> bool:
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

# All mispellings as a dictionary
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
    
    msg = replied_message.content
    english_teacher = await ai.chat.completions.create(messages=shame_examples + [
        {
            'role': 'user',
            'content': msg
        }
    # ], max_tokens=1024, model="gpt-4-0125-preview", temperature=0)
    ], max_tokens=1024, model="gpt-3.5-turbo-0125", temperature=0)
    shame = english_teacher.choices[0].message.content
    try:
        await message.reply(shame[:2000])
    except Exception:
        await message.channel.send(f'{message.author.mention} {shame}'[:2000])


# On message event
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.content == '!shame':
        await shamer(message)
        return

    words = message.content.split()
    words = [word.strip('.,!?') for word in words]
    terrible_spelling = False
    said_your = False
    for word in words:
        word_lower = word.lower()
        if word_lower in all_yours:
            terrible_spelling = True
            said_your = True
            break
        elif word_lower == 'your':
            said_your = True
            break
        elif word_lower == 'you\'re':
            said_your = True
            break
        elif word_lower == 'yours':
            said_your = True
            break
    if not said_your:
        return
    bad_usage = await used_your_wrong(message.content)
    if bad_usage and terrible_spelling:
        await message.reply('HOW DO YOU MESS UP ***SO*** BADLY AS TO SPELL '+random.choice(all_wrong_yours_list).upper()+' WRONG?!?! AND YOU USED IT IN THE WRONG CONTEXT?!?!!!! GRAHHHHHHH')
    elif terrible_spelling:
        await message.reply('AAAAAAAAAAAAAAAAAAAA WRONG SPELLING!!!! (╯°□°)╯︵ ┻━┻')
    elif bad_usage:
        await message.reply('You used the wrong ' + random.choice(all_wrong_yours_list) + '!!!!! (╯°□°)╯︵ ┻━┻')


# Runs the bot
bot.run(discord_bot_secret_key)