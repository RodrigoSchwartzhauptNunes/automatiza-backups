#!/usr/bin/python
#=======================================================================
#by: Rodrigo S Nunes
#=======================================================================
#Modo de usar
#./bk-ubnt.py {IP_ADDRESS]
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
#=======================================================================
#Variaveis para serem alteradas
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
child.sendline ('EN'+'\r')
time.sleep(2)
child.sendline (password)
time.sleep(3)
child.sendline ('copy backup ftp://'+ftpuser+'@'+FTPSERVER+'/'+HOST+'/'+HOST+
'-dia-'+str(day)+'-'+str(month)+'-'+str(year)+'-'+str(hora)+'-'+str(min)+'-'+str(seg)+'.cfg')
time.sleep(3)
child.sendline (ftppassword)
time.sleep(3)
child.sendline ('y'+'\r')
time.sleep(2)
child.sendline ('exit \r')
