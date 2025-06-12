# Made by Serofyte, ChatGPT, and youtube tutorials
# Yappatron website: https://yappatron.serofyte.net
# Join my discord server: https://serofyte.net/discord

import discord
from discord.ext import commands
from gpt4all import GPT4All
import os

# token and path stuffs
BOT_TOKEN = "no" # no token for you fuckers
MODEL_PATH = r"C:\Users\Default.DESKTOP-0D2N4NP\Documents\gpt\Llama-3.2-1B-Instruct-Q4_0.gguf"
TARGET_CHANNEL_ID = 1378627232716689429 # reply in this channel without needing ping

# start
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# llm load
model = GPT4All(model_name=MODEL_PATH, allow_download=False)

# message in console
@bot.event
async def on_ready():
    print(f"Yappatron is online as {bot.user}")

# actual runtime
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild is None:
        return

    should_respond = False

    # if mentioned
    if bot.user in message.mentions:
        clean_content = message.content.replace(f"<@{bot.user.id}>", "").strip()
        should_respond = True

    # or if in the yappatron channel
    elif message.channel.id == TARGET_CHANNEL_ID:
        clean_content = message.content.strip()
        should_respond = True

    if should_respond:

        # he yapp
        prompt = f"""You are Yappatron, a chaotic AI that only talks in memes and random brainrot.
Talk normally, don't be super obvious that you are a troll. Please do not send images or links.
Respond to what the user says or asks.

Don't use a format, just talk in a few sentences to respond. Here is the user's message that you
must reply to: \"{clean_content}\"
"""

        # no clue bro this part was all chat gpt (skill issues)
        try:
            with model.chat_session():
                response = model.generate(prompt, max_tokens=150).strip()

            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(f"Model error: {e}")
            print("Error:", e)

    await bot.process_commands(message)

bot.run(BOT_TOKEN)
