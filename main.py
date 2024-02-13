# https://discordpy.readthedocs.io/en/latest/api.html
import discord

# Opens discord_key.secret and reads the key
with open('discord_key.secret', 'r') as f:
    discord_bot_secret_key = f.read()

# Creates the bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

your_set = {"you're","your","youre","ur"}

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    words = message.content.split()
    for word in words:
        if word in your_set:
            await message.reply('AAAAAAAAAAAAAAAAAAAA (╯°□°)╯︵ ┻━┻')


# Runs the bot
bot.run(discord_bot_secret_key)