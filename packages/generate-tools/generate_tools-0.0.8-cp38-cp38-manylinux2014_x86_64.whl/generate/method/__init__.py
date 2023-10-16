from .delete_memory import DeleteMemory
from .insert_memory import InsertMemory
from .solved import Solved
from .update_memory import UpdateMemory


class Method(
    DeleteMemory,
    InsertMemory,
    Solved,
    UpdateMemory
):
    pass
