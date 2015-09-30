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
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.formatting import color, colors, bold
import pylast

ADD_STRINGS = [
    "-a", "-add", "--add",
    "-s", "-set", "--set"
]

network = None

class LastSection(StaticSection):
    api_key = ValidatedAttribute('api_key')


def setup(bot):
    global network
    bot.config.define_section('lastfm', LastSection)
    network = pylast.LastFMNetwork(api_key = bot.config.lastfm.api_key)


def configure(config):
    config.define_section('lastfm', LastSection, validate=False)
    config.lastfm.configure_setting('api_key', 'last.fm API key')


@commands('lastfm', 'np')
def now_playing(bot, trigger):
    global network
    db_key = 'lastfm_username'
    if trigger.group(2):
        args = trigger.group(2).split(' ')
        if args[0] in ADD_STRINGS:
            if len(args) == 1:
                bot.reply('please provide a username. (.np -s <url>)')
            else:
                username = args[1].strip()
                if network.get_user(username).get_id():
                    bot.db.set_nick_value(trigger.nick, db_key, username)
                    bot.reply('last.fm username set.')
                else:
                    bot.reply('no such last.fm user. Are you trying to trick me? :^)')
        return
    username = bot.db.get_nick_value(trigger.nick, db_key)
    if not username:
        bot.reply('you have no last.fm username set. Please set one with .np -s <username>')
    else:
        user = network.get_user(username)
        current_track = user.get_now_playing()
        if not current_track:
            bot.say('{0} is not listening to anything right now.'.format(trigger.nick))
        else:
            trackinfo = '{0} - {1}'.format(current_track.get_artist().get_name(), current_track.get_title())
            bot.say('{0} is now playing {1} | {2}'.format(trigger.nick, bold(trackinfo), color(current_track.get_url(), colors.BLUE)))


@commands('compare', 'lastfmcompare')
def compare(bot, trigger):
    global network
    db_key = 'lastfm_username'
    args = trigger.group(2).split(' ')
    if not len(args) == 1:
        bot.reply('please provide 2 usernames.')
    else:
        user1 = bot.db.get_nick_value(trigger.nick, db_key)
        user2 = bot.db.get_nick_value(args[0], db_key)
        if not user1:
            bot.reply('you have no last.fm username set. Please set one with .np -s <username>')
            return
        elif not user2:
            bot.reply('{0} has no last.fm username set. Ask them to set one with .np -s <username>'.format(user2))
            return
        try:
            result = network.get_user(user1).compare_with_user(user2)
        except pylast.WSError:
            bot.reply('last.fm API is still broken.')
            return
        bot.reply('Result: {0}').format(result)

