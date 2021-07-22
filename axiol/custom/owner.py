import discord
from discord.ext import commands
from functions import updatedb
from discord.ext.commands import GuildConverter
import database as db

# A private cog which only works for me
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    def cog_check(self, ctx):
        return ctx.author.id == 791950104680071188
        

    @commands.command()
    async def accuracy(self, ctx, *, txt=None):
        if txt is None:
            return await ctx.send("You need to define both main text and user inputted content sepeated by `|`")
        text = txt.split("|")[0].lstrip(' ').rstrip(' ').lower()
        content = txt.split("|")[1].lstrip(' ').rstrip(' ').lower()
        wrong_chars = []
        correct_chars = []
        for x, y in zip(text, content):
            if x == y:
                correct_chars.append(y)
            else:
                wrong_chars.append(y)
        accuracy = round((len(correct_chars) / (len(wrong_chars)+len(correct_chars))) * 100, 2) if len(correct_chars) != 0 else 0

        await ctx.send(f"Main text: {text}\nUser input: {content}\n\nMain text characters: __{len(text)}__\nInput text characters: __{len(content)}__\n```Mistakes: __{len(wrong_chars)}__\nAccuracy: {accuracy}%```")


    @commands.command()
    async def get_guilds(self, ctx, user:discord.User=None):
        if user is None:
            return await ctx.send("You need to define the user to find in which guilds they are!")
        data = {}
        for guild in self.bot.guilds:
            for member in guild.members:
                if member == user:
                    data.update({guild.name: guild.id})
        if data:
            await ctx.send(f"**{user}** found in __{len(data)}__ guilds\n```json\n{data}```")
        else:
            await ctx.send(f"**{user}** found in __0__ guilds")



    @commands.command()
    async def get_members(self, ctx, *, guild=None):
        if guild is None:
            return await ctx.send("You need to define the guild too")
        
        converter = GuildConverter()
        try:
            guildobj = await converter.convert(ctx, guild)
        except commands.errors.GuildNotFound:
            return await ctx.send(f"**{guild}** Guild not found")

        members = ""
        for i in guildobj.members:
            members += f"`{i}` - "
            if len(members) > 1500:
                members += "**\nMessage was too long so this is not complete**"
                break
            
        await ctx.send(members)


    @commands.command()
    async def get_doc(self, ctx, doc_name, guild):
        if doc_name is None or guild is None:
            return await ctx.send("You need to define both document name and guild name/id")
        converter = GuildConverter()
        try:
            guildobj = await converter.convert(ctx, guild)
        except commands.errors.GuildNotFound:
            return await ctx.send(f"**{guild}** Guild not found")

        try:
            plugindb = getattr(db, doc_name.upper())
        except:
            return await ctx.send(f"No document with name **{doc_name.upper()}**")

        doc = plugindb.find_one({"_id":guildobj.id})
        
        await ctx.send(f"**{doc_name.upper()}** Document for **{guildobj.name}**\n```json\n{doc}```")


def setup(bot):
    bot.add_cog(Owner(bot))
