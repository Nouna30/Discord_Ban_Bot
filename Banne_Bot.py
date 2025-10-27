import os
import logging
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

#Project Overview: 
##A bot that automatically bans anyone who sends a msg in a specific channel. 
##That channel will display a clear warning not to send messages. 
##The purpose is to immediately ban spammers or hacked accounts ,the bot will ban the acc and delete all messages they sent in the previous 5 minutes.
##Individual work no team work, estimated time is 1 week from now





# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PROTECTED_CHANNEL_ID = int(os.getenv("PROTECTED_CHANNEL_ID")) 
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))



# Crée un fichier de log nommé discord.log qui permettra de debugger le bot en cas d'erreur ou pour suivre son activité.
file_handler  = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') 

root_logger = logging.getLogger()
#Capture tous les messages, du niveau DEBUG jusqu’à CRITICAL
root_logger.setLevel(logging.DEBUG)  

# on definit la forme du log enoyer dans el channel
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
root_logger.addHandler(stream_handler)

# ---------------- Handler personnalisé pour envoyer les logs dans un salon Discord ----------------
class DiscordHandler(logging.Handler):
    def __init__(self, bot, channel_id):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id

    async def send_log(self, record):
        # attendre que le bot soit prêt (garantit accès aux guilds / channels)
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            try:
                # format du message
                msg = f"[{record.levelname}] {record.getMessage()}"
                await channel.send(msg)
            except Exception as e:
                logging.getLogger(__name__).exception("DiscordHandler: erreur envoi log: %s", e)

    # cette methode dans ce cas permet d’envoyer le message sans bloquer ton programme principal.
    def emit(self, record):
        # On programme l'envoi du message dans la boucle asynchrone du bot
        try:
            # planifie la coroutine sur la loop du bot
            asyncio.run_coroutine_threadsafe(self.send_log(record), self.bot.loop)
        except Exception:
            self.handleError(record)


intents = discord.Intents.default()
intents.message_content = True
# intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Création et ajout du handler Discord
discord_handler = DiscordHandler(bot, LOG_CHANNEL_ID)
discord_handler.setLevel(logging.DEBUG)
discord_handler.setFormatter(formatter)
logging.getLogger().addHandler(discord_handler)



@bot.event
async def on_ready():
    logging.info(f"Bot ready: {bot.user} (id: {bot.user.id})")
    logging.info(f"Le bot enverra maintenant les logs dans le salon '{LOG_CHANNEL_ID}' si trouvé.")


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
            logging.warning("Missing permissions to ban or delete messages.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
    # on dot ajouter cette commande pour que les commandes seront traiter car dan sle cas ou on definie uen on_messag personalise on remplace le gestionnaire interne de Discord.py qui détecte les commandes.
    await bot.process_commands(message) 

@bot.command()
async def testlog(ctx):
    logging.debug("DEBUG test message")
    logging.info("INFO test message")
    logging.warning("WARNING test message")
    logging.error("ERROR test message")
    await ctx.send("Logs envoyés (vérifie le salon 'log').")


bot.run(TOKEN)

