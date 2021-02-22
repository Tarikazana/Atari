# bot.py
##############################################################
##                                                          ##
##                  -    Imports  -                         ##
##                                                          ##
##############################################################
import asyncio
import io
import sys
import os
import random
import re
from discord import errors
import requests
import json
from tinydb import TinyDB, Query
from tinydb.operations import delete
import discord, datetime, time
from discord import message
from discord.utils import get
from discord import TextChannel
from discord import channel
from discord.activity import Game
from discord.enums import Status
from discord.ext import commands, tasks
from discord.abc import GuildChannel
from discord.ext.commands.converter import TextChannelConverter
from discord.ext.commands.core import has_permissions
from discord.guild import Guild
from discord.ext.commands import Bot
from dotenv import load_dotenv
from requests.models import ReadTimeoutError
from random import Random, choice
import platform,socket,psutil
import time
import aiohttp
from datetime import datetime
start = time.time()

##############################################################
##                  Loading dotenv Stuff                    ##
##############################################################

## for print
class bcolors:
    CYAN = '\033[95m'   #PURPLE IN TERMINAL
    CYAN2 = '\033[94m'  #OKBLUE IN TERMINAL
    CYAN3 = '\033[96m'  #OKCYAN IN TERMINAL
    PURPLE = '\033[92m'     #OKGREEN IN TERMINAL
    PURPLE2 = '\033[91m'    #FAIL IN TERMINAL
    WARNING = '\033[93m'    #YELLOW IN TERMINAL
    ENDC = '\033[0m'        #same
    BOLD = '\033[1m'        #same
    UNDERLINE = '\033[4m'   #same

print(f"{bcolors.CYAN}loading dotenv content...{bcolors.ENDC}")

load_dotenv()   #loads stuff from .env
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_VERSION = os.getenv('BOT_VERSION')
BOT_PREFIX = os.getenv('PREFIX')
WHITELIST = os.getenv('SERVER_WHITELIST')
SHERI_API_KEY = os.getenv('SHERI_API_KEY')
FURRYV2_API_KEY = os.getenv('FURRYV2_API_KEY')

DEFAULT_EMBED_COLOR = discord.Colour(0xfc03ad)
print('done.')

##############################################################
##                       Startup                            ##
##############################################################

print(f"{bcolors.CYAN}starting Atari...{bcolors.ENDC}")
print(f"{bcolors.CYAN}   _____   __               .__ {bcolors.ENDC}")
print(f"{bcolors.CYAN}  /  _  \_/  |______ _______|__|{bcolors.ENDC}")
print(f"{bcolors.CYAN} /  /_\  \   __\__  \\\\_  __ \  |{bcolors.ENDC}")
print(f"{bcolors.CYAN}/    |    \  |  / __ \|  | \/  |{bcolors.ENDC}")
print(f"{bcolors.CYAN}\____|__  /__| (____  /__|  |__|{bcolors.ENDC}")
print(f"{bcolors.CYAN}        \/          \/          {bcolors.ENDC}")

##############################################################
##                  Specify bot prefix in .env              ##
##############################################################
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True, voice_states=True)
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)
## bot = commands.AutoShardedBot(shard_count=10, command_prefix=BOT_PREFIX)
## It is recommended to use this client only if you have surpassed at least 1000 guilds.

session = None

status = ["Tawi", "_help", "_music"]

bot.automation = False

@bot.event
async def on_ready():
    bot.load_extension('cogs.music')
    bot.load_extension('cogs.system')

    original_stdout = sys.stdout # Save a reference to the original standard output
    text_channel_list = []
    i=1
    #   atari/data/guilds/{ctx.guild.id}/users/{member.id}/{member.id}.json
    for guild in bot.guilds:
        if not os.path.exists(f'atari/data/guilds'):
            os.makedirs(f'atari/data/guilds')
            print(f"created atari/data/guilds...")
        if not os.path.exists(f'atari/data/guilds/{guild.id}'):
            os.makedirs(f'atari/data/guilds/{guild.id}')
            print(f"created atari/data/guilds/{guild.id}...")
        with open(f'atari/data/guilds/{guild.id}/{guild.id}.json', 'w') as textfile:
            print(f"writing into atari/data/guilds/{guild.id}/{guild.id}.json ...")
            sys.stdout = textfile
            print('{"_default":{')
            sys.stdout = original_stdout # Reset the standard output to its original value
            
        for channel in guild.text_channels:
            with open(f'atari/data/guilds/{guild.id}/{guild.id}.json', 'a') as textfile:
                print(f"listing textchannels in atari/data/guilds/{guild.id}/{guild.id}.json ...")
                sys.stdout = textfile
                print('"'+str(i)+'": ' '{"channel_id": "' + str(channel.id) + '", "channel_name": "' + str(channel.name) + '", "channel_position": "' + str(channel.position) + '", "nsfw": "' + str(channel.nsfw) + '", "category_id": "' + str(channel.category_id) + '"},')
                sys.stdout = original_stdout # Reset the standard output to its original value
                
            text_channel_list.append(channel)
            i=i+1
        with open(f'atari/data/guilds/{guild.id}/{guild.id}.json', 'rb+') as f:
            print(f"truncating atari/data/guilds/{guild.id}/{guild.id}.json ...")
            f.seek(0,2)                 # end of file
            size=f.tell()               # the size...
            f.truncate(size-3)          # truncate at that size - how ever many characters
            
            
        with open(f'atari/data/guilds/{guild.id}/{guild.id}.json', 'a') as textfile:
            print(f"closed atari/data/guilds/{guild.id}/{guild.id}.json ...")
            sys.stdout = textfile
            print("}}}")
            sys.stdout = original_stdout # Reset the standard output to its original value

    
    # current date and time
    now = datetime.now()
    timestamp = round(datetime.timestamp(now))
    print(f"{bcolors.PURPLE}{datetime.fromtimestamp(timestamp)} - {bot.user} has connected to Discord!{bcolors.ENDC}")

    print ("------------------------------------")
    print (f"Bot Name: {bot.user.name}")
    print (f"Bot ID: {bot.user.id}")
    print (f"Bot Created: {datetime.fromtimestamp(round(datetime.timestamp(bot.user.created_at)))}")
    print (f"Discord Version: {discord.__version__}")
    print (f"Bot Version: {BOT_VERSION}")
    print ("------------------------------------")

    print(f"{bcolors.PURPLE}setting activity...{bcolors.ENDC}")

    ## useful docs for setting activities
    ## https://medium.com/python-in-plain-english/how-to-change-discord-bot-status-with-discord-py-39219c8fceea
    ## https://stackoverflow.com/questions/59126137/how-to-change-discord-py-bot-activity
    change_status.start()
    automated_yiff.start()
    # automated_fact.start()
    change_cooldown.start()
    print(f"{bcolors.WARNING}activity set.{bcolors.ENDC}")

    print(
        f'{bot.user} is connected to {len(bot.guilds)} guilds\n'
    )
    for x in bot.guilds:
        print ("-")
        print(f'{x.name}(id: {x.id})')
        print(f'Guild Members:{x.member_count}')
        
    print ("------------------------------------")
    print(f"{bcolors.PURPLE}Started in {round(time.time()-start,2)} seconds.{bcolors.ENDC}\n")
    print ("\nMessage Log:")

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=choice(status)))

bot.spamuserlist = []
@tasks.loop(seconds=5)
async def change_cooldown():
    list=bot.spamuserlist
    if len(list)==0: return
    print("spamuserlist: "+str(bot.spamuserlist))
    del bot.spamuserlist[0]

@tasks.loop(seconds=86400)
async def automated_fact():
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    channel_list_len = len(text_channel_list)
    i = 0
    while i < channel_list_len:
        if 'random-facts-and-thoughts' in str(text_channel_list[i]):
            channel = bot.get_channel(text_channel_list[i].id)
            if str(channel.id) not in WHITELIST: return
            em = discord.Embed(
            title=None,
            description=None,
            color=discord.Colour(0x000000)
            )
            try:
                url = "https://uselessfacts.jsph.pl/today.json?language=en"
                r = requests.get(url, timeout=5)
                print(r)
                if r:
                    print (r.json())
                    #em.set_image(url=str(r.json()["url"]))
                    #em.set_author(name=">> Source <<", url=str(r.json()["permalink"]))
                    em.add_field(name="- Random fact of today -", value=str(r.json()["text"]), inline=False)
                    #source=str(r.json()["permalink"])
                    #em.add_field(name="Source", value=f"[{(source)}]", inline=False)
                    await channel.send(embed=em)
            except requests.exceptions.ReadTimeout:
                await channel.send('`Connection to api timed out.`')
                return
            except requests.exceptions.ConnectionError:
                await channel.send('`Connection error.`')
                return
        i=i+1

@tasks.loop(seconds=300)
async def automated_yiff():
    if bot.automation == False: return
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    channel_list_len = len(text_channel_list)
    i = 0
    while i < channel_list_len:
        if 'automated-yiff' in str(text_channel_list[i]):
            channel = bot.get_channel(text_channel_list[i].id)
            if str(channel.id) not in WHITELIST: return
            if channel.is_nsfw():
                em = discord.Embed(
                    title=None,
                    description=None,
                    color=discord.Colour(0x000000)
                )
                try:
                    url = "https://www.sheri.bot/api/yiff"
                    headers = {'Authorization': 'Token '+SHERI_API_KEY}
                    r = requests.get(url, headers=headers, timeout=5)
                    print(r)
                    if r:
                        #print (r.json())
                        em.set_image(url=str(r.json()["url"]))
                        em.set_author(name=">> Link", url=str(r.json()["url"]))
                        await channel.send(embed=em)
                except requests.exceptions.ReadTimeout:
                    await channel.send('`Connection to api timed out.`')
                    return
                except requests.exceptions.ConnectionError:
                    await channel.send('`Connection error.`')
                    return
            else:
                await channel.send("`NSFW. You can't use that here.`")
                return
        i=i+1
    return
    

## Getting rid of default commands

bot.remove_command('help')
bot.remove_command('say')

######################################################
##                  - COMMANDS -                    ##
######################################################

