# welcome.py
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
from __future__ import annotations
from typing import Optional, Union, Any, Dict, List
from gi.repository import Adw, Gio, Gtk
from ...components import RegisterDialog
from ...define import RES_PATH

@Gtk.Template(resource_path=f'{RES_PATH}/pages/welcome/welcome.ui')
class WelcomePage(Adw.Bin):
    __gtype_name__ = 'WelcomePage'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_actions()

    def _setup_actions(self) -> None:
        group = Gio.SimpleActionGroup.new()
        open_register_dialog_action = Gio.SimpleAction(
            name='open-register-dialog'
        )

        open_register_dialog_action.connect('activate', self._open_regiter_dialog)

        group.add_action(open_register_dialog_action)
        self.insert_action_group('welcome', group)

    def _open_regiter_dialog(self, action, parameter):
        dialog = RegisterDialog()
        dialog.present()
