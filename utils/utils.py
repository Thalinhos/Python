from datetime import  datetime
import pytz
def getBrHour():
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    return str(now)

from prisma import Prisma
db = Prisma()