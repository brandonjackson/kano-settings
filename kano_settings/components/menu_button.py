#!/usr/bin/env python

# menu_button.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# This controls the button styling in the default introduction screen which shows all the settings

from gi.repository import Gtk, Pango
import kano_settings.constants as constants


class Menu_button():
    def __init__(self, name, description=''):

        # Contains the info about the level and the image
        self.container = Gtk.Grid()

        # Info about the different settings
        self.title = Gtk.Label(name)
        self.title.get_style_context().add_class("intro_label")
        self.title.set_alignment(xalign=0, yalign=0.8)

        #info = config_file.read_from_file(custom_info[x])

        # Replace some of the info displayed with whitespace so it fits
        if description:
            if len(description) >= 12:
                description = description[0:12] + '...'

        self.description = Gtk.Label(description)
        self.description.modify_font(Pango.FontDescription("Bariol 13"))
        self.description.get_style_context().add_class("custom_label")
        self.description.set_size_request(120, 10)
        self.description.set_alignment(xalign=0, yalign=0.2)

        self.button = Gtk.Button()
        self.button.set_can_focus(False)
        self.img = Gtk.Image()
        self.img.set_from_file(constants.media + "/Icons/Icon-" + name + ".png")

        self.container.attach(self.title, 2, 0, 1, 1)
        self.container.attach(self.description, 2, 1, 1, 1)
        self.container.attach(self.img, 0, 0, 2, 2)
        self.container.set_row_spacing(5)
        self.container.set_column_spacing(10)
        self.container.props.valign = Gtk.Align.CENTER

        self.button.add(self.container)
        self.button.set_size_request(200, 100)

        self.button.height = 100
        self.button.width = 200