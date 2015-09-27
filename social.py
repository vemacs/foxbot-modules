# coding=utf8
from sopel.module import commands, example

db_prefix = 'social_'
keys = {
    'desktop': db_prefix + 'desktop_url',
    'homepage': db_prefix + 'homepage_url',
    'homescreen': db_prefix + 'homescreen_url',
    'waifu': db_prefix + 'waifu_url'
}

@commands('lasturl')
def lasturl(bot, trigger):
    sender = trigger.sender
    if bot.memory.contains('last_seen_url') and bot.memory['last_seen_url'][sender]:
        url = bot.memory['last_seen_url'][sender]
        bot.say('[LAST URL] %s' % url)


@commands('dtop', 'desktop')
def desktop(bot, trigger):
    if not trigger.group(2):
        url = bot.db.get_nick_value(trigger.nick, keys['desktop'])
        if not url:
            bot.say('You have no saved desktop!')
            return
        bot.say('%s [%s]' % (url, trigger.nick))
        return
    if trigger.group(2).split(' ')[0] == '-s':
        if trigger.group(2).split(' ')[1].strip() == '':
            bot.reply('Please provide a URL! (.dtop -s <url>)')
            return
        url = trigger.group(2).split(' ')[1].strip()
        bot.db.set_nick_value(trigger.nick, keys['desktop'], url)
        bot.reply('Desktop set!')
        return
    nick = trigger.group(2).split(' ')[0]
    url = bot.db.get_nick_value(nick, keys['desktop'])
    if not url:
        bot.say('%s has no saved desktop!' % nick)
        return
    bot.say('%s [%s]' % (url, nick))

@commands('hp', 'homepage')
def homepage(bot, trigger):
    if not trigger.group(2):
        url = bot.db.get_nick_value(trigger.nick, keys['homepage'])
        if not url:
            bot.say('You have no saved homepage!')
            return
        bot.say('%s [%s]' % (url, trigger.nick))
        return
    if trigger.group(2).split(' ')[0] == '-s':
        if trigger.group(2).split(' ')[1].strip() == '':
            bot.reply('Please provide a URL! (.homepage -s <url>)')
            return
        url = trigger.group(2).split(' ')[1].strip()
        bot.db.set_nick_value(trigger.nick, keys['homepage'], url)
        bot.reply('Homepage set!')
        return
    nick = trigger.group(2).split(' ')[0]
    url = bot.db.get_nick_value(nick, keys['homepage'])
    if not desktop_url:
        bot.say('%s has no saved homepage!' % nick)
        return
    bot.say('%s [%s]' % (url, nick))

@commands('hscr', 'homescreen')
def homescreen(bot, trigger):
    if not trigger.group(2):
        url = bot.db.get_nick_value(trigger.nick, keys['homescreen'])
        if not url:
            bot.say('You have no saved homescreen!')
            return
        bot.say('%s [%s]' % (url, trigger.nick))
        return
    if trigger.group(2).split(' ')[0] == '-s':
        if trigger.group(2).split(' ')[1].strip() == '':
            bot.reply('Please provide a URL! (.homescreen -s <url>)')
            return
        url = trigger.group(2).split(' ')[1].strip()
        bot.db.set_nick_value(trigger.nick, keys['homescreen'], url)
        bot.reply('Homescreen set!')
        return
    nick = trigger.group(2).split(' ')[0]
    url = bot.db.get_nick_value(nick, keys['homescreen'])
    if not desktop_url:
        bot.say('%s has no saved homescreen!' % nick)
        return
    bot.say('%s [%s]' % (url, nick))

@commands('waifu')
def waifu(bot, trigger):
    if not trigger.group(2):
        url = bot.db.get_nick_value(trigger.nick, keys['waifu'])
        if not url:
            bot.say('You have no saved waifu!')
            return
        bot.say('%s [%s]' % (url, trigger.nick))
        return
    if trigger.group(2).split(' ')[0] == '-s':
        if trigger.group(2).split(' ')[1].strip() == '':
            bot.reply('Please provide a URL! (.waifu -s <url>)')
            return
        url = trigger.group(2).split(' ')[1].strip()
        bot.db.set_nick_value(trigger.nick, keys['waifu'], url)
        bot.reply('Waifu set!')
        return
    nick = trigger.group(2).split(' ')[0]
    url = bot.db.get_nick_value(nick, keys['waifu'])
    if not desktop_url:
        bot.say('%s has no saved waifu!' % nick)
        return
    bot.say('%s [%s]' % (url, nick))
