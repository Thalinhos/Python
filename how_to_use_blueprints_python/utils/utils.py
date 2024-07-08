from datetime import datetime
import pytz
def getBrHour():
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    return str(now)

# from prisma import Prisma
# db = Prisma()

import sqlite3
from typing import List, Union

def rawQuery(sql_string: str) -> Union[List[tuple], str]:
    try:
        conn = sqlite3.connect('./prisma/clinica.db')
        cur = conn.cursor()
        cur.execute(sql_string)
        results = cur.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

