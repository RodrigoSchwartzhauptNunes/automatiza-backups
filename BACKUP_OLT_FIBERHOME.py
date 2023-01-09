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
#=======================================================================
#Variaveis para serem alteradas
user = 'XXXXX'
password = 'XXXXX'
FTPSERVER = 'XXX.XXX.XXX.XXX'
ftpuser = 'XXX'
ftppassword = 'XXXXXXXXXX'
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
child.expect('#')
child.sendline ('upload ftp config '+FTPSERVER+' '+ftpuser+' '+ftppassword+' '+HOST+'/'+HOST+'_DIA_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'.cfg')
time.sleep(10)
child.sendline ('exit \r')
child.sendline ('exit \r')
