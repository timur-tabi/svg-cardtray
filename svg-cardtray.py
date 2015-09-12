#!/usr/bin/env python

# This program creates a tray for storing playing cards.  The tray should be
# cut from wood or plastic on a laser cutter.

# Note that CorelDraw's SVG import feature assumes a page size of 8.5 x 11.

# This program requires pysvg (http://codeboje.de/pysvg/)

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

import sys
import os
import pysvg.builders
import pysvg.structure
import pysvg.style
import pysvg.shape
from pysvg.turtle import Turtle, Vector
from optparse import OptionParser

# P1 acrylic size at Ponoko.com
WIDTH = 181
HEIGHT = 181

# How CorelDraw defines a Hairline width
HAIRLINE = 0.5 #.01

# The width of the tabs
TAB = 10


# A notch (rectangle with only three sides) starting from (x,y)
def notchl(turtle, width, height):
    turtle.left(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(height)
    turtle.right(90)
    turtle.forward(width)
    turtle.left(90)

# A notch (rectangle with only three sides) starting from (x,y)
def notchr(turtle, width, height):
    turtle.right(90)
    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)
    turtle.left(90)
    turtle.forward(width)
    turtle.right(90)

def rectangle(turtle, length, width):
    turtle.forward(length)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)
    turtle.forward(width)

def deck_divider():
    global o, a, notch_top, notch_bottom

    WIDTH = 2 * o.m + o.h
    HEIGHT = (o.n + 1) * (o.d + o.n + 5)

    svg = pysvg.structure.svg(width='%smm' % WIDTH, height='%smm' % HEIGHT)
    svg.set_viewBox('0 0 %s %s' % (WIDTH, HEIGHT))

    s = Turtle(stroke='blue', strokeWidth=str(HAIRLINE))
    s.moveTo(Vector(o.m, 0))
    s.penDown()

    # For N decks, we need N+1 dividers
    for i in range(0, o.n + 1):
        # Fixme: since we need notches on the bottom, we can't share the
        # edges
        s.forward(o.h)
        s.right(90)

        s.forward(notch_top)
        notchl(s, o.m, TAB)
        s.forward(notch_bottom)

        s.right(90)
        s.forward(notch_front)
        notchl(s, o.m, TAB)
        s.forward(notch_back)

        s.right(90)
        s.forward(notch_bottom)
        notchl(s, o.m, TAB)
        s.forward(notch_top)

        s.penUp()
        s.moveTo(s.getPosition() + Vector(0, o.d + o.m + 5))    # Fixme: adjust the gap between dividers
        s.setOrientation(Vector(1, 0))  # right
        s.penDown()

    s.finish()
    print s.getXML()
    s=s.addTurtlePathToSVG(svg)

    print 'Dividers size: %smm * %smm' % (WIDTH, HEIGHT)
    svg.save('tray_divider.svg')

def deck_bottom():
    global o, a
    global notch_back, notch_front

    WIDTH = (o.n + 1) * o.m + (o.n * o.w)
    HEIGHT = (2 * o.m) + o.h
    svg = pysvg.structure.svg(width='%smm' % WIDTH, height='%smm' % HEIGHT)
    svg.set_viewBox('0 0 %s %s' % (WIDTH, HEIGHT))

    s = Turtle(stroke='blue', strokeWidth=str(HAIRLINE))
    s.moveTo(Vector(0, 0))
    s.penDown()

    # Back
    for i in range(0, o.n):
        pos = s.getPosition()
        s.forward(o.m + (o.w / 2) - (TAB / 2))
        notchr(s, o.m, TAB)
        s.moveTo(pos + Vector(o.w + o.m, 0))
    s.moveTo(Vector(WIDTH, pos.y))
    s.right(90)

    # Right side
    s.forward(o.m + notch_back)
    notchr(s, o.m, TAB)
    s.forward(o.m + notch_front)
#    s.moveTo(Vector(WIDTH, HEIGHT))
    s.right(90)

    #       _____________
    #      |             |
    #    __|             |__
    # __|                   |__
    width = o.w - (2 * 5.0)     # finger notch width    # Fixme: '5' should be a variable
    for i in range(0, o.n):
        s.forward(o.m)
        s.right(90)
        s.forward(o.m)
        s.left(90)
        s.forward(5)    # Fixme: '5' should be a variable

        notchr(s, 10, width)

        s.forward(5)    # Fixme: '5' should be a variable
        s.left(90)
        s.forward(o.m)
        s.right(90)
    s.forward(o.m)
    s.right(90)

    # Left side
    s.forward(o.m + notch_front)
    notchr(s, o.m, TAB)
    s.forward(o.m + notch_back)
    s.penUp()

    # Notch holes for dividers
    s.penUp()
    for i in range(1, o.n):
        s.moveTo(Vector((o.m + o.w) * i, o.m + notch_back))
        s.setOrientation(Vector(1, 0))  # right
        s.penDown()
        rectangle(s, o.m, TAB)
        s.penUp()

    s.finish()
    print s.getXML()
    s=s.addTurtlePathToSVG(svg)

    print 'Bottom size: %smm * %smm' % (WIDTH, HEIGHT)
    svg.save('tray_bottom.svg')

