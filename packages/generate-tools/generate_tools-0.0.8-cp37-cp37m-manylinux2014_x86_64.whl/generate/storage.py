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

import logging
import sqlite3

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, name: str, extension: str, table: str):
        self.name = name
        self.extension = extension
        self.table = table
        self.conn: sqlite3.Connection = None
        self.is_connected: bool = False

    def connect(self):
        conn = sqlite3.connect(self.name + self.extension)

        conn.executescript(
            self.table
        )

        conn.execute("VACUUM")

        conn.commit()

        #conn.row_factory = sqlite3.Row

        self.conn = conn
        self.is_connected: bool = True

        logger.info("Database Anda Telah Terhubung.")

    def close(self):
        self.conn.close()

        self.is_connected: bool = False

        logger.info("Database Anda Telah Ditutup.")

    def get_conn(self) -> sqlite3.Connection:
        if not self.is_connected:
            self.connect()

        return self.conn

    def resolved(self, target: str, peer_id: int):
        """
        This function for getting memory user

        Arguments
            target (`str`):
                The target, give name memory for getting details.

            peer_id (`int`):
                `Integer` get database for target peer_id if exist.

        Example
            
            result = gen.resolved(target='email', peer_id=user_id)
            print(result)
        """
        return self.conn.execute(
            f"SELECT * FROM {target} WHERE user_id = ?", (peer_id,)
        ).fetchall()

    def insert_memory(
        self,
        objec: str,
        data: tuple
    ):
        """
        This function for insert memory

        Arguments
            objec (`str`):
                The objec, get data for insert to memory.

            data (`tuple`):
                The data insert to memory values.

        Example
            
            gen.insert_memory(objec='email user_id username domain', data=(user_id, username, domain))
        """
        name = objec.split(' ')[0]
        values = ', '.join('?' for _ in range(len(objec.split(' ')[1:])))
        struk = ', '.join(i for i in objec.split(' ')[1:])
        self.conn.execute(
            f'INSERT INTO {name}({struk}) VALUES({values})', data
        )
        self.conn.commit()

    def update_memory(
        self,
        objec: str,
        data: tuple
    ):
        """
        This function for update memory

        Arguments
            objec (`str`):
                The objec, get data for update to memory.

            data (`tuple`):
                The data update to memory values.

        Example
            
            gen.update_memory(objec='email username domain', data=(username, domain, user_id))
        """
        name = objec.split(' ')[0]
        values = ', '.join('?' for _ in range(len(objec.split(' ')[1:])))
        struk = ', '.join(f'{i} = ?' for i in objec.split(' ')[1:])
        self.conn.execute(
            f'UPDATE {name} SET {struk} WHERE user_id = ?', data
        )
        self.conn.commit()

    def delete_memory(
        self,
        objec: str,
        data: tuple
    ):
        """
        This function for delete memory

        Arguments
            objec (`str`):
                The objec, get data for delete from memory.

            data (`tuple`):
                The data delete from memory.

        Example
            
            gen.update_memory(objec='email username domain', data=(username, domain, user_id))
        """
        name = objec.split(' ')[0]
        struk = ' AND '.join(f'{i} = ?' for i in objec.split(' ')[1:])
        self.conn.execute(
            f'DELETE FROM {name} WHERE {struk}', data
        )
        self.conn.commit()
