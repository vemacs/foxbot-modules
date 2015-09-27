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

from random import random
from sopel.module import rule, unblockable, event
from sopel.formatting import bold, color, colors

chance = 0.25

@rule('^\[(.+)\]$')
def intensify(bot, trigger):
    bot.say(bold('[{0} INTENSIFIES]'.format(trigger.group(1).upper())))


@rule('^wew$')
def wew(bot, trigger):
    if random() <= chance:
        bot.say(bold('w e w l a d'))


@rule('^same$')
def same(bot, trigger):
    if random() <= chance:
        if not trigger.nick == bot.config.core.nick:
            bot.say('same')


@rule('^ayy+')
def ayy(bot, trigger):
    if random() <= chance:
        bot.say('lmao')


@rule('.*')
@event("JOIN")
def honk_join(bot, trigger):
    if random() <= chance:
        if not trigger.nick == bot.config.core.nick:
            bot.action('honks {0}'.format(trigger.nick))


@rule('.*')
@event("JOIN")
@unblockable
def abuse_tomoko(bot, trigger):
    if trigger.nick == 'Tomoko_A_Best':
        bot.say(color('[NORMIE ALERT]', colors.RED))
