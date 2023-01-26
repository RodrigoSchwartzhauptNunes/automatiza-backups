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
#=======================================================================
#ACESSO EQUIPAMENTOS
Login  = 'XXXXXXXXXX'
Password = 'XXXXXXXXXX'

#FTP
HOSTFTP = 'XXXXXXXXXX'
userftp = 'XXXXXXXXXX'
passwordftp = 'XXXXXXXXXX'
#=======================================================================
#INICIO CODIGO
child = pexpect.spawn ('ssh '+Login+'@'+HOST)
child.timeout = 1500
child.logfile = sys.stdout #VER PROCESSO NA TELA
time.sleep(3)
child.sendline (Password)
time.sleep(5)
child.sendline ('enable'+'\r')
time.sleep(2)
child.sendline ('\r')
time.sleep(2)
child.sendline ('backup system ftp://'+userftp+'@'+HOSTFTP+':21/'+HOST+'/sytem_'+HOST+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'.tar.gz')
time.sleep(2)
child.sendline (passwordftp)
time.sleep(5)
child.sendline ('no'+'\r')
time.sleep(10)
child.sendline ('backup log ftp://'+userftp+'@'+HOSTFTP+':21/'+HOST+'/log_'+HOST+'_dia_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'_'+str(seg)+'.tar.gz')
time.sleep(2)
child.sendline (passwordftp)
child.expect('#:')
child.sendline ('exit')
time.sleep(2)
child.sendline ('exit')
time.sleep(2)
child.sendline ('y')
#FIM CODIGO
