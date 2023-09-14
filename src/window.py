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
from gi.repository import Adw, Gtk
from .components import PasswordManagerShortcutsWindow
from .pages import AuthenticationPage, WelcomePage, DashboardPage
from .define import PROFILE, RES_PATH
from .user import User

@Gtk.Template(resource_path=f'{RES_PATH}/window.ui')
class PasswordManagerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PasswordManagerWindow'

    container_page = Gtk.Template.Child()
    pages = Gtk.Template.Child()

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
        if not User.get().data:
            print('no has users in database')
            self.navigate('welcome')
        else:
            self.navigate('authentication')

    def navigate(self, to: str) -> None:
        if to == 'authentication':
            self.pages.set_child(AuthenticationPage(self))
        elif to == 'welcome':
            self.pages.set_child(WelcomePage(self))
        elif to == 'dashboard':
            window = DashboardPage(self)
            self.pages.set_child(window)
            window.verify_user()

