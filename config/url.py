#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
    '/',                    pre_fix + 'blog.Index',
    '/page/(\d+)',          pre_fix + 'blog.Index',
    '/view/(\d+)',          pre_fix + 'blog.View',
    '/admin/login',         pre_fix + 'blog.AdminLogin',
    '/admin/logout',        pre_fix + 'blog.AdminLogout',
    '/admin/index',         pre_fix + 'blog.AdminIndex',
    '/admin/page/(\d+)',    pre_fix + 'blog.AdminIndex',
    '/admin/add',           pre_fix + 'blog.AddBlog',
    '/admin/edit/(\d+)',    pre_fix + 'blog.EditBlog',
    '/admin/del/(\d+)',     pre_fix + 'blog.DelBlog',
    '/authcode',            pre_fix + 'blog.AuthCode',
)
