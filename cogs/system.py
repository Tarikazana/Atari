import asyncio
import os
import discord
from discord.ext import commands
from discord.utils import get
from tinydb import TinyDB, Query
from tinydb.operations import delete


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if os.path.isfile(f'atari/data/guilds/{member.guild.id}/automod.json'): # automod
            channel = member.guild.system_channel
            guild = member.guild
            if channel is not None:
                await channel.send('Welcome {0.mention}'.format(member))
            if not os.path.isfile(f'atari/data/guilds/{member.guild.id}/raidmembers.json'):
                db = TinyDB(f'atari/data/guilds/{member.guild.id}/raidmembers.json')
                db.insert({'m_id': str(member.id)})
                if not os.path.isfile(f'atari/data/guilds/{member.guild.id}/raidprotect.json'):
                    db = TinyDB(f'atari/data/guilds/{member.guild.id}/raidprotect.json')
                    db.insert({'joins': '0'})
            else:
                db = TinyDB(f'atari/data/guilds/{member.guild.id}/raidprotect.json')
                out = db.all()
                out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"',"")
                out = list(out.split(","))
                print(str(out[1]))
                update = str(int(out[1])+1)
                db.update({'joins': str(update)})
                out = db.all()
                out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"',"")
                out = list(out.split(","))
                print("int:"+str(out[1]))
                if int(out[1]) == 1:
                    print("T-30s")
                    await asyncio.sleep(30)
                    db = TinyDB(f'atari/data/guilds/{member.guild.id}/raidprotect.json')
                    db.update({'joins': '0'})
                    os.remove(f"atari/data/guilds/{member.guild.id}/raidmembers.json")
                    print("List clear.")
                if int(out[1]) > 2:
                    db = TinyDB(f'atari/data/guilds/{member.guild.id}/raidmembers.json')
                    out = db.all()
                    out = str(out).replace("{","").replace("}","").replace(":",",").replace("'",'"').replace("]","").replace("[","").replace('"',"")
                    out = list(out.split(","))

                    i=1
                    for x in out:
                        try:
                            await guild.kick(discord.Object(id=int(out[i])))
                            i=i+2
                        except:
                            print("members kicked.")
                            return
                

                
                





    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if os.path.isfile(f'atari/data/guilds/{member.guild.id}/automod.json'): # automod
            channel = member.guild.system_channel
            if channel is not None:
                await channel.send('Baii "{0.name}"'.format(member))
    
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name} ~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

def setup(bot):
  bot.add_cog(Greetings(bot))

