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
import math
from gi.repository import Adw, Gtk
from ...define import RES_PATH

@Gtk.Template(resource_path=f'{RES_PATH}/components/register_dialog/register_dialog.ui')
class RegisterDialog(Adw.Window):
    __gtype_name__ = 'RegisterDialog'

    avatar = Gtk.Template.Child()
    first_name = Gtk.Template.Child()
    last_name = Gtk.Template.Child()
    first_name_label = Gtk.Template.Child()
    last_name_label = Gtk.Template.Child()
    bar_passwd = Gtk.Template.Child()


    def __init__(self):
        super().__init__()
        self._application = Gtk.Application.get_default()
        self.set_transient_for(self._application.get_active_window())
        self.bar_passwd.add_offset_value("very-weak", 1);
        self.bar_passwd.add_offset_value("weak", 2);
        self.bar_passwd.add_offset_value("moderate", 4);
        self.bar_passwd.add_offset_value("strong", 6);

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

