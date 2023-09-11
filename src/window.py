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

from typing import Dict, Union, List
import gi
gi.require_version('Gda', '6.0')
from gi.repository import Adw, Gio, Gtk
from .components import PasswordManagerShortcutsWindow
from .pages import WelcomePage
from .define import PROFILE, RES_PATH

@Gtk.Template(resource_path=f'{RES_PATH}/window.ui')
class PasswordManagerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PasswordManagerWindow'

    main_leaflet = Gtk.Template.Child()
    welcome = Gtk.Template.Child()
    authenticate = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()
        self._application = Gtk.Application.get_default()
        self._check_users()

    def setup(self):
        # set shortcuts window
        self.set_help_overlay(PasswordManagerShortcutsWindow())

        # Set devel style
        if PROFILE == 'Devel':
            self.add_css_class('devel')

    def _check_users(self):
        if not self._application.user_data:
            print('no has users in database')
            self.main_leaflet.set_visible_child(self.welcome)
            # self.main_leaflet.navigate(Adw.NavigationDirection.FORWARD);
        else:
            self.main_leaflet.set_visible_child(self.authenticate)
