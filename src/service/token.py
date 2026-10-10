"junta settings com token"

from src.core.module import Settings
from src.auth.token import JWT

class WatchToken(JWT):

    def __init__(self, settings:Settings)-> None:

        secret = settings.required_secrets("secret")


        super().__init__(secret)