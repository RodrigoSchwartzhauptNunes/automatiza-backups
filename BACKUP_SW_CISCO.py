#!/usr/bin/python
#=======================================================================
#By: Rodrigo S Nunes
#=======================================================================
#Modo de usar
#./bkp-sw-cisco.py {IP_ADDRESS} {PASTA}
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
#Argumentos Server FTP
user = 'XXXX'
password = 'XXXXXX'
FTPSERVER = 'XXX.XXX.XXX.XXX'
#=======================================================================
child = pexpect.spawn ('ssh '+HOST)
child.timeout = 150
child.logfile = sys.stdout
time.sleep(2)
child.sendline (user)
time.sleep(1)
child.sendline (password)
time.sleep(2)
child.sendline ('copy startup-config ftp://'+user+'@'+FTPSERVER+'/'+PATH+'/'+PATH+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'  source-interface vlan 58' )
time.sleep(5)
child.sendline (password+'\r')
time.sleep(1)
child.sendline ('exit')

