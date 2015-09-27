# coding=utf8
from sopel.module import rule, unblockable, event
from sopel.formatting import bold

@rule('^\[(.+)\]$')
def intensify(bot, trigger):
    bot.say(bold('[{0} INTENSIFIES]'.format(trigger.group(1).upper())))

@rule('.*')
@event("JOIN")
@unblockable
def honk_join(bot, trigger):
    if not trigger.nick == bot.config.core.nick:
        bot.action('honks {0}'.format(trigger.nick))
