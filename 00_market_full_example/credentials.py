from fasthtml.common import *
from fastsql.core import *
from l402.server.macaroons import MacaroonService
import time


@dataclass
class Macaroon:
    id: int
    token_id: str
    root_key: str
    macaroon: str
    created_at: int


class FastSQLMacaroonService(MacaroonService):

    def __init__(self, db_url):
        self.db = Database(db_url)
        self.macaroons = self.db.create(Macaroon, pk='id')

    async def insert_root_key(self, token_id: bytes, root_key: bytes,
                              macaroon: str):
        self.macaroons.insert(
            Macaroon(token_id=token_id.hex(),
                     root_key=root_key.hex(),
                     macaroon=macaroon,
                     created_at=int(time.time())))

    async def get_root_key(self, token_id: bytes) -> bytes:
        result = self.macaroons(where="token_id = :token_id",
                                token_id=token_id.hex())
        return bytes.fromhex(result[0].root_key) if result else None
