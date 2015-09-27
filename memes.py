# coding=utf8
from sopel.module import rule
from sopel.formatting import bold

@rule('^\[(.+)\]$')
def intensify(bot, trigger):
    bot.say(bold('[{0} INTENSIFIES]'.format(trigger.group(1).upper())))

