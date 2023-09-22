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

    # container_page = Gtk.Template.Child()
    navigation_view = Gtk.Template.Child()
    welcome_page = Gtk.Template.Child()
    authentication_page = Gtk.Template.Child()
    dashboard_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()
        self._application = Gtk.Application.get_default()
        self.__set_pages()
        self.navigation_view.push(self.dashboard_page)
        # self._check_users()

    def __set_pages(self):
        self.welcome_page.set_child(WelcomePage(self))
        self.authentication_page.set_child(AuthenticationPage(self))
        self.dashboard_page.set_child(DashboardPage(self))

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
            self.navigation_view.push(self.authentication_page)
        elif to == 'welcome':
            self.navigation_view.push(self.welcome_page)
        elif to == 'dashboard':
            # window = DashboardPage(self)
            self.navigation_view.push(self.dashboard_page)
            # self.pages.set_child(window)
            # window.verify_user()

