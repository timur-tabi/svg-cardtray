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

import pysvg.structure
from pysvg.turtle import Turtle, Vector
from optparse import OptionParser

# How CorelDraw defines a Hairline width
HAIRLINE = 0.5 #.01

# The width of the tabs
TAB = 10

class DeckSVG(object):
    def __init__(self, width, height, filename, start = Vector(0, 0)):
        self.t = Turtle(stroke='blue', strokeWidth=str(HAIRLINE))
        self.width = width
        self.height = height
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

    def r(self):
        self.t.right(90)

    def l(self):
        self.t.left(90)

    def f(self, length):
        self.t.forward(length)

    def v(self, x, y):
        return Vector(x, y)

    def here(self):
        return self.t.getPosition()

    def up(self):
        self.t.penUp();

    def down(self):
        self.t.penDown();

    # Move to a specific position
    def move(self, x, y):
        self.t.moveTo(Vector(x, y))

    # Move relative to the current position
    def shift(self, x, y):
        self.t.moveTo(self.t.getPosition() + Vector(x, y))

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

def deck_divider():
    global o, a, notch_front, notch_back

    with DeckSVG(2 * o.m + o.h, (o.n + 1) * (o.d + o.n + 5), 'tray_divider.svg') as t:
        # For N decks, we need N+1 dividers
        for i in range(0, o.n + 1):
            # Fixme: since we need notches on the bottom, we can't share the edges
            # We can fix this by putting unused notches on the top.

            # Top
            t.f(o.h + 2 * o.m)
            t.r()

            # Right
            t.f(5)
            t.r()
            t.f(o.m)
            t.l()
            t.f(o.d - 5)
            t.r()

            # Bottom
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

            # Move to next divider
            t.up()
            t.shift(0, o.d + o.m + 5)    # Fixme: adjust the gap between dividers
            t.east()
            t.down()

def deck_bottom():
    global o, a
    global notch_back, notch_front

    WIDTH = (o.n + 1) * o.m + (o.n * o.w)

    with DeckSVG(WIDTH, (2 * o.m) + o.h, 'tray_bottom.svg') as t:
        # Back
        for i in range(0, o.n):
            pos = t.here()
            t.f(o.m + (o.w / 2) - (TAB / 2))
            t.notchr(o.m, TAB)
            t.t.moveTo(pos + Vector(o.w + o.m, 0))
        t.move(WIDTH, pos.y)
        t.r()

        # Right side
        t.f(o.m + notch_back)
        t.notchr(o.m, TAB)
        t.f(o.m + notch_front)
        t.r()

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
        t.r()

        # Left side
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

def deck_front():
    global o, a

    with DeckSVG((2 * (o.m + 5)) + ((o.n - 1) * (2 * 5 + o.m)), o.d + o.m, 'tray_front.svg', start = Vector(o.m, 0)) as t:
        # Left piece
        t.f(5)
        t.r()
        t.f(o.d + o.m)
        t.r()
        t.f(5)    # Fixme: '5' should be a variable
        t.r()
        t.f(o.m)
        t.l()
        t.f(o.m)
        t.r()
        t.f(o.d - 5)
        t.r()
        t.f(o.m)
        t.l()
        t.f(5)    # Fixme: '5' should be a variable

        # Move to upper-left corner of first middle piece
        t.up()
        t.move(o.m + 5, 0)    # Fixme: '5' should be a variable
        t.east()
        t.down()

        for i in range(0, o.n - 1):
            t.f(5)
            t.notchr(5, o.m)    # Top notch
            t.f(5)
            t.r()

            next_pos = t.here()  # This is where the next divider is drawn

            t.f(o.d + o.m)
            t.r()
            t.f(5)
            t.notchr(5, o.m)    # Bottom notch
            t.f(5)

            t.up()
            t.t.moveTo(next_pos)
            t.east()  # right
            t.down()

        # Right piece
        t.f(5)    # Fixme: 5 should be a variable
        t.r()
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
        t.f(5)

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
