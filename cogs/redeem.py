from discord.ext import commands

from bot import MilkBot
from lib.config import Config

BLACKLIST = 'XXXX'


class Redeem():

    def __init__(self, bot: MilkBot):
        self.bot = bot
        self.keys = Config('redeem.json')

    @commands.command()
    @commands.guild_only()
    async def redeem(self, ctx: commands.Context):
        used_keys = {user: key for key, user in self.keys.all().items() if user}
        try:
            key = used_keys[ctx.author.id]
        except KeyError:
            try:
                key = next(k for k, u in self.keys.all().items() if not u)
            except StopIteration:
                await ctx.send('Error: Run out of keys to redeem. @Developer will need to generate more.')
                return
            await self.keys.put(key, ctx.author.id)

        await ctx.author.send(f"Your exclusive Lazarus Discord skin key: {key}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def addkeys(self, ctx: commands.Context, *keys: str):
        existing_keys = set(self.keys.all().keys())
        keys = set(keys)
        new_keys = keys - existing_keys
        await self.keys.put_many(dict.fromkeys(new_keys))
        await ctx.send(f"Added {len(new_keys)} keys")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def redeemedkeys(self, ctx: commands.Context):
        redeemed_keys = {k: u for k, u in self.keys.all().items() if u}
        await ctx.send(f"Redeemed {len(redeemed_keys)} of {len(self.keys.all())} keys")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def removekey(self, ctx: commands.Context, key):
        try:
            user_id = self.keys[key]
            if user_id and user_id != BLACKLIST:
                user = ctx.guild.get_member(user_id)
                user = user.mention if user else user_id
                await ctx.send(f"Key {key} owned by {user} blacklisted")
            else:
                raise KeyError()
        except KeyError:
            await ctx.send(f"Key {key} blacklisted")

        await self.keys.put(key, BLACKLIST)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def lookupkey(self, ctx: commands.Context, key):
        try:
            user_id = self.keys[key]
            if user_id and user_id != BLACKLIST:
                user = ctx.guild.get_member(user_id)
                user = user.mention if user else user_id
                await ctx.send(f"Key {key} owned by {user}")
            elif user_id == BLACKLIST:
                await ctx.send(f"Key {key} blacklisted")
            else:
                await ctx.send(f"Key {key} unredeemed")
        except KeyError:
            await ctx.send(f"Key {key} not found")


def setup(bot):
    bot.add_cog(Redeem(bot))
