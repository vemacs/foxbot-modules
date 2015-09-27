# coding=utf8
from sopel.module import commands

add_strings = [
    "-a", "-add", "--add",
    "-s", "-set", "--set"
]


@commands('lasturl')
def lasturl(bot, trigger):
    sender = trigger.sender
    if bot.memory.contains('last_seen_url') and sender in bot.memory['last_seen_url']:
        url = bot.memory['last_seen_url'][sender]
        bot.say('[LAST URL] %s' % url)
    else:
        bot.reply('no URLs in memory.')


@commands('dtop', 'desktop')
def desktop(bot, trigger):
    run_command(bot, trigger, 'desktop')


@commands('waifu')
def waifu(bot, trigger):
    run_command(bot, trigger, 'waifu')


@commands('hs', 'homescreen')
def homescreen(bot, trigger):
    run_command(bot, trigger, 'homescreen')


@commands('hp', 'homepage')
def homepage(bot, trigger):
    run_command(bot, trigger, 'homepage')


def run_command(bot, trigger, cmd):
    db_prefix = 'social_'
    db_key = db_prefix + cmd
    nick = trigger.nick
    if trigger.group(2):
        args = trigger.group(2).split(' ')
        if args[0] in add_strings:
            if len(args) == 1:
                bot.reply('please provide a URL. (.%s -s <url>)' % cmd)
            else:
                url = args[1].strip()
                bot.db.set_nick_value(trigger.nick, db_key, url)
                bot.reply('%s set.' % cmd)
        else:
            nick = args[0]
    else:
        url = bot.db.get_nick_value(nick, db_key)
        if not url:
            if nick == trigger.nick:
                bot.reply('you have no saved %s.' % cmd)
            else:
                bot.reply('%s has no saved %s.' % (nick, cmd))
        else:
            bot.reply('%s [%s]' % (url, nick))
