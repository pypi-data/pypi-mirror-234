#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""web-mini -- efficient css and html minifer inspired by \
https://pypi.org/project/css-html-js-minify/"""

from typing import Tuple

from . import css, html

__version__: str = "1.2.7"
__all__: Tuple[str, ...] = "__version__", "css", "html", "compileall"


def compileall() -> None:
    """compile all css and html regex"""

    css.css_fns.compileall()
    html.html_fns.compileall()
