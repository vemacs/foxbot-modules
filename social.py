# -*- coding: utf-8 -*-

# Copyright (C) 2015 Lee Watson

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


from sopel.module import commands

ADD_STRINGS = [
    "-a", "-add", "--add",
    "-s", "-set", "--set"
]


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


@commands('selfie')
def selfie(bot, trigger):
    run_command(bot, trigger, 'selfie')


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
