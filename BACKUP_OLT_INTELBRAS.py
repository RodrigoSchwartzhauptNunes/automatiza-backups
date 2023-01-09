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
ftppassword = 'XXXXXXXX'
#=======================================================================
#Main code
child = pexpect.spawn ('ssh '+user+'@'+HOST)
child.timeout = 150
child.logfile = sys.stdout
child.expect('Password:')
child.sendline (password)
time.sleep(10)
child.sendline ('backup network ftp '+FTPSERVER+' filename '+PATH+'/'+PATH+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'.txt user '+ftpuser)
child.expect('Password:')
child.sendline (ftppassword)
time.sleep(10)
child.sendline('logout')
