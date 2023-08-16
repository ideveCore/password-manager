# window.py
#
# Copyright 2023 Ideve Core
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import gi
gi.require_version('Gda', '6.0') 
from gi.repository import Adw, Gda, Gtk
from .components import PasswordManagerShortcutsWindow
from .define import PROFILE

@Gtk.Template(resource_path='/io/github/idevecore/PasswordManager/window.ui')
class PasswordManagerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PasswordManagerWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

    def setup(self):
        # set shortcuts window
        self.set_help_overlay(PasswordManagerShortcutsWindow())

        # Set devel style
        if PROFILE == 'Devel':
            self.add_css_class('devel')
