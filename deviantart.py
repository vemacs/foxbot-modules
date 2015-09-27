# coding=utf8
"""
deviantart.py - Deviantart Sopel module, Displays additional info about deviantart links
Copyright 2014 Max Gurela

Licensed under the Eiffel Forum License 2.
"""
from __future__ import unicode_literals
from sopel import tools, web
from sopel.module import rule
from sopel.formatting import color, bold

import json
import re


def setup(bot):
    regex = re.compile('((?:.+\.)?deviantart\.com/.*)')
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = get_page_info


def get_info(url=None):
    if url:
        api_url = 'http://backend.deviantart.com/oembed?url={0}'.format(url)
    else:
        return None
    data = web.get(api_url)
    data = json.loads(data)
    return data


@rule('.*https?://((?:.+\.)?deviantart\.com/.*).*')
def get_page_info(bot, trigger):
    try:
        requested = get_info('http://' + trigger.group(1))
    except:
        return
    if not requested:
        bot.say('[deviantart] Error:  does not exist.')
    else:
        message = '[deviantart] {0} by {1} ({2}) [{3}]'.format(get_prefix(), requested['title'], requested['author_name'], requested['type'], requested['category'])
        bot.say(message)
