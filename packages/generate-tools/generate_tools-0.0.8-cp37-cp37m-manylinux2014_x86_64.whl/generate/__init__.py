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


__version__ = "0.0.8"
__license__ = "GNU Affero General Public License v3.0 (AGPL-3.0)"
__copyright__ = "Copyright (C) 2022-present AyiinXd <https://github.com/AyiinXd>"


from .generate import Generate
from .storage import Storage


print(f'\nGenerateTools v{__version__}\n{__license__}\n{__copyright__}\n\n')
