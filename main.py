# https://discordpy.readthedocs.io/en/latest/api.html
import random
import discord
import openai
import json

# Opens openai_key.secret and reads the key
with open('openai_key.secret', 'r') as f:
    ai = openai.Client(api_key=f.read())

# Opens discord_key.secret and reads the key
with open('discord_key.secret', 'r') as f:
    discord_bot_secret_key = f.read()

# Opens your_examples.json and reads the examples
with open('your_examples.json', 'r') as f:
    prompt = json.load(f)

def used_your_wrong(message: str) -> bool:
    correct_token_id = 34192
    incorrect_token_id = 41568
    # Asks AI to determine if it's right or wrong. Provides several examples to get a good answer.
    completion = ai.chat.completions.create(messages=prompt + [
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

# On message event
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    words = message.content.split()
    words = [word.strip('.,!?') for word in words]
    terrible_spelling = False
    said_your = False
    for word in words:
        word_lower = word.lower()
        if word.lower() in all_yours:
            terrible_spelling = True
            said_your = True
            break
        elif word.lower() == 'your':
            said_your = True
            break
        elif word.lower() == 'you\'re':
            said_your = True
            break
        elif word.lower() == 'yours':
            said_your = True
            break
    if terrible_spelling == True:
        await message.reply('AAAAAAAAAAAAAAAAAAAA WRONG SPELLING!!!! (╯°□°)╯︵ ┻━┻')
    if said_your:
        if used_your_wrong(message.content):
            await message.reply('You used the wrong ' + random.choice(all_wrong_yours_list) + '!!!!! (╯°□°)╯︵ ┻━┻')


# Runs the bot
bot.run(discord_bot_secret_key)