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
import requests
import json
import discord, datetime, time
from discord import message
from discord import TextChannel
from discord import channel
from discord.activity import Game
from discord.enums import Status
from discord.ext import commands
from discord.abc import GuildChannel
from discord.ext.commands.converter import TextChannelConverter
from discord.ext.commands.core import has_permissions
from discord.guild import Guild
from discord.ext.commands import Bot
from dotenv import load_dotenv

##############################################################
##                  Loading dotenv Stuff                    ##
##############################################################

print('loading dotenv content...')

load_dotenv()   #loads stuff from .env
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BOT_VERSION = os.getenv('BOT_VERSION')
BOT_PREFIX = os.getenv('PREFIX')
WHITELIST = os.getenv('SERVER_WHITELIST')

DEFAULT_EMBED_COLOR = discord.Colour(0xfc03ad)
print('done.')

##############################################################
##                       Startup                            ##
##############################################################

print('starting Atari...')

##############################################################
##                  Specify bot prefix in .env              ##
##############################################################

bot = commands.Bot(command_prefix=BOT_PREFIX)

intents = discord.Intents(messages=True, guilds=True)
intents.messages = True


@bot.event
async def on_ready():
    print(bot.user, ' has connected to Discord!\n')

    print ("------------------------------------")
    print (f"Bot Name: {bot.user.name}")
    print (f"Bot ID: {bot.user.id}")
    print (f"Discord Version: {discord.__version__}")
    print (f"Bot Version: {BOT_VERSION}")
    print ("------------------------------------")

    print('setting activity...')

    ## useful docs for setting activities
    ## https://medium.com/python-in-plain-english/how-to-change-discord-bot-status-with-discord-py-39219c8fceea
    ## https://stackoverflow.com/questions/59126137/how-to-change-discord-py-bot-activity
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Tawi"))
    print('activity set.')

    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})'
    )
    print(f'Guild Members:{guild.member_count}')
    print ("------------------------------------")
    print ("\nMessage Log:")


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
    em.add_field(name=BOT_PREFIX + "ping", value="Sends a ping to the bot and returns an value in `ms`\nalias: " + BOT_PREFIX + "p", inline=False)
    em.add_field(name=BOT_PREFIX + "shut", value="Tell Atari to shut up for 10 minutes. Status gets displayed.", inline=False)
    em.add_field(name=BOT_PREFIX + "say", value="Say smth with the bot.\n`No mentions please.`", inline=False)
    em.add_field(name=BOT_PREFIX + "remindme", value="Reminds you of smth.\nalias: " + BOT_PREFIX + "rm", inline=False)
    em.add_field(name="'Hey Atari'", value="Followed by\n`- is [...] ugly` > is smth ugly on a scale from 0-100%.", inline=False)
    em.add_field(name="other stuff", value="Will respond to greetings, such as\n```md\n- Hewwo\n- Hey\n- Hi```\nI will respond if you\n```md\n- call me cute\n- ask me how I am```\n*and there are some things that get triggered randomly*\n\nYou can ask <@!349471395685859348> for help.", inline=False)
 
    await ctx.message.delete()
    await ctx.send(embed=em)

    em = discord.Embed(
        title="- Images -",
        description="**Commands**",
        color=DEFAULT_EMBED_COLOR
    )
    em.add_field(name=BOT_PREFIX + "fursuit", value="Returns a fursuit image.", inline=False)
    em.add_field(name=BOT_PREFIX + "fox", value="Returns a fox image.", inline=False)
    em.add_field(name=BOT_PREFIX + "husky", value="Returns a husky image.", inline=False)
    em.add_field(name=BOT_PREFIX + "lion", value="Returns a lion image.", inline=False)
    em.add_field(name=BOT_PREFIX + "mur", value="Returns a mur image.", inline=False)
    em.add_field(name=BOT_PREFIX + "tiger", value="Returns a tiger image.", inline=False)
    em.add_field(name=BOT_PREFIX + "wolf", value="Returns a wolf image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furboop", value="Returns a boop image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furcuddle", value="Returns a cuddle image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furflop", value="Returns a flop image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furhowl", value="Returns a howl image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furhold", value="Returns a hold image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furhug", value="Returns a hug image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furkiss", value="Returns a kiss image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furlick", value="Returns a lick image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furpropose", value="Returns a propose image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furbulge", value="Returns a bulge image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furyiffgay", value="Returns a gay yiff image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furyiffstraight", value="Returns a straight yiff image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furyifflesbian", value="Returns a lesbian yiff image.", inline=False)
    em.add_field(name=BOT_PREFIX + "furyiffgynomorph", value="Returns a gynomorph yiff image.", inline=False)
    em.add_field(name=BOT_PREFIX + "yiff", value="Returns a yiff image from Sheri's api.", inline=False)

    em.set_footer(text="Requested by " + ctx.message.author.name + "", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=em)

