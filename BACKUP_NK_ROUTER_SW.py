#=======================================================================
#PYTHON2 {SCRIPT} {IP} {PASTA NO FTP}
#BY: Rodrigo S Nunes
#=======================================================================
#BIBLIOTECAS
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
#ARGUMENTOS
HOST = sys.argv[1]
PATH = sys.argv[2]
#=======================================================================
#ACESSO EQUIPAMENTOS
Login  = 'XXXXXX'
Password = 'XXXXXXX'

#FTP
HOSTFTP = 'XXX.XXX.XXX.XXX'
userftp = 'XXX'
passwordftp = 'XXXXXXXXXXXX'
#=======================================================================
#INICIO CODIGO
child = pexpect.spawn ('ssh '+Login+'@'+HOST)
child.timeout = 150
child.logfile = sys.stdout #VER PROCESSO NA TELA
#time.sleep(2)
#child.sendline (Login)
time.sleep(2)
child.sendline (Password)
time.sleep(3)
child.sendline ('file copy cf3:\config.cfg ftp://'+userftp+':'+passwordftp+'@'+HOSTFTP+'/'+HOST+'/'+PATH+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'.txt')
time.sleep(10)
child.sendline ('logout')
#FIM CODIGO
