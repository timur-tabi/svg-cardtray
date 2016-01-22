svg-cardtray is a Python program that generates laser cutter patterns for
a board game card tray.  You specify the dimensions of the cards and the
thickness of the largest deck, and it will generate a pattern in SVG
format.

This program requires the pysvg 0.2.2 module from
https://pypi.python.org/pypi/pysvg.

-------------------------------------------------------------------------------

INSTALLATION

1. In you're using Windows, install Python 2.7 from http://python.org.  The
   MSI installer is the easiest way.  You can install Python just for
   yourself, or for all users.

2. Download version pysvg from https://pypi.python.org/pypi/pysvg/0.2.2
   Only version 0.2.2 is supported, not 0.2.1 and not 0.2.2b.  In 0.2.2b,
   the capitalization of some of the pysvg modules was changed, and the
   script does not handle that.

3. Extract the zip file into a directory.  Open a Command Prompt and cd
   to that directory.  Then type in this:

	setup.py install

You should now be able to run svg-cardtray.py from a command line.

-------------------------------------------------------------------------------

USAGE

        Usage: svg-cardtray.py [options]

        Options:
          -h, --help  show this help message and exit
          -H H        card height in millimeters
          -W W        card width in millimeters
          -d D        deck thickness in millimeters
          -n N        number of decks
          -m M        material thickness in millimeters

The Height and Width are the sizes of the cards.  Round up to the nearest
millimeter, and add an extra millimeter if you want the cards to sit loosely
in the tray.

The Deck Thickness is the thickness of the largest deck.  The entire tray
will be designed to hold decks of this size.

The Number of Decks is obvious.

The Material Thickness is the thickness of the material (typically wood
or acrylic plastic) that will be cut.  Fractional values are supported, but
the number must be very accurate, otherwise the pieces may not fit together.

For the material thickness, if the value is too small (e.g. you measured
wrong or rounded down), then the tabs will not fit into the slots.  They
will need to be sanded.  The front panels will jut out a bit.

If the material thickness is too large, then the tabs will be loose in the
slots.  The front panels will be recessed (the tabs will stick out a bit).

The script will display the paths created and generate four files:
tray_back.svg, tray_bottom.svg, tray_divider.svg, and tray_front.svg.
Load these into your laser cutter's design software (verify the scale is
correct), cut, and then assemble.

Note that some extreme values will not work at the moment, so verify the
design before cutting.
