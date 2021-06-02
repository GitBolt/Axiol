import discord
import asyncio
from discord.ext import commands
import utils.variables as var
import utils.database as db
from utils.functions import getprefix

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Moderation") == True:
            return ctx.guild.id


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.User=None, *, reason="No reason given :("):
        if member == ctx.author:
            await ctx.send("You can't ban yourself :eyes:")
        await ctx.guild.ban(member, reason=reason)

        await member.send(embed=discord.Embed(
                        title=f"You have been banned from {ctx.guild.name}",
                        description="Sorry I'm just a bot and I follow orders :(", 
                        color=var.C_RED).add_field(name="Reason", value=reason
                        ).add_field(name="Banned by", value=ctx.author)
                        )
        await ctx.send(f"`{member}` got banned :O")



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member:discord.User=None):
        if member == ctx.author:
            await ctx.send("You are not even banned why you trying to unban yourself :joy:")
        await ctx.guild.unban(member)

        await ctx.send(f'`{member}` is now unbanned!')
        await member.send(embed=discord.Embed(
                        title=f"You have been unbanned from {ctx.guild.name}!",
                        description="Yay I would be happy to see you back!", 
                        color=var.C_GREEN
                        ).add_field(name="Unbanned by", value=ctx.author)
                        )
    


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member=None):
        if not discord.utils.get(ctx.guild.roles, name='Muted'):
            mutedrole = await ctx.guild.create_role(name="Muted", colour=discord.Colour(0xa8a8a8))
            for i in ctx.guild.text_channels:
                await i.set_permissions(mutedrole, send_messages=False)
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(mutedrole)
        await ctx.send(f"`{member}` have been muted!")



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member=None):
        if not discord.utils.get(ctx.guild.roles, name='Muted'): 
            await ctx.send("There is no muted role yet hence I cannot unmute, Muting someone automatically makes one.")
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(mutedrole)
        await ctx.send(f"`{member}` have been unmuted")

    

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member=None, *, reason="No reason provided"):
        if member == ctx.author:
            await ctx.send("You can't kick yourself :eyes:")
        await member.kick(reason=reason)

        await member.send(embed=discord.Embed(
                        title=f"You have been kicked from {ctx.guild.name}",
                        color=var.C_RED
                        ).add_field(name="Reason", value=reason
                        ).add_field(name="Kicked by", value=ctx.author)
                        )
        await ctx.send(f"`{member}` have been kicked from the server")



    @commands.command(aliases=["clean", "clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit:int=None):
        if limit is not None:
            await ctx.channel.purge(limit=limit+1)

            info = await ctx.send(embed=discord.Embed(
                                description=f"Deleted {limit} messages",
                                color=var.C_ORANGE)
                                )
            await asyncio.sleep(2)
            await info.delete()
        else:
            await ctx.send(f"You need to define the amount too! Follow this format:\n```{getprefix(ctx)}purge <amount>```\n Amount should be in numbers.")


def setup(bot):
    bot.add_cog(Moderation(bot))