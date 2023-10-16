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


class AuthorizedNeeded(Exception):
    def __init__(self):
        super().__init__(
            '[ Generator Need Authorized ] - Generator Client is not Authorized'
        )

class IsAuthorized(Exception):
    def __init__(self):
        super().__init__(
            '[ Generator Authorized ] - Generator Client has been Authorized'
        )

class LengthNeeded(Exception):
    """Needed to unmute the userbot, raised by
    :meth:`~pycover.pycover.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Needed arguments length',
        )


class ModuleNotFound(ImportWarning):
    def __init__(self, error: str):
        super().__init__(
            f'[ IMPORT WARNING ] - Install module ( {error} ) for running this command'
        )

class PeerIdInvalid(Exception):
    def __init__(self, ids: int):
        super().__init__(
            f'[ PeerIdInvalid ] - ID Not Found ( {ids} ) Maybe you dont adding user to memory'
        )
