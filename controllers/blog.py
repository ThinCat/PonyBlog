#!/usr/bin/env python
# coding: utf-8

import web
import hashlib
import HTMLParser
from config import settings
from config.url import urls
from datetime import datetime
from authcode import Captcha

render = settings.render
db = settings.db
L = settings.L
blog_tb = 'blog'
admin_tb = 'admin'

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'isAdmin': False, 'adminUser': None})

def get_by_id(id):
    s = db.select(blog_tb, where='id=$id', vars=locals())
    if not s:
        return False
    return s[0]

class Index:

    def GET(self, page=1):
        page = int(page)
        perpage = 5
        offset = (page - 1) * perpage
        blogs = db.select("blog", order="id DESC", offset=offset, limit=perpage)
        postcount = db.query("SELECT COUNT(*) AS count FROM blog")[0]
        pages = postcount.count / perpage
        if postcount.count % perpage > 0:
            pages += 1
        if page > pages:
            raise web.seeother('/')
        else:
            return render.index(blogs=blogs, pages=pages, currentpage=page)

class View:

    def GET(self, id):
        blog = get_by_id(id)
        if not blog:
            return render.error(L('Articles not found'), None)
        content = HTMLParser.HTMLParser().unescape(blog.content)
        pre = db.query('select id,title from blog where id < $id order by id desc limit 1', vars=locals())
        #pre = db.query('select * from blog where id = (select max(id) from blog where id < $id)', vars=locals())
        next = db.query('select id,title from blog where id > $id order by id asc limit 1', vars=locals())
        #next = db.query('select * from blog where id = (select min(id) from blog where id > $id)', vars=locals())
        if len(pre) > 0:
            pre = pre[0]
        else:
            pre = None
        if len(next) > 0:
            next = next[0]
        else:
            next = None
        return render.view(blog, content, pre, next)

class AdminLogin:

    def GET(self):
        return render.login()

    def POST(self):
        loginurl = '/admin/login'
        i = web.input()
        username = i.get('username', None)
        password = i.get('password', None)
        authcode = i.get('authcode', None)
        if not username or not password or not authcode:
            return render.error(L('Username, password and captcha is need'), loginurl)
        if session.captcha != authcode.lower():
            return render.error(L('Captcha not correct'), loginurl)
        admin = db.select(admin_tb, where='username=$username', vars=locals())
        if not admin:
            return render.error(L('User not found'), loginurl)
        m = hashlib.md5()
        m.update(password)
        password_md5 = m.hexdigest()
        if password_md5 == admin[0].password:
            session.isAdmin = True
            session.adminUser = username
            raise web.seeother('/admin/index')
        else:
            return render.error(L('Password not correct'), loginurl)

class AdminLogout:
    def GET(self):
        session.isAdmin = False
        session.adminUser = None
        raise web.seeother('/')

class AdminIndex:

    def GET(self, page=1):
        if session.isAdmin == True:
            page = int(page)
            perpage = 5
            offset = (page - 1) * perpage
            blogs = db.select("blog", order="id DESC", offset=offset, limit=perpage)
            postcount = db.query("SELECT COUNT(*) AS count FROM blog")[0]
            pages = postcount.count / perpage
            if postcount.count % perpage > 0:
                pages += 1
            if page > pages:
                raise web.seeother('/admin/index')
            else:
                adminUser = session.adminUser
                return render.admin(blogs=blogs, pages=pages, currentpage=page, adminUser=adminUser)
        else:
            raise web.seeother('/admin/login')
            return

class AddBlog:

    def POST(self):
        i = web.input()
        title = i.get('title', None)
        content = i.get('content', None)
        if not title or not content:
            return render.error(L('Title and content is need'), None)
        db.insert(blog_tb, title=title, content=content, time=datetime.now())
        return render.error(L('Add complete'), '/admin/index')

class EditBlog:

    def GET(self, id):
        blog = get_by_id(id)
        adminUser = session.adminUser
        return render.edit(blog, adminUser)

    def POST(self, id):
        i = web.input()
        title = i.get('title', None)
        content = i.get('content', None)
        if not id or not title or not content:
            return render.error(L('Title and content is need'), None)
        db.update(blog_tb, title=title, content=content, time=datetime.now(), where='id=$id', vars=locals())
        return render.error(L('Edit complete'), '/admin/index')

class DelBlog:

    def GET(self, id):
        db.delete(blog_tb, where='id=$id', vars=locals())
        return render.error(L('Delete complete'), '/admin/index')

class AuthCode:

    def GET(self):
        web.header('Content-Type','image/jpeg')
        return Captcha(session).getCaptcha()


