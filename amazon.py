# coding=utf8
"""
amazon.py - amazon plugin adapted from
https://github.com/infinitylabs/uguubot/blob/master/plugins/amazon.py

Licensed under the Eiffel Forum License 2.
"""
from __future__ import unicode_literals
from sopel import tools, web
from sopel.module import commands, rule
from lxml import html
import json
import re


def setup(bot):
    regex = re.compile('((www\.)?amazon\.com/[^ ]+)')
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = amazon_url


@rule(r'(https?:\/\/(www\.)?amazon\..+/[^ ]+)')
def amazon_url(bot, trigger):
    item = html.fromstring(web.get(trigger.group(1)))
    try:
        title = item.xpath("//span[@id='productTitle']/text()")[0]
    except:
        title = item.xpath("//span[@id='btAsinTitle']/text()")[0]
    try:
        price = item.xpath("//span[@id='priceblock_ourprice']/text()")[0]
    except:
        try:
            price = item.xpath("//span[@id='priceblock_saleprice']/text()")[0]
        except:
            try:
                price = item.xpath("//b[@class='priceLarge']/text()")[0]
            except:
                price = "$?"
    try:
        rating = item.xpath("//div[@id='avgRating']/span/text()")[0].strip()
    except:
        rating = item.xpath("//div[@class='gry txtnormal acrRating']/text()")[0].strip()
    try:
        breadcrumb = ' '.join(item.xpath("//li[@class='breadcrumb']")[0].text_content().split())
    except:
        breadcrumb = "Unknown"

    star_count = round(float(rating.split(' ')[0]), 0)
    stars = ''
    for x in xrange(0, int(star_count)):
        stars += u'\u2605'
    for y in xrange(int(star_count), 5):
        stars += u'\u2606'

    bot.say('[Amazon] {0} | {1} | {2} | {3}', title, breadcrumb, price, stars)
