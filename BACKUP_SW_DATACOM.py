#!/usr/bin/python
#-------------------------------------
#By: Rodrigo S Nunes
#-------------------------------------
#Modo de uso
# ./BACKUP_SW_DATACOM.py {HOST} {PATH}
#=======================================================================
import sys,pexpect
import getpass
import time
from datetime import datetime
today = datetime.now()
day = today.day
month = today.month
year = today.year
#hora = today.hour
#min = today.minute
#seg = today.second
#=======================================================================
#Argumentos
HOST = sys.argv[1]
PATH = sys.argv[2]
#=======================================================================
#Variaves de acesso equipamento
user = 'XXXXXXX'
password = 'XXXXXXX'
#=======================================================================
#Main code
child = pexpect.spawn ('telnet '+HOST)
child.timeout = 150
child.logfile = sys.stdout
time.sleep(2)
child.expect('login:')
child.sendline (user) 
child.expect('Password:')
child.sendline (password)
time.sleep(10)
child.sendline ('config')
child.sendline ('save '+PATH+'_'+HOST+'_dia-_'+str(day)+'_'+str(month)+'_'+str(year)+'.cfg')
time.sleep(10)
child.sendline ('copy file '+PATH+'_'+HOST+'_dia-_'+str(day)+'_'+str(month)+'_'+str(year)+'.cfg scp://170.150.224.249/home/bmjnet/'+PATH+'/ source '+HOST+' username bmjnet password PwdBmjNet ')
time.sleep(5)
time.sleep(5)
child.sendline ('exit')
child.sendline ('file delete '+PATH+'_'+HOST+'_dia-_'+str(day)+'_'+str(month)+'_'+str(year)+'.cfg')
time.sleep(5)
child.sendline ('exit')
