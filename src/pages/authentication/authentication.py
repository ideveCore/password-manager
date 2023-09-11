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
import argon2

@Gtk.Template(resource_path=f'{RES_PATH}/pages/authentication/authentication.ui')
class AuthenticationPage(Adw.Bin):
    __gtype_name__ = 'AuthenticationPage'

    master_password = Gtk.Template.Child()
    pepper = Gtk.Template.Child()
    label_error = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._application = Gtk.Application.get_default()

    def _validate_data(self):
        argon2_type = argon2.Type.ID
        time_cost = 10
        memory_cost = 97656
        parallelism = 5
        output_len = 64
        ph = argon2.PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=output_len,
            type=argon2_type
        )
        if not self.master_password.get_text().strip():
            self.master_password.get_style_context().add_class('error')
            return False
        else:
            self.master_password.get_style_context().remove_class('error')
        if not self.pepper.get_text().strip():
            self.pepper.get_style_context().add_class('error')
            return False
        else:
            self.pepper.get_style_context().remove_class('error')

        try:
            middle = len(self.pepper.get_text().strip()) // 2
            passwd = f'{self.pepper.get_text().strip()[:middle]}{self.master_password.get_text().strip()}{self.pepper.get_text().strip()[middle:]}'
            print(ph.verify(self._application.user_data[0].master_password, passwd))
            self.label_error.set_visible(False)
        except Exception as error:
            self.label_error.set_label(_('Invalid credentials'))
            self.label_error.set_visible(True)

    @Gtk.Template.Callback()
    def _on_submit_user_data(self, _target):
        self._validate_data()
