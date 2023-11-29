import disnake
from disnake.ext import commands
import timems
from typing import Optional, Self
import configparser
config = configparser.ConfigParser()
config.read('confiig.ini')

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="Ban command ", default_member_permissions=disnake.Permissions(ban_members=True))
    async def ban(self, inter, member: disnake.Member = commands.Param(name="member"),reason: str = commands.Param(name="reason")):
        log = inter.guild.get_channel(int(config.get('channel', 'channel_log')))
        err: Optional[str] = {
            member.bot: "You can't ban bots !",
            member.top_role >= inter.author.top_role or member.top_role == inter.author.top_role: (
                f"Your role is lower or equal to {member.mention}"
            ),
            member.id == inter.author.id: "You can't ban yourself!",
            True: None,
        }[True]
        if err is None:
            await member.ban(reason=reason)
            embed = disnake.Embed(
                title="Ban",
                color=0x3b3b3b,
            ).set_thumbnail(
                member.avatar,
            ).add_field(
                name="Member:",
                value=f"{member.mention} ({member.id})",
                inline=False,
            ).add_field(
                name="Moderator",
                value=f"{inter.author.mention} ({inter.author.id})",
                inline=False,
            ).add_field(
                name="Reason",
                value=reason,
                inline=False,
            )
            await inter.send(embed=embed, ephemeral=True)
            await log.send(embed=embed)
            return
        await inter.send(embed=disnake.Embed(
            title="Error",
            description=err,
            color=0x3b3b3b,
        ).set_thumbnail(member.avatar), ephemeral=True)
    
    @commands.slash_command(description="Kick command", default_member_permissions=disnake.Permissions(kick_members=True))
    async def kick(self, inter, member: disnake.Member = commands.Param(name="member"), reason: str = commands.Param(name="reason")):
        log = inter.guild.get_channel(int(config.get('channel', 'channel_log')))
        err: Optional[str] = {
            member.bot: "You can't kick bots !",
            member.top_role >= inter.author.top_role or member.top_role == inter.author.top_role: (
                f"Your role is lower or equal to {member.mention}"
            ),
            member.id == inter.author.id: "You can't kick yourself!",
            True: None,
        }[True]
        if err is not None:
            await inter.send(embed=disnake.Embed(
                title="Error",
                description=err,
                color=0x3b3b3b,
            ).set_thumbnail(member.avatar), ephemeral=True)
            return
        await member.kick(reason=reason)
        embed = disnake.Embed(
            title="Kick",
            color=0x3b3b3b,
        ).set_thumbnail(
            member.avatar,
        ).add_field(
            name="Member:",
            value=f"{member.mention} ({member.id})",
            inline=False,
        ).add_field(
            name="Moderator",
            value=f"{inter.author.mention} ({inter.author.id})",
            inline=False,
        ).add_field(
            name="Reason",
            value=reason,
            inline=False,
        )
        await inter.send(embed=embed, ephemeral=True)
        await log.send(embed=embed)
    
    @commands.slash_command(description="Mute command", default_member_permissions=disnake.Permissions(moderate_members=True))
    async def mute(self, inter, member: disnake.Member = commands.Param(name="member"),duration: str = commands.Param(name="time"), reason: str = commands.Param(name="reason")):
        log = inter.guild.get_channel(int(config.get('channel', 'channel_log')))
        err: Optional[str] = {
            member.bot: "You can't mute bots !",
            member.top_role >= inter.author.top_role or member.top_role == inter.author.top_role: (
                f"Your role is lower or equal to {member.mention}"
            ),
            member.id == inter.author.id: "You can't mute yourself!",
            True: None,
        }[True]
        if err is not None:
            await inter.send(embed=disnake.Embed(
                title="Error",
                description=err,
                color=0x3b3b3b,
            ).set_thumbnail(member.avatar), ephemeral=True)
            return
        await member.timeout(duration=timems.ms(duration), reason=reason)   
        embed = disnake.Embed(
             title="Mute",
             color=0x3b3b3b,
        ).set_thumbnail(
            member.avatar,
        ).add_field(
            name="Member:",
            value=f"{member.mention} ({member.id})",
            inline=False,
        ).add_field(
            name="Moderator:",
            value=f"{inter.author.mention} ({inter.author.id})",
            inline=False,
        ).add_field(
            name="Time:",
            value=duration,
            inline=False,
        ).add_field(
            name="Reason",
            value=reason,
            inline=False,
        )
        await inter.send(embed=embed, ephemeral=True)
        await log.send(embed=embed)
    
    @commands.slash_command(description="Unmute command", default_member_permissions=disnake.Permissions(moderate_members=True))
    async def unmute(self, inter, member: disnake.Member = commands.Param(name="member"), reason: str = commands.Param(name="reason")):
        log = inter.guild.get_channel(int(config.get('channel', 'channel_log')))
        err: Optional[str] = {
            member.bot: "You can't unmute bots !",
            member.top_role >= inter.author.top_role or member.top_role == inter.author.top_role: (
                f"Your role is lower or equal to {member.mention}"
            ),
            member.id == inter.author.id: "You can't unmute yourself!",
            True: None,
        }[True]
        if err is not None:
            await inter.send(embed=disnake.Embed(
                title="Error",
                description=err,
                color=0x3b3b3b,
            ).set_thumbnail(member.avatar), ephemeral=True)
            return
        await member.timeout(duration=0, reason=reason)   
        embed = disnake.Embed(
            title="Unmute",
            color=0x3b3b3b,
        ).set_thumbnail(
            member.avatar,
        ).add_field(
            name="Member:",
            value=f"{member.mention} ({member.id})",
            inline=False,
        ).add_field(
            name="Moderator:",
            value=f"{inter.author.mention} ({inter.author.id})",
            inline=False,
        ).add_field(
            name="Reason:",
            value=reason,
            inline=False,
        )
        await inter.send(embed=embed, ephemeral=True)
        await log.send(embed=embed)

def setup(client):
    client.add_cog(ModerationCog(client))