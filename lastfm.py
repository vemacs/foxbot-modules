# coding=utf8
from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.formatting import color, colors
import pylast
from util.constants import ADD_STRINGS

class LastSection(StaticSection):
    api_key = ValidatedAttribute('api_key')


def setup(bot):
    bot.config.define_section('lastfm', LastSection)


def configure(config):
    config.define_section('lastfm', LastSection, validate=False)
    config.lastfm.configure_setting('api_key', 'last.fm API key')


@commands('lastfm', 'np')
def now_playing(bot, trigger):
    db_key = 'lastfm_username'
    if trigger.group(2):
        args = trigger.group(2).split(' ')
        if args[0] in ADD_STRINGS:
            if len(args) == 1:
                bot.reply('please provide a username. (.np -s <url>)')
            else:
                username = args[1].strip()
                bot.db.set_nick_value(trigger.nick, db_key, username)
                bot.reply('last.fm username set.')
        return
    username = bot.db.get_nick_value(trigger.nick, db_key)
    if not username:
        bot.reply('you have no last.fm username set. Please set one with .np -s <username>')
    else:
        network = pylast.LastFMNetwork(api_key = bot.config.lastfm.api_key)
        user = network.get_user(username)
        current_track = user.get_now_playing()
        if not current_track:
            bot.say('{0} is not listening to anything right now.'.format(trigger.nick))
        else:
            bot.say('{0} is now playing: {1} - {2} | {3}'.format(trigger.nick, current_track.get_artist().get_name(), current_track.get_title(), color(current_track.get_url(), colors.BLUE)))

