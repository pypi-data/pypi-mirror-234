# Copyright (C) 2022-2023 AyiinXd <https://github.com/AyiinXd>

# This file is part of GeneratorPassword.

# GeneratorPassword is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GeneratorPassword is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with GeneratorPassword.  If not, see <http://www.gnu.org/licenses/>.

import string

from random import choice
from typing import Union

import generate
from generate.exception import AuthorizedNeeded, LengthNeeded


class Password:
    def generate_password(
        self: 'generate.Generate',
        user_id: int,
        name: str = None,
        length: Union[int, str] = None
    ):
        if not self.is_authorize:
            raise AuthorizedNeeded()
        if not length:
            raise LengthNeeded()
        if name:
            self._name = name + self._space
        else:
            self._name = self.name[:2] + self._space
        passwd = self._name.upper() + ''.join(choice(self._string) for _ in range(int(length)))
        random_id = ''.join(choice(string.digits) for _ in range(8))
        try:
            result = self.solved('password', user_id)
            if result:
                self.update(objec='password key random_id', data=(passwd, random_id, user_id))
        except KeyError:
            self.insert(objec='password user_id key random_id', data=(user_id, passwd, random_id))
        return passwd
