#!/usr/bin/env python

# This program creates a tray for storing playing cards.  The tray should be
# cut from wood or plastic on a laser cutter.

# Note that CorelDraw's SVG import feature assumes a page size of 8.5 x 11.

# This program requires pysvg (http://codeboje.de/pysvg/), version 0.2.2
# or version 0.2.2b, which can be downloaded from
# https://pypi.python.org/pypi/pysvg

# Copyright 2013-2014 Timur Tabi
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# This software is provided by the copyright holders and contributors "as is"
# and any express or implied warranties, including, but not limited to, the
# implied warranties of merchantability and fitness for a particular purpose
# are disclaimed. In no event shall the copyright holder or contributors be
# liable for any direct, indirect, incidental, special, exemplary, or
# consequential damages (including, but not limited to, procurement of
# substitute goods or services; loss of use, data, or profits; or business
# interruption) however caused and on any theory of liability, whether in
# contract, strict liability, or tort (including negligence or otherwise)
# arising in any way out of the use of this software, even if advised of
# the possibility of such damage.

import math
import pysvg.structure
from pysvg.turtle import Turtle, Vector
from optparse import OptionParser

# How CorelDraw defines a Hairline width
HAIRLINE = 0.01

# The width of the tabs
TAB = 10

# Returns True if the number is even
def is_even(number):
    return number % 2 == 0

