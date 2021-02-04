# bot.py
##############################################################
##                                                          ##
##                  -    Imports  -                         ##
##                                                          ##
##############################################################
import asyncio
import os
import random
import re
from discord import errors
import requests
import json
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
from random import choice
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
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('GUILD_ID')
BOT_VERSION = os.getenv('BOT_VERSION')
BOT_PREFIX = os.getenv('PREFIX')
WHITELIST = os.getenv('SERVER_WHITELIST')
SHERI_API_KEY = os.getenv('SHERI_API_KEY')
FURRYV2_API_KEY = os.getenv('FURRYV2_API_KEY')
E621_API_KEY = os.getenv('E621_API_KEY')
E621_USER = os.getenv('E621_USER')

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

bot = commands.Bot(command_prefix=BOT_PREFIX)
## bot = commands.AutoShardedBot(shard_count=10, command_prefix=BOT_PREFIX)
## It is recommended to use this client only if you have surpassed at least 1000 guilds.

intents = discord.Intents(messages=True, guilds=True)
intents.messages = True

session = None

status = ["Tawi", "_help"]

bot.automation = False

@bot.event
async def on_ready():
    # current date and time
    now = datetime.now()
    timestamp = round(datetime.timestamp(now))
    print(f"{bcolors.PURPLE}{datetime.fromtimestamp(timestamp)} - {bot.user} has connected to Discord!{bcolors.ENDC}")

    print ("------------------------------------")
    print (f"Bot Name: {bot.user.name}")
    print (f"Bot ID: {bot.user.id}")
    print (f"Bot Created: {bot.user.created_at}")
    print (f"Discord Version: {discord.__version__}")
    print (f"Bot Version: {BOT_VERSION}")
    print ("------------------------------------")

    print(f"{bcolors.PURPLE}setting activity...{bcolors.ENDC}")

    ## useful docs for setting activities
    ## https://medium.com/python-in-plain-english/how-to-change-discord-bot-status-with-discord-py-39219c8fceea
    ## https://stackoverflow.com/questions/59126137/how-to-change-discord-py-bot-activity
    change_status.start()
    automated_yiff.start()
    print(f"{bcolors.WARNING}activity set.{bcolors.ENDC}")

    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})'
    )
    print(f'Guild Members:{guild.member_count}')
    print ("------------------------------------")
    print(f"{bcolors.PURPLE}Started in {round(time.time()-start,2)} seconds.{bcolors.ENDC}\n")
    print ("\nMessage Log:")

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=choice(status)))

@tasks.loop(seconds=60)
async def automated_yiff():
    if bot.automation == False: return
    channel = discord.utils.get(bot.get_all_channels(), guild__name=GUILD, name=f'automated-yiff')
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
    

## Getting rid of default commands

bot.remove_command('help')
bot.remove_command('say')

######################################################
##                  - COMMANDS -                    ##
######################################################

