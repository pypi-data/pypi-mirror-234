"Script used for testing features as its developed"

import e620py
import logging
import json

handler = logging.StreamHandler()
consolelog_format = logging.Formatter(
    '%(asctime)s - %(name)s : %(levelname)s - %(message)s', datefmt='%H:%M:%S'
)
handler.setFormatter(consolelog_format)

logging.getLogger("e620py").addHandler(handler)
logging.getLogger("e620py").setLevel(logging.DEBUG)

poolhandler = e620py.handlers.PoolHandler()
posthandler = e620py.handlers.PostHandler()
pool = poolhandler.get_pools(name_search = "Sus", fetch_limit=1)[0]
objects = posthandler.get_posts(f"pool:{pool['id']}")

# objects = posthandler.get_posts("scalie", 1)

print(json.dumps(objects, indent=1))