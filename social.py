# coding=utf8
from sopel.module import commands

@commands('lasturl')
def lasturl(bot, trigger):
    sender = trigger.sender
    if bot.memory.contains('last_seen_url') and bot.memory['last_seen_url'][sender]:
        url = bot.memory['last_seen_url'][sender]
        bot.say('[LAST URL] %s' % url)