@bot.command(name="help", description="Returns all commands available", aliases=['h'])
async def help(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
    em = discord.Embed(
        title="- Help -",
        description="**Commands**",
        color=DEFAULT_EMBED_COLOR
    )

    em.set_thumbnail(url=bot.user.avatar_url)
    em.set_image(url=bot.user.avatar_url)
    em.add_field(name=BOT_PREFIX + "help", value="Shows this message\nalias: " + BOT_PREFIX + "h", inline=False)
    em.add_field(name=BOT_PREFIX + "images", value="Image help", inline=False)
    em.add_field(name=BOT_PREFIX + "ping", value="Sends a ping to the bot and returns an value in `ms`\nalias: " + BOT_PREFIX + "p", inline=False)
    em.add_field(name=BOT_PREFIX + "say", value="Say smth with the bot.`", inline=False)
    em.add_field(name=BOT_PREFIX + "remindme", value="Reminds you of smth.\nalias: " + BOT_PREFIX + "rm", inline=False)
    em.add_field(name="'Hey Atari'", value="Followed by\n`- is [...] ugly` > is smth ugly on a scale from 0-100%.", inline=False)
    em.add_field(name="other stuff", value="Will respond to greetings, such as\n```md\n- Hewwo\n- Hey\n- Hi```\nI will respond if you\n```md\n- call me cute\n- ask me how I am```\n*and there are some things that get triggered randomly*\n\nYou can ask <@!349471395685859348> for help.", inline=False)
 
    await ctx.message.delete()
    await ctx.send(embed=em)

@bot.command(name="images", description="Image help")
async def images(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
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
    await ctx.send(embed=em)

@bot.command(name="ping", description="Sends a ping to the bot and returns an value in `ms`", aliases=['p'])
async def ping(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
    before = time.monotonic()
    message = await ctx.reply("Pong!")
    ping1 = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping1)}ms`")

@bot.command(name="info", description="Sends info from os", aliases=['i'])
async def info(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
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
async def whitelist(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
    em = discord.Embed(
        title=f"Whitelist from " + GUILD,
        description="",
        color=DEFAULT_EMBED_COLOR
    )
    
    em.set_thumbnail(url='https://cdn.discordapp.com/icons/751025913415598120/10aff266134d6388ddbd2b1e19a1f421.webp?size=128')
    em.add_field(name="\u200b", value="<#799037603764240406>", inline=True)
    em.add_field(name="\u200b", value="\u200b", inline=True)
    em.add_field(name="\u200b", value="\u200b", inline=True)

    em.set_footer(text="Requested by " + ctx.message.author.name + "", icon_url=ctx.message.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=em)

@bot.command()
async def add(ctx):
    guildid=str(ctx.message.guild.id)
    authorid=str(ctx.message.author.id)
    if guildid == GUILD_ID and authorid == '349471395685859348':
        with open(".env", "r") as read_obj:
            # Read all lines in the file one by one
            for line in read_obj:
                # For each line, check if line contains the string
                if str(ctx.channel.id) in line:
                    await ctx.send('Channel already added.')
                    return
        f = open(".env", "a")
        f.write(f", {ctx.channel.id}")
        f.close()
        em = discord.Embed(
            title="Channel added.",
            description="Atari must be restarted in order to apply changes.",
            color=DEFAULT_EMBED_COLOR
        )
        
        em.set_footer(text="Requested by " + ctx.message.author.name + "", icon_url=ctx.message.author.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=em)
    else:
        if guildid == GUILD_ID:
            await ctx.send('Only <@!349471395685859348> can use this.')
            return
        else: return

@bot.command(pass_context=True)
async def verifyme(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
    user = ctx.message.author
    role = get(ctx.guild.roles, name="✓ rules")
    mods = get(ctx.guild.roles, name="Management")
    await user.add_roles(role)
    await ctx.message.delete()
    channel = discord.utils.get(bot.get_all_channels(), guild__name=GUILD, name=f'new-joins')
    await channel.send(f"{ctx.author.name} just accepted le rules. Make sure to greet them <@&{mods.id}>!")
    #DM Channel answer:
    await ctx.author.send("You're now verified. Enjoy your stay!")

@bot.command()
async def nsfw(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
    bot.automation = True
    #DM Channel answer:
    await ctx.author.send("NSFW on.")
    

@bot.command()
async def say(ctx, *, arg):
    if str(ctx.channel.id) not in WHITELIST: return
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
async def magicmath(ctx, *, arg):
    if str(ctx.channel.id) not in WHITELIST: return
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
    if str(ctx.channel.id) not in WHITELIST: return
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

    

@bot.command(name="furinsult", description="insults you lol", aliases=['insult'])
async def furinsult(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return
    
    await ctx.send('awww')

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Fuck you {ctx.message.author.name}*")
    ## for my aussie frien lmao
    if '750277467578695740' in member.mention:
        await ctx.send(f"*They’re actually called flip-flops {member.name}*")
    else:
        await ctx.send(f"*Fuck you {member.name}*")

async def sheri_api_nsfw(ctx, api_url):
    if str(ctx.channel.id) not in WHITELIST: return
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
    if str(ctx.channel.id) not in WHITELIST: return
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
    if str(ctx.channel.id) not in WHITELIST: return
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
async def pat(ctx):
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/pat", ctx=ctx)

@bot.command()
async def paws(ctx):
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
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Boops {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} boops {member.mention}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/boop", ctx=ctx)

@bot.command()
async def nboop(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Boops {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} boops {member.mention}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nboop", ctx=ctx)

@bot.command()
async def hug(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Hugs {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} hugs {member.mention}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/hug", ctx=ctx)

@bot.command()
async def nhug(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Hugs {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} hugs {member.mention}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nhug", ctx=ctx)

@bot.command()
async def kiss(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Kisses {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} kisses {member.mention}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/kiss", ctx=ctx)

@bot.command()
async def nkiss(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Kisses {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} kisses {member.mention}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nkiss", ctx=ctx)

@bot.command()
async def lick(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Licks {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} licks {member.mention}*")
    await sheri_api_sfw(api_url="https://www.sheri.bot/api/lick", ctx=ctx)

@bot.command()
async def nlick(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Licks {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} licks {member.mention}*")
    await sheri_api_nsfw(api_url="https://www.sheri.bot/api/nlick", ctx=ctx)

@bot.command()
async def fursuit(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

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
    if str(ctx.channel.id) not in WHITELIST: return

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
    if str(ctx.channel.id) not in WHITELIST: return
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


@bot.command(name="remindme", description="Reminds you of smth.", aliases=['rm'])
async def remindme(ctx, *reminder):
    if str(ctx.channel.id) not in WHITELIST: return
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
    reminder = reminder.replace("my", "your")
    reminder = reminder.replace("me", "you")
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

bot.shut = False
@bot.listen('on_message')
async def message(message):
    # current date and time
    now = datetime.now()
    timestamp = round(datetime.timestamp(now))
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        if str(message.channel.id) not in WHITELIST: return
        if str(message.guild.id) != GUILD_ID: return
        if message.attachments != None and message.content == '':
            print(f"{bcolors.CYAN3}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n [image]{bcolors.ENDC}")
        if message.content != '':
            print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author}{bcolors.ENDC} in {bcolors.CYAN}{message.channel.name}{bcolors.ENDC} on {message.guild.name}:\n {message.content}{bcolors.ENDC}")
    if message.author.bot: return
    if message.author.id == 355330245433360384: return

    """
    preventing Atari from responding in channels
    """
    #Whitelist
    if str(message.channel.id) not in WHITELIST: return

    content = message.content
    rnd = random.randrange(0, 100)
    if message.attachments != None and content == '':
        print(f"{bcolors.CYAN3}{datetime.fromtimestamp(timestamp)} - {message.author} in {message.channel.name} on {message.guild.name}:\n {message.attachments}{bcolors.ENDC}")
    if content != '':
        print(f"{bcolors.CYAN}{datetime.fromtimestamp(timestamp)} - {message.author}{bcolors.ENDC} in {bcolors.CYAN}{message.channel.name}{bcolors.ENDC} on {message.guild.name}:\n {content} // {bcolors.PURPLE}rnd = {rnd}{bcolors.ENDC}")
    

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
        

    if 'CUTE' in content.upper() and message.author.id == 289802289638539274 and rnd > 49:
        await message.channel.send('*Lynix is so cute uwu*')

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
        
    
    if content.upper().startswith("NO U") or content.upper().startswith("NO YOU") and rnd > 69:
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
        

    if content.upper().startswith("I'M") and rnd > 69:
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
    if content.upper().startswith("IM") and rnd > 69:
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

    if 'IS' in content.upper() and 'UGLY' in content.upper():
                await message.reply(f"{rnd}%".format(message))
                return
    if 'IS' in content.upper() and 'CUTE' in content.upper():
        await message.reply(f"{rnd}%".format(message))
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
            if 'IS' in msg.content.upper() and 'UGLY' in msg.content.upper():
                await msg.reply(f"{rnd}%".format(msg))
                return
            if 'IS' in msg.content.upper() and 'CUTE' in msg.content.upper():
                await msg.reply(f"{rnd}%".format(msg))
                return
            if msg.content.upper().startswith("YOU AREN'T CUTEN'T") or 'CUTE' in msg.content.upper() or 'CUTIE' in msg.content.upper() and not "AREN'T" in msg.content.upper() and not "CUTEN'T" in msg.content.upper() and not "NOT" in msg.content.upper() and not "IS" in msg.content.upper() or 'CUTE' in msg.content.upper() and "AREN'T" in msg.content.upper() and 'NOT' in msg.content.upper() and not "IS" in msg.content.upper() or "CUTEN'T" in msg.content.upper() and 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper() and not "IS" in msg.content.upper():
                await message.channel.send("You're cute aswell, {0.author.name}.".format(msg))
                return


## run that stuff
bot.run(TOKEN)