#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""minify html"""

from __future__ import annotations

import re
from typing import List

from . import const, recache

html_fns: recache.ReCache = recache.ReCache()

TAG_RE: re.Pattern[str] = re.compile(r"<[^>]+>", re.I | re.M | re.S)
TAG_SPACE_RE: re.Pattern[str] = re.compile(r">\s+<")
TAG_BREAK_RE: re.Pattern[str] = re.compile(r"\s{2,}|[\r\n]")


@html_fns.recache(r"<!--.*?-->", re.S)
def html_remove_comments(pat: re.Pattern[str], html: str) -> str:
    """remove html comments"""
    return pat.sub("", html)


def html_remove_type(html: str) -> str:
    """remove html `type` attr from <script> and <style>"""
    return (
        html.replace('<style type="text/css">', "<style>")
        .replace("<style type='text/css'>", "<style>")
        .replace("<style type=text/css>", "<style>")
        .replace('<script type="text/javascript">', "<script>")
        .replace("<script type='text/javascript'>", "<script>")
        .replace("<script type=text/javascript>", "<script>")
    )


@html_fns.recache(r"(?:" + "|".join(const.UNNEEDED_HTML_TAGS) + r")", re.I)
def html_remove_unneeded_tags(pat: re.Pattern[str], html: str) -> str:
    """remove optional html tags"""
    return pat.sub("", html)


@html_fns.recache(r'([a-zA-Z]+)="([a-zA-Z0-9-_\.]+)"')
def html_unquote_attrs(pat: re.Pattern[str], html: str) -> str:
    """remove all html quotes on attibutes if possible"""
    return TAG_RE.sub(lambda m: pat.sub(r"\1=\2", m.group()), html)


@html_fns.recache(
    r"(<\s*(?:pre|code|textarea).*>|<\s*/\s*(?:pre|code|textarea)\s*>)",
    re.I,
)
def html_remove_whitespace(pat: re.Pattern[str], html: str) -> str:
    """remove useless html whitespace ( does not minify whitespace-sensitive tags )"""

    tags: int = 0
    split: List[str] = [
        TAG_SPACE_RE.sub("> <", tag) if idx % 2 == 1 else tag
        for idx, tag in enumerate(pat.split(html))
    ]

    for idx, tag in enumerate(split):
        if idx % 2 == 0 and tags == 0:
            split[idx] = TAG_BREAK_RE.sub(" ", tag)
        elif (idx + 1) % 2 == 0:
            tags += 1 if "/" not in tag else -1

    return "".join(split)


def minify_html(html: str) -> str:
    """run all html stages"""

    html_fns.compileall()

    html = html_remove_comments(html)
    html = html_remove_type(html)
    html = html_remove_unneeded_tags(html)
    html = html_remove_whitespace(html)
    html = html_unquote_attrs(html)

    return html