# Fixme: combine this with the bottom piece
def deck_back():
    global o, a, notch_top, notch_bottom

    WIDTH = (o.n + 1) * o.m + (o.n * o.w)
    HEIGHT = o.d + o.m
    svg = pysvg.structure.svg(width='%smm' % WIDTH, height='%smm' % HEIGHT)
    svg.set_viewBox('0 0 %s %s' % (WIDTH, HEIGHT))

    s = Turtle(stroke='blue', strokeWidth=str(HAIRLINE))
    s.moveTo(Vector(0, 0))
    s.penDown()

    # Top
    s.forward(WIDTH)
    s.right(90)

    # Right side
    s.forward(notch_top)
    notchr(s, o.m, TAB)
    s.forward(notch_bottom)
    s.right(90)

    # Bottom
    for i in range(0, o.n):
        pos = s.getPosition()
        s.forward(o.m + (o.w / 2) - (TAB / 2))
        notchl(s, o.m, TAB)
        s.moveTo(pos - Vector(o.w + o.m, 0))
    s.moveTo(Vector(0, pos.y))
    s.right(90)

    # Left side
    s.forward(notch_bottom)
    notchr(s, o.m, TAB)
    s.forward(notch_top)

    # Notch holes for dividers
    notch_y = (o.d - TAB) / 2
    s.penUp()
    for i in range(1, o.n):
        s.moveTo(Vector((o.m + o.w) * i, notch_y))
        s.setOrientation(Vector(1, 0))  # right
        s.penDown()
        s.forward(o.m)
        s.right(90)
        s.forward(TAB)
        s.right(90)
        s.forward(o.m)
        s.right(90)
        s.forward(TAB)
        s.penUp()

    s.finish()
    print s.getXML()
    s=s.addTurtlePathToSVG(svg)

    print 'Back size: %smm * %smm' % (WIDTH, HEIGHT)
    svg.save('tray_back.svg')

def deck_front():
    global o, a
    global notch_top, notch_bottom

    WIDTH = (2 * (o.m + 5)) + ((o.n - 1) * (2 * 5 + o.m))
    HEIGHT = o.d + o.m
    svg = pysvg.structure.svg(width='%smm' % WIDTH, height='%smm' % HEIGHT)
    svg.set_viewBox('0 0 %s %s' % (WIDTH, HEIGHT))

    s = Turtle(stroke='blue', strokeWidth=str(HAIRLINE))
    s.moveTo(Vector(0, 0))
    s.penDown()

    # Left piece
    s.forward(o.m + 5)    # Fixme: '5' should be a variable
    s.right(90)
    s.forward(o.d + o.m)
    s.right(90)
    s.forward(5)    # Fixme: '5' should be a variable
    s.right(90)
    s.forward(o.m)
    s.left(90)
    s.forward(o.m)
    s.right(90)
    s.forward(notch_bottom)
    notchr(s, o.m, TAB)
    s.forward(notch_top)

    # Move to upper-left corner of first middle piece
    s.penUp()
    s.moveTo(Vector(o.m + 5, 0))    # Fixme: '5' should be a variable
    s.setOrientation(Vector(1, 0))  # right
    s.penDown()

    for i in range(0, o.n - 1):
        start_pos = s.getPosition()
        s.forward(2 * 5 + o.m)    # Fixme: '5' should be a variable
        next_pos = s.getPosition()  # This is where the next divider is drawn
        s.right(90)
        s.forward(o.d + o.m)
        s.right(90)
        s.forward(5)    # Fixme: '5' should be a variable
        notchr(s, o.m, o.m)
        s.forward(5)

        # The notch hole for the dividers
        s.penUp()
        s.moveTo(start_pos + Vector(5, notch_top))  # Fixme: '5' should be a variable
        s.setOrientation(Vector(1, 0))  # right
        s.penDown()
        s.forward(o.m)
        s.right(90)
        s.forward(TAB)
        s.right(90)
        s.forward(o.m)
        s.right(90)
        s.forward(TAB)

        s.penUp()
        s.moveTo(next_pos)
        s.setOrientation(Vector(1, 0))  # right
        s.penDown()

    # Right piece
    s.forward(o.m + 5)    # Fixme: '5' should be a variable
    s.right(90)
    s.forward(notch_top)
    notchr(s, o.m, TAB)
    s.forward(notch_bottom)
    s.right(90)
    s.forward(o.m)
    s.left(90)
    s.forward(o.m)
    s.right(90)
    s.forward(5)        # Fixme: '5' should be a variable

    s.finish()
    print s.getXML()
    s = s.addTurtlePathToSVG(svg)

    print 'Front size: %smm * %smm' % (WIDTH, HEIGHT)
    svg.save('tray_front.svg')

# Defaults for Dominion Victory cards
parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-H", dest="h", help="card height", type="float", default = 92)
parser.add_option("-W", dest="w", help="card width", type="float", default = 60)
parser.add_option("-d", dest="d", help="deck thickness", type="float", default = 20)
parser.add_option("-n", dest="n", help="number of decks", type="int", default = 5)
parser.add_option("-m", dest="m", help="material thickness (default=%default)", type="int", default = 3)

(o, a) = parser.parse_args()

# Fixme: we should be smarter about limits
if o.d < 20:
    o.d = 20

# Calculate the space above and below the notches on the ends of the dividers
notch_top = (o.d - TAB) / 2
notch_bottom = o.d - (notch_top + TAB)

# Calculate the space behind and in front of the notches on the bottoms of
# the dividers
notch_back = (o.h - TAB) / 2
notch_front = o.h - (notch_back + TAB)

deck_divider()
deck_bottom()
deck_back()
deck_front()

# The deck dividers (and left/right sides)
# Start with the upper-left corner and draw clockwise

