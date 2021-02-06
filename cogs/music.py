import discord
from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed

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
    print('join command worked')
    member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
    if member is not None and member.voice is not None:
      vc = member.voice.channel
      player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
      if not player.is_connected:
        player.store('channel', ctx.channel.id)
        await self.connect_to(ctx.guild.id, str(vc.id))
        await ctx.channel.send(f"`// joined {ctx.author.name}. //`")

  commands.position = []
  @commands.command(name='play')
  async def play(self, ctx, *, query):
    try:
      player = self.bot.music.player_manager.get(ctx.guild.id)
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

      await ctx.channel.send(embed=embed)

      def check(m):
        return m.author.id == ctx.author.id
      
      response = await self.bot.wait_for('message', check=check)
      track = tracks[int(response.content)-1]

      player.add(requester=ctx.author.id, track=track)
      commands.position.append('x')
      if not player.is_playing:
        await ctx.channel.send(f"`Added: {track.get('info').get('title')} // position: {len(player.queue)}`")
        await ctx.channel.send(f"`// Now playing: {track.get('info').get('title')} //`")
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
        player.queue.clear()
        await ctx.channel.send(f"`// Queue clear. //`")

    except Exception as error:
      print(error)

  @commands.command(name="current",description="Shows the current playing song.",usage="current",aliases=['np','nowplaying'])
  async def current(self,ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    if len(player.queue) == 1:
      embed=Embed(title=player.current.title,description=f"Now playing\n➤ {len(player.queue)} Song queued.",url=f"https://youtube.com/watch?v={player.current.identifier}")
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
        await player.stop()
        await ctx.channel.send(f"`// Skipped. //`")
        if len(player.queue) == 0:
          await ctx.channel.send(f"`// No Tracks in queue. //`")
        else:
          await player.play()


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