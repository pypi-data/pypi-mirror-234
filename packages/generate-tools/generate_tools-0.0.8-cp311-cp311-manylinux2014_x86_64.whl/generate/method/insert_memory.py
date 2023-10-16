import generate
from generate.exception import IsAuthorized


class InsertMemory:
    def insert(
        self: 'generate.Generate',
        objec: str,
        data: tuple
    ):
        """
        This function for delete memory

        Arguments
            objec (`str`):
                The objec, get data for delete from memory.

            data (`tuple`):
                The data delete from memory values.

        Example
            
            gen.insert(
                objec='email username domain',
                data=(username, domain, user_id)
            )
        """
        if not self.is_authorize:
            raise IsAuthorized()
        
        return self.memory.insert_memory(
            objec=objec,
            data=data
        )
