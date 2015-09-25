#!/usr/bin/env python
# coding: utf-8
import web
from lang import Lang

db = web.database(dbn='mysql', db='xcblog', user='root', pw='r00t$web')

render = web.template.render('templates/', cache=False)

# 'en' for english, 'cn' for chinese
language = 'en'

web.config.debug = False

config = web.storage(
    author = 'ThinCat',
    email = 'thinblackcat@sina.com',
    site_name = 'PonyBlog',
    site_desc = 'A tiny blog system base on web.py',
    static = '/static',
)

def L(strKey, lang=language):
    if lang == 'en':
        return strKey
    if lang == 'cn':
        return Lang[strKey]

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
web.template.Template.globals['lang'] = Lang
web.template.Template.globals['L'] = L
