# -*- coding: utf-8 -*-
"""
    :author: Dream Zhou (周梦雄)
    :url: https://heypython.cn
    :copyright: © 2020 Dream Zhou <zhoumengxiong@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template

from . import app


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
