# coding=utf8
from sopel.module import commands

@commands('lasturl')
def lasturl(bot, trigger):
    sender = trigger.sender
    if bot.memory.contains('last_seen_url') and bot.memory['last_seen_url'][sender]:
        url = bot.memory['last_seen_url'][sender]
        bot.say('[LAST URL] %s' % url)


@commands('dtop', 'desktop')
def dtop(bot, trigger):
    if not trigger.group(2):
        desktop_url = bot.db.get_nick_value(trigger.nick, 'desktop_url')
        if not desktop_url:
            bot.say('You have no saved desktop!')
            return
        bot.say('%s [%s]' % (desktop_url, trigger.nick))
        return
    if trigger.group(2).split(' ')[0] == '-s':
        if trigger.group(2).split(' ')[1].strip() == '':
            bot.reply('Please provide a URL!')
            return
        url = trigger.group(2).split(' ')[1].strip()
        bot.db.set_nick_value(trigger.nick, 'desktop_url', url)
        bot.reply('Desktop set!')
        return
