#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""colour helpers"""

from __future__ import annotations

import re
import typing


def rgb_to_hex(match: re.Match[str]) -> str:
    """rgb -> hex"""

    r, g, b = match.groups()
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def rgba_to_hex(match: re.Match[str]) -> str:
    """rgba -> hexa"""

    r, g, b, a = match.groups()
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}{int(float(a) * 255):02x}"


def hsl_to_hex(match: re.Match[str]) -> str:
    """hsl -> hex"""

    h, s, l = match.groups()
    r, g, b = hsl_to_rgb(int(h), float(s), float(l))

    return f"#{r:02x}{g:02x}{b:02x}"


def hsla_to_hex(match: re.Match[str]) -> str:
    """hsla -> hexa"""

    h, s, l, a = match.groups()
    r, g, b = hsl_to_rgb(int(h), float(s), float(l))

    return f"#{r:02x}{g:02x}{b:02x}{int(float(a) * 255):02x}"


def hue_to_rgb(p: float, q: float, t: float) -> float:
    """convers the hue to the rgb value"""

    if t < 0:
        t += 1

    if t > 1:
        t -= 1

    if t < 1 / 6:
        return p + (q - p) * 6 * t

    if t < 1 / 2:
        return q

    if t < 2 / 3:
        return p + (q - p) * (2 / 3 - t) * 6

    return p


def hsl_to_rgb(h: float, s: float, l: float) -> typing.Tuple[int, int, int]:
    """convers hsl values to rgb values"""

    h /= 360
    s /= 100
    l /= 100

    if s == 0:
        r = g = b = l
    else:
        q: float

        if l < 0.5:
            q = l * (1 + s)
        else:
            q = l + s - l * s

        p: float = 2 * l - q

        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

    return int(r * 255), int(g * 255), int(b * 255)
