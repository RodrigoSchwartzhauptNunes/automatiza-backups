#instalar apt install python-pexpect
#!/usr/bin/python
#====================================================================
#BACKUP OLT NOKIA
#By Rodrigo S Nunes
#====================================================================
#USE DESSA MANEIRA
#SCRIP_BACKUP_OLT_NOKIA.py {IP} {PASTA NO FTP}
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
PATH = sys.argv[2]
#====================================================================
#Argumentos USER EQUIPAMENTO
user = 'XXX'
password = 'XXXXXXXX'
#====================================================================
#necessario configurar usuario e senha na olt antes
#de executar o script
#====================================================================
#Main code
child = pexpect.spawn ('telnet '+HOST)
child.timeout = 1500
child.logfile = sys.stdout
time.sleep(2)
child.sendline (user)
time.sleep(2)
child.sendline (password)
time.sleep(3)
child.logfile = open('/home/bkp/'+PATH+'/'+PATH+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'.txt','wb')
time.sleep(3)
child.sendline ('environment inhibit-alarms')
time.sleep(3)
child.sendline ('exit')
time.sleep(3)
child.sendline ('admin display-config')
time.sleep(10)
#Para backups com tftp
#child.sendline ('admin software-mngt database upload actual-active:10.48.0.4:dm_'+PATH+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'_complete.tar:dm_complete.tar ')
#time.sleep(10)
child.sendline ('info configure flat')
child.expect('configure mcast-control mcast-svc-context Default') #Esperando
child.sendline ('logout')
#End
