#!/usr/bin/python
#====================================================================
#BACKUP-OLT-HW.py
#By Rodrigo S Nunes
#====================================================================
#Logs
#Versao nova com repeticao e lista de IPs via API do Zabbix
#====================================================================
import sys,pexpect
from zabbix_api import ZabbixAPI
import getpass
import time
import os
from datetime import datetime
today = datetime.now()
day = today.day
month = today.month
year = today.year
hora = today.hour
min = today.minute
seg = today.second
#====================================================================
#Argumentos USER EQUIPAMENTO
username = 'vXXXXXXXX'
password = 'XXXXXXXX'

#ZABBIX
addressz = "http://XXXXXXXX"
usernamez = 'XXXXXXXX'
passwordz = 'XXXXXXXX'

#SERVIDOR-FTP
userftp = 'XXXXXXXX'
FTPSERVER = 'XXXXXXXX'

#====================================================================
#necessario configurar usuario e senha na olt antes
#de executar o script
#====================================================================
#Main code
try:
    zapi = ZabbixAPI(server=addressz); zapi.login(usernamez, passwordz)
    id_grupo = zapi.hostgroup.get({"search":{"name":"OLT-HW"}, "output":["groupid","name"] })
    nomes_grupo = zapi.host.get({"groupids":id_grupo[0]['groupid'], "output":["host","hostid"] })
    for y in nomes_grupo:
            ips_host = zapi.hostinterface.get({"hostids":y['hostid'], "output":["ip"]})
            for x in ips_host:
                try:
                    PATH = x['ip']
                    print (PATH)
                    if not os.path.exists('/home/'+userftp+'/'+PATH+''):
                        os.makedirs('/home/'+userftp+'/'+PATH+'')
                    try:
                        child = pexpect.spawn ('ssh '+username+'@'+PATH)
                        child.timeout = 1500
                        child.logfile = sys.stdout
                        time.sleep(10)
                        child.sendline (password)
                        time.sleep(3)
                        child.sendline ('EN'+'\r')
                        time.sleep(5)
                        child.sendline ('backup configuration ftp '+FTPSERVER+' '+PATH+'/'+PATH+'-dia-'+str(day)+'-'+str(month)+'-'+str(year)+'-'+str(hora)+'-'+str(min)+'-'+str(seg)+'.cfg')
                        time.sleep(3)
                        child.sendline ('y'+'\r')
                        time.sleep(3)
                        child.sendline ('quit')
                        time.sleep(3)
                        child.sendline ('y'+'\r')
                    except:
                        print ("Falha ao acessar equipamento")
                except:
                    print("Falha ao criar pasta")
except:
    print ("FALHA CODIGO INTEIRO")
