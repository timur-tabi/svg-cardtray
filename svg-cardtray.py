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
    turtle.forward(width);
    turtle.right(90)
    turtle.forward(height);
    turtle.right(90)
    turtle.forward(width);
    turtle.left(90)

# A notch (rectangle with only three sides) starting from (x,y)
def notchr(turtle, width, height):
    turtle.right(90)
    turtle.forward(width);
    turtle.left(90)
    turtle.forward(height);
    turtle.left(90)
    turtle.forward(width);
    turtle.right(90)

def deck_divider():
    global o, a, vspace

    WIDTH = 2 * o.m + o.h
    HEIGHT = o.n * o.d

    svg = pysvg.structure.svg(width='%smm' % WIDTH, height='%smm' % HEIGHT)
    svg.set_viewBox('0 0 %s %s' % (WIDTH, HEIGHT))

    s = Turtle(stroke='blue', strokeWidth=str(HAIRLINE))
    s.moveTo(Vector(o.m, 0))
    s.penDown()

    # (0, 0) is the upper-left corner
    # Fixme: since we need notches on the bottom, we can't share the
    # edges
    s.forward(o.h)
    s.right(90)

    # For N decks, we need N+1 dividers
    for i in range(0, o.n + 1):
        # Fixme: one notch only, and it must be the same position as the
        # front and back notch holes
        s.forward(vspace)
        notchl(s, o.m, TAB)
        if tabs > 1:
            s.forward(vspace)
            notchl(s, o.m, TAB)
        s.forward(vspace)

        # Fixme: needs notches for the bottom
        s.right(90)
        s.forward(o.h)

        s.right(90)
        s.forward(vspace)
        notchl(s, o.m, TAB)
        if tabs > 1:
            s.forward(vspace)
            notchl(s, o.m, TAB)
        s.forward(vspace)

        # Fixme: since we need notches on the bottom, we can't share the
        # edges
        s.penUp()
        s.moveTo(s.getPosition() + Vector(o.h, o.d))
        s.setOrientation(Vector(0, 1))  # down
        s.penDown()

    s.finish()
    print s.getXML()
    s=s.addTurtlePathToSVG(svg)

    print 'Dividers size: %smm * %smm' % (WIDTH, HEIGHT)
    svg.save('/Users/timur/Windows Share/LaserCutter/tray_divider.svg')

def deck_bottom():
    global o, a

    WIDTH = (o.n + 1) * o.m + (o.n * o.w)
    HEIGHT = (2 * o.m) + o.h
    svg = pysvg.structure.svg(width='%smm' % WIDTH, height='%smm' % HEIGHT)
    svg.set_viewBox('0 0 %s %s' % (WIDTH, HEIGHT))

    # The Y-position of the divider notch holes
    notch_y = o.m + (o.h - TAB) / 2

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
    s.forward(notch_y)
    notchr(s, o.m, TAB)
    s.moveTo(Vector(WIDTH, HEIGHT))
    s.right(90)

    #       _____________
    #      |             |
    #    __|             |__
    # __|                   |__
    width = o.w - (2 * 5.0)     # finger notch width
    for i in range(0, o.n):
        s.forward(o.m)
        s.right(90)
        s.forward(o.m)
        s.left(90)
        s.forward(5)

        notchr(s, 10, width)

        s.forward(5)
        s.left(90)
        s.forward(o.m)
        s.right(90)
    s.forward(o.m)
    s.right(90)

    # Left side
    # Right side
    s.penUp()
    s.moveTo(Vector(0, 0))
    s.setOrientation(Vector(0, 1))  # down
    s.penDown()
    s.forward(notch_y)
    notchl(s, o.m, TAB)
    s.moveTo(Vector(0, HEIGHT))

    # Notch holes for dividers
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

    print 'Bottom size: %smm * %smm' % (WIDTH, HEIGHT)
    svg.save('/Users/timur/Windows Share/LaserCutter/tray_bottom.svg')

# Fixme: combine this with the bottom piece
def deck_back():
    global o, a, vspace

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
    s.forward(vspace)
    notchr(s, o.m, TAB)
    if tabs > 1:
        s.forward(vspace)
        notchr(s, o.m, TAB)
    s.forward(vspace)
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
    s.forward(vspace)
    notchr(s, o.m, TAB)
    if tabs > 1:
        s.forward(vspace)
        notchr(s, o.m, TAB)
    s.forward(vspace)

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
    svg.save('/Users/timur/Windows Share/LaserCutter/tray_back.svg')

def deck_front():
    global o, a
    global vspace, tabs

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

    # Fixme: one notch only, and it must be the same position as the
    # front and back notch holes
    s.forward(vspace)
    notchr(s, o.m, TAB)
    if tabs > 1:
        s.forward(vspace)
        notchr(s, o.m, TAB)
    s.forward(vspace)

    s.penUp()
    s.moveTo(Vector(o.m + 5, 0))    # Fixme: '5' should be a variable
    s.setOrientation(Vector(1, 0))
    s.penDown()

    # fixme: needs notch holes inside front panels
    for i in range(0, o.n - 1):
        s.forward(2 * 5 + o.m)    # Fixme: '5' should be a variable
        s.right(90)
        s.forward(o.d + o.m)
        s.right(90)
        s.forward(5)    # Fixme: '5' should be a variable
        notchr(s, o.m, o.m)
        s.forward(5)

        s.penUp()
        s.moveTo(s.getPosition() + Vector(2 * 5 + o.m, -(o.d + o.m)))    # Fixme: '5' should be a variable
        s.setOrientation(Vector(1, 0))
        s.penDown()

    # Right piece
    s.forward(o.m + 5)    # Fixme: '5' should be a variable
    s.right(90)

    # Fixme: one notch only, and it must be the same position as the
    # front and back notch holes
    s.forward(vspace)
    notchr(s, o.m, TAB)
    if tabs > 1:
        s.forward(vspace)
        notchr(s, o.m, TAB)
    s.forward(vspace)

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
    svg.save('/Users/timur/Windows Share/LaserCutter/tray_front.svg')

parser = OptionParser(usage="usage: %prog [options]")
parser.add_option("-H", dest="h", help="card height", type="float", default = 50)
parser.add_option("-W", dest="w", help="card width", type="float", default = 30)
parser.add_option("-d", dest="d", help="deck thickness", type="float", default = 30)
parser.add_option("-n", dest="n", help="number of decks", type="int", default = 4)
parser.add_option("-m", dest="m", help="material thickness (default=%default)", type="int", default = 3)

(o, a) = parser.parse_args()

# Calculate the number of tabs.  Fixme: this should be smarter
if o.d < 20:
    o.d = 20

if o.d < 50:
    tabs = 1
else:
    tabs = 2

# The space between vertical tabs
vspace = (o.d - (TAB * tabs)) / (1.0 + tabs)

deck_divider()
deck_bottom()
deck_back()
deck_front()

# The deck dividers (and left/right sides)
# Start with the upper-left corner and draw clockwise

