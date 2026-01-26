import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from database.queries.orm import SyncOrm, sneakers_data 


# SyncOrm.create_tables()


SyncOrm.insert_test_data()
