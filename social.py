# coding=utf8
from sopel.module import commands
from util.constants import ADD_STRINGS


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
    db_key = 'social_' + cmd
    nick = trigger.nick
    if trigger.group(2):
        args = trigger.group(2).split(' ')
        if args[0] in ADD_STRINGS:
            if len(args) == 1:
                bot.reply('please provide a URL. (.{0} -s <url>)'.format(cmd))
            else:
                url = args[1].strip()
                bot.db.set_nick_value(trigger.nick, db_key, url)
                bot.reply('{0} set.'.format(cmd))
            return
        nick = args[0]
    url = bot.db.get_nick_value(nick, db_key)
    if not url:
        if nick == trigger.nick:
            bot.reply('you have no saved {0}.'.format(cmd))
        else:
            bot.reply('{0} has no saved {1}.'.format(nick, cmd))
    else:
        bot.say('{0} [{1}]'.format(url, nick))

