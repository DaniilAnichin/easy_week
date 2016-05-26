#!/use/bin/python
# -*- coding: utf-8 -*-
import gettext

eng = gettext.translation('messages', './locale', languages=['en'])
ua = gettext.translation('messages', './locale', languages=['ua'])
ru = gettext.translation('messages', './locale', languages=['ru'])

ua.install()
