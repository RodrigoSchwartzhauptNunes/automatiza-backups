#!/usr/bin/python
#=======================================================================
#By: Rodrigo S Nunes
#=======================================================================
#Modo de usar
#./bk-olt-fiberhome.py {IP_ADDRESS}
#=======================================================================
#Bibliotecas
import sys,pexpect
import getpass
import time
from datetime import datetime
today = datetime.now()
day = today.day
month = today.month
year = today.year
hora = today.hour
min = today.minute
seg = today.second
#=======================================================================
#Argumentos
HOST = sys.argv[1]
PATH = sys.argv[2]
#=======================================================================
#Variaveis a serem alteradas
user = 'XXXX'
password = 'XXXXX'
FTPSERVER = 'XXX.XXX.XXX.XXX'
ftpuser = 'XXX'
ftppassword = 'XXXXXXXXX'
#=======================================================================
#Main code
child = pexpect.spawn ('telnet '+HOST)
child.timeout = 150
child.logfile = sys.stdout
time.sleep(2)
child.sendline (user)
time.sleep(2)
child.sendline (password)
time.sleep(3)
child.sendline ('ftp '+FTPSERVER+' source ip '+HOST)
time.sleep(3)
child.sendline (ftpuser)
time.sleep(1)
child.sendline (ftppassword)
child.expect('[ftp]')
child.sendline('cd '+PATH)
child.sendline('put config.cfg bkp-sw-'+HOST+'-dia-'+str(day)+'-'+str(month)+'-'+str(year)+'-'+str(hora)+'-'+str(min)+'-'+str(seg)+'.cfg')
time.sleep(5)
child.sendline ('quit')
