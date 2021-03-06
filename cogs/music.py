import discord
import re
from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed

url_rx = re.compile(r'https?://(?:www\.)?.+')

DEFAULT_EMBED_COLOR = discord.Colour(0xfc03ad)

class MusicCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.music = lavalink.Client(self.bot.user.id)
    self.bot.music.add_node('IP', Port, 'Passwd', 'na', 'music-node')
    self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
    self.bot.music.add_event_hook(self.track_hook)

  @commands.command(name='join')
  async def join(self, ctx):
    member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
    print(member)
    print(member.id)
    print(ctx.author.id)
    print(member.voice)
    if member is not None and member.voice is not None:
      vc = member.voice.channel
      player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
      if not player.is_connected:
        player.store('channel', ctx.channel.id)
        await self.connect_to(ctx.guild.id, str(vc.id))
        await ctx.channel.send(f"`// joined {ctx.author.name}. //`")

  commands.position = []
  @commands.command(name='play')
  async def play(self, ctx, *, query = None):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    if not player.is_connected:
        try:
          vc = ctx.author.voice.channel
          player.store('channel', ctx.channel.id)
          await self.connect_to(ctx.guild.id, str(vc.id))
          await ctx.channel.send(f"`// joined {ctx.author.name}. //`")
        except:
          await ctx.channel.send(f"`// Connect Atari with _join. //`")
    if query == None:
      if len(player.queue) >= 1:
        await player.play()
        return
      else:
        await ctx.channel.send(f"`// Required Song missing. //`")
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)
      if url_rx.match(query):
        isurl = True
      else:
        isurl = False
        query = f'ytsearch:{query}'
      results = await player.node.get_tracks(query)
      tracks = results['tracks'][0:10]
      i = 0
      query_result = ''
      for track in tracks:
        i = i + 1
        query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
      embed = Embed()
      embed.description = query_result
      
      if isurl == False:
        await ctx.channel.send(embed=embed)

        def check(m):
          return m.author.id == ctx.author.id
        
        response = await self.bot.wait_for('message', check=check)
        try:
          response_int = type(int(response.content))
        except:
          response_int = type(response.content)
        
        print(response_int)
        if response_int != int:
          await ctx.channel.send(f"`// That ain't lookin like a numba Chief. //`")
          while response_int != int:
            response = await self.bot.wait_for('message', check=check)
            try:
              response_int = type(int(response.content))
            except:
              response_int = type(response.content)
              await ctx.channel.send(f"`// Still no numba Chief. //`")
            print(response_int)
          await ctx.channel.send(f"`// There ya go. //`")
          track = tracks[int(response.content)-1]
        else:
          track = tracks[int(response.content)-1]
      else:
        track = tracks[0]

      player.add(requester=ctx.author.id, track=track)
      commands.position.append('x')
      if not player.is_playing:
        await ctx.channel.send(f"`Added: {track.get('info').get('title')} // position: {len(player.queue)}`")
        await ctx.channel.send(f"`// Now playing: {track.get('info').get('title')} //`")
        await player.stop()
        await player.play()
        return
      await ctx.channel.send(f"`Added: {track.get('info').get('title')} // position: {len(player.queue)+1}`")

    except Exception as error:
      print(error)

  @commands.command(name='stop')
  async def stop(self, ctx):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      if player.is_playing:
        await player.stop()

    except Exception as error:
      print(error)

  @commands.command(name='cq')
  async def cq(self, ctx):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      player.queue.clear()
      await ctx.channel.send(f"`// Queue clear. //`")

    except Exception as error:
      print(error)

  @commands.command(name='pause')
  async def pause(self, ctx):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      if player.paused == False:
        await player.set_pause(True)
        await ctx.channel.send(f"`// Paused. //`")
      else:
        await player.set_pause(False)
        await ctx.channel.send(f"`// Unpaused. //`")

    except Exception as error:
      print(error)

  @commands.command(name='resume')
  async def resume(self, ctx):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      if player.paused == True:
        await player.set_pause(False)
        await ctx.channel.send(f"`// Unpaused. //`")
      else:
        await ctx.channel.send(f"`// blep? //`")

    except Exception as error:
      print(error)

  @commands.command(name='vol')
  async def vol(self, ctx, arg):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      newvol = int(arg)
      await player.set_volume(newvol)
        
    except Exception as error:
      print(error)

  @commands.command(name="current",description="Shows the current playing song.",usage="current",aliases=['np','nowplaying'])
  async def current(self,ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    if len(player.queue) == 1:
      if 'www.twitch.tv/' in player.current.identifier:
        embed=Embed(title=player.current.title,description=f"Now playing\n➤ {len(player.queue)} Song queued.\nrepeat: {player.repeat}\n",url=f"{player.current.identifier}")
      else:
        embed=Embed(title=player.current.title,description=f"Now playing\n➤ {len(player.queue)} Song queued.",url=f"https://youtube.com/watch?v={player.current.identifier}")
    else:
      if 'www.twitch.tv/' in player.current.identifier:
        embed=Embed(title=player.current.title,description=f"Now playing\n➤ {len(player.queue)} Songs queued.",url=f"{player.current.identifier}")
      else:
        embed=Embed(title=player.current.title,description=f"Now playing\n➤ {len(player.queue)} Songs queued.",url=f"https://youtube.com/watch?v={player.current.identifier}")
    await ctx.send(embed=embed)

  @commands.command(name="queue",description="Shows queue.",usage="current",aliases=['q'])
  async def queue(self,ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    if len(player.queue) == 0:
      embed=Embed(title=None,description=f"// No Songs queued. //")
    else:
      embed = discord.Embed(
        title="- Queue -",
        description=None
      )
      if len(player.queue) >= 3:
        embed.add_field(name="Next 3 songs:", value=f"{player.queue[0].title}\n{player.queue[1].title}\n{player.queue[2].title}", inline=False)
      if len(player.queue) == 2:
        embed.add_field(name="Next 2 songs:", value=f"{player.queue[0].title}\n{player.queue[1].title}", inline=False)
      if len(player.queue) == 1:
        embed.add_field(name="Next song:", value=f"{player.queue[0].title}", inline=False)
      
      
    await ctx.send(embed=embed)

  @commands.command(name='dc')
  async def dc(self, ctx):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      if player.is_playing:
        await player.stop()
        player.queue.clear()
        await ctx.channel.send(f"`// Queue clear. //`")
      await ctx.guild.change_voice_state(channel=None)
      await ctx.channel.send(f"`// Disconnected. //`")

    except Exception as error:
      print(error)

  @commands.command(name='skip')
  async def skip(self, ctx):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)

      if player.is_playing:
        if len(player.queue) == 0:
          await ctx.channel.send(f"`// No Tracks in queue. //`")
          await ctx.channel.send(f"`// Do _stop to stop the song. //`")
        else:
          await player.skip()
          await ctx.channel.send(f"`// Skipped. //`")

    except Exception as error:
      print(error)

  async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await self.connect_to(guild_id, None)
      
  async def connect_to(self, guild_id: int, channel_id: str):
    ws = self.bot._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)

def setup(bot):
  bot.add_cog(MusicCog(bot))