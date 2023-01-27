#!/usr/bin/python
#====================================================================
#BACKUP-OLT-FURUKAWA.py
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
username = 'XXXXXXXXX'
password = 'XXXXXXXXX'
enablepassword = 'XXXXXXXXX'

#ZABBIX
addressz = "http:/XXXXXXXXX"
usernamez = 'XXXXXXXXX'
passwordz = 'XXXXXXXXX'

#SERVIDOR-FTP
userftp = 'XXXXXXXXX'
ftppassword = 'XXXXXXXXX'
FTPSERVER = 'XXXXXXXXX'

#====================================================================
#necessario configurar usuario e senha na olt antes
#de executar o script
#====================================================================
#Main code
try:
    zapi = ZabbixAPI(server=addressz); zapi.login(usernamez, passwordz)
    id_grupo = zapi.hostgroup.get({"search":{"name":"XXXXXXXXX"}, "output":["groupid","name"] })
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
                        time.sleep(5)
                        child.sendline (password)
                        child.expect ('>')
                        child.sendline ('enable'+'\n')
                        time.sleep(2)
                        child.sendline (enablepassword)
                        child.expect('#')
                        child.sendline ('copy ftp config upload startup-config')
                        time.sleep(2)
                        child.sendline (FTPSERVER)
                        time.sleep(2)
                        child.sendline ('/'+PATH+'/'+PATH+'_'+str(day)+'_'+str(month)+'_'+str(year))
                        time.sleep(2)
                        child.sendline (userftp)
                        time.sleep(2)
                        child.sendline (ftppassword)
                        time.sleep(5)
                        child.sendline ('exit')
                    except:
                        print ("Falha ao acessar equipamento")
                except:
                    print("Falha ao criar pasta")
except:
    print ("FALHA CODIGO INTEIRO")
