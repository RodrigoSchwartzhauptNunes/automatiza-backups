#!/usr/bin/python
#=======================================================================
#By:Rodrigo S Nunes
#=======================================================================
#backup OLT ZTE VIA TELNET
#Usage
#./BACKUP_OLT_ZTE.py {PASTA NO FTP}
#=======================================================================
#Bibliotecas
import sys,pexpect
import getpass
import time
from datetime import datetime
#=======================================================================
#Variaveis
today = datetime.now()
day = str(today.day)
month = str(today.month)
year = str(today.year)
hora = str(today.hour)
min = str(today.minute)
seg = str(today.second)
seg = today.second
#=======================================================================
#Argumentos
HOST = sys.argv[1]
PATH = sys.argv[2]
#=======================================================================
#Variaveis para serem alteradas
userftp = 'XXX'
passwordftp = 'XXXXXX'
user = 'XXXXXX'
password = 'XXXXXXX'
FTPSERVER = 'XXXXXXXXXX'
#=======================================================================
#Main code
child = pexpect.spawn ('telnet '+HOST)
child.timeout = 150
child.logfile = sys.stdout
time.sleep(1)
child.sendline (user)
time.sleep(1)
child.sendline (password)
time.sleep(2)
child.sendline ('file upload cfg-startup startrun.sav ftp ipaddress '+FTPSERVER+' path '+PATH+' user '+userftp+' password '+passwordftp+'' )
time.sleep(20)
child.sendline ('exit')
child.sendline ('y'+'\r')
#===========================================================================
time.sleep(5)
child = pexpect.spawn ('ssh '+userftp+'@'+FTPSERVER)
child.timeout = 150
child.logfile = sys.stdout
time.sleep(5)
child.sendline (userftp)
child.sendline (passwordftp)
time.sleep(1)
child.sendline ('cp /home/'+userftp+'/'+PATH+'/startrun.sav /home/'+userftp+'/'+PATH+'/'+PATH+'_DIA_'+day+'_'+month+'_'+year+'_'+hora+'_'+min+' ')
time.sleep(5)
child.sendline ('exit')
