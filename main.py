from disnake.ext import commands
from disnake.enums import ButtonStyle
from disnake import TextInputStyle
from disnake import *
from disnake.utils import get
import disnake
import asyncio
import sqlite3
import configparser
import os
import datetime
import random
from random import randint
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="%", help_command=None, intents=intents)
bd = sqlite3.connect("bot.db")
c = bd.cursor()

config = configparser.ConfigParser()
config.read('config.ini')


for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		bot.load_extension("cogs." + f[:-3])


@bot.event
async def on_message(message):
  await bot.process_commands(message)
  member = message.author
  channel1 = message.guild.get_channel(int(config.get('channel', 'channel_lock1')))
  channel2 = message.guild.get_channel(int(config.get('channel', 'channel_lock2')))
  levl1 = message.guild.get_role(int(config.get('roles', 'level1')))
  levl2 = message.guild.get_role(int(config.get('roles', 'level2')))
  levl3 = message.guild.get_role(int(config.get('roles', 'level3')))
  if not member.bot:
    if c.execute("SELECT id FROM members WHERE id = ?",
                 (member.id, )).fetchone() is None:
      c.execute("INSERT INTO members VALUES (?, ?, ?, ?)", (
        member.id,
        0,
        0,
        0,
      ))
      bd.commit()
    else:
      if message.channel == channel1 or message.channel == channel2:
          pass
      else:
          exp = random.randint(1, 6)
          c.execute("UPDATE members SET exp = exp + ? WHERE id = ?", (exp, member.id))
          c.execute("UPDATE members SET msg = msg + ? WHERE id = ?",(1, member.id))                  
          bd.commit()
          if c.execute("SELECT exp FROM members WHERE id = ?",(member.id, )).fetchone()[0] >= 1000:
            c.execute("UPDATE members SET exp = 0 WHERE id = ?",(member.id, ))
            c.execute("UPDATE members SET level = level + 1 WHERE id = ?",(member.id, ))
            bd.commit()
            if c.execute("SELECT level FROM members WHERE id = ?", (member.id, )).fetchone()[0] == 5:
              await member.add_roles(levl1)
            if c.execute("SELECT level FROM members WHERE id = ?", (member.id, )).fetchone()[0] == 10:
              await member.add_roles(levl2)
            if c.execute("SELECT level FROM members WHERE id = ?", (member.id, )).fetchone()[0] == 25:
              await member.add_roles(levl3)
 

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        if after.channel.id == int(config.get('channel', 'channel_voice')):
            category = bot.get_channel(int(config.get('channel', 'category_voice')))
            new_channel = await member.guild.create_voice_channel(name=member.display_name, category=category)
            await member.move_to(new_channel)
            start_time = datetime.datetime.now()
            while member.voice and member.voice.channel == new_channel:
                await asyncio.sleep(1)
            await new_channel.delete()
    if before.channel and not after.channel:
        if before.channel.name == member.display_name:
            await before.channel.delete() 

                 
@bot.slash_command(description="A person's profile or your profile!")
async def user(ctx, user: disnake.Member = None):
  member = ctx.author if user == None else user
  if c.execute("SELECT id FROM members WHERE id = ?", (member.id, )).fetchone() is None:
    c.execute(
      "INSERT INTO members VALUES (?,?,?,?)",
      [int(member.id), int(0), int(0), int(0)])
    bd.commit()
    await ctx.send("Отправьте сообщение еще раз")
  else:
      tmp = c.execute(f"SELECT exp, level, msg FROM members WHERE id = ?", (member.id, )).fetchone()
      exp, level, msg = tmp
      status = str(member.status)
      status = "Offline" if status == "offline" else "Idle" if status == "idle" else "Online" if status == "online" else "Dnd" if status == "dnd" else "Invisible" if status == "invisible" else None
      embed = disnake.Embed(title=f"{member.name} profile", description=member.mention, color=0x38449B)
      embed.add_field(name="Number of messages ", value=msg, inline=False)
      embed.add_field(name="Status", value=status, inline=False)
      embed.add_field(name="Registration in discord", value=member.created_at.strftime("%Y.%m.%d"), inline=True)
      embed.add_field(name="Logged into the server ", value=member.joined_at.strftime("%Y.%m.%d"), inline=True)
      embed.add_field(name="Experience", value=exp, inline=False)
      embed.add_field(name="Level", value=level, inline=True)
      embed.set_thumbnail(member.avatar)
      await ctx.send(embed=embed) 
 
          
                                                                                  
@bot.slash_command(description="Clearing messages")
@commands.has_permissions(moderate_members=True)
async def clear(inter, quantity: int = commands.Param(name="quantity", description='Number of messages you want to delete ')):
  if quantity <= 1 or quantity > 100:
    await inter.send("The number of cleared messages should not be less than 1 or more than 100.", ephemeral=True)
  else:
    await inter.channel.purge(limit=quantity)
    await inter.send("Now everything is clean!", ephemeral=True)          

@clear.error
async def clear_error(inter, error):
	    if isinstance(error, commands.CommandError):
	       await inter.send("You do not have rights to clear messages.", ephemeral = True)       
                  
@bot.event
async def on_ready():
  print("The bot is working, please give it a star in the repository: https://github.com/InserTym/your_bot⭐")
  c.execute("""CREATE TABLE IF NOT
	      EXISTS members (
	      id int,
	      exp int,
	      level int,
	      msg int)""")
  bd.commit()
  await bot.change_presence(
    status=disnake.Status.idle,
    activity=disnake.Game(name=f"Give a star: https://github.com/InserTym/your_bot⭐"))
  channel = bot.get_channel(int(config.get('channel', 'channel_menu')))
  embed=disnake.Embed(title="Menu", description="""Menu for reading important information.""", color=0x3b3b3b)
  await channel.purge(limit=5)
  await channel.send(embed=embed, view=select())

               
                       
class Menu(disnake.ui.Select):
    def __init__(self):
        options = [           
            disnake.SelectOption(
                label="Rules", description=".", emoji="📚"),                        
            disnake.SelectOption(
                label="Roles", description=".", emoji="🎩"),
            disnake.SelectOption(
                label="Navigation", description=".", emoji="🧭") 
             
                ]                                          
        super().__init__(
            placeholder="Menu",
            min_values=1,
            max_values=1,
            options=options,
        )
        
    async def callback(self, ctx: disnake.MessageInteraction):        
       teesg = ctx.values[0]
       if teesg in "Rules":
           embed=disnake.Embed(title="Rules", description=""".""", color=0x3b3b3b)
           await ctx.send(embed=embed, ephemeral = True)    
       elif teesg in "Roles":
           embed=disnake.Embed(title="Roles", description=""".""", color=0x3b3b3b)
           await ctx.send(embed=embed, ephemeral = True) 
       else:
           embed=disnake.Embed(title="Navigation", description=""".""", color=0x3b3b3b)
           await ctx.send(embed=embed, ephemeral = True)             
                                                                             
class select(disnake.ui.View): 
    def __init__(self):
        super().__init__(
            timeout=None
        )
        self.add_item(Menu())  


                                        
bot.run(config.get('bot', 'token'))  
