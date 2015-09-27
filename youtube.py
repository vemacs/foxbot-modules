# coding=utf8
"""
youtube.py  YouTube Module
Copyright 2012, Dimitri Molenaars, Tyrope.nl.
Copyright © 2012-2014, Elad Alfassa, <elad@fedoraproject.org>
Copyright 2012, Edward Powell, embolalia.net
Copyright 2015, Max Gurela
Licensed under the Eiffel Forum License 2.

http://sopel.dfbta.net

This module will respond to .yt and .youtube commands and searches the youtubes.
"""
from __future__ import unicode_literals, division

from sopel import web, tools
from sopel.module import rule, commands, example
from sopel.formatting import color, colors, bold
import datetime
import json
import re
import sys
if sys.version_info.major < 3:
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser

ISO8601_PERIOD_REGEX = re.compile(
    r"^(?P<sign>[+-])?"
    r"P(?!\b)"
    r"(?P<y>[0-9]+([,.][0-9]+)?(?:Y))?"
    r"(?P<mo>[0-9]+([,.][0-9]+)?M)?"
    r"(?P<w>[0-9]+([,.][0-9]+)?W)?"
    r"(?P<d>[0-9]+([,.][0-9]+)?D)?"
    r"((?:T)(?P<h>[0-9]+([,.][0-9]+)?H)?"
    r"(?P<m>[0-9]+([,.][0-9]+)?M)?"
    r"(?P<s>[0-9]+([,.][0-9]+)?S)?)?$")
regex = re.compile('(youtube.com/watch\S*v=|youtu.be/)([\w-]+)')


def configure(config):
    """
    Google api key can be created by signing up your bot at
    [https://console.developers.google.com](https://console.developers.google.com).

    | [google]     | example                        | purpose                               |
    | ------------ | ------------------------------ | ------------------------------------- |
    | public_key   | aoijeoifjaSIOAohsofhaoAS       | Google API key (server key preferred) |
    """

    if config.option('Configure youtube module? (You will need to register a new application at https://console.developers.google.com/)', False):
        config.interactive_add('google', 'public_key', None)


def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = ytinfo


def shutdown(bot):
    del bot.memory['url_callbacks'][regex]


def ytget(bot, trigger, uri):
    if not bot.config.google.public_key:
        return None
    bytes = web.get(uri + '&key=' + bot.config.google.public_key)
    try:
        result = json.loads(bytes)
    except ValueError:
        return None
    result = result['items'][0]

    splitdur = ISO8601_PERIOD_REGEX.match(result['contentDetails']['duration'])
    dur = []
    for k, v in splitdur.groupdict().iteritems():
        if v is not None:
            dur.append(v.lower())
    result['contentDetails']['duration'] = ' '.join(dur)

    pubdate = datetime.datetime.strptime(result['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    result['snippet']['publishedAt'] = pubdate.strftime('%D %T')

    for k in result['statistics']:
        result['statistics'][k] = '{:,}'.format(long(result['statistics'][k]))

    return result


@commands('yt', 'youtube')
@example('.yt Anime 404')
def ytsearch(bot, trigger):
    """
    .youtube <query> - Search YouTube
    """
    if not trigger.group(2):
        return
    uri = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=' + trigger.group(2)
    raw = web.get(uri + '&key=' + bot.config.google.public_key)
    vid = json.loads(raw)['items'][0]['id']['videoId']
    uri = 'https://www.googleapis.com/youtube/v3/videos?id=' + vid + '&part=contentDetails,snippet,statistics'
    video_info = ytget(bot, trigger, uri)
    if video_info is None:
        return

    title = video_info['snippet']['title']
    uploader = video_info['snippet']['channelTitle']
    duration = video_info['contentDetails']['duration']
    views = video_info['statistics']['viewCount']
    likes = video_info['statistics']['likeCount']
    dislikes = video_info['statistics']['dislikeCount']

    message = '[YT Search] {0} | https://youtu.be/{1} | Duration: {2} | Views: {3} | Uploader: {4} | {5} | {6}'.format(
      bold(title), video_info['id'], duration, views, uploader, color(likes, colors.GREEN), color(likes, colors.RED))

    bot.say(message)


@rule('.*(youtube.com/watch\S*v=|youtu.be/)([\w-]+).*')
def ytinfo(bot, trigger, found_match=None):
    """
    Get information about the given youtube video
    """
    match = found_match or trigger
    uri = 'https://www.googleapis.com/youtube/v3/videos?id=' + match.group(2) + '&part=contentDetails,snippet,statistics'

    video_info = ytget(bot, trigger, uri)
    if video_info is None:
        return

    title = video_info['snippet']['title']
    uploader = video_info['snippet']['channelTitle']
    duration = video_info['contentDetails']['duration']
    views = video_info['statistics']['viewCount']
    likes = video_info['statistics']['likeCount']
    dislikes = video_info['statistics']['dislikeCount']

    message = '[YouTube] {0} | Duration: {1} | Views: {2} | Uploader: {3} | {4} | {5}'.format(
      bold(title), duration, views, uploader, color(likes, colors.GREEN), color(likes, colors.RED))

    bot.say(message)
