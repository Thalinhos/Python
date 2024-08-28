import os
import asyncio
import httpx
from bs4 import BeautifulSoup
import math

subRedes = [32, 36, 37]

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
    def __init__(self, ip: str, serial: str, c: int | None = None, m: int | None = None, y: int | None = None, k: int | None = None, mono: int | None = None, color: int | None = None, total: int | None = None):
        self.ip = ip
        self.serial = serial
        self.c = c
        self.m = m
        self.y = y
        self.k = k
        self.mono = mono
        self.color = color
        self.total = total

    def print_info(self):
        print(f'{self.ip}: {self.serial}')
        print('Páginas impressas:')
        print(f"  ciano:   {self.c if self.c is not None else 'n/a'}")
        print(f"  magenta: {self.m if self.m is not None else 'n/a'}")
        print(f"  yellow:  {self.y if self.y is not None else 'n/a'}")
        print(f"  black:   {self.k if self.k is not None else 'n/a'}")
        print(f"  mono:    {self.mono if self.mono is not None else 'n/a'}")
        print(f"  color:   {self.color if self.color is not None else 'n/a'}")
        print(f"  total:   {self.total if self.total is not None else 'n/a'}")
        print('--------------------------')

def extrair_ip(infoimp):
    return infoimp.ip

async def ping_ip(ip):
    try:
        count_arg, timeout_arg = verificaOS()
        timeout_value = '5000' if os.name == 'nt' else '5'

        process = await asyncio.create_subprocess_exec(
            'ping', count_arg, '1', timeout_arg, timeout_value, ip,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )

        await process.wait()
        return ip if process.returncode == 0 else None
    except Exception as e:
        print(f"Erro ao pingar {ip}: {e}")
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

NO_COLOR_ID = 'UsagePage.EquivalentImpressionsTable.Total.Total'
MONO_ID = 'UsagePage.EquivalentImpressionsTable.Monochrome.Total'
COLOR_ID = 'UsagePage.EquivalentImpressionsTable.Color.Total'

def parse_float(value):
    # '15,124.9'
    if value:
        valuTry_cleaned = value.replace(',', '')
        valuTry_float = float(valuTry_cleaned)
        valuTry_ceil = math.ceil(valuTry_float)
        return valuTry_ceil
    return None

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
                print(f"Serial não encontrado para {ip}")
                return None
            
            noValueTotal = soupSerial.find(id=NO_COLOR_ID)
            monoValueTotal = soupSerial.find(id=MONO_ID)
            colorValueTotal = soupSerial.find(id=COLOR_ID)

            mono_value = None
            color_value = None

            mono_value = parse_float(monoValueTotal and monoValueTotal.get_text(strip=True))
            color_value = parse_float(colorValueTotal and colorValueTotal.get_text(strip=True))
            total_value = parse_float(noValueTotal.get_text(strip=True))

            resColor = await client.get(urlColor, headers={'User-Agent': 'Mozilla/5.0'})
            resColor.raise_for_status()
            soupColor = BeautifulSoup(resColor.text, 'html.parser')
            serialColorYellow = soupColor.find(id=YELLOW_ID)
            serialColorMagenta = soupColor.find(id=MAGENTA_ID)
            serialColorCiano = soupColor.find(id=CIANO_ID)
            serialColorBlack = soupColor.find(id=BLACK_ID)

            return InfoImp(
                ip=ip, 
                serial=serialNumber.get_text(strip=True),
                c=serialColorCiano and int(serialColorCiano.get_text(strip=True)),
                m=serialColorMagenta and int(serialColorMagenta.get_text(strip=True)),
                y=serialColorYellow and int(serialColorYellow.get_text(strip=True)),
                k=serialColorBlack and int(serialColorBlack.get_text(strip=True)),
                mono=mono_value if mono_value is not None else None,
                color=color_value if color_value is not None else None,
                total=total_value if total_value is not None else None
            )
        
    except httpx.HTTPStatusError as e:
        print(f"Erro de HTTP ao acessar {ip}: {e}")
        return None
    except Exception as e:
        print(f"Erro ao procurar impressora em {ip}: {e}")
        return None

async def main():
    try:
        ips_ativos = await verificarRede()
        resultados = [x for x in await asyncio.gather(*(verificarImp(ip) for ip in ips_ativos)) if x is not None]

        print('-------------------------')
        for r in sorted(resultados, key=extrair_ip):
            r.print_info()
    
    except Exception as e:
        print(f"Erro na execução do programa: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    input('Digite uma tecla para sair.')
