import logging
import traceback

from discord.ext import commands

from bot import MilkBot


class ErrorHandler():

    def __init__(self, bot: MilkBot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.message.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(ctx._(str(error)))
        elif isinstance(error, commands.DisabledCommand):
            await ctx.message.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(str(error).replace('to run command', 'to run that command'))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                str(error).replace('Bot requires', 'I require').replace('to run command', 'to run that command'))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            logging.error(f'In {ctx.command.qualified_name}:')
            logging.error('\n'.join(traceback.format_tb(error.original.__traceback__)))
            logging.error(f'{error.original.__class__.__name__}: {error.original}')
            await ctx.send('There was an issue processing that command, please try again.')
        else:
            logging.info(f'{error.__class__.__name__}: {error}')


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
