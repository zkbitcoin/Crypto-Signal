
"""Notify a user via discord
"""

import os
import structlog
#from webcord import Webhook
from discord_webhook import DiscordWebhook, DiscordEmbed

class DiscordNotifier():
    """Class for handling Discord notifications
    """

    def __init__(self, webhook, username, avatar=None):
        """Initialize DiscordNotifier class

        Args:
            webhook (str): Discord web hook to allow message sending.
            username (str): Display name for the discord bot.
            avatar (str, optional): Defaults to None. Url of an image to use as an avatar.
        """

        self.logger = structlog.get_logger()
        self.discord_username = username
        self.discord_webhook = webhook
        #self.discord_client = Webhook(webhook, avatar_url=avatar)

        #self.discord_client = Webhook(webhook, avatar_url=avatar)
        #self.discord_client = DiscordWebhook(url=webhook, username=username)


    #def notify(self, message):
    def notify(self, exchange, market_pair, candle_period, messages, send_charts):
        """Sends the message.

        Args:
            messages (dict): A dict with the messages to send.
        """
        
        market_pair = market_pair.replace('/', '_').lower()
        chart_file = '{}/{}_{}_{}.png'.format('./charts', exchange, market_pair, candle_period)  

        webhook = DiscordWebhook(url=self.discord_webhook, content='Webhook Message')
             

        if send_charts == True and os.path.exists(chart_file):
            with open(chart_file, 'rb') as f:
                webhook.add_file(file=f.read(), filename=chart_file)

        embed = DiscordEmbed(title='Embed Title', description='The messagess', color=242424)

        webhook.add_embed(embed)
        webhook.execute()    
