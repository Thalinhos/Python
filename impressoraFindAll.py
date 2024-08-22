import os
import time
import asyncio
from bs4 import BeautifulSoup
import httpx

subRedes = [32,36,37]

WINDOWS_COUNTER_DIGIT_SHELL = '-n'  # Windows
LINUX_COUNTER_DIGIT_SHELL = '-c'    # Unix-like (Linux, macOS)
TIMEOUT_ARG_WINDOWS = '-w'          # Timeout em Windows (em milissegundos)
TIMEOUT_ARG_UNIX = '-W'             # Timeout em Unix-like (em segundos)

def verificaOS():
    if os.name == 'nt':
        return WINDOWS_COUNTER_DIGIT_SHELL, TIMEOUT_ARG_WINDOWS
    elif os.name == 'posix':
        return LINUX_COUNTER_DIGIT_SHELL, TIMEOUT_ARG_UNIX
    else:
        raise Exception("Sistema operacional não suportado")

class InfoImp:
    def __init__(self, ip: str, serial: str, c: int | None = None, m: int | None = None, y: int | None = None, k: int | None = None):
        self. ip = ip
        self.serial = serial
        self.c = c
        self.m = m
        self.y = y
        self.k = k

    def print_info(self):
        print(f'{self.ip}: {self.serial}')
        print('Páginas impressas:')
        print(f"  ciano:   {self.c or 'n/a'}")
        print(f"  magenta: {self.m or 'n/a'}")
        print(f"  yellow:  {self.y or 'n/a'}")
        print(f"  black:   {self.k or 'n/a'}")
        print('--------------------------')
    
def extrair_ip(infoimp):
    return infoimp.ip

async def ping_ip(ip):
    try:
        count_arg, timeout_arg = verificaOS()
        
        if os.name == 'nt':  # Windows
            process = await asyncio.create_subprocess_exec(
                'ping', count_arg, '1', timeout_arg, '5000', ip,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
        else:               # Unix-like
            process = await asyncio.create_subprocess_exec(
                'ping', count_arg, '1', timeout_arg, '5', ip, 
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
        
        await process.wait()
        return ip if process.returncode == 0 else None
    except Exception as e:
        # print(f"Erro ao pingar {ip}: {e}")
        return None

async def verificarRede(ipPrefix='10.244', inicioPing=2, finalPing=254):
    ip_list = [f"{ipPrefix}.{subRede}.{n}" for subRede in subRedes for n in range(inicioPing, finalPing + 1)]
    tasks = [ping_ip(ip) for ip in ip_list]
    resultados = await asyncio.gather(*tasks)
    ipAtivos = [ip for ip in resultados if ip is not None]
    return ipAtivos


PAGE_SERIAL_NUMBER = '/hp/device/InternalPages/Index?id=UsagePage'
PAGE_COLORS_VALUES = '/hp/device/InternalPages/Index?id=SuppliesStatus'

SERIAL_ID = 'UsagePage.DeviceInformation.DeviceSerialNumber'
YELLOW_ID = 'YellowCartridge1-PagesPrintedWithSupply'
MAGENTA_ID = 'MagentaCartridge1-PagesPrintedWithSupply'
CIANO_ID = 'CyanCartridge1-PagesPrintedWithSupply'
BLACK_ID = 'BlackCartridge1-PagesPrintedWithSupply'

async def verificarImp(ip) -> InfoImp | None:
    urlSerial = f"https://{ip}{PAGE_SERIAL_NUMBER}"
    urlColor = f"https://{ip}{PAGE_COLORS_VALUES}"

    try:
        async with httpx.AsyncClient(verify=False) as client:
            resSerial = await client.get(urlSerial, headers={'User-Agent': 'Mozilla/5.0'})
            resSerial.raise_for_status()
            soupSerial = BeautifulSoup(resSerial.text, 'html.parser')
            serialNumber = soupSerial.find(id=SERIAL_ID)
            
            if serialNumber is None:
                print("Pagina inválida")
                return None

            resColor = await client.get(urlColor, headers={'User-Agent': 'Mozilla/5.0'})
            resColor.raise_for_status()
            soupColor = BeautifulSoup(resColor.text, 'html.parser')
            serialColorYellow = soupColor.find(id=YELLOW_ID)
            serialColorMagenta = soupColor.find(id=MAGENTA_ID)
            serialColorCiano = soupColor.find(id=CIANO_ID)
            serialColorBlack = soupColor.find(id=BLACK_ID)

            return InfoImp(ip = ip, serial = serialNumber.get_text(strip=True),
                c = serialColorCiano and int(serialColorCiano.get_text(strip = True)),
                m = serialColorMagenta and int(serialColorMagenta.get_text(strip = True)),
                y = serialColorYellow and int(serialColorYellow.get_text(strip = True)),
                k = serialColorBlack and int(serialColorBlack.get_text(strip = True)))
            
    except Exception as e:
        return None
        # print('Erro ao procurar ip: ', e)


async def main():
    ips_ativos = await verificarRede()
    resultados = [x for x in await asyncio.gather(*(verificarImp(ip) for ip in ips_ativos)) if x is not None]

    print('-------------------------')
    for r in sorted(resultados, key=extrair_ip):
        r.print_info()
    

if __name__ == "__main__":
    asyncio.run(main())

