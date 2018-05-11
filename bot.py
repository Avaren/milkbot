import logging
import ujson

from discord.ext import commands

EXTENSIONS = ['cogs.errors', 'cogs.redeem']


class MilkBot(commands.AutoShardedBot):

    def __init__(self):
        super(MilkBot, self).__init__(command_prefix='!')

        self.settings = load_settings()

        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
                logging.info(f'Loaded extension {extension}')
            except Exception as e:
                logging.info(f'Failed to load extension {extension}\n{type(e).__name__}: {e}')

        logging.info("Initialisation complete.")

    def run(self):
        super(MilkBot, self).run(self.settings['token'])


def load_settings():
    with open('settings.json') as f:
        return ujson.load(f)


def run():
    bot = MilkBot()
    bot.run()
