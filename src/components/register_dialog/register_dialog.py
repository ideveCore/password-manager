# register.py
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
import math, time, secrets
from gi.repository import Adw, Gtk
import pwvalid, binascii
import argon2
from ...define import RES_PATH

@Gtk.Template(resource_path=f'{RES_PATH}/components/register_dialog/register_dialog.ui')
class RegisterDialog(Adw.Window):
    __gtype_name__ = 'RegisterDialog'

    avatar = Gtk.Template.Child()
    first_name = Gtk.Template.Child()
    last_name = Gtk.Template.Child()
    username = Gtk.Template.Child()
    email = Gtk.Template.Child()
    master_password = Gtk.Template.Child()
    tip = Gtk.Template.Child()
    first_name_label = Gtk.Template.Child()
    last_name_label = Gtk.Template.Child()
    bar_passwd = Gtk.Template.Child()
    pepper = Gtk.Template.Child()


    def __init__(self):
        super().__init__()
        self._application = Gtk.Application.get_default()
        self.set_transient_for(self._application.get_active_window())
        self.bar_passwd.add_offset_value("very-weak", 1);
        self.bar_passwd.add_offset_value("weak", 2);
        self.bar_passwd.add_offset_value("moderate", 4);
        self.bar_passwd.add_offset_value("strong", 6);
        self.pepper.set_text(self._generate_pepper())

    @Gtk.Template.Callback()
    def _on_first_name_changed(self, _target):
        self.avatar.set_text(f'{self.first_name.get_text().strip()} {self.last_name.get_text().strip()}')
        self.first_name_label.set_label(self.first_name.get_text().strip())
    
    @Gtk.Template.Callback()
    def _on_last_name_changed(self, _target):
        self.avatar.set_text(f'{self.first_name.get_text().strip()} {self.last_name.get_text().strip()}')
        self.last_name_label.set_label(f' {self.last_name.get_text().strip()}')

    @Gtk.Template.Callback()
    def _on_passwd_changed(self, _target):
        level = min(math.ceil(len(_target.get_text()) / 5), 20)
        print(level)
        self.bar_passwd.set_value(math.floor(level));

    def _validate_user_data(self):
        if not self.first_name.get_text().strip():
            self.first_name.get_style_context().add_class('error')
            return False
        else:
            self.first_name.get_style_context().remove_class('error')
        if not self.last_name.get_text().strip():
            self.last_name.get_style_context().add_class('error')
            return False
        else:
            self.last_name.get_style_context().remove_class('error')
        if not self.username.get_text().strip():
            self.username.get_style_context().add_class('error')
            return False
        else:
            self.username.get_style_context().remove_class('error')
        try:
            if not pwvalid.isDeliverable(self.email.get_text().strip()):
                self.email.get_style_context().add_class('error')
                return False
            else:
                self.email.get_style_context().remove_class('error')
        except Exception as error:
            self.email.get_style_context().add_class('error')
            return False

        if not self.master_password.get_text().strip():
            self.master_password.get_style_context().add_class('error')
            return False
        else:
            self.master_password.get_style_context().remove_class('error')
        if not self.tip.get_text().strip():
            self.tip.get_style_context().add_class('error')
            return False
        else:
            self.tip.get_style_context().remove_class('error')

        return True

    @Gtk.Template.Callback()
    def _on_submit_user_data(self, _target):
        # if self._validate_user_data():
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
        salt = self.pepper.get_text().encode("utf-8")
        hash = ph.hash(self.master_password.get_text(), salt=salt)
        #$argon2id$v=19$m=65536,t=3,p=4$AQIDBAUGBwg$rovfC3g5qNs6Zzy0Q2oiX9sQrM+I92h0UQXFek8uFEs
        print(hash)
        # pepper = secrets.token_bytes(4)
        # pepper_hex = pepper.hex()
        # print(pepper_hex)
        # print(int(time.time() * 1000))

    @Gtk.Template.Callback()
    def _on_update_pepper(self, _target):
        self.pepper.set_text(self._generate_pepper())

    def _generate_pepper(self):
        pepper = secrets.token_bytes(8)
        return pepper.hex()

