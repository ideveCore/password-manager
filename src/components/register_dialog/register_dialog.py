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
from __future__ import annotations
import math, time, secrets
from gi.repository import Adw, Gio, GLib, Gtk
from ...db import Union, User_db_item
from ...application_data import Application_data as data
from ...argon2 import Argon2
from ...user import User
from ...define import RES_PATH

@Gtk.Template(resource_path=f'{RES_PATH}/components/register_dialog/register_dialog.ui')
class RegisterDialog(Adw.Window):

    __gtype_name__ = 'RegisterDialog'
    instance: Union[RegisterDialog, None] = None
    avatar = Gtk.Template.Child()
    first_name = Gtk.Template.Child()
    last_name = Gtk.Template.Child()
    username = Gtk.Template.Child()
    email = Gtk.Template.Child()
    master_password = Gtk.Template.Child()
    repeat_master_password = Gtk.Template.Child()
    tip = Gtk.Template.Child()
    first_name_label = Gtk.Template.Child()
    last_name_label = Gtk.Template.Child()
    bar_passwd = Gtk.Template.Child()
    pepper = Gtk.Template.Child()
    send = Gtk.Template.Child()

    def __init__(self, parent: Adw.ApplicationWindow, *args):
        super().__init__(*args)
        self._application = Gtk.Application.get_default()
        self._parent = parent
        self.set_transient_for(self._application.get_active_window())
        self.bar_passwd.add_offset_value("very-weak", 1)
        self.bar_passwd.add_offset_value("weak", 2)
        self.bar_passwd.add_offset_value("moderate", 4)
        self.bar_passwd.add_offset_value("strong", 6)
        self.pepper.set_text(Argon2.get().generate_salt())
        self._setup_actions()

    def _setup_actions(self):
        group = Gio.SimpleActionGroup()
        helper_action = Gio.SimpleAction(name='helper', parameter_type=GLib.VariantType('s'))
        helper_action.connect('activate', self._helper_action)
        group.add_action(helper_action)
        self.insert_action_group('register', group)

    def _helper_action(self, _action, _parameter):
        dialog = Adw.MessageDialog.new()
        dialog.set_transient_for(self)
        dialog.add_response('ok', _('Ok'))
        dialog.set_response_appearance('ok', Adw.ResponseAppearance.SUGGESTED);
        dialog.connect('response', lambda self, _dialog: dialog.close())

        if GLib.Variant.get_string(_parameter) == 'pepper':
            dialog.set_heading(_('Peppers?'))
            dialog.set_body(_("""A pepper is a random sequence or value kept secret by the user. 
The pepper is a unique value that is not stored in the database only in the application session and cannot be changed, if the pepper is lost it is not possible to recover the data.
The main purpose of a pepper is to add an extra layer of security to password storage."""))
        elif GLib.Variant.get_string(_parameter) == 'master_password':
            dialog.set_heading(_('Master password?'))
            dialog.set_body(_("""A master password if often to protect an application or serving of password manager"""))

        dialog.present()

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
        if not '@' in self.email.get_text().strip():
            self.email.get_style_context().add_class('error')
            return False
        else:
            self.email.get_style_context().remove_class('error')
        if not self.master_password.get_text().strip():
            self.master_password.get_style_context().add_class('error')
            return False
        else:
            self.master_password.get_style_context().remove_class('error')
        if not self.repeat_master_password.get_text().strip() or not self.repeat_master_password.get_text().strip() == self.master_password.get_text().strip():
            self.repeat_master_password.get_style_context().add_class('error')
            return False
        else:
            self.repeat_master_password.get_style_context().remove_class('error')

        if not self.tip.get_text().strip():
            self.tip.get_style_context().add_class('error')
            return False
        else:
            self.tip.get_style_context().remove_class('error')

        return True

    @Gtk.Template.Callback()
    def _on_submit_user_data(self, _target):
        spinner = Gtk.Spinner.new()
        spinner.set_spinning(True)
        self.send.set_sensitive(False)
        self.send.set_child(spinner)

        if self._validate_user_data():
            self._credentials = f'First name = {self.first_name.get_text().strip()}\nLast name = {self.last_name.get_text().strip()}\nUsername = {self.username.get_text().strip()}\nEmail = {self.email.get_text().strip()}\nPepper = {self.pepper.get_text().strip()}\nMaster password = {self.master_password.get_text().strip()}\nMaster password tip = {self.tip.get_text().strip()}'
            dialog_save_credentials = Adw.MessageDialog.new()
            dialog_save_credentials.set_heading(_('Save credentials'))
            dialog_save_credentials.set_transient_for(self)
            dialog_save_credentials.set_body(_("You must keep these credentials in a safe place and keep at least two copies of them. If you lose these credentials, you won't be able to recover your data."))
            dialog_save_credentials.add_response('save_credentials', _('Save credentials'))
            dialog_save_credentials.set_response_appearance('save_credentials', Adw.ResponseAppearance.SUGGESTED);
            dialog_save_credentials.connect('response', self._on_dialog_save_credentials_response)
            dialog_save_credentials.present()
        else:
            self.send.set_label(_('Register'))
            self.send.set_sensitive(True)

    def _on_dialog_save_credentials_response(self, _dialog, _id):
        if _id == 'save_credentials':
            self._save_file_dialog()

    @Gtk.Template.Callback()
    def _on_update_pepper(self, _target):
        self.pepper.set_text(Argon2.get().generate_salt())

    def _save_file_dialog(self):
        self._dialog = Gtk.FileDialog.new()
        self._dialog.set_title('Save credentials')
        self._dialog.set_initial_name('passwdman-credentials.txt')
        cancellable = Gio.Cancellable.new()
        self._dialog.save(self, cancellable, self._save_file_response)
   
    def _save_file_response(self, _dialog, _task):
        try:
            destination_file = _dialog.save_finish(_task)
            destination_file.replace_contents_async(self._credentials.encode('utf-8'), None, False, Gio.FileCreateFlags.REPLACE_DESTINATION, None, self._on_saved_credentials)
        except Exception as error:
            self.send.set_label(_('Register'))
            self.send.set_sensitive(True)

    def _on_saved_credentials(self, _file, _task):
        result = _file.replace_contents_finish(_task)
        if result:
            hash = Argon2.get().hash_password(pepper=self.pepper.get_text().strip(), password=self.master_password.get_text().strip())
            user = User_db_item(
                id=None,
                first_name=self.first_name.get_text().strip(),
                last_name=self.last_name.get_text().strip(),
                username=self.username.get_text().strip(),
                email=self.email.get_text().strip(),
                master_password=hash,
                master_password_tip=self.tip.get_text().strip(),
                timestamp=int(time.time()),
            )

            User.get().data = data.get().save_user(user)
            self._application.settings.set_string('pepper', self.pepper.get_text().strip())
            User.get().data.master_password = self.master_password.get_text().strip()
            self._parent.navigate('dashboard')
            self.close()
        else:
            print('Erro in save file')

        self.send.set_label(_('Register'))
        self.send.set_sensitive(True)

