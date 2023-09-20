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
from gi.repository import Gio, Gtk, GObject
from ...define import RES_PATH
from ...application_data import Application_data as data
from ...user import User
from ...password_hasher import Argon2PasswordHasher

@Gtk.Template(resource_path=f'{RES_PATH}/pages/authentication/authentication.ui')
class AuthenticationPage(Gtk.Box):
    __gtype_name__ = 'AuthenticationPage'

    master_password = Gtk.Template.Child()
    pepper = Gtk.Template.Child()
    label_error = Gtk.Template.Child()
    auth_button = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self._application = Gtk.Application.get_default()
        self._parent = parent
        self._setup()
    
    def _setup(self):
        pepper_from_settings = self._application.settings.get_string('pepper') 
        if pepper_from_settings:
            self.pepper.set_text(pepper_from_settings)

    def _validate_data(self, task, task_data: object, cancellable: Gio.Cancellable, user_data):
        if task.return_error_if_cancelled():
            return
        user_master_password_hash = data.get().get_user_master_password(id=User.get().data.id)
        if user_master_password_hash:
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

            if Argon2PasswordHasher().verify_password(pepper=self.pepper.get_text().strip(),  password=self.master_password.get_text().strip(), hash=user_master_password_hash):
                self.label_error.set_visible(False)
                User.get().data.master_password = self.master_password.get_text().strip()
                self._parent.navigate('dashboard')
            else:
                self.label_error.set_label(_('Invalid credentials'))
                self.label_error.get_style_context().add_class('label-error')
                self.label_error.set_visible(True)

    @Gtk.Template.Callback()
    def _on_submit_user_data(self, _target):
        spinner = Gtk.Spinner.new()
        spinner.set_spinning(True)
        self.auth_button.set_sensitive(False)
        self.auth_button.set_child(spinner)
        self.label_error.get_style_context().remove_class('label-error')

        task = Gio.Task.new(self, None, self._on_verify_done, None)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._validate_data)

    def _on_verify_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        self.auth_button.set_label(_('Authentication'))
        self.auth_button.set_sensitive(True)

