"""Notify another app via webhook
"""

import json
import os
import asyncio
import requests
import structlog

from notifiers.utils import NotifierUtils
import redis


class WebhookNotifier(NotifierUtils):
    """Class for handling webhook notifications
    """
    def __init__(self, url, username, password):
        self.logger = structlog.get_logger()
        self.url = url
        self.username = username
        self.password = password
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379)
        self.p = self.r.pubsub(ignore_subscribe_messages=True)
        self.p.subscribe('crypto_signal.crypto_signal')

    def __del__(self):
        self.p.close()
        self.r.close()

    def notify(self, messages, chart_file):
        """Sends the notification messages.

        Args:
            messages (dict): A dict with the messages to send.
        """

        #market_pair = market_pair.replace('/', '_').lower()
        #chart_file = '{}/{}_{}_{}.png'.format('./charts', exchange, market_pair, candle_period)

        #data = {'messages': messages}
        #data = json.dumps(data)
        #Content type must be included in the header
        headers = {"content-type": "application/json"}

        self.r.publish('crypto_signal.crypto_signal', json.dumps({
            "event": "message",
            "subscription": "crypto_signal.crypto_signal",
            "data": {
                "messages": messages
            }
        }))

        #
        #result = ws.recv()
        #result = json.loads(result)
        #print ("Received '%s'" % result)

        #if chart_file and os.path.exists(chart_file):
        #    files = {'chart': open(chart_file, 'rb')}
        #
        #    if self.username and self.password:
        #        request = requests.post(
        #            self.url, files=files, data=data, auth=(self.username, self.password))
        #    else:
        #        request = requests.post(self.url, files=files, data=data)
        #else:
        #if self.username and self.password:
        #    request = requests.post(
        #        self.url,  headers=headers, data=data, auth=(self.username, self.password))
        #else:
        #    request = requests.post(self.url,  headers=headers, data=data)

        #if not request.status_code == requests.codes.ok:
        #    self.logger.error("Request failed: %s - %s",
        #                      request.status_code, request.content)
