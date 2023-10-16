import generate
from generate.exception import IsAuthorized


class UpdateMemory:
    def update(
        self: 'generate.Generate',
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
            
            gen.updates(
                objec='email username domain',
                data=(username, domain, user_id)
            )
        """
        if not self.is_authorize:
            raise IsAuthorized()
        
        return self.memory.update_memory(
            objec=objec,
            data=data
        )
