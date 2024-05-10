import random
import subprocess
import sys
import time
import pyautogui as pa

nome = sys.argv[1] 
mensagem = sys.argv[2] 

# frases = ['te amo, amor', 'to com saudades', 'ja falei que te amo hoje?', 'linda linda linda']

subprocess.Popen(['firefox'], shell=True)
time.sleep(2)
pa.write('https://web.whatsapp.com/')
pa.press('Enter')

time.sleep(6)
pa.click(x=230, y=217)
pa.write(f'{nome} \n')

time.sleep(3)
pa.click(x=831, y=964)

time.sleep(3)
# pa.write( f'{frases[random.randint(0, len(frases) - 1)]} \n'  ) 
pa.write( f'{mensagem} \n'  )

time.sleep(3)

pa.hotkey('ctrl', 'w')
print('funcionou')



