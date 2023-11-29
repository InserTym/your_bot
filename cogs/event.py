import disnake
from disnake.ext import commands
from typing import Self
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

class EventsCog(commands.Cog):
    def __init__(self: Self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
     if before.content != after.content:
           log = before.guild.get_channel(int(config.get('channel', 'channel_log')))
           channel = before.channel
           ebed = disnake.Embed(title=f"{after.author} edit message",  color=0x3b3b3b)
           ebed.add_field(name="Before:", value=before.content, inline=False)
           ebed.add_field(name="After:", value=after.content, inline=False)
           ebed.add_field(name="Channel:", value=channel.mention, inline=False)
           ebed.set_thumbnail(before.author.avatar)
           await log.send(embed=ebed)
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
     member = message.author
     if member.bot == False:
       log = message.guild.get_channel(int(config.get('channel', 'channel_log')))
       channel = message.channel
       ebed = disnake.Embed(title=f"{message.author} delete message", color=0x3b3b3b)
       ebed.add_field(name="Message:", value=message.content, inline=False)
       ebed.add_field(name="Channel:", value=channel.mention, inline=False)
       ebed.set_thumbnail(message.author.avatar)
       await log.send(embed=ebed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
     channel = member.guild.get_channel(int(config.get('channel', 'channel_log')))
     await channel.send(f"Hi  {member.mention}👋")
                     
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
           pass
        elif message.content.lower() == 'nometa':
           await message.channel.send('Skull bro, https://nometa.xyz/')
        elif message.content.lower() == 'role':
           await message.channel.send('<id:customize>')                                             
        await self.bot.process_commands(message)



def setup(client):
    client.add_cog(EventsCog(client))
