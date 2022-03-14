from pypresence import Presence
from resources.lib.config import config
import time


rpc = Presence("896669007342633000")
try:
    rpc.connect()
    if config['showrpc']:
        rpc.update(details="Just started app", state="Nothing is beeing listened...", large_image="multimate",
                   start=int(time.time()))
except:
    pass
