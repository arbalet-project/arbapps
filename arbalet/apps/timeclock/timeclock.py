#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Time clock - simple time clock demonstrator.

    Copyright 2015 Joseph Silvestre, Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""

from arbalet.core import Application, Rate
import datetime


class TimeClockApp(Application):
    def __init__(self, parser):

        Application.__init__(self, parser)

        self.CHAR_COLORS = self.args.type
        self.BG_COLOR = 'black'

    def run(self):

        # Update the screen every second.
        rate = Rate(1.0)

        tick_second = False

        while True:
            with self.model:
                # Get the current time.
                now = datetime.datetime.today()
                hour = now.hour
                minute = now.minute

                # Extract the digits of each number in order to draw them
                # separately.
                hour_digits = self.extract_digits(hour)
                minute_digits = self.extract_digits(minute)

                # Display digits on the screen.
                self.draw_row(0, hour_digits)
                self.draw_row(1, minute_digits)

                # Flash the separator every two seconds.
                self.flash_separator(tick_second)
            tick_second = not tick_second

            rate.sleep()


    def draw_row(self, rowNum, digits):
        """
        Draw a row of digits. A row is composed of two digits.
        """

        # Some half-harcoded value to handle positionning and margins.
        digitCoordinates = [
            [1, rowNum * 5 + rowNum * 3 + 1],
            [6, rowNum * 5 + rowNum * 3 + 1]
        ]

        self.draw_number(digits[0],
            digitCoordinates[0][0], digitCoordinates[0][1], self.CHAR_COLORS)
        self.draw_number(digits[1],
            digitCoordinates[1][0], digitCoordinates[1][1], self.CHAR_COLORS)


    def draw_number(self, digit, baseX, baseY, color):
        """
        Draw a digit in a specific color.
        A digit has a 3 pixels width and a 5 pixels height.
        Base coordinates represents the top-left pixel.
        A digit matrix is like a mask, falsy value means nothing is drawn,
        truthy value means a pixel will be drawn.
        """
        digitMatrix = self.matrixes[digit]

        for w in range(3):
            for h in range(5):
                x = baseX + w
                y = baseY + h
                if digitMatrix[h][w]:
                    # Color pixel if the mask allows it.
                    self.model.set_pixel(y, x, color)
                else:
                    # Reset color if it was not BG_COLOR.
                    self.model.set_pixel(y, x, self.BG_COLOR)


    def flash_separator(self, tick_second):
        """
        Display (or not) the separator based on flag.
        """
        if tick_second:
            self.draw_separator(self.CHAR_COLORS)
        else:
            self.draw_separator(self.BG_COLOR)


    def draw_separator(self, color):
        """
        A separator is simply two colored pixels.
        """
        self.model.set_pixel(7, 4, color)
        self.model.set_pixel(7, 5, color)


    def extract_digits(self, number):
        """
        Extract digits from a number. Only works for number < 100
        """
        if number < 10:
            return [0, number]
        else:
            extracted = str(number)
            return [int(extracted[0]), int(extracted[1])]
    
    # Matrix of matrixes. Each matrix represents a digit.
    matrixes = [
        # Represent a 0.
        [
            [True, True, True],
            [True, False, True],
            [True, False, True],
            [True, False, True],
            [True, True, True]
        ],

        # Represent a 1.
        [
            [False, False, True],
            [False, True, True],
            [False, False, True],
            [False, False, True],
            [False, False, True]
        ],

        # Represent a 2.
        [
            [True, True, True],
            [False, False, True],
            [True, True, True],
            [True, False, False],
            [True, True, True]
        ],

        # Represent a 3.
        [
            [True, True, True],
            [False, False, True],
            [True, True, True],
            [False, False, True],
            [True, True, True]
        ],

        # Represent a 4.
        [
            [True, False, False],
            [True, False, False],
            [True, False, True],
            [True, True, True],
            [False, False, True]
        ],

        # Represent a 5.
        [
            [True, True, True],
            [True, False, False],
            [True, True, True],
            [False, False, True],
            [True, True, True]
        ],

        # Represent a 6.
        [
            [True, True, True],
            [True, False, False],
            [True, True, True],
            [True, False, True],
            [True, True, True]
        ],

        # Represent a 7.
        [
            [True, True, True],
            [False, False, True],
            [False, False, True],
            [False, False, True],
            [False, False, True]
        ],

        # Represent a 8.
        [
            [True, True, True],
            [True, False, True],
            [True, True, True],
            [True, False, True],
            [True, True, True]
        ],

        # Represent a 9.
        [
            [True, True, True],
            [True, False, True],
            [True, True, True],
            [False, False, True],
            [True, True, True]
        ]
    ]