@bot.command(name="help", description="Returns all commands available", aliases=['h'])
async def help(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    em = discord.Embed(
        title="- Help -",
        description="**Commands**",
        color=DEFAULT_EMBED_COLOR
    )

    em.set_thumbnail(url=bot.user.avatar_url)
    em.set_image(url=bot.user.avatar_url)
    em.add_field(name=BOT_PREFIX + "help", value="Shows this message\nalias: " + BOT_PREFIX + "h", inline=False)
    em.add_field(name=BOT_PREFIX + "remove", value="Disables Atari in this channel.", inline=False)
    em.add_field(name=BOT_PREFIX + "add", value="Enables Atari in this channel.", inline=False)
    em.add_field(name=BOT_PREFIX + "music", value="Music help", inline=False)
    em.add_field(name=BOT_PREFIX + "ping", value="Sends a ping to the bot and returns an value in `ms`\nalias: " + BOT_PREFIX + "p", inline=False)
    em.add_field(name=BOT_PREFIX + "say", value="Say smth with the bot.", inline=False)
    em.add_field(name=BOT_PREFIX + "owo", value="OwOifier", inline=False)
    em.add_field(name=BOT_PREFIX + "fgen", value="Fursona Generator", inline=False)
    em.add_field(name=BOT_PREFIX + "adopt @user", value="ask a user to adopt them", inline=False)
    em.add_field(name=BOT_PREFIX + "adopted", value="see adoption status", inline=False)
    em.add_field(name=BOT_PREFIX + "avatar", value="Avatar of user", inline=False)
    em.add_field(name=BOT_PREFIX + "remindme", value="Reminds you of smth.\nalias: " + BOT_PREFIX + "rm", inline=False)
    em.add_field(name=BOT_PREFIX + "iscute", value="is smth cute on a scale from 0-100%", inline=False)
    em.add_field(name=BOT_PREFIX + "isugleh", value="is smth ugleh on a scale from 0-100%", inline=False)
    em.add_field(name="other stuff", value="Will respond to greetings, such as\n```md\n- Hewwo\n- Hey\n- Hi```\nI will respond if you\n```md\n- call me cute\n- ask me how I am```\n*and there are some things that get triggered randomly*\n\nYou can ask <@!349471395685859348> for help.", inline=False)
    

    await ctx.message.delete()
    await ctx.send(embed=em)

@bot.command(name="images", description="Image help")
async def images(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    em = discord.Embed(
        title="- Images -",
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    em.add_field(name="**NSFW**", value=BOT_PREFIX + "sixnine\n" 
    + BOT_PREFIX + "anal\n" 
    + BOT_PREFIX + "bang\n" 
    + BOT_PREFIX + "bisexual\n"
    + BOT_PREFIX + "booty\n"
    + BOT_PREFIX + "christmas\n"
    + BOT_PREFIX + "cumflation\n"
    + BOT_PREFIX + "cuntboy\n"
    + BOT_PREFIX + "dick\n"
    + BOT_PREFIX + "dp\n"
    + BOT_PREFIX + "fbound\n"
    + BOT_PREFIX + "fcreampie\n"
    + BOT_PREFIX + "femboypresentation\n"
    + BOT_PREFIX + "finger\n"
    + BOT_PREFIX + "fpresentation\n"
    + BOT_PREFIX + "fseduce\n"
    + BOT_PREFIX + "fsolo\n"
    + BOT_PREFIX + "ftease\n"
    + BOT_PREFIX + "futabang\n"
    + BOT_PREFIX + "gay\n"
    + BOT_PREFIX + "gif\n"
    + BOT_PREFIX + "lesbian\n"
    + BOT_PREFIX + "maws\n"
    + BOT_PREFIX + "mbound\n"
    + BOT_PREFIX + "mcreampie\n"
    + BOT_PREFIX + "mpresentation\n"
    + BOT_PREFIX + "mseduce\n"
    + BOT_PREFIX + "msolo\n"
    + BOT_PREFIX + "mtease\n"
    + BOT_PREFIX + "nboop\n"
    + BOT_PREFIX + "nbulge\n"
    + BOT_PREFIX + "ncomics\n"
    + BOT_PREFIX + "ncuddle\n"
    + BOT_PREFIX + "nfemboy\n"
    + BOT_PREFIX + "nfuta\n"
    + BOT_PREFIX + "ngroup\n"
    + BOT_PREFIX + "nhold\n"
    + BOT_PREFIX + "nhug\n"
    + BOT_PREFIX + "nlick\n"
    + BOT_PREFIX + "npokemon\n"
    + BOT_PREFIX + "nprotogen\n"
    + BOT_PREFIX + "nseduce\n"
    + BOT_PREFIX + "nsfwselfies\n"
    + BOT_PREFIX + "nsolo\n"
    + BOT_PREFIX + "ntease\n"
    + BOT_PREFIX + "ntrap\n"
    + BOT_PREFIX + "pawjob\n"
    + BOT_PREFIX + "petplay\n"
    + BOT_PREFIX + "ride\n"
    + BOT_PREFIX + "suck\n"
    + BOT_PREFIX + "toys\n"
    + BOT_PREFIX + "vore\n"
    + BOT_PREFIX + "yiff\n"

    , inline=True)

    em.add_field(name="**SFW**", value=BOT_PREFIX + "bellyrub\n" 
    + BOT_PREFIX + "blep\n"
    + BOT_PREFIX + "boop\n"
    + BOT_PREFIX + "cry\n"
    + BOT_PREFIX + "cuddle\n"
    + BOT_PREFIX + "hold\n"
    + BOT_PREFIX + "howl\n"
    + BOT_PREFIX + "hug\n"
    + BOT_PREFIX + "kiss\n"
    + BOT_PREFIX + "lick\n"
    + BOT_PREFIX + "pat\n"
    + BOT_PREFIX + "paws\n"
    + BOT_PREFIX + "pokemon\n"
    + BOT_PREFIX + "proposal\n"
    + BOT_PREFIX + "trickortreat\n"

    , inline=True)

    em.add_field(name="**PUBLIC**", value=BOT_PREFIX + "bunny\n" 
    + BOT_PREFIX + "cat\n"
    + BOT_PREFIX + "deer\n"
    + BOT_PREFIX + "fox\n"
    + BOT_PREFIX + "husky\n"
    + BOT_PREFIX + "lion\n"
    + BOT_PREFIX + "mur\n"
    + BOT_PREFIX + "nature\n"
    + BOT_PREFIX + "rpanda\n"
    + BOT_PREFIX + "shiba\n"
    + BOT_PREFIX + "snek\n"
    + BOT_PREFIX + "snep\n"
    + BOT_PREFIX + "tiger\n"
    + BOT_PREFIX + "wolf\n"
    + BOT_PREFIX + "yeen\n"
    + BOT_PREFIX + "fursuit\n"

    , inline=True)

    em.set_footer(text="Requested by " + ctx.message.author.name + "")
    await ctx.message.delete()
    await ctx.send(embed=em)

@bot.command(name="music", description="Music help")
async def music(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    em = discord.Embed(
        title="- Music -",
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    em.add_field(name="**Commands**", value=BOT_PREFIX + "join\n" 
    + BOT_PREFIX + "play\n"
    + BOT_PREFIX + "stop\n"
    + BOT_PREFIX + "pause\n"
    + BOT_PREFIX + "resume\n"
    + BOT_PREFIX + "skip\n"
    + BOT_PREFIX + "dc - disconnect\n"
    + BOT_PREFIX + "cq - clear queue\n"
    + BOT_PREFIX + "queue\n"
    + BOT_PREFIX + "current\n"
    + BOT_PREFIX + "nowplaying\n"
    + BOT_PREFIX + "vol - volume in %\n"
    , inline=True)

    em.set_footer(text="Requested by " + ctx.message.author.name + "")
    await ctx.message.delete()
    await ctx.send(embed=em)

@bot.command(name="ping", description="Sends a ping to the bot and returns an value in `ms`", aliases=['p'])
async def ping(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    before = time.monotonic()
    message = await ctx.reply("Pong!")
    ping1 = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping1)}ms`")

@bot.command(name="info", description="Sends info from os", aliases=['i'])
async def info(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    message = await ctx.send(f"**Platform info**\n```architecture - {platform.machine()}```")
    await message.edit(content=f"**Platform info**\n```architecture - {platform.machine()}\nversion - {platform.version()}```")
    await message.edit(content=f"**Platform info**\n```architecture - {platform.machine()}\nversion - {platform.version()}\nrelease - {platform.release()}```")
    await message.edit(content=f"**Platform info**\n```architecture - {platform.machine()}\nversion - {platform.version()}\nrelease - {platform.release()}\nplatform - {platform.system()}```")
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}```")
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}\nhostname - {socket.gethostname()}\ncollecting processor and ram info```")
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}\nhostname - {socket.gethostname()}\ncollecting processor and ram info.```")
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}\nhostname - {socket.gethostname()}\ncollecting processor and ram info..```")
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}\nhostname - {socket.gethostname()}\ncollecting processor and ram info...```")
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}\nhostname - {socket.gethostname()}\nprocessor - {platform.processor()}```")
    ram = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    await message.edit(content=f"**Platform info**\n```platform - {platform.system()}\nrelease - {platform.release()}\nversion - {platform.version()}\narchitecture - {platform.machine()}\nhostname - {socket.gethostname()}\nprocessor - {platform.processor()}\nram - {ram}```")

@bot.command()
async def remove(ctx):
    if ctx.message.author.guild_permissions.administrator:
        guild = ctx.guild
        channelid = ctx.channel.id
        if not os.path.exists(f'atari/data/guilds/{guild.id}/blacklist'):
                os.makedirs(f'atari/data/guilds/{guild.id}/blacklist')
        db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
        db.insert({'id': str(channelid)})
        em = discord.Embed(
            title="Channel removed.",
            description=None,
            color=discord.Colour(0x000000)
        )
        em.set_footer(text="Requested by " + ctx.message.author.name + "", icon_url=ctx.message.author.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=em)
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=int(1), check=None)

@bot.command()
async def fgen(ctx):
    number= random.randrange(10000, 99999)
    embed=discord.Embed(title="Fursona Generator ~", description="Look at that cutie!", color=0x03fca1)
    embed.set_thumbnail(url="https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed"+str(number)+".jpg")
    embed.add_field(name="\u200B", value="cdn: [download](https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed"+str(number)+".jpg)\nSource: thisfursonadoesnotexist.com")
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, *, user: discord.User = None):
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/status.json')
    Frootloops = Query()
    status = json.dumps(db.search(Frootloops.status != None))
    status = str(status).replace("{","").replace("}","").replace(":",",").replace("'",'"')
    status = list(status.split(","))
    embed.set_footer(text='ID: ' + str(user.id) + "\nStatus: "+str(status[1]).replace('"','').replace("]","").replace("[",""))
    return await ctx.send(embed=embed)

@bot.command()
async def warn(ctx, user: discord.User = None, *, arg):
    guild = ctx.guild
    user = user
    reason = str(arg)
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Warning", value=f"for {reason}", inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    
    db = TinyDB(f'atari/data/guilds/{guild.id}/users/{user.id}/status.json')
    db.update({'status': f'warned for {reason}'})
    await ctx.send(embed=embed)

@bot.command()
async def unwarn(ctx, user: discord.User = None):
    guild = ctx.guild
    user = user
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Status Update", value=f"Status: normal", inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    
    db = TinyDB(f'atari/data/guilds/{guild.id}/users/{user.id}/status.json')
    db.update({'status': 'normal'})
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def verifyme(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    newuser = ctx.message.author
    temp = get(ctx.guild.roles, name="waiting for approval")
    rules = get(ctx.guild.roles, name="✓ rules")
    mods = get(ctx.guild.roles, name="Management")
    muted = get(ctx.guild.roles, name="Muted")
    try:
        if newuser.roles[1] == muted:
            return
    except IndexError:
        pass
    await newuser.send("Hey there! Please have a bit of patience while we verify you.")
    await newuser.add_roles(temp)
    await ctx.message.delete()
    
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    channel_list_len = len(text_channel_list)
    i = 0
    
    while i < channel_list_len:
        if 'pending-approval' in str(text_channel_list[i]):
            ctxchannel = bot.get_channel(text_channel_list[i].id)
            print(str(text_channel_list[i]))
            guild = ctx.guild
            db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
            channelid = ctx.channel.id
            channel = Query()
            out = db.search(channel.id == str(channelid))
            
            if str(out) != '[]':
                await ctx.message.delete()
                await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
                await asyncio.sleep(3)
                await ctx.channel.purge(limit=1, check=None)
                return
            
            if ctxchannel.guild.id == ctx.guild.id:
                em = discord.Embed(
                    title=f"New User: {newuser.name}",
                    description=(f"React to grant or decline access.\n\n:ballot_box_with_check: : grant access\n\n:x: : decline access"),
                    color=discord.Colour(0x000000)
                )  
                msg = await ctxchannel.send(embed=em)
        i = i+1

    await msg.add_reaction('☑️')
    await msg.add_reaction('❌')
    
    def check(reaction, user):
        return user != bot.user
        
    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check)
        print('reacton:'+str(reaction.emoji))
        if str(reaction.emoji) == '❌':
            await ctxchannel.purge(limit=1, check=None)
            message = f"You have been banned from {ctx.guild.name} // access declined."
            await newuser.send(message)
            await newuser.ban(reason="access declined.")
            await ctxchannel.send(f"{newuser.name} is banned!")
            await asyncio.sleep(3)
            await ctxchannel.purge(limit=1, check=None)

        if str(reaction.emoji) == '☑️':
            await ctxchannel.purge(limit=1, check=None)
            role = ctx.guild.get_role(811347242194567189)
            await newuser.remove_roles(role)
            await newuser.add_roles(rules)

            await ctxchannel.send(f"I granted {newuser.name} access.")

            text_channel_list = []
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    text_channel_list.append(channel)
            channel_list_len = len(text_channel_list)
            i = 0
            while i < channel_list_len:
                if 'new-joins' in str(text_channel_list[i]):
                    ctxchannel = bot.get_channel(text_channel_list[i].id)
                    guild = ctx.guild
                    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
                    channelid = ctx.channel.id
                    channel = Query()
                    out = db.search(channel.id == str(channelid))
                    
                    if str(out) != '[]':
                        await ctx.message.delete()
                        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
                        await asyncio.sleep(3)
                        await ctx.channel.purge(limit=1, check=None)
                        return
                    if ctxchannel.guild.id == ctx.guild.id:
                        em = discord.Embed(
                            title=None,
                            description=(f"{newuser.name} just got access. Make sure to greet them <@&{mods.id}>!"),
                            color=discord.Colour(0x000000)
                        )  
                        await ctxchannel.send(embed=em)
                        #DM Channel answer:
                        await newuser.send("You're now verified. Enjoy your stay!")
                i=i+1
        return


################################
## For Xeno ~

@bot.command()
async def adopt(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/adoptions_accepted.json')
    adoptions = Query()
    out = db.all()
    out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
    out = list(out.split(","))
    try:
        print(str(out[1]))
        if str(out[1]):
            if str(out[1]) == str(ctx.author.id):
                await ctx.send(f"`User already adopted by you.`")
                return
            if not os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json'):
                db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json')
                db.insert({'got_asked': '1'})
            else:
                db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json')
                out = db.all()
                out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
                out = list(out.split(","))
                out = int(out[1])+1
                db.update({'got_asked': str(out)})
            await ctx.send(f"`User already adopted by` <@!{str(out[1])}>")
            return
    except:
        pass
    db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/adoptions_refused.json')
    adoptions = Query()
    out = db.search(adoptions.member_id == str(ctx.author.id))
    out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","")
    out = list(out.split(","))
    
    try:
        if str(ctx.author.id) in str(out[1]):
            await ctx.send("`User refused already.`")
            return
    except:
        pass

    if member == ctx.message.author or member == 'null':
        em = discord.Embed(
        title=None,
        description=f"You can't adopt yourself ~",
        color=DEFAULT_EMBED_COLOR
        )
    else:
        em = discord.Embed(
        title=None,
        description=f"{ctx.author.mention} wants to adopt you, {member.mention}!\nDo you accept?\n**Be careful, your decision is final!**",
        color=DEFAULT_EMBED_COLOR
        )
        try:
            url = "https://www.sheri.bot/api/hug"
            headers = {'Authorization': 'Token '+SHERI_API_KEY}
            r = requests.get(url, headers=headers, timeout=5)
            print(r)
            if r:
                #print (r.json())
                em.set_image(url=str(r.json()["url"]))
        except requests.exceptions.ReadTimeout:
            await ctx.send('`Connection to api timed out.`')
            return
        except requests.exceptions.ConnectionError:
            await ctx.send('`Connection error.`')
            return
    msg = await ctx.send(embed=em)

    await msg.add_reaction('☑️')
    await msg.add_reaction('❌')
    
    def check(reaction, user):
        return user == member
        
    reaction, user = await bot.wait_for('reaction_add', check=check)
    print('reacton:'+str(reaction.emoji))

    if str(reaction.emoji) == '❌':
        await ctx.send(f"Sorry {ctx.author.mention}!\n {member.mention} refused.")
        if not os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json'):
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json')
            db.insert({'got_asked': '1'})
        else:
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json')
            out = db.all()
            out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
            out = list(out.split(","))
            out = int(out[1])+1
            db.update({'got_asked': str(out)})
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/adoptions_refused.json')
        db.insert({'member_id': str(ctx.author.id)})

    if str(reaction.emoji) == '☑️':
        await ctx.send(f"Congratulations {ctx.author.mention}!\n {member.mention} accepted.\nDo `_adopted` to see your status.")
        if not os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json'):
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json')
            db.insert({'got_asked': '1'})
        else:
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/got_asked.json')
            out = db.all()
            out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
            out = list(out.split(","))
            out = int(out[1])+1
            db.update({'got_asked': str(out)})
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{ctx.author.id}/adopted.json')
        db.insert({'member_id': str(member.id)})
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/adoptions_accepted.json')
        db.insert({'member_id': str(ctx.author.id)})
        
@bot.command()
async def adopted(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        user = ctx.author
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{ctx.author.id}/adopted.json')
        adoptions = Query()
        out = db.all()
        out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
        out = list(out.split(","))
        adoptedusers = []
        i=0
        for x in out:
            adoptedusers.append(f"<@!{out[i]}>")
            i=i+1
        if str(adoptedusers).replace("[","").replace("]","").replace("<@!member_id>","").replace("'","").replace(",","") == "<@!>":
            embed.add_field(name="Adoptions:", value="`None`")
        else:
            embed.add_field(name="Adoptions:", value=str(adoptedusers).replace("[","").replace("]","").replace("<@!member_id>","").replace("'","").replace(",",""))
        if not os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/got_asked.json'):
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/got_asked.json')
            db.insert({'got_asked': '0'})
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/got_asked.json')
        out = db.all()
        out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
        out = list(out.split(","))
        
        embed.add_field(name="Got asked for adoption:", value="`"+str(out[1])+"x`")
        
        if os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/adoptions_accepted.json'):
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/adoptions_accepted.json')
            adoptions = Query()
            out = db.all()
            out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
            out = list(out.split(","))
            embed.add_field(name="adopted by: ", value=f"<@!{str(out[1])}>")
        else:
            embed.add_field(name="adopted by: ", value="`Noone`")

        return await ctx.send(embed=embed)
    
    else:
        user = member
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/adopted.json')
        adoptions = Query()
        out = db.all()
        out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
        out = list(out.split(","))
        adoptedusers = []
        i=0
        for x in out:
            adoptedusers.append(f"<@!{out[i]}>")
            i=i+1
        if str(adoptedusers).replace("[","").replace("]","").replace("<@!member_id>","").replace("'","").replace(",","") == "<@!>":
            embed.add_field(name="Adoptions:", value="`None`")
        else:
            embed.add_field(name="Adoptions:", value=str(adoptedusers).replace("[","").replace("]","").replace("<@!member_id>","").replace("'","").replace(",",""))
        if not os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/got_asked.json'):
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/got_asked.json')
            db.insert({'got_asked': '0'})
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/got_asked.json')
        out = db.all()
        out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
        out = list(out.split(","))
        embed.add_field(name="Got asked for adoption:", value="`"+str(out[1])+"x`")
        
        if os.path.isfile(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/adoptions_accepted.json'):
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{user.id}/adoptions_accepted.json')
            adoptions = Query()
            out = db.all()
            out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
            out = list(out.split(","))
            embed.add_field(name="adopted by: ", value=f"<@!{str(out[1])}>")
        else:
            embed.add_field(name="adopted by: ", value="`Noone`")

        return await ctx.send(embed=embed)

@bot.command()
async def nsfw(ctx):
    info = await bot.application_info()
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    bot.automation = True
    #DM Channel answer:
    await ctx.author.send("NSFW on.")
    Tari = info.owner
    await Tari.send(f"`{ctx.author}` used `_nsfw` in {ctx.channel} on {ctx.guild}.")

@bot.command()
async def avatar(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    if member == ctx.message.author or member == 'null':
        em = discord.Embed(
        title=None,
        description=f"Avatar of {ctx.message.author.name}",
        color=DEFAULT_EMBED_COLOR
        )
        url = str(ctx.message.author.avatar_url).replace(".webp",".png")
        em.set_image(url=f"{url}")
    else:
        em = discord.Embed(
        title=None,
        description=f"Avatar of {member.name}",
        color=DEFAULT_EMBED_COLOR
        )
        url = str(member.avatar_url).replace(".webp",".png")
        em.set_image(url=f"{url}")
    await ctx.send(embed=em)

@bot.command()
async def channelname(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    db = TinyDB(f'atari/data/guilds/{guild.id}/{guild.id}.json')    # create a new storage for the database
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.channel_id == str(channelid))
    out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"')
    out = list(out.split(","))
    await ctx.send(out[3])

@bot.command()
async def add(ctx):
    if ctx.message.author.guild_permissions.administrator:
        guild = ctx.guild
        db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
        channelid = ctx.channel.id
        channel = Query()
        db.update(delete("id"), channel.id == str(channelid))
        await ctx.message.delete()
        await ctx.send("`Successfully removed channel from blacklist.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return


@bot.command()
async def lvl(ctx, member: discord.User = 'null'):
    def squareBrackets(string:str):
        newString = "[" + string + "]"
        return newString

    def fillGaps(string:str):
        amountToFill = 25 - len(string)
        return string + "-" * amountToFill # If you multiply strings, it will just make a bunch of them over and over in the same string. So "hello"*3 would give you "hellohellohello"

    def main(i):
        i=i
        string = "x"*i
        bar = str(squareBrackets(fillGaps(string)))
        return bar 

    if member == ctx.message.author or member == 'null':
        try:
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{ctx.message.author.id}/{ctx.message.author.id}.json')
        except:
            await ctx.send("`// No Data. //`")
            return
        user = Query()
        lvl = json.dumps(db.search(user.lvl != None))
        lvl = str(lvl).replace("{","").replace("}","").replace(":",",").replace("'",'"')
        lvl = list(lvl.split(","))
        em = discord.Embed(
        title=None,
        description=f"Userdata of {ctx.message.author.name}",
        color=DEFAULT_EMBED_COLOR
        )
        url = str(ctx.message.author.avatar_url).replace(".webp",".png")
        em.set_thumbnail(url=f"{url}")
        em.add_field(name="Level", value=str(lvl[1]).replace('"',''), inline=False)
        xp = int(str(lvl[3]).replace('"','').replace("]",""))
        level = int(str(lvl[1]).replace('"',''))
        maxxp = level*level*250
        level2xp = 100/maxxp
        level2xp = level2xp*xp
        level2xp = level2xp/4
        level2xp = int(round(level2xp,0))
        em.add_field(name="XP", value=str(lvl[3]).replace('"','').replace("]","")+"/"+str(maxxp), inline=False)
        em.add_field(name="Progress", value="`"+str(main(level2xp))+"`", inline=False)

        
    else:
        try:
            db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/{member.id}.json')
        except:
            await ctx.send("`// No Data. //`")
            return
        user = Query()
        lvl = json.dumps(db.search(user.lvl != None))
        lvl = str(lvl).replace("{","").replace("}","").replace(":",",").replace("'",'"')
        lvl = list(lvl.split(","))
        em = discord.Embed(
        title=None,
        description=f"Userdata of {member.name}",
        color=DEFAULT_EMBED_COLOR
        )
        url = str(member.avatar_url).replace(".webp",".png")
        em.set_thumbnail(url=f"{url}")
        em.add_field(name="Level", value=str(lvl[1]).replace('"',''), inline=False)
        xp = int(str(lvl[3]).replace('"','').replace("]",""))
        level = int(str(lvl[1]).replace('"',''))
        maxxp = level*level*250
        level2xp = 100/maxxp
        print(level2xp)
        level2xp = level2xp*xp
        print(level2xp)
        level2xp = level2xp/4
        level2xp = int(round(level2xp,0))
        print(level2xp)
        em.add_field(name="XP", value=str(lvl[3]).replace('"','').replace("]","")+"/"+str(maxxp), inline=False)
        em.add_field(name="Progress", value="`"+str(main(level2xp))+"`", inline=False)
    await ctx.send(embed=em)
    

@bot.command()
async def say(ctx, *, arg):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    resp = str(arg)
    if 'ATARI' in resp.upper() and 'CUTE' in resp.upper():
        await ctx.send('Get rickrolled instead https://www.youtube.com/watch?v=DLzxrzFCyOs')
        return
    if 'TARI' in resp.upper() and 'CUTE' in resp.upper() or 'TAR1' in resp.upper() and 'CUTE' in resp.upper() or 'T4R1' in resp.upper() and 'CUTE' in resp.upper():
        await ctx.send('Get rickrolled instead https://www.youtube.com/watch?v=DLzxrzFCyOs')
        return
    if 'ATARI' in resp.upper():
        await ctx.send(f"{resp}"[:4] + " - *screeeeeeeeee*")
        return
    await ctx.message.delete()
    await ctx.send(resp)

@bot.command()
async def owo(ctx, *, arg):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    resp = str(arg)
    uwu=[" ;;w;; "," (・`ω´・) "," >w< "," owo "," ^w^ "," UwU "]
    resp2 = resp.replace("y","nye").replace(" a "," da ").replace("o","aw").replace("p","pw").replace("s","sh").replace("g","w").replace("l","w").replace("r","w")
    resp = resp.replace("l","w").replace("r","w").replace("na","nya").replace("ne","nye").replace("nu","nyu").replace("ni","nyi").replace("no","nyo").replace("!",choice(uwu))
    await ctx.message.delete()
    await ctx.send(choice([resp,resp2]))
    return

@bot.command()
async def magicmath(ctx, *, arg):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    resp = int(arg)
    await ctx.send('Number: '+str(resp))
    i = 1
    while i < 4:
        if (resp % 2) == 0:
            await ctx.send(str(resp)+' is even.')
            resp1=resp
            resp=resp/2
            await ctx.send(str(resp1)+'/2='+str(resp))
        else:
            await ctx.send(str(resp)+' is odd.')
            resp1=resp
            resp=resp*3+1
            await ctx.send(str(resp1)+'*3+1='+str(resp))
        i += 1
    await ctx.send('Ending up with: '+str(resp))

@bot.command(name="spam", description="uhhhhh yeah.")
async def spam(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*blep*")
    else:
        await ctx.message.delete()
        await ctx.send(f"*{member.mention}*")
        await ctx.send(f"*{member.mention}*")
        await ctx.send(f"*{member.mention}*")
        await ctx.send(f"*{member.mention}*")
        await ctx.send(f"*{member.mention}*")
        deleted = await ctx.channel.purge(limit=6, check=None)


@bot.command()
async def clear(ctx, arg):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=int(arg), check=None)
    await ctx.send('Deleted {} message(s)'.format(len(deleted)))
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=int(1), check=None)
    

