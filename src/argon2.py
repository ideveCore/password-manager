# argon2.py
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
import secrets
from typing import Union
import argon2

class Argon2:

    instance: Union[Argon2, None] = None
    ph = None

    @staticmethod
    def new() -> Argon2:
        instance = Argon2()
        instance._setup()
        return instance

    @staticmethod
    def get() -> Argon2:
        if not Argon2.instance:
            Argon2.instance = Argon2.new()
        return Argon2.instance

    @staticmethod
    def hash_password(pepper, password) -> Union[str, None]:
        if pepper and password:
            middle = len(pepper) // 2
            passwd = f'{pepper[:middle]}{password}{pepper[middle:]}'
            if Argon2.ph:
                hash = Argon2.ph.hash(passwd, salt=Argon2.generate_salt().encode('utf-8'))
                return hash

    @staticmethod
    def verify_password(pepper: str, password_hash: str, password: str) -> bool:
        try:
            middle = len(pepper) // 2
            passwd = f'{pepper[:middle]}{password}{pepper[middle:]}'
            if Argon2.ph:
                Argon2.ph.verify(password_hash, passwd)
            else:
                return False
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def generate_salt() -> str:
        salt = secrets.token_bytes(8)
        return salt.hex()

    @staticmethod
    def _setup():
        Argon2.ph = argon2.PasswordHasher(
            time_cost=20,
            memory_cost=131072,
            parallelism=2,
            hash_len=64,
            type=argon2.Type.ID
        )

