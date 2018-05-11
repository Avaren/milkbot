import logging

import bot

logging.basicConfig(style='{', format="{asctime}:{levelname}:{name}:{message}", level=logging.INFO)
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.CRITICAL)

if __name__ == '__main__':
    bot.run()
