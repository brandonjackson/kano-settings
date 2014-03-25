#!/usr/bin/env python

# top_bar.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# This controls the styling of the (pretend) top window bar.

from gi.repository import Gtk, Pango
import kano_settings.components.icons as icons

TOP_BAR_HEIGHT = 44
SPACE_TAKEN = 220
HEADER_SPACE = 25


class Top_bar():
    def __init__(self, WINDOW_WIDTH):

        # Makes it easier to centre other widgets even if we change this
        self.height = TOP_BAR_HEIGHT

        # This is to give the correct colour of the top bar as Event Boxes are the only containers that we can colour
        # This contains everything, but can't pack directly into as is only a simple container
        self.background = Gtk.EventBox()
        self.background.set_size_request(WINDOW_WIDTH, TOP_BAR_HEIGHT)
        self.background.style = self.background.get_style_context()
        self.background.style.add_class('top_bar_container')

        # Main title of the window bar.
        self.header = Gtk.Label("Kano Settings")
        #self.header.props.halign = Gtk.Align.CENTER
        self.header.modify_font(Pango.FontDescription("Bariol 13"))
        self.header.get_style_context().add_class("header")

        self.align_header = Gtk.Alignment(xalign=1, yalign=0, xscale=0, yscale=0)
        self.align_header.add(self.header)
        # space of buttons and header text takes up about 220
        # so we have WINDOW_WIDTH - 220 of space to play with
        # move header 50 to the left
        padding_left = (WINDOW_WIDTH - SPACE_TAKEN) / 2 - HEADER_SPACE
        padding_right = (WINDOW_WIDTH - SPACE_TAKEN) / 2 + HEADER_SPACE
        self.align_header.set_padding(13, 0, padding_left, padding_right)

        # Icons of the buttons
        self.pale_prev_arrow = Gtk.Image()
        self.pale_prev_arrow.set_from_pixbuf(icons.Icons("pale_left_arrow").subpixbuf)
        self.pale_next_arrow = Gtk.Image()
        self.pale_next_arrow.set_from_pixbuf(icons.Icons("pale_right_arrow").subpixbuf)
        self.dark_prev_arrow = Gtk.Image()
        self.dark_prev_arrow.set_from_pixbuf(icons.Icons("dark_left_arrow").subpixbuf)
        self.dark_next_arrow = Gtk.Image()
        self.dark_next_arrow.set_from_pixbuf(icons.Icons("dark_right_arrow").subpixbuf)
        self.cross = Gtk.Image()
        self.cross.set_from_pixbuf(icons.Icons("cross").subpixbuf)

        # Prev Button
        self.prev_button = Gtk.Button()
        #self.prev_button.set_image(self.prev_arrow)
        self.prev_button.set_size_request(TOP_BAR_HEIGHT, TOP_BAR_HEIGHT)
        self.prev_button.set_can_focus(False)

        # Next button
        self.next_button = Gtk.Button()
        #self.next_button.set_image(self.next_arrow)
        self.next_button.set_size_request(TOP_BAR_HEIGHT, TOP_BAR_HEIGHT)
        self.next_button.set_can_focus(False)

        # Close button
        self.close_button = Gtk.Button()
        self.close_button.set_image(self.cross)
        self.close_button.set_size_request(TOP_BAR_HEIGHT, TOP_BAR_HEIGHT)
        self.close_button.set_can_focus(False)

        """        # Container of all the elements
        self.container = Gtk.Box()
        self.container.set_homogeneous(False)
        self.container.add(self.prev_button)
        self.container.pack_start(self.next_button, False, False, 0)
        self.container.pack_start(self.align_header, True, True, 0)
        self.container.pack_end(self.close_button, False, False, 0)
        self.background.add(self.container)"""

        self.container = Gtk.Grid()
        self.container.attach(self.prev_button, 0, 0, 1, 1)
        self.container.attach(self.next_button, 1, 0, 1, 1)
        self.container.attach(self.align_header, 2, 0, 1, 1)
        self.container.attach(self.close_button, 3, 0, 1, 1)
        self.container.set_size_request(WINDOW_WIDTH, 44)

        self.background.add(self.container)