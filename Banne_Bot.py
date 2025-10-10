import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta ,  timezone
import logging

#Project Overview: 
##A bot that automatically bans anyone who sends a msg in a specific channel. 
##That channel will display a clear warning not to send messages. 
##The purpose is to immediately ban spammers or hacked accounts ,the bot will ban the acc and delete all messages they sent in the previous 5 minutes.
##Individual work no team work, estimated time is 1 week from now





# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PROTECTED_CHANNEL_ID = int(os.getenv("PROTECTED_CHANNEL_ID")) # utiliser pour copier le id su salon ( chennel ) et le transformer en entier (integer)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # Crée un fichier de log nommé discord.log qui permettra de debugger le bot en cas d'erreur ou pour suivre son activité.

intents = discord.Intents.default()
intents.message_content = True
# intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # verifiyer si le message envoyer est dans le salon qu'on veut 
    if message.channel.id == PROTECTED_CHANNEL_ID:
        try:
            #### POUR SUPPRIMER LES MESSAGE
            now = datetime.now(timezone.utc)
            five_minutes_ago = now - timedelta(minutes=5)

            messeges_to_delete = message.channel.history(limit=100)

            async for msg in messeges_to_delete:
                if msg.author.id == message.author.id and msg.created_at > five_minutes_ago:
                    await msg.delete()

            #### POUR ENVOYER UN WARNNING
            await message.author.send(f"You have been banned from {message.guild.name} for sending a message in the protected channel.")
            
            #### POUR ENVOYER UN WARNING DANS CHANNEL
            await message.channel.send(f"User {message.author.mention} has been banned for sending a message in this protected channel.")
            #### POUR BANNIR
            #await message.guild.ban(message.author, reason="Sent message in protected channel")
            await message.author.ban(reason="Sent message in protected channel")

        except discord.Forbidden:
            print("Missing permissions")
        except Exception as e:
            print(f"Error: {e}")



bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
