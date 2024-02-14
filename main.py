# https://discordpy.readthedocs.io/en/latest/api.html
import discord
import openai

# Opens discord_key.secret and reads the key
with open('discord_key.secret', 'r') as f:
    discord_bot_secret_key = f.read()

# Creates the bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

misspellings_your = {
    "yur", "youre", "yor", "you'r", "ur", "yore", "youre", "yuor", "yoir", 
    "youre'", "yhour", "your'e", "yur", "yours", "yuo", "yout", "yorr",
    "yuur", "yoour", "yuer", "yours", "yourr", "yuore",
    "yure", "yuor", "yhur", "youur", "yorr", "yoor", "yowr", "yuour", "yours","yoooour"
}

misspellings_youre = {
    "your'e", "youre", "yuore", "yore", "you'r", "yure", "yo're",
    "youre'", "yor'e", "yuo're", "y'oure", "youre", "yu're", "u're", "yur'e",
    "yourre", "your'e", "yorue", "yuoure", "yuo're", "you'are", "youre", "your'e",
    "yow're", "you'er", "yure'", "yuor'e", "yoru'e", "youer"
}
all_yours = misspellings_your.union(misspellings_youre)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    words = message.content.split()
    terrible_spelling = False
    for word in words:
        if word.lower() in all_yours:
            terrible_spelling = True
            break
    if terrible_spelling == True:
        await message.reply('AAAAAAAAAAAAAAAAAAAA (╯°□°)╯︵ ┻━┻')


# Runs the bot
bot.run(discord_bot_secret_key)