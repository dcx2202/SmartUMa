import db_manager
import time
from datetime import datetime

for i in range(5):
    db_manager.insert_entry_to_database(
        str(datetime.now().date()), str(datetime.now().time()), i)
    db_manager.insert_exit_to_database(
        str(datetime.now().date()), str(datetime.now().time()), i)
    print('iteration: {}'.format(i))
    time.sleep(1)