@bot.command(name="furinsult", description="insults you lol", aliases=['insult'])
async def furinsult(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    
    #await ctx.send('awww')

    if member == ctx.message.author or member == 'null':
        resp = [f"*Fuck you {ctx.message.author.name}*",
        f"I thought of {ctx.message.author.name} today. It reminded me to take out the trash.", 
        f"{ctx.message.author.name}, you are like a cloud. When you disappear it’s a beautiful day.", 
        f"Hold still. I’m trying to imagine {ctx.message.author.name} with personality.", 
        f"{ctx.message.author.name}, I’ll never forget the first time we met. But I’ll keep trying.", 
        f"{ctx.message.author.name}, don’t be ashamed of who you are. That’s your parents’ job.", 
        f"{ctx.message.author.name}, someday you'll go far, and I hope you stay there",
        f"No"]

        await ctx.send(choice(resp))
    ## for my aussie frien lmao
    #if '750277467578695740' in member.mention:
        #await ctx.send(f"*They’re actually called flip-flops {member.name}*")
    else:
        resp = [f"*Fuck you {member.name}*",
        f"I thought of {member.name} today. It reminded me to take out the trash.", 
        f"{member.name}, you are like a cloud. When you disappear it’s a beautiful day.", 
        f"Hold still. I’m trying to imagine {member.name} with personality.", 
        f"{member.name}, I’ll never forget the first time we met. But I’ll keep trying.", 
        f"{member.name}, don’t be ashamed of who you are. That’s your parents’ job.", 
        f"{member.name}, someday you'll go far, and I hope you stay there",
        f"No"]

        await ctx.send(choice(resp))

@bot.command(name="furcompliment", description="compliments you", aliases=['compliment'])
async def compliment(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    
    #await ctx.send('awww')

    if member == ctx.message.author or member == 'null':
        resp = [f"*Fuck you {ctx.message.author.name}*",
        f"You're an awesome friend {ctx.message.author.name}.", 
        f"{ctx.message.author.name}, you're a gift to those around you.",
        f"{ctx.message.author.name}, you're a smart cookie",
        f"{ctx.message.author.name}, you are awesome!",
        f"{ctx.message.author.name}, I like your style.",
        f"{ctx.message.author.name}, you have the best laugh.",
        f"{ctx.message.author.name}, I appreciate you.",
        f"{ctx.message.author.name}, you are the most perfect you there is.",
        f"{ctx.message.author.name}, you are enough.",
        f"{ctx.message.author.name}, you're strong.",
        f"{ctx.message.author.name}, your perspective is refreshing.",
        f"{ctx.message.author.name}, I'm grateful to know you.",
        f"{ctx.message.author.name}, you light up the room.",
        f"{ctx.message.author.name}, you deserve a hug right now.",
        f"{ctx.message.author.name}, you should be proud of yourself.",
        f"{ctx.message.author.name}, you're more helpful than you realize.",
        f"{ctx.message.author.name}, you have a great sense of humor.",
        f"{ctx.message.author.name}, you've got an awesome sense of humor!",
        f"{ctx.message.author.name}, you are really courageous.",
        f"{ctx.message.author.name}, your kindness is a pleasure to all who encounter it.",
        f"{ctx.message.author.name}, on a scale from 1 to 10, you're an 11.",
        f"{ctx.message.author.name}, you are strong.",
        f"{ctx.message.author.name}, you're even more beautiful on the inside than you are on the outside.",
        f"{ctx.message.author.name}, I'm inspired by you.",
        f"{ctx.message.author.name}, you're like a ray of sunshine on a really dreary day.",
        f"{ctx.message.author.name}, you are making a difference.",
        f"Thank you for being there for me, {ctx.message.author.name}.",
        f"{ctx.message.author.name}, you bring out the best in other people.",
        f"{ctx.message.author.name}, colors seem brighter when you're around.",
        f"{ctx.message.author.name}, you're wonderful.",
        f"{ctx.message.author.name}, you're better than a triple-scoop ice cream cone. With sprinkles.",
        f"{ctx.message.author.name}, our community is better because you're in it.",
        f"{ctx.message.author.name}, you're more fun than bubble wrap.",
        f"{ctx.message.author.name}, your voice is magnificent.",
        f"{ctx.message.author.name}, you're someone's reason to smile.",
        f"{ctx.message.author.name}, you're really something special.",
        f"{ctx.message.author.name}, thank you for being who you are."
        ]

        await ctx.send(choice(resp))
    ## for my aussie frien lmao
    #if '750277467578695740' in member.mention:
        #await ctx.send(f"*They’re actually called flip-flops {member.name}*")
    else:
        resp = [f"*Fuck you {member.name}*",
        f"You're an awesome friend {member.name}.", 
        f"{member.name}, you're a gift to those around you.",
        f"{member.name}, you're a smart cookie",
        f"{member.name}, you are awesome!",
        f"{member.name}, I like your style.",
        f"{member.name}, you have the best laugh.",
        f"{member.name}, I appreciate you.",
        f"{member.name}, you are the most perfect you there is.",
        f"{member.name}, you are enough.",
        f"{member.name}, you're strong.",
        f"{member.name}, your perspective is refreshing.",
        f"{member.name}, I'm grateful to know you.",
        f"{member.name}, you light up the room.",
        f"{member.name}, you deserve a hug right now.",
        f"{member.name}, you should be proud of yourself.",
        f"{member.name}, you're more helpful than you realize.",
        f"{member.name}, you have a great sense of humor.",
        f"{member.name}, you've got an awesome sense of humor!",
        f"{member.name}, you are really courageous.",
        f"{member.name}, your kindness is a pleasure to all who encounter it.",
        f"{member.name}, on a scale from 1 to 10, you're an 11.",
        f"{member.name}, you are strong.",
        f"{member.name}, you're even more beautiful on the inside than you are on the outside.",
        f"{member.name}, I'm inspired by you.",
        f"{member.name}, you're like a ray of sunshine on a really dreary day.",
        f"{member.name}, you are making a difference.",
        f"Thank you for being there for me, {member.name}.",
        f"{member.name}, you bring out the best in other people.",
        f"{member.name}, colors seem brighter when you're around.",
        f"{member.name}, you're wonderful.",
        f"{member.name}, you're better than a triple-scoop ice cream cone. With sprinkles.",
        f"{member.name}, our community is better because you're in it.",
        f"{member.name}, you're more fun than bubble wrap.",
        f"{member.name}, your voice is magnificent.",
        f"{member.name}, you're someone's reason to smile.",
        f"{member.name}, you're really something special.",
        f"{member.name}, thank you for being who you are."
        ]

        await ctx.send(choice(resp))

async def sheri_api_nsfw(ctx, api_url):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    if ctx.channel.is_nsfw():
        em = discord.Embed(
            title=None,
            description=None,
            color=discord.Colour(0x000000)
        )
        try:
            url = api_url
            headers = {'Authorization': 'Token '+SHERI_API_KEY}
            r = requests.get(url, headers=headers, timeout=5)
            print(r)
            if r:
                #print (r.json())
                em.set_image(url=str(r.json()["url"]))
                em.set_author(name=">> Link", url=str(r.json()["url"]))
                await ctx.send(embed=em)
        except requests.exceptions.ReadTimeout:
            await ctx.send('`Connection to api timed out.`')
            return
        except requests.exceptions.ConnectionError:
            await ctx.send('`Connection error.`')
            return
    else:
        await ctx.send("`NSFW. You can't use that command here.`")
        return

async def sheri_api_sfw(ctx, api_url):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    em = discord.Embed(
        title=None,
        description=None,
        color=discord.Colour(0x000000)
    )
    try:
        url = api_url
        headers = {'Authorization': 'Token '+SHERI_API_KEY}
        r = requests.get(url, headers=headers, timeout=5)
        print(r)
        if r:
            #print (r.json())
            em.set_image(url=str(r.json()["url"]))
            em.set_author(name=">> Link", url=str(r.json()["url"]))
            await ctx.send(embed=em)
    except requests.exceptions.ReadTimeout:
        await ctx.send('`Connection to api timed out.`')
        return
    except requests.exceptions.ConnectionError:
        await ctx.send('`Connection error.`')
        return

async def rf_api(ctx, api_url):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    em = discord.Embed(
        title=None,
        description=None,
        color=discord.Colour(0x000000)
    )
    try:
        url = api_url
        r = requests.get(url, timeout=5)
        print(r)
        if r:
            print (r.json())
            #em.set_image(url=str(r.json()["url"]))
            #em.set_author(name=">> Link", url=str(r.json()["url"]))
            em.add_field(name="- Random Fact -", value=str(r.json()["text"]), inline=False)
            await ctx.send(embed=em)
    except requests.exceptions.ReadTimeout:
        await ctx.send('`Connection to api timed out.`')
        return
    except requests.exceptions.ConnectionError:
        await ctx.send('`Connection error.`')
        return

## random facts command
@bot.command()
async def randomfact(ctx):
    await rf_api(api_url="https://uselessfacts.jsph.pl/random.json?language=en", ctx=ctx)

## Sheri api // nsfw

@bot.command()
async def sixnine(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/69", ctx=ctx)

@bot.command()
async def anal(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/anal", ctx=ctx)

@bot.command()
async def bang(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/bang", ctx=ctx)

@bot.command()
async def bisexual(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/bisexual", ctx=ctx)

@bot.command()
async def boob(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/boob", ctx=ctx)

@bot.command()
async def boobwank(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/boobwank", ctx=ctx)

@bot.command()
async def booty(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/booty", ctx=ctx)

@bot.command()
async def christmas(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/christmas", ctx=ctx)

@bot.command()
async def cumflation(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/cumflation", ctx=ctx)

@bot.command()
async def cuntboy(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/cuntboy", ctx=ctx)

@bot.command()
async def dick(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/dick", ctx=ctx)

@bot.command()
async def dp(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/dp", ctx=ctx)

@bot.command()
async def fbound(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/fbound", ctx=ctx)

@bot.command()
async def fcreampie(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/fcreampie", ctx=ctx)

@bot.command()
async def femboypresentation(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/femboypresentation", ctx=ctx)

@bot.command()
async def finger(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/finger", ctx=ctx)

@bot.command()
async def fpresentation(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/fpresentation", ctx=ctx)

@bot.command()
async def fseduce(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/fseduce", ctx=ctx)

@bot.command()
async def fsolo(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/fsolo", ctx=ctx)

@bot.command()
async def ftease(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ftease", ctx=ctx)

@bot.command()
async def futabang(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/futabang", ctx=ctx)

@bot.command()
async def gay(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/gay", ctx=ctx)

@bot.command()
async def gif(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/gif", ctx=ctx)

@bot.command()
async def lesbian(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/lesbian", ctx=ctx)

@bot.command()
async def mbound(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/mbound", ctx=ctx)

@bot.command()
async def mcreampie(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/mcreampie", ctx=ctx)

@bot.command()
async def mpresentation(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/mpresentation", ctx=ctx)

@bot.command()
async def mseduce(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/mseduce", ctx=ctx)

@bot.command()
async def msolo(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/msolo", ctx=ctx)

@bot.command()
async def mtease(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/mtease", ctx=ctx)

@bot.command()
async def nbulge(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nbulge", ctx=ctx)

@bot.command()
async def ncomics(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ncomics", ctx=ctx)

@bot.command()
async def ncuddle(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ncuddle", ctx=ctx)

@bot.command()
async def nfemboy(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nfemboy", ctx=ctx)

@bot.command()
async def nfuta(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nfuta", ctx=ctx)

@bot.command()
async def ngroup(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ngroup", ctx=ctx)

@bot.command()
async def nhold(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nhold", ctx=ctx)

@bot.command()
async def npokemon(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/npokemon", ctx=ctx)

@bot.command()
async def nprotogen(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nprotogen", ctx=ctx)

@bot.command()
async def nseduce(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nseduce", ctx=ctx)

@bot.command()
async def nsfwselfies(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nsfwselfies", ctx=ctx)

@bot.command()
async def nsolo(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nsolo", ctx=ctx)

@bot.command()
async def ntease(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ntease", ctx=ctx)

@bot.command()
async def ntrap(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ntrap", ctx=ctx)

@bot.command()
async def pawjob(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/pawjob", ctx=ctx)

@bot.command()
async def petplay(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/petplay", ctx=ctx)

@bot.command()
async def ride(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/ride", ctx=ctx)

@bot.command()
async def suck(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/suck", ctx=ctx)

@bot.command()
async def toys(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/toys", ctx=ctx)

@bot.command()
async def vore(ctx, member: discord.User = None):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    print(member)
    if member == ctx.message.author or member == None:
        await ctx.send(f"**Swallows {ctx.message.author.name} whole**")
        await sheri_api_nsfw(api_url="https://www.sheri.bot/api/vore", ctx=ctx)
        return
    if member.id == 349471395685859348 and ctx.message.author.id != 289802289638539274 or member.id == 563703335639711765:
        await ctx.send(f"Heh, you would like that eh :3")
        return
    if member.id == bot.user.id:
        await ctx.send("nuuuu qwq")
    else:
        await ctx.send(f"**{ctx.message.author.name} swallows {member.mention} whole**")
        await sheri_api_nsfw(api_url="https://www.sheri.bot/api/vore", ctx=ctx)
        return

@bot.command()
async def yiff(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/yiff", ctx=ctx)


## Sheri api // sfw

@bot.command()
async def bellyrub(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/belly_rub", ctx=ctx)

@bot.command()
async def blep(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/blep", ctx=ctx)

@bot.command()
async def cry(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/cry", ctx=ctx)

@bot.command()
async def cuddle(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/cuddle", ctx=ctx)

@bot.command()
async def hold(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/hold", ctx=ctx)

@bot.command()
async def maws(ctx):
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/maws", ctx=ctx)

@bot.command()
async def paws(ctx):
    if ctx.guild.id == 803486660296704000:
        await ctx.send("`NSFW. You can't use that here.`")
        return
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/paws", ctx=ctx)

@bot.command()
async def pokemon(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/pokemon", ctx=ctx)

@bot.command()
async def proposal(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/proposal", ctx=ctx)

@bot.command()
async def trickortreat(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/trickortreat", ctx=ctx)

## Sheri api // public

@bot.command()
async def bunny(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/bunny", ctx=ctx)

@bot.command()
async def cat(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/cat", ctx=ctx)

@bot.command()
async def deer(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/deer", ctx=ctx)

@bot.command()
async def fox(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/fox", ctx=ctx)

@bot.command()
async def dragone(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    em = discord.Embed(
        title=None,
        description="cute dragon uwu",
        color=discord.Colour(0x000000)
    )
    file = discord.File("atari/data/fenz.png", filename="fenz.png")
    em.set_image(url="attachment://fenz.png")
    await ctx.send(file=file, embed=em)

@bot.command()
async def dragon(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    dragon = ["https://cdn.discordapp.com/attachments/804009510050070629/807039974637174834/images_7.jpeg",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/2b9048eb-6b49-4cff-9800-11f338a3623e/daopew1-7b9fe91a-6947-4ffc-b6ed-b8b84b05eac2.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMmI5MDQ4ZWItNmI0OS00Y2ZmLTk4MDAtMTFmMzM4YTM2MjNlXC9kYW9wZXcxLTdiOWZlOTFhLTY5NDctNGZmYy1iNmVkLWI4Yjg0YjA1ZWFjMi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.TzLS_XmEgxdfeLcF_UrU9rY7ZTeWkiYMg5KoDYPNnhg",
    "https://cdn.discordapp.com/attachments/804009510050070629/807041214204739614/45c.jpeg",
    "https://cdn.discordapp.com/attachments/804009510050070629/807041226809278474/7d3118369b57cca2d6581e10ea6cc13d.jpg",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9de92e75-ddc7-4869-859e-2f6e4cca04b0/de38qyc-92307e83-edd6-4666-95df-56e8d4473a3b.png/v1/fill/w_1280,h_1280,q_80,strp/fluffy_dragon_by_ledommk_de38qyc-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD0xMjgwIiwicGF0aCI6IlwvZlwvOWRlOTJlNzUtZGRjNy00ODY5LTg1OWUtMmY2ZTRjY2EwNGIwXC9kZTM4cXljLTkyMzA3ZTgzLWVkZDYtNDY2Ni05NWRmLTU2ZThkNDQ3M2EzYi5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.NcILF0RvIgb0ixa8K5nNVaCkP_f10EeVFlD602na7MY",
    "https://www.pngkey.com/png/full/557-5571823_lythalia-angel-dragon-furry-cat-art.png",
    "https://pbs.twimg.com/media/D8TH6h5UwAE8ixK.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807042581228814366/6284e072b66d0ed6415744549113068e.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807042581380726814/0e55d20db9a4d1a084b29e3eb1776cd0.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807042581607088148/de9k2rx-b29089a4-63c3-4562-99e7-2f27ee17d67b.jpg",
    "https://i.redd.it/h86yqqkx79h51.png",
    "https://cutewallpaper.org/21/furry-wallpaper-phone/furry,-Dragon-Wallpapers-HD-Desktop-and-Mobile-Backgrounds.jpg",
    "https://fsa.zobj.net/crop.php?r=pOyYVYryGAYVkAG0lbQbSKf62uPodFNQqfFiQY7JZ-1yPEjEdT0ISUtoPhz5P2j9T9uThJ7pv9eXkdE3wbFgGW3sWGdbjMih3HZFdcTt1vE1IM9qpJ3fq8stJFvrBfjAFR2UKone6CHE-3rl",
    "https://c4.wallpaperflare.com/wallpaper/369/546/513/anthro-dragon-furry-waterfall-wallpaper-preview.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045109543075880/ZymSpellbook.png",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045074021122048/The-Dragon-Prince.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045073732108299/The-Dragon-Prince-Season-4-1.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045073388044288/Netflixs-The-Dragon-Prince-1280x720.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045073158144000/images_8.jpeg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045072809099274/film__19362-how-to-train-your-dragon-the-hidden-world--hi_res-b49e2fdd.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045072507371540/MV5BN2FiZDUxZTMtMzUxMi00NzYxLTg0NzEtNzViYTY4N2Y2MWFjXkEyXkFqcGdeQW1yb3NzZXI._V1_CR780484272_AL_UY268.jpg",
    "https://cdn.discordapp.com/attachments/806674289419091968/807045109887533056/962ceafa183985d4680cf662782bac93.jpg",
    "https://cdn.discordapp.com/attachments/804009510050070629/808067811540860940/image0-7.png",
    "https://cdn.discordapp.com/attachments/804010508180127853/808986052668555274/image0.png",
    "https://cdn.discordapp.com/attachments/806674289419091968/809464233553166366/1612947112.flufferderg_mikie100.jpg"
    ]
    currentpicture=choice(dragon)
    em = discord.Embed(
        title=None,
        description="So many cute dragons uwu",
        color=discord.Colour(0x000000)
    )
    em.set_image(url=str(currentpicture))
    em.set_author(name=">> Link", url=str(currentpicture))
    await ctx.send(embed=em)

@bot.command()
async def husky(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/husky", ctx=ctx)

@bot.command()
async def lion(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/lion", ctx=ctx)

@bot.command()
async def mur(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/mur", ctx=ctx)

@bot.command()
async def nature(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/nature", ctx=ctx)

@bot.command()
async def rpanda(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/rpanda", ctx=ctx)

@bot.command()
async def shiba(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/shiba", ctx=ctx)

@bot.command()
async def snek(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/snek", ctx=ctx)

@bot.command()
async def snep(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/snep", ctx=ctx)

@bot.command()
async def tiger(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/tiger", ctx=ctx)

@bot.command()
async def wolf(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/wolves", ctx=ctx)

@bot.command()
async def yeen(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/yeen", ctx=ctx)




@bot.command()
async def boop(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Boops {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} boops {member.name}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/boop", ctx=ctx)

@bot.command()
async def nboop(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Boops {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} boops {member.name}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nboop", ctx=ctx)

@bot.command()
async def pat(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await sheri_api_sfw(api_url="https://www.sheri.bot/api/pat", ctx=ctx)
    else:
        em = discord.Embed(
        title=None,
        description=(f"*{ctx.message.author.name} pats {member.name}*"),
        color=DEFAULT_EMBED_COLOR
        )
        file = discord.File("atari/data/ychpatpat.png", filename="ychpatpat.png")
        em.set_image(url="attachment://ychpatpat.png")
        await ctx.send(file=file, embed=em)
    
@bot.command()
async def restart(ctx):
    info = await bot.application_info()
    Tari = info.owner
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send("restarting...")
        await Tari.send(f"✓ `{ctx.author}` requested a restart in {ctx.channel} on {ctx.guild}.")
        await asyncio.sleep(3)
        sys.exit(f"{ctx.message.author.name} requested a restart.")
    else:
        await Tari.send(f"✘ `{ctx.author}` requested a restart in {ctx.channel} on {ctx.guild}, but had missing permissions.")
        await ctx.send(f"Sorry {ctx.message.author.name}, you do not have permissions to do that!")


@bot.command()
async def hug(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Hugs {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} hugs {member.name}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/hug", ctx=ctx)

@bot.command()
async def nhug(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Hugs {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} hugs {member.name}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nhug", ctx=ctx)

@bot.command()
async def kiss(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Kisses {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} kisses {member.name}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/kiss", ctx=ctx)

@bot.command()
async def nkiss(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Kisses {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} kisses {member.name}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nkiss", ctx=ctx)

@bot.command()
async def lick(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Licks {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} licks {member.name}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/lick", ctx=ctx)

@bot.command()
async def nlick(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Licks {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} licks {member.name}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nlick", ctx=ctx)

@bot.command()
async def iscute(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    rnd = random.randrange(0, 100)
    if member == ctx.message.author or member == 'null':
        await ctx.reply(f"{rnd}%".format(message))
        return
    else:
        await ctx.reply(f"{member.name} is {rnd}% cute")
        print(ctx.message.author)
        print(member)
        return

@bot.command()
async def isugleh(ctx, member: discord.User = 'null'):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    rnd = random.randrange(0, 100)
    if member == ctx.message.author or member == 'null':
        await ctx.reply(f"{rnd}%".format(message))
        return
    else:
        await ctx.reply(f"{member.name} is {rnd}% ugleh")
        return

@bot.command()
async def fursuit(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    try:
        headers = {'Authorization': FURRYV2_API_KEY, "User-Agent": "Atari/4.0.0 (https://twitter.com/Tarikazana, https://github.com/Tarikazana/Atari)"}
        r = requests.get('https://yiff.rest/V2/Furry/Fursuit', headers=headers, timeout=5)
        print(r)
        print(headers)
        if r:
            print (r.json())

            em.set_image(url=str(r.json()["images"][0]["url"]))

            await ctx.send(embed=em)
    except requests.exceptions.ReadTimeout:
        await ctx.send('`Connection to api timed out.`')
        return
    except requests.exceptions.ConnectionError:
        await ctx.send('`Connection error.`')
        return

@bot.command()
async def howl(ctx):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    try:
        headers = {'Authorization': FURRYV2_API_KEY, "User-Agent": "Atari/4.0.0 (https://twitter.com/Tarikazana)"}
        r = requests.get('https://yiff.rest/V2/Furry/Howl', headers=headers, timeout=5)
        if r:
            print (r.json())

            em.set_image(url=str(r.json()["images"][0]["url"]))

            await ctx.send(embed=em)
    except requests.exceptions.ReadTimeout:
        await ctx.send('`Connection to api timed out.`')
        return
    except requests.exceptions.ConnectionError:
        await ctx.send('`Connection error.`')
        return 

@bot.command()
async def textbox(ctx,*text):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    text = str(text)
    text = re.sub(r"[^\w\s]", '', text)
    text = re.sub(r"\s+", '%20', text)
    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    em.set_image(url="http://djosgaming.de:5000/textbox.png?avatar=" + str(bot.user.avatar_url).replace('webp','png') + "&background=https://media.discordapp.net/attachments/770230039299227649/798844465313873931/62411_anime_scenery_rain_rain.jpg&avatar_size=80&crt_overlay=False&avatar_position=right&text=" + str(text))
    await ctx.send(embed=em)

@bot.command()
async def reactionroles(ctx):
    await ctx.message.delete()
    msg = await ctx.send('**Role Menu: Self-Roles**\nReact to give yourself a role.\n\n:couple_ww: : Lesbian\n\n:rainbow_flag: : Gay\n\n:space_invader: : Bisexual')
    await msg.add_reaction('👩‍❤️‍👩')
    await msg.add_reaction('🏳️‍🌈')
    await msg.add_reaction('👾')
    
    def check(reaction, user):
        return user != bot.user
        
    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check)
        print('reacton:'+str(reaction.emoji))
        if str(reaction.emoji) == '🏳️‍🌈':
            await ctx.send('🏳️‍🌈')
            await reaction.remove(user)

        if str(reaction.emoji) == '👾':
            await ctx.send('👾')
            await reaction.remove(user)

        if str(reaction.emoji) == '👩‍❤️‍👩':
            await ctx.send('👩‍❤️‍👩')
            await reaction.remove(user)

        if str(reaction.emoji) != '👾' and str(reaction.emoji) != '🏳️‍🌈' and str(reaction.emoji) != '👩‍❤️‍👩':
            await reaction.remove(user)

@bot.command(name="mute", description="Mutes a user", aliases=['m'])
async def mute(ctx, member: discord.Member):
     if ctx.message.author.guild_permissions.administrator:
        user = member
        role = get(member.guild.roles, name='Muted')
        roles = user.roles
        del roles[0]
        await user.remove_roles(*roles)
        await user.add_roles(role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await ctx.send(embed=embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await ctx.send(embed=embed)

@bot.command()
async def setup(ctx):
    """
    msg = await ctx.send("```Do you want me to setup a role template for you?```")

    await msg.add_reaction('☑️')
    await msg.add_reaction('❌')
    
    def check(reaction, user):
        return user == ctx.message.author

    reaction = await bot.wait_for('reaction_add', check=check)
    print('reacton:'+str(reaction[0].emoji))

    if str(reaction[0].emoji) == '☑️':

        message = await ctx.send("```assigning roles for you...```")

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        async for member in ctx.guild.fetch_members(limit=None):
            role1 = get(ctx.guild.roles, name="━━ user status ━━")
            role2 = get(ctx.guild.roles, name="━━ permissions ━━")
            role3 = get(ctx.guild.roles, name="━━ characteristics ━━")
            role4 = get(ctx.guild.roles, name="━━ Atari Level System ━━")
            try:
                await member.add_roles(role1)
                await member.add_roles(role2)
                await member.add_roles(role3)
                await member.add_roles(role4)
            except:
                await ctx.guild.create_role(name="━━ user status ━━")
                await ctx.guild.create_role(name="━━ permissions ━━")
                await ctx.guild.create_role(name="━━ characteristics ━━")
                await ctx.guild.create_role(name="━━ Atari Level System ━━")
                role1 = get(ctx.guild.roles, name="━━ user status ━━")
                role2 = get(ctx.guild.roles, name="━━ permissions ━━")
                role3 = get(ctx.guild.roles, name="━━ characteristics ━━")
                role4 = get(ctx.guild.roles, name="━━ Atari Level System ━━")
                try:
                    await member.add_roles(role1)
                    await member.add_roles(role2)
                    await member.add_roles(role3)
                    await member.add_roles(role4)
                except AttributeError:
                    await asyncio.sleep(2)
                    role1 = get(ctx.guild.roles, name="━━ user status ━━")
                    role2 = get(ctx.guild.roles, name="━━ permissions ━━")
                    role3 = get(ctx.guild.roles, name="━━ characteristics ━━")
                    role4 = get(ctx.guild.roles, name="━━ Atari Level System ━━")
                    await member.add_roles(role1)
                    await member.add_roles(role2)
                    await member.add_roles(role3)
                    await member.add_roles(role4)
            await message.edit(content=f"```Running setup... // member {member.name} setup.```")
        await message.edit(content=f"```Finished.```")

    if str(reaction[0].emoji) == '❌':
        pass
    """
    msg2 = await ctx.send("```Do you want me to setup a 'muted' role?\nNote: It's recommended to do this in order to have Atari's mute feature working.\nOnly skip this step if you know what you're doing!```")

    await msg2.add_reaction('☑️')
    await msg2.add_reaction('❌')

    def check(reaction, user):
        return user == ctx.message.author
        
    reaction = await bot.wait_for('reaction_add', check=check)
    print('reacton:'+str(reaction[0].emoji))

    msg3 = await ctx.send("```Creating Roles...```")

    if str(reaction[0].emoji) == '☑️':
        role = get(ctx.guild.roles, name="Muted")
        role2 = get(ctx.guild.roles, name="✓ links")
        try:
            await ctx.message.author.add_roles(role)
            await ctx.message.author.remove_roles(role)
        except:
            await ctx.guild.create_role(name="Muted")
            await msg3.edit(content=f"```\"Muted\" created.```")
        try:
            await ctx.message.author.add_roles(role2)
            await ctx.message.author.remove_roles(role2)
        except:
            await ctx.guild.create_role(name="✓ links")
            await msg3.edit(content=f"```\"✓ links\" created.```")
        guild = ctx.message.guild
        muted = get(guild.roles, name='Muted')
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        muted: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel("muted", overwrites=overwrites)
        db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/automod.json')
        db.insert({'active': 'true'})
        await msg3.edit(content=f"```finished.```")
        await ctx.message.author.send("Thank you for using Atari. From the developer, Tari#0820, I shall pass on a huge hug.")
        await ctx.message.author.send("You should see, that a new channel was created, called \"muted\". That's Atari's moderation channel. It's used for isolating muted users.")

    if str(reaction[0].emoji) == '❌':
        await ctx.message.author.send("Thank you for using Atari. From the developer, Tari#0820, I shall pass on a huge hug.")
        await ctx.message.author.send("Nprmally you should see, that a new channel was created, called \"muted\". That's Atari's moderation channel. It's used for isolating muted users.\nYou choose to decline this. If you want to have it later, simply run _setup again.")

@bot.command(name="remindme", description="Reminds you of smth.", aliases=['rm'])
async def remindme(ctx, *reminder):
    guild = ctx.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = ctx.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        await ctx.message.delete()
        await ctx.send("`This channel has been blacklisted. Undo it with _add.`")
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1, check=None)
        return
    reminder=str(reminder)

    if reminder == '()' or reminder == "('to',)":
        em = discord.Embed(
        title="- Command: " + BOT_PREFIX + "remindme -",
        description="Command help:",
        color=DEFAULT_EMBED_COLOR
    )

        em.add_field(name="Description:", value="Set a reminder", inline=False)
        em.add_field(name="Usage:", value=BOT_PREFIX + "remindme to [reminder]\n[Time in M/H/D]", inline=False)
        em.add_field(name="Example:", value="User:" + BOT_PREFIX + "remindme to do smth\nAtari:Surely, when shall I remind you?\nUser:1m", inline=False)
        em.add_field(name="Important:", value="*It's recommended to not use days, since Atari is still in development and after every restart the reminders are reset.*", inline=False)
        await ctx.message.delete()
        await ctx.send(embed=em)
        return

    reminder = reminder[1:]
    reminder = reminder[:-1]

    reminder = reminder.replace("'", '')
    reminder = reminder.replace(",", '')
    reminder = reminder.replace("to ", '')
    reminder = reminder.replace(" my ", " your ")
    reminder = reminder.replace(" me ", " you ")
    reminder = reminder.replace(".", "")
    await ctx.send("Surely, when shall I remind you?")
    try:
        msg = await bot.wait_for('message', check=None, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send('Please specify a time next time.')
    else:
        # D/H/M
        if 'D' in msg.content.upper():
            msg.content = msg.content[:-1]
            msgtime = 'days'

        if 'H' in msg.content.upper():
            msg.content = msg.content[:-1]
            msgtime = 'hours'

        if 'M' in msg.content.upper():
            msg.content = msg.content[:-1]
            msgtime = 'minutes'

        try:
            msgcatch = int(f"{msg.content}")

        except ValueError:
            await ctx.send("Uhhh only numbers pls ^^'")
        
        if msgtime == 'days':
            if int(msg.content) == 1:
                await ctx.send(f'I will remind you in {msg.content} {msgtime[:-1]}.')
            if int(msg.content) > 1:
                await ctx.send(f'I will remind you in {msg.content} {msgtime}.')
            reminder_time = int(msg.content) * 60 * 60 * 24
        
        if msgtime == 'hours':
            if int(msg.content) == 1:
                await ctx.send(f'I will remind you in {msg.content} {msgtime[:-1]}.')
            if int(msg.content) > 1:
                await ctx.send(f'I will remind you in {msg.content} {msgtime}.')
            reminder_time = int(msg.content) * 60 * 60

        if msgtime == 'minutes':
            if int(msg.content) == 1:
                await ctx.send(f'I will remind you in {msg.content} {msgtime[:-1]}.')
            if int(msg.content) > 1:
                await ctx.send(f'I will remind you in {msg.content} {msgtime}.')
            reminder_time = int(msg.content) * 60

                   
        print(f'msg.content - {msg.content}')
        print(f'reminder_time - {reminder_time}')
        await asyncio.sleep(reminder_time)
        await ctx.reply(f"Hey, {ctx.message.author.name}. \nI should remind you to {reminder}.")
"""
@bot.command()
async def roles(ctx):
    guild = ctx.guild
    user = ctx.message.author
    original_stdout = sys.stdout # Save a reference to the original standard output
    with open(f'atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json', 'w') as textfile:
        print(f"writing into atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json ...")
        sys.stdout = textfile
        print('{"_default":{')
        sys.stdout = original_stdout # Reset the standard output to its original value
    i=0
    print(f"listing roles in atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json ...")
    for role in user.roles:
        with open(f'atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json', 'a') as textfile:
            sys.stdout = textfile
            print('"'+str(i)+'": ' '{"role_id": "' + str(role.id) + '"},')
            sys.stdout = original_stdout # Reset the standard output to its original value
            
        i=i+1
    with open(f'atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json', 'rb+') as f:
        print(f"truncating atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json ...")
        f.seek(0,2)                 # end of file
        size=f.tell()               # the size...
        f.truncate(size-3)          # truncate at that size - how ever many characters
        
        
    with open(f'atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json', 'a') as textfile:
        print(f"closed atari/data/guilds/{guild.id}/users/{ctx.message.author.id}/roles.json ...")
        sys.stdout = textfile
        print("}}")
        sys.stdout = original_stdout # Reset the standard output to its original value

    roles = user.roles
    del roles[0]
    await user.remove_roles(*roles)
    print("removed roles")

    role_ids = 
    db = TinyDB(f'atari/data/guilds/{ctx.guild.id}/users/{member.id}/adoptions_accepted.json')
    adoptions = Query()
    out = db.all()
    out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"','').replace(" ","")
    out = list(out.split(","))
    
    roles = user.guild.get_role(role_id)
    await user.add_roles(*roles)
"""
    

async def automute(member: discord.Member):
    user = member
    role = get(member.guild.roles, name='Muted')
    roles = user.roles
    del roles[0]
    await user.remove_roles(*roles)
    await user.add_roles(role)

bot.shut = False
bot.msgcontent = 'null'
bot.msguser = 'null'
bot.spamcontent = 'null'
bot.spamuser = 'null'
bot.before=time.monotonic()
@bot.listen('on_message')
async def message(message):
    bot.after = (time.monotonic() - bot.before) * 1000
    # current date and time
    now = datetime.now()
    timestamp = round(datetime.timestamp(now))

    original_stdout = sys.stdout # Save a reference to the original standard output
    try:
        content = bytes(message.content, 'utf-8')
        content = (content).decode('utf-8')
    except UnicodeEncodeError:
        print("string is not UTF-8")
        return

    guild = message.guild
    try:
        if not os.path.exists(f'atari/data/guilds/{guild.id}/blacklist'):
            os.makedirs(f'atari/data/guilds/{guild.id}/blacklist')
        if not os.path.exists(f'atari/data/guilds/{guild.id}/users'):
            os.makedirs(f'atari/data/guilds/{guild.id}/users')
        if not os.path.exists(f'atari/data/guilds/{guild.id}/users/{message.author.id}'):
            os.makedirs(f'atari/data/guilds/{guild.id}/users/{message.author.id}')
        if not os.path.isfile(f'atari/data/guilds/{guild.id}/users/{message.author.id}/status.json'):
            db = TinyDB(f'atari/data/guilds/{guild.id}/users/{message.author.id}/status.json')
            db.insert({'status': 'normal'})
        if not os.path.exists(f'atari/logs/{guild.id}'):
            os.makedirs(f'atari/logs/{guild.id}')
    except AttributeError:
        pass

    # we do not want the bot to reply to itself
    if message.author == bot.user:
        guild = message.guild
        db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
        channelid = message.channel.id
        channel = Query()
        out = db.search(channel.id == str(channelid))
        
        if str(out) != '[]':
            return
        if message.attachments != None and content == '':
            with open(f'atari/logs/{guild.id}/logs-{datetime.now().day}.{datetime.now().month}.{datetime.now().year}.txt', 'a') as textfile:
                sys.stdout = textfile
                print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [image]")
                sys.stdout = original_stdout # Reset the standard output to its original value
            print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {bcolors.ENDC}{bcolors.PURPLE}{message.author} in {message.channel.name} on {message.guild.name}:\n [image]{bcolors.ENDC}")
        if content != '':
            with open(f'atari/logs/{guild.id}/logs-{datetime.now().day}.{datetime.now().month}.{datetime.now().year}.txt', 'a') as textfile:
                sys.stdout = textfile
                try:
                    print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {content}")
                except UnicodeEncodeError:
                    print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [except UnicodeEncodeError] string is not UTF-8")
                    sys.stdout = original_stdout
                    print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [except UnicodeEncodeError] string is not UTF-8{bcolors.ENDC}")
                    return
                sys.stdout = original_stdout # Reset the standard output to its original value
            print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {bcolors.ENDC}{bcolors.PURPLE}{message.author}{bcolors.ENDC} in {bcolors.CYAN}{message.channel.name}{bcolors.ENDC} on {message.guild.name}:\n {content}{bcolors.ENDC}")
    if message.author.bot: return
    if message.author.id == 355330245433360384: return
    
    rnd = random.randrange(0, 100)
    if message.attachments != None and content == '':
        with open(f'atari/logs/{guild.id}/logs-{datetime.now().day}.{datetime.now().month}.{datetime.now().year}.txt', 'a') as textfile:
                sys.stdout = textfile
                print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {message.attachments}")
                sys.stdout = original_stdout # Reset the standard output to its original value
        print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {message.attachments}{bcolors.ENDC}")
    if content != '':
        with open(f'atari/logs/{guild.id}/logs-{datetime.now().day}.{datetime.now().month}.{datetime.now().year}.txt', 'a') as textfile:
                sys.stdout = textfile
                try:
                    print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {content}")
                except UnicodeEncodeError:
                    print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [except UnicodeEncodeError] string is not UTF-8")
                    sys.stdout = original_stdout
                    print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [except UnicodeEncodeError] string is not UTF-8{bcolors.ENDC}")
                    return
                sys.stdout = original_stdout # Reset the standard output to its original value
        print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author}{bcolors.ENDC} in {bcolors.CYAN}{message.channel.name}{bcolors.ENDC} on {message.guild.name}:\n {content}")

        
    #content = content

    ## LEVELSYSTEM ##
    
    
    if message.author.id in bot.spamuserlist:
            print("Spamuserlist: "+str(bot.spamuserlist))
            print(f"{message.author.name} spammed.")
            bot.before=time.monotonic()
            return
    if bot.after < 1000:
        bot.before=time.monotonic()
        bot.spamuserlist.append(message.author.id)

    if message.guild.id == "803486660296704000":
        approval = get(message.author.roles, name="✓ rules")
        if str(approval) != "✓ rules":
            return

    if not (bot.spamcontent in content and bot.spamuser == message.author.id) and len(content) > 4:

        db = TinyDB(f'atari/data/guilds/{guild.id}/users/{message.author.id}/{message.author.id}.json')
        Fruit = Query()
        lvl = db.all()

        if str(lvl) == '[]':
            db.insert({'lvl': '1', 'xp': 1})
        else:
            user = Query()
            lvl = json.dumps(db.search(user.lvl != None))
            lvl = str(lvl).replace("{","").replace("}","").replace(":",",").replace("'",'"')
            lvl = list(lvl.split(","))
            newxp = str(round(int(str(lvl[3]).replace('"','').replace("]",""))+1))
            currlvl = str(lvl[1]).replace('"','').replace("]","").replace(" ","")
            lvlrole = f"Lvl {currlvl}"
            role = get(message.author.roles, name=lvlrole)
            if role == None:
                if int(currlvl) > 1:
                    oldrole = get(message.guild.roles, name=f"Lvl {str(int(currlvl)-1)}")
                    await message.author.remove_roles(oldrole)
                role = get(message.guild.roles, name=lvlrole)
                try:
                    await message.author.add_roles(role)
                except:
                    await guild.create_role(name=lvlrole, colour=discord.Colour(0x8cff00))
                    role = get(message.guild.roles, name=lvlrole)
                    try:
                        await message.author.add_roles(role)
                    except AttributeError:
                        await asyncio.sleep(2)
                        role = get(message.guild.roles, name=lvlrole)
                        await message.author.add_roles(role)

            if int(newxp) > round(int(str(lvl[1]).replace('"','').replace("]",""))*250*int(currlvl)):
                newlvl = str(round(int(str(lvl[1]).replace('"','').replace("]",""))+1))
                db.update({'lvl': newlvl, 'xp': 0})
            else:
                db.update({'lvl': currlvl, 'xp': newxp})

    bot.spamcontent = message.content
    bot.spamuser = message.author.id
    bot.before=time.monotonic()



    if str(bot.user.id) in content and not "_" in content:
        await message.channel.send(f"{message.author.mention}")

    bad_words = [" cock ","nigger","nigga","bastard","fags","pussy","dick","cunt","faggot"]
    bad_words_count=0
    info = await bot.application_info()
    Tari = info.owner
    if os.path.isfile(f'atari/data/guilds/{message.guild.id}/automod.json'): # automod
        for x in bad_words:
            if bad_words[bad_words_count] in content.lower():
                await automute(message.author)
                await message.delete()
                await Tari.send(f"`{message.author}` used `'{message.content}'` in {message.channel} on {message.guild}.")
                return
            bad_words_count=bad_words_count+1
        if "burn" in content.lower() and "furries" in content.lower() or "burn" in content.lower() and "furrys" in content.lower():
            await automute(message.author)
            await message.delete()
            await Tari.send(f"`{message.author}` used `'{message.content}'` in {message.channel} on {message.guild}.")
            return


    if 'https://' in content.lower() or 'http://' in content.lower():
        if os.path.isfile(f'atari/data/guilds/{message.guild.id}/automod.json'): # link protection
            if bot.msgcontent in content and bot.msguser == message.author.id:
                await message.delete()
                return
            linkrole = get(message.guild.roles, name="✓ links")
            y = len(message.author.roles)-1
            j = 0
            while j <= y:
                if str(linkrole.id) in str(message.author.roles[j].id): return
                #print(message.author.roles[j].id)
                j=j+1
            with open(f'atari/logs/{guild.id}/logs-{datetime.now().day}.{datetime.now().month}.{datetime.now().year}.txt', 'a') as textfile:
                sys.stdout = textfile
                try:
                    print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {content}")
                except UnicodeEncodeError:
                    print(f"{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [except UnicodeEncodeError] string is not UTF-8")
                    sys.stdout = original_stdout
                    print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [except UnicodeEncodeError] string is not UTF-8{bcolors.ENDC}")
                    return
                print(f"{bcolors.CYAN}Missing role '✓ links' - message from {message.author} deleted.{bcolors.ENDC}")
                sys.stdout = original_stdout # Reset the standard output to its original value
            print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {content}{bcolors.ENDC}")
            print(f"{bcolors.CYAN}Missing role '✓ links' - message from {message.author} deleted.{bcolors.ENDC}")
            await message.delete()
            await message.channel.send('`You have no permission to send links.`')

            bot.msgcontent = content
            bot.msguser = message.author.id
            return

    """
    preventing Atari from responding in channels
    """
    #Whitelist
    guild = message.guild
    db = TinyDB(f'atari/data/guilds/{guild.id}/blacklist/removed.json')
    channelid = message.channel.id
    channel = Query()
    out = db.search(channel.id == str(channelid))
    
    if str(out) != '[]':
        return

    if content.upper().startswith('!D BUMP'):
        await asyncio.sleep(7200)
        await message.channel.send('Server can be bumped again.')

    if 'SHUT' in content.upper() and rnd < 50:
        if 'SHUT' in content.upper() and 'ATARI' in content.upper():
            await message.channel.send('*lmao*')
            return
        if content.upper().startswith('?SHUT'):
            await message.channel.send("Surely, {0.author.name}.".format(message))
            bot.shut=True
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="muted."))
            print('Bot is muted.')
            time.sleep(600)
            await message.channel.send("I'm back <3".format(message))
            bot.shut=False
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Tawi"))
            print('Bot is unmuted.')
        if content.upper().startswith('?UNSHUT'):
            await message.channel.send("<3".format(message))
            bot.shut=False
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Tawi"))
            print('Bot is unmuted.')
    elif content.upper().startswith('SHUT') and rnd > 49:
        await message.channel.send("Shut, {0.author.name} *lmao*.".format(message))
        return            
    
    if bot.shut==True: return

    if content.upper() == 'E' and rnd > 49:
        await message.channel.send('A')
        await message.channel.send('Sports')

    if content.upper() == 'E' and rnd < 50:
        await message.channel.send('6')
        await message.channel.send('2')
        await message.channel.send('1')
    
    if content.upper().startswith("ITS IN THE GAME") or content.upper().startswith("IT'S IN THE GAME"):
        await message.channel.send('ikr')

    if content.upper().startswith('HELLO ATARI'):
        await message.channel.send('Hello!')
        

    if content.upper().startswith('HEWWO ATARI'):
        await message.channel.send('Hewwo!')
        

    if content.upper().startswith('HEY ATARI'):
        await message.channel.send('Hey! :3')
        

    if content.upper().startswith('HI ATARI'):
        await message.channel.send('Hiya!')
        

    if content.upper().startswith('MOIN ATARI'):
        await message.channel.send('Moin :p')
        
    
    if content.upper().startswith('UWU'):
        await message.channel.send('uwu')
        

    if content.upper().startswith('OWO'):
        await message.channel.send('owo')
        
    
    if content.upper().startswith('U ON'):
        await message.channel.send('*e*')
        await message.channel.send('u on')

    if content.upper().startswith("I'M ATARI") or content.upper().startswith("IM ATARI"):
        await message.channel.send('*e*')
        await message.channel.send("And I'm {0.author.name} lmao".format(message))
        return

    if content.upper().startswith("I'M FAOLAN") or content.upper().startswith("IM FAOLAN"):
        await message.channel.send("***Puts on a teal bandana, 3 tails, wings and one robo contact*** Look! I'm Faolan! Howdy howdy howdy!".format(message))
        return

    if content.upper().startswith("I'M BLADE") or content.upper().startswith("IM BLADE"):
        await message.channel.send("***Puts on Spyro costume*** Look! I'm Blade! Rawr rawr rawr!".format(message))
        return

    if content.upper().startswith("I'M TARI") or content.upper().startswith("IM TARI"):
        await message.channel.send("***Puts on proto costume*** Look! I'm Tari! Beep boop beep!".format(message))
        return

    if content.upper().startswith("I'M XENO") or content.upper().startswith("IM XENO"):
        await message.channel.send("***GETS COOKIE JAR*** Look! I'm Xeno! I'm Cute! >w<".format(message))
        return
        
    
    if 'HORNY' in content.upper() and rnd > 49:
        await message.channel.send('***OwO!***')
        

    if 'HORNI' in content.upper() and rnd > 49:
        await message.channel.send('***OwO!***')
        

    if 'TAWI' in content.upper():
        await message.channel.send('*Tawi uwu*')
        
    
    if content.upper().startswith("TARI IS CUTE")or content.upper().startswith('TAR1 IS CUTE') or content.upper().startswith('T4R1 IS CUTE'):
        await message.channel.send('***no u***')
        

    if 'NOE' in content.upper() and rnd > 49:
        await message.channel.send('*yes*')
        

    if 'DAD BOT' in content.upper():
        await message.channel.send('*sweats*')



    ## User specific stuff I added bc I had the bored

    if 'CUTE' in content.upper() and message.author.id == 683813339369177148 and rnd > 49:
        await message.channel.send('*Alpha is cute*')
        return
        

    if 'CUTE' in content.upper() and message.author.id == 289802289638539274 and rnd > 49:
        await message.channel.send('*Lynix is so cute uwu*')
        return

    if 'VORE' in content.upper() and not BOT_PREFIX+'VORE' in content.upper():
        if rnd > 90:
            await message.channel.send("I'm kinda hungyyy")
            await message.channel.send(f"come hereee {message.author.mention}")
            try:
                msg = await bot.wait_for('message', check=None, timeout=15.0)
            except asyncio.TimeoutError:
                await message.channel.send(f'**noms {message.author.name}**')
            else:
                await message.channel.send("**noms you**".format(msg))
                return
        if rnd > 49:
            await message.channel.send("**vore**")
            return
        if rnd > 24:
            await message.channel.send("*nuuu don't eat me qwq*")
            return
        if rnd > -1:
            await message.channel.send("*vore owo*")
            return
        
    
    if content.upper().startswith("NO U") and rnd > 69 or content.upper().startswith("NO YOU") and rnd > 69:
        await message.channel.send('https://i.etsystatic.com/23988690/r/il/a59855/2478171220/il_570xN.2478171220_llv4.jpg')
    
    if content.upper().startswith("NO U") or content.upper().startswith("NO YOU"):
        await message.channel.send('no u')
        
    if content.upper().startswith("AAAAA"):
        await message.channel.send('*aaaaaaaaaa*')

    if content.upper().startswith("BRRRR"):
        await message.channel.send('*brrrrrrrrr*')

    ## well... yeeaaaaa let's not talk about this
    if 'BLYAT' in content.upper() or 'SUKA' in content.upper():
        await message.channel.send('*nyet suka blyat*')
        await message.channel.send('*Битч*')
        

    if content.upper().startswith("EEEEE"):
        await message.channel.send('*eeeeeeeeee*')
        

    if content.upper().startswith("I'M ") and rnd > 69:
        content = content.capitalize().replace("I'm ", '')
        content = content.replace(".", '')
        print("Name before: "+message.author.display_name)
        oldnick=message.author.display_name
        response = f"Hi {content}, I'm Atari"
        await message.channel.send(response)

        await message.author.edit(nick=content)
        await asyncio.sleep(10)
        await message.author.edit(nick=oldnick)
        await message.channel.send(f"lmao sry, {oldnick}")

        
    ## for my german friends that forget how to type that ' thingy
    if content.upper().startswith("IM ") and rnd > 69:
        content = content.capitalize().replace("Im ", '')
        content = content.replace(".", '')
        print("Name before: "+message.author.display_name)
        oldnick=message.author.display_name
        await message.author.edit(nick=content)
        response = f"Hi {content}, I'm Atari"
        await message.channel.send(response)
        await asyncio.sleep(10)
        await message.author.edit(nick=oldnick)
        await message.channel.send(f"lmao sry, {oldnick}")
        
    ## more user specific stuff I added bc I had the bored      
    if content.upper().startswith("IM") and message.author.id == 355330245433360384 and rnd > 90:
        await message.channel.send("Flonky, you're such a bot :3")
        return

    if content.upper().startswith("I'M") and message.author.id == 355330245433360384 and rnd > 90:
        await message.channel.send("Flonky, you're such a bot :3")
        return

    ## how to make a bot have conversations pt1

    if 'HRU' in content.upper() and 'ATARI' in content.upper() or 'HOW ARE YOU' in content.upper() and 'ATARI' in content.upper():
        await message.channel.send("I'm doing goood, {0.author.name}. <3".format(message))
        return

    if content.upper().startswith("IS <@!797844828834365461>") and rnd < 90 or content.upper().startswith("IS ATARI") and rnd < 90:
        await message.reply("***no***")
        return

    if content.upper().startswith("IS <@!797844828834365461>") and rnd > 89 or content.upper().startswith("IS ATARI") and rnd > 89:
        await message.reply("***||~~yes~~||***")
        return

    if 'ATARI' in content.upper() and not BOT_PREFIX+'SAY' in content.upper():
        if 'ATARI' in content.upper() and 'NOT NOT' in content.upper():
                await message.channel.send("**not not**".format(message))
                return
        if 'ATARI' in content.upper() and ('CUTE' in content.upper() or 'CUTIE' in content.upper()) and not "AREN'T" in content.upper() and not "CUTEN'T" in content.upper() and not "CUTIEN'T" in content.upper() and not "NOT" in content.upper():
            await message.channel.send("aaaaaaaaaa")
            await message.channel.send("You're cuteee")
            return
        if 'ATARI' in content.upper() and ('CUTE' in content.upper() or 'CUTIE' in content.upper()) and ("AREN'T" in content.upper() or "CUTEN'T" in content.upper() or "CUTIEN'T" in content.upper() or "NOT" in content.upper()) and rnd > 49:
            await message.channel.send("qwq".format(message))
            return
        if 'ATARI' in content.upper() and ('CUTE' in content.upper() or 'CUTIE' in content.upper()) and ("AREN'T" in content.upper() or "CUTEN'T" in content.upper() or "CUTIEN'T" in content.upper() or "NOT" in content.upper()) and rnd < 50:
            await message.channel.send("But...".format(message))
            await message.channel.send("But...".format(message))
            await message.channel.send("But you are.".format(message))
            return
        

        try:
            msg = await bot.wait_for('message', check=None, timeout=60.0)
        except asyncio.TimeoutError:
            await message.channel.send('<3')
        else:
            if 'NOT NOT' in msg.content.upper():
                await message.channel.send("**not not**".format(msg))
                return
            if msg.content.upper().startswith("YOU'RE NOT CUTE") and rnd > 49 or msg.content.upper().startswith("YOU'RE NOT A CUTIE") and rnd > 49 or "AREN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "CUTEN'T" in msg.content.upper() and rnd > 49 or "CUTEN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper() and rnd > 49:
                await message.channel.send("qwq".format(msg))
                return
            if msg.content.upper().startswith("YOU'RE NOT CUTE") and rnd < 50 or msg.content.upper().startswith("YOU'RE NOT A CUTIE") and rnd < 50 or "AREN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "CUTEN'T" in msg.content.upper() and rnd < 50 or "CUTEN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper() and rnd < 50:
                await message.channel.send("But...".format(msg))
                await message.channel.send("But...".format(msg))
                await message.channel.send("But you are.".format(msg))
                return
            if 'HRU' in msg.content.upper() or 'HOW ARE YOU' in msg.content.upper():
                await message.channel.send("I'm finee, {0.author.name}.".format(msg))
            if msg.content.upper().startswith("YOU AREN'T CUTEN'T") or 'CUTE' in msg.content.upper() or 'CUTIE' in msg.content.upper() and not "AREN'T" in msg.content.upper() and not "CUTEN'T" in msg.content.upper() and not "NOT" in msg.content.upper() and not "IS" in msg.content.upper() or 'CUTE' in msg.content.upper() and "AREN'T" in msg.content.upper() and 'NOT' in msg.content.upper() and not "IS" in msg.content.upper() or "CUTEN'T" in msg.content.upper() and 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper() and not "IS" in msg.content.upper():
                await message.channel.send("You're cute aswell, {0.author.name}.".format(msg))
                return


## run that stuff
bot.run(TOKEN)