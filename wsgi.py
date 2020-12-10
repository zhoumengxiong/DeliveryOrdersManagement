# -*- coding: utf-8 -*-
"""
    :author: Dream Zhou (周梦雄)
    :url: https://heypython.cn
    :copyright: © 2020 Dream Zhou <zhoumengxiong@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from workorder import app
