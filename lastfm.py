# coding=utf8
from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.formatting import color, colors
import pylast

class LastSection(StaticSection):
    api_key = ValidatedAttribute('api_key')

db_prefix = 'lastfm_'
keys = {
    'lastfm': db_prefix + 'username',
}

add_strings = [
    "-a", "-add", "--add",
        "-s", "-set", "--set"
]

def setup(bot):
    bot.config.define_section('lastfm', LastSection)

def configure(config):
    config.define_section('lastfm', LastSection, validate=False)
    config.swallow.configure_setting('api_key',
                                     'last.fm API key')

@commands('lastfm', 'np')
def now_playing(bot, trigger):
    if trigger.group(2):
        if trigger.group(2).split(' ')[0] in add_strings:
            if len(trigger.group(2).split(' ')[1].strip()) == 0:
                bot.reply('please provide a username! (.np -s <url>)')
                return
            url = trigger.group(2).split(' ')[1].strip()
            bot.db.set_nick_value(trigger.nick, keys['lastfm'], url)
            bot.reply('username set!')
            return
    if not bot.db.get_nick_value(trigger.nick, keys['lastfm']):
        bot.reply('you have no last.fm username set! Please set one with .np -s <username>')
        return
    network = pylast.LastFMNetwork(api_key = bot.config.lastfm.api_key)
    user = network.get_user(trigger.nick)
    current_track = user.get_now_playing()
    if not current_track:
        bot.say('%s is not playing anything right now.' % trigger.nick)
        return
    bot.say('%s is now playing: %s' % (trigger.nick, color(current_track, colors.GREEN)))
