#!/usr/bin/env python
# coding: utf-8

import random
from io import BytesIO
from captcha.image import ImageCaptcha

class Captcha:
    def __init__(self, session):
        self.session = session

    def getCaptcha(self):
        _chars = 'ABCDEFGHJKLMNPQRSTUVWXY23456789'
        chars = random.sample(_chars, 4)
        self.session.captcha = (''.join(chars)).lower()
        image = ImageCaptcha(fonts=['./static/fonts/arial.ttf', './static/fonts/arial.ttf'])
        data = image.generate(chars)
        return data