#!/usr/bin/python
#====================================================================
#BACKUP ROUTER JUNIPER
#By Rodrigo S Nunes
#====================================================================
#USE DESSA MANEIRA
#BACKUP_TELIC_DANOS.py {IP}
#====================================================================
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
#====================================================================
#Argumentos externos
HOST = sys.argv[1]
#====================================================================
#Argumentos USER EQUIPAMENTO
user = 'XXXXXXX'
password = 'XXXXXXX'

#FTP SERVER
userftp = 'XXXXXXX'
passwordftp = 'XXXXXXX'
ipftp = 'XXXXXXX'
#====================================================================
#necessario configurar usuario e senha na olt antes
#de executar o script
#====================================================================
#Main code
child = pexpect.spawn ('ssh -p 63987 '+user+'@'+HOST)
child.timeout = 1500
child.logfile = sys.stdout
time.sleep(2)
child.sendline (password)
time.sleep(3)
child.sendline ('configure')
time.sleep(2)
child.sendline ('save ftp://'+userftp+':'+passwordftp+'@'+ipftp+'/'+HOST+'/'+HOST+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'.txt')
time.sleep(10)
child.sendline ('exit')
time.sleep(2)
child.sendline ('exit')
#End
