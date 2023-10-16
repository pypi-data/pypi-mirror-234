import generate
from generate.exception import IsAuthorized, PeerIdInvalid


class Solved:
    def solved(
        self: 'generate.Generate',
        target: str = None,
        peer_id: int = None
    ):
        if not self.is_authorize:
            raise IsAuthorized()

        try:
            return self.memory.resolved(target=target, peer_id=peer_id)
        except KeyError:
            raise PeerIdInvalid(ids=peer_id)
