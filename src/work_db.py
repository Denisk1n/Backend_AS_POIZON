import sys
import os
from datetime import datetime
import asyncio
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database.queries.orm import AsyncOrm


# asyncio.run(AsyncOrm.create_tables())


# asyncio.run(AsyncOrm.insert_test_data())


#asyncio.run(SyncOrm.selectProductCards())

# SyncOrm.selectProductInfo()

#SyncOrm.selectProductCardsWithFilters()


asyncio.run(AsyncOrm.insert_static_data())