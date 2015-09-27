# coding=utf8
"""
gelbooru.py - People on IRC will love your leggings fetish!
Copyright 2014 Max Gurela
Adapted for use with sopel from https://github.com/infinitylabs/uguubot/blob/master/plugins/gelbooru.py

Licensed under the Eiffel Forum License 2 (It's GPL compatible!).
"""
from __future__ import unicode_literals
from sopel.module import commands, rule
from sopel.formatting import color, colors
from sopel import tools, web
from bs4 import BeautifulSoup
import random
import re

gelbooru_cache = []
lastsearch = ''


def setup(bot):
    regex = re.compile('gelbooru.com.*(?:\?|&)id\=([-_a-zA-Z0-9]+)')
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = gelbooru_url


def refresh_cache(bot, inp):
    global gelbooru_cache
    gelbooru_cache = []
    num = 0
    search = ''
    if inp == '':
        search = 'rating:safe'
    else:
        search = inp.replace('explicit', 'rating:explicit').replace('nsfw', 'rating:explicit').replace('safe', 'rating:safe').replace('sfw', 'rating:safe')
    if not 'rating:' in search:
        search += ' rating:safe'
    soup = get_soup('http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=10&tags={0}'.format(search))
    posts = soup.find_all('post')

    while num < len(posts):
        gelbooru_cache.append((posts[num].get('id'), posts[num].get('score'), posts[num].get('file_url'), posts[num].get('rating'), posts[num].get('tags')))
        num += 1

    random.shuffle(gelbooru_cache)
    return


@commands('gb', 'gelbooru')
def gelbooru(bot, trigger):
    """
    .gelbooru <tags> -- Gets a random image, based on given tags from gelbooru.com
    """
    global lastsearch
    global gelbooru_cache

    if trigger.group(2):
        search = trigger.group(2).strip().lower()
    else:
        search = ''
    if not search in lastsearch or len(gelbooru_cache) < 2:
        refresh_cache(bot, search)
    lastsearch = search

    if len(gelbooru_cache) == 0:
        bot.say('No results for search "{0}"'.format(trigger.group(2).strip()))
        return

    id, score, url, rating, tags = gelbooru_cache.pop()

    if 'e' in rating:
        rating = color('NSFW', colors.RED)
    elif 'q' in rating:
        rating = color('Questionable', colors.YELLOW)
    elif 's' in rating:
        rating = colors('Safe', colors.GREEN)

    bot.say('[Gelbooru] Score: {0} | Rating: {1} | http://gelbooru.com/index.php?page=post&s=view&id={2} | Tags: {3}'.format(score, rating, id, tags.strip()))


@rule(r'(?:.*)(?:gelbooru.com.*?id=)([-_a-zA-Z0-9]+)(?: .+)?')
def gelbooru_url(bot, trigger):
    soup = get_soup('http://gelbooru.com/index.php?page=dapi&s=post&q=index&id={0}'.format(trigger.group(1)))
    posts = soup.find_all('post')

    id, score, url, rating, tags = (posts[0].get('id'), posts[0].get('score'), posts[0].get('file_url'), posts[0].get('rating'), posts[0].get('tags'))

    if 'e' in rating:
        rating = color('NSFW', colors.RED)
    elif 'q' in rating:
        rating = color('Questionable', colors.YELLOW)
    elif 's' in rating:
        rating = colors('Safe', colors.GREEN)

    bot.say('[Gelbooru] Score: {0} | Rating: {1} | Tags: {2}'.format(score, rating, tags.strip()))


def get_soup(url):
    return BeautifulSoup(web.get(url), 'lxml')
