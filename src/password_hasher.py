# password_hasher.py
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
from typing import Union
import secrets, argon2

class GenerateSalt:
    def __init__(self, base) -> None:
        self.base = base
        self.salt = self.__generate()

    def __generate(self) -> str:
        return secrets.token_bytes(self.base).hex()

    def encode(self) -> bytes:
        return self.salt.encode('utf-8')


class Error(ValueError):
    def __init__(self, message) -> None:
        super().__init__(message)

class PasswordHasherStartegy:
    def hash_password(self, pepper: str, password: str) -> Union[str, None]:
        pass

    def verify_password(self, pepper: str, password: str) -> Union[bool, None]:
        pass


class Argon2PasswordHasher(PasswordHasherStartegy):
    def __init__(self) -> None:
        super().__init__()
        self.__password_hasher = argon2.PasswordHasher(
            time_cost=70,
            memory_cost=131072,
            parallelism=2,
            hash_len=64,
            type=argon2.Type.ID
        )
    def hash_password(self, pepper: str, password: str) -> Union[str, Error]:
        if pepper and password:
            middle = len(pepper) // 2
            passwd = f'{pepper[:middle]}{password}{pepper[middle:]}'
            return self.__password_hasher.hash(passwd, salt=GenerateSalt(8).encode())
        else:
            raise ValueError('Pepper or Password is invalid')

    def verify_password(self, pepper: str, password: str, hash: str) -> Union[bool, Error]:
        try:
            middle = len(pepper) // 2
            passwd = f'{pepper[:middle]}{password}{pepper[middle:]}'
            self.__password_hasher.verify(hash, passwd)
            return True
        except Exception as error:
            raise Error(error)