@bot.command(name="ping", description="Sends a ping to the bot and returns an value in `ms`", aliases=['p'])
async def ping(ctx):
    if str(ctx.channel.id) not in WHITELIST: return
    before = time.monotonic()
    message = await ctx.reply("Pong!")
    ping1 = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping1)}ms`")

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

@bot.command()
async def say(ctx, *args):
    if str(ctx.channel.id) not in WHITELIST: return
    resp = str(args)
    resp = resp.replace("'", '')
    resp = resp.replace(",", '')
    resp = resp.replace("(", '')
    resp = resp.replace(")", '')
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
async def yiff(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('http://www.sheri.bot/api/yiff/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def wolf(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('http://www.sheri.bot/api/wolves/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def tiger(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('http://www.sheri.bot/api/tiger/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def mur(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('http://www.sheri.bot/api/mur/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def lion(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('http://www.sheri.bot/api/lion/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def husky(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('http://www.sheri.bot/api/husky/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def fox(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://www.sheri.bot/api/fox/')
    print (r.json())
    em.set_image(url=str(r.json()["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furboop(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Boop')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Boops {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} boops {member.mention}*")
    await ctx.send(embed=em)

@bot.command()
async def furcuddle(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Cuddle')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furflop(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Flop')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def fursuit(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Fursuit')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furhold(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/hold')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furhowl(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Howl')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furhug(ctx, member: discord.User = 'null'):
    if str(ctx.channel.id) not in WHITELIST: return
    
    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Hug')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))

    await ctx.send('*awww*')

    ## thx for this flonky :3

    if member == ctx.message.author or member == 'null':
        await ctx.send(f"*Hugs {ctx.message.author.name}*")
    else:
        await ctx.send(f"*{ctx.message.author.name} hugs {member.mention}*")
    await ctx.send(embed=em)
    

@bot.command()
async def furkiss(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Kiss')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furlick(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Lick')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furpropose(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Propose')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furbulge(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Bulge')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furyiffgay(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Yiff/Gay')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furyiffstraight(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Yiff/Straight')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furyifflesbian(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Yiff/Lesbian')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)

@bot.command()
async def furyiffgynomorph(ctx):
    if str(ctx.channel.id) not in WHITELIST: return

    em = discord.Embed(
        title=None,
        description=None,
        color=DEFAULT_EMBED_COLOR
    )
    r = requests.get('https://yiff.rest/V2/Furry/Yiff/Gynomorph')
    print (r.json())
    em.set_image(url=str(r.json()["images"][0]["url"]))
    await ctx.send(embed=em)


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
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        print(f'{message.author}: {message.content}')
        return
    if message.author.bot: return

    """
    preventing Atari from responding in channels
    """
    #Whitelist
    if str(message.channel.id) not in WHITELIST: return

    content = message.content
    rnd = random.randrange(0, 100)
    print(f'{message.author}: {content} // rnd = {rnd}')
    

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
    elif 'SHUT' in content.upper() and rnd > 49:
        await message.channel.send("Shut, {0.author.name} *lmao*.".format(message))
        return            
    
    if bot.shut==True: return


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
        
    
    if content.upper().startswith("NO U"):
        await message.channel.send('no u')
        

    if content.upper().startswith("AAAAA"):
        await message.channel.send('*aaaaaaaaaa*')

    if content.upper().startswith("BRRRR"):
        await message.channel.send('*brrrrrrrrr*')

    ## well... yeeaaaaa let's not talk about this
    if 'BLYAT' in content.upper():
        await message.channel.send('*nyet suka blyat*')
        await message.channel.send('*Битч*')
        

    if content.upper().startswith("EEEEE"):
        await message.channel.send('*eeeeeeeeee*')
        

    if content.upper().startswith("I'M") and rnd > 90:
        content = content.capitalize().replace("I'm ", '')
        content = content.replace(".", '')
        response = f"Hi {content}, I'm Atari"
        await message.channel.send(response)
        
    ## for my german friends that forget how to type that ' thingy
    if content.upper().startswith("IM") and rnd > 90:
        content = content.capitalize().replace("Im ", '')
        content = content.replace(".", '')
        response = f"Hi {content}, I'm Atari"
        await message.channel.send(response)
        
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

    if 'ATARI' in content.upper() and not BOT_PREFIX+'SAY' in content.upper():
        if 'ATARI' in content.upper() and 'CUTE' in content.upper():
            await message.channel.send("aaaaaaaaaa")
            await message.channel.send("You're cuteee")
            return
        

        try:
            msg = await bot.wait_for('message', check=None, timeout=60.0)
        except asyncio.TimeoutError:
            await message.channel.send('<3')
        else:
            if msg.content.upper().startswith("YOU AREN'T CUTEN'T") or 'CUTE' in msg.content.upper() and not "AREN'T" in msg.content.upper() and not "CUTEN'T" in msg.content.upper() or 'CUTE' in msg.content.upper() and "AREN'T" in msg.content.upper() and 'NOT' in msg.content.upper() or "CUTEN'T" in msg.content.upper() and 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper():
                await message.channel.send("You're cute aswell, {0.author.name}.".format(msg))
            if "AREN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "CUTEN'T" in msg.content.upper() and rnd > 49 or "CUTEN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper() and rnd > 49:
                await message.channel.send("qwq".format(msg))
            if "AREN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "CUTEN'T" in msg.content.upper() and rnd < 50 or "CUTEN'T" in msg.content.upper() and not 'NOT' in msg.content.upper() and not "AREN'T" in msg.content.upper() and rnd < 50:
                await message.channel.send("But...".format(msg))
                await message.channel.send("But...".format(msg))
                await message.channel.send("But you are.".format(msg))
            if 'HRU' in msg.content.upper() or 'HOW ARE YOU' in msg.content.upper():
                await message.channel.send("I'm finee, {0.author.name}.".format(msg))
            if 'UGLY' in msg.content.upper():
                await msg.reply(f"{rnd}%".format(msg))


## run that stuff
bot.run(TOKEN)