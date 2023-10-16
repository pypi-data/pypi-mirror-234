import generate
from generate.exception import IsAuthorized


class Start:
    def start(self: 'generate.Generate'):
        if not self.is_authorize:
            self.is_authorize = True
            self.authorize()
