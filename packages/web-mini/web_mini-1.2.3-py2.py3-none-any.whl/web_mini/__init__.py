#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""web-mini -- efficient css and html minifer inspired by \
https://pypi.org/project/css-html-js-minify/"""

from typing import Tuple

from . import css, html

__version__: str = "1.2.3"
__all__: Tuple[str, ...] = "__version__", "html", "css"