class DeckSVG(object):
    def __init__(self, width, height, filename, start = Vector(0, 0)):
        global o, a

        self.t = Turtle(stroke=o.color, strokeWidth=str(o.line))
        self.width = int(math.ceil(width))
        self.height = int(math.ceil(height))
        self.filename = filename
        self.t.moveTo(start)
        self.t.setOrientation(Vector(1, 0))
        self.t.penDown()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.t.finish()
        print self.t.getXML()

        # Some versions of pysvg have ".Svg" and some have ".svg", so just
        # try one at a time until it works.
        try:
            self.svg = pysvg.structure.Svg(width='%smm' % self.width, height='%smm' % self.height)
        except AttributeError:
            self.svg = pysvg.structure.svg(width='%smm' % self.width, height='%smm' % self.height)
        self.svg.set_viewBox('0 0 %s %s' % (self.width, self.height))

        self.t.addTurtlePathToSVG(self.svg)
        print 'Saving to %s (size: %umm x %umm)' % (self.filename, self.width, self.height)
        self.svg.save(self.filename)

    def r(self, before = None, after = None):
        if before:
            self.t.forward(before)
        self.t.right(90)
        if after:
            self.t.forward(after)

    def l(self, before = None, after = None):
        if before:
            self.t.forward(before)
        self.t.left(90)
        if after:
            self.t.forward(after)

    def f(self, length):
        self.t.forward(length)

    def v(self, x, y):
        return Vector(x, y)

    def here(self):
        return self.t.getPosition()

    def up(self):
        self.t.penUp()

    def down(self):
        self.t.penDown()

    # Move to a specific position
    def move(self, x = 0, y = 0, v = None):
        if not v:
            v = Vector(x, y)
        self.t.moveTo(v)

    # Move relative to the current position
    def shift(self, x = 0, y = 0, v = None):
        if not v:
            v = Vector(x, y)
        self.t.moveTo(self.t.getPosition() + v)

    # Move to a specific position without drawing
    def relocate(self, x = 0, y = 0, v = None):
        if not v:
            v = Vector(x, y)
        self.t.penUp()
        self.t.moveTo(v)
        self.t.penDown()

    def east(self):
        self.t.setOrientation(Vector(1, 0))

    def north(self):
        self.t.setOrientation(Vector(0, -1))

    def west(self):
        self.t.setOrientation(Vector(-1, 0))

    def south(self):
        self.t.setOrientation(Vector(0, 1))

    def notchl(self, width, height):
        self.t.left(90)
        self.t.forward(width)
        self.t.right(90)
        self.t.forward(height)
        self.t.right(90)
        self.t.forward(width)
        self.t.left(90)

    def notchr(self, width, height):
        self.t.right(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.forward(height)
        self.t.left(90)
        self.t.forward(width)
        self.t.right(90)

    def rectangle(self, length, width):
        self.t.forward(length)
        self.t.right(90)
        self.t.forward(width)
        self.t.right(90)
        self.t.forward(length)
        self.t.right(90)
        self.t.forward(width)

# Draw a single divider.  If short==True, then make it a short divider for
# the left and right sides.
def deck_tabbed_divider(t, short):
    global o, a, notch_front, notch_back

    # The amount the bottom is inset (from the bottom of the card) for
    # even-numbered trays.
    INSET = 15

    # Top
    t.east()
    if short:
        t.f(o.m + o.h - INSET)
    else:
        t.f(o.m + o.h + o.m)
    t.r()

    # Right
    if short:
        t.f(o.d)
        t.r()
#        t.f(o.m)
    else:
        t.f(5)
        t.r()
        t.f(o.m)
        t.l()
        t.f(o.d - 5)
        t.r()

    # Bottom
    if short:
        t.f(notch_front - INSET)
    else:
        t.f(notch_front)
    t.notchl(o.m, TAB)
    t.f(notch_back)
    t.r()

    # Left
    t.f(o.d - 5)
    t.l()
    t.f(o.m)
    t.r()
    t.f(5)


def deck_divider():
    global o, a, notch_front, notch_back

    gap = 5

    with DeckSVG(2 * o.m + o.h, (o.n + 1) * (o.d + o.n + gap), 'tray_divider.svg') as t:
        # For N decks, we need N+1 dividers
        # If N is odd, then they are all long dividers
        # If N is even, then (N + 1) / are short, the rest are long
        for i in range(0, o.n + 1):
            here = t.here()
            if is_even(o.n):
                deck_tabbed_divider(t, is_even(i))
            else:
                deck_tabbed_divider(t, False)

            # Move to next divider
            t.relocate(v = here + Vector(0, o.d + o.m + gap))

# If it's even, then we want front tabs only on every other internal
# divider (i.e. not the edges)
def deck_bottom():
    global o, a
    global notch_back, notch_front

    # Needs to match value in deck_front_even()
    width = o.w / 3

    # The amount the bottom is inset for even-numbered trays
    INSET = 15

    with DeckSVG((o.n + 1) * o.m + (o.n * o.w), (2 * o.m) + o.h, 'tray_bottom.svg') as t:
        # Back
        for i in range(0, o.n):
            pos = t.here()
            t.f(o.m + (o.w / 2) - (TAB / 2))
            t.notchr(o.m, TAB)
            t.move(v = pos + Vector(o.w + o.m, 0))
        t.f(o.m)
        t.r()

        # Right side
        t.f(o.m + notch_back)
        t.notchr(o.m, TAB)
        if is_even(o.n):
            t.f(notch_front - INSET)
        else:
            t.f(o.m + notch_front)
        t.r()

        if is_even(o.n):
            for i in range(0, o.n / 2):
                t.f(o.m + o.w - width)
                t.l()
                t.f(INSET)
                t.r()
                t.f(width)
                t.notchl(o.m, o.m)
                t.f(width)
                t.r()
                t.f(INSET)
                t.l()
                t.f(o.w - width)
            t.f(o.m)
        else:
            #       _____________
            #      |             |
            #    __|             |__
            # __|                   |__
            width = o.w - (2 * 5.0)     # finger notch width    # Fixme: '5' should be a variable
            for i in range(0, o.n):
                t.f(o.m)
                t.r()
                t.f(o.m)
                t.l()
                t.f(5)    # Fixme: '5' should be a variable

                t.notchr(10, width)

                t.f(5)    # Fixme: '5' should be a variable
                t.l()
                t.f(o.m)
                t.r()
            t.f(o.m)

        # Left side
        t.r()
        if is_even(o.n):
            t.f(notch_front - INSET)
        else:
            t.f(o.m + notch_front)
        t.notchr(o.m, TAB)
        t.f(o.m + notch_back)
        t.up()

        # Notch holes for dividers
        t.up()
        for i in range(1, o.n):
            t.move((o.m + o.w) * i, o.m + notch_back)
            t.east()  # right
            t.down()
            t.rectangle(o.m, TAB)
            t.up()

# Fixme: combine this with the bottom piece
def deck_back():
    global o, a

    with DeckSVG((o.n + 1) * o.m + (o.n * o.w), o.d + o.m, 'tray_back.svg', start = Vector(o.m, 0)) as t:
        # Top
        t.f(o.w)
        for i in range(1, o.n):
            t.notchr(5, o.m)
            t.f(o.w)

        # Upper-right corner
        t.r()
        t.f(5)
        t.l()
        t.f(o.m)
        t.r()

        # Right side
        t.f(o.d - 5)
        t.r()

        # Bottom
        for i in range(0, o.n):
            pos = t.here()
            t.f(o.m + (o.w / 2) - (TAB / 2))
            t.notchl(o.m, TAB)
            t.t.moveTo(pos - Vector(o.w + o.m, 0))
        t.move(0, pos.y)
        t.r()

        # Left side
        t.f(o.d - 5)

        # Upper-left corner
        t.r()
        t.f(o.m)
        t.l()
        t.f(5)

# Make a single front tab for the left edge
#     ___
#   _|   |
#  |_    |
#    |___|
def deck_front_tab_left(t, width):
    global o, a

    # Top side
    t.relocate(0, 5)

    t.east()
    t.f(o.m)

    t.l()
    t.f(5)
    t.r()
    t.f(width)
    t.r()

    # Right side
    t.f(o.d + o.m)
    t.r()

    # Bottom side
    t.f(width)
    t.r()
    t.f(o.m)
    t.l()

    t.f(o.m)
    t.r()
    t.f(o.d - 5)

# Make a single front tab for the right edge
#   ___
#  |   |_
#  |    _|
#  |___|
def deck_front_tab_right(t, width):
    global o, a

    # Top side
    t.east()
    t.f(width)
    t.r()

    # Right side
    t.f(5)
    t.l()
    t.f(o.m)

    t.r()
    t.f(o.d - 5)
    t.r()

    t.f(o.m)

    t.l()
    t.f(o.m)
    t.r()
    t.f(width)
    t.r()

    # Left side
    t.f(o.d + o.m)


# Make a single front tab, with different left and right lengths
#   ___   ___
#  |   |_|   |
#  |    _    |
#  |___| |___|
def deck_front_tab(t, left, right):
    global o, a

    t.east()

    # Top side
    t.f(left)
    t.notchr(5, o.m)
    t.f(right)
    t.r()

    # Right side
    t.f(o.d + o.m)
    t.r()

    # Bottom side
    t.f(right)
    t.notchr(o.m, o.m)
    t.f(left)
    t.r()

    # Left side
    t.f(o.d + o.m)

# Make all the front tabs, if there are an even number of tabs
#
# If there are an even number of decks, then we can eliminate half
# of the tabs by making each other tab twice as wide.
def deck_front_even():
    global o, a

    # Needs to match value in deck_bottom()
    width = o.w / 3
    gap = 5
    count = o.n / 2

    with DeckSVG(count * (2 * width + o.m) + (count - 1) * gap, o.d + o.m, 'tray_front.svg') as t:
        for i in range(0, count):
            here = t.here()
            deck_front_tab(t, width, width)
            t.relocate(v = here + Vector(2 * width + o.m + gap, 0)) # This is where the next divider is drawn

# Make all the front tabs, if there are an odd number of tabs
#
# However, if the number of tabs is odd, then it becomes really
# messy.  For now, do it the traditional way
def deck_front_odd():
    global o, a

    width = 5
    gap = 5

    with DeckSVG(2 * (o.m + width) + (o.n - 1) * (o.m + 2 * width) + (o.n * gap), o.d + o.m, 'tray_front.svg') as t:
        here = t.here()
        # Left tab
        deck_front_tab_left(t, width)
        t.relocate(v = here + Vector(width + o.m + gap, 0))

        # Middle tabs
        for i in range(0, o.n - 1):
            here = t.here()
            deck_front_tab(t, width, width)
            t.relocate(v = here + Vector(2 * width + o.m + gap, 0))

        # Right tab
        deck_front_tab_right(t, width)

def deck_front():
    if is_even(o.n):
        deck_front_even()
    else:
        deck_front_odd()

# Defaults for Dominion Victory cards
parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-H", dest="h", help="card height in millimeters (default=%default)",
                  type="float", default = 92)
parser.add_option("-W", dest="w", help="card width in millimeters (default=%default)",
                  type="float", default = 60)
parser.add_option("-d", dest="d", help="deck thickness in millimeters (default=%default)",
                  type="float", default = 20)
parser.add_option("-n", dest="n", help="number of decks (default=%default)",
                  type="int", default = 5)
parser.add_option("-m", dest="m", help="material thickness (default=%default)",
                  type="float", default = 3)
parser.add_option('-c', dest='color', help='drawing color (default=%default)',
                  type='string', default = 'red')
parser.add_option('-l', dest='line', help='line width (default=%default)',
                  type='float', default = HAIRLINE)

(o, a) = parser.parse_args()

# We need to restrict the deck thickness so that the notches are drawn correctly
if o.d < 10:
    o.d = 10

# Calculate the space behind and in front of the notches on the bottoms of
# the dividers
notch_back = (o.h - TAB) / 2
notch_front = o.h - (notch_back + TAB)

deck_divider()
deck_bottom()
deck_back()
deck_front()
