#!/usr/bin/env python
# coding: utf-8
import web

db = web.database(dbn='mysql', db='xcblog', user='root', pw='r00t$web')

render = web.template.render('templates/', cache=False)

web.config.debug = False

config = web.storage(
    email='xcblog@gmail.com',
    site_name = '晓城博客',
    site_desc = '一个简单的个人博客系统',
    static = '/static',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
