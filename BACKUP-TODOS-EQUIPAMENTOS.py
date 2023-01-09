#BACKUP-TODOS-EQUIPAMENTOS-2.3.1.py
#====================================================================
#AUTOMATIZACAO DE BACKUPS
#By:Rodrigo S Nunes
#====================================================================
#LOG
#Atualizado (24/11/22) = Ajustado expressao regular Olt_Huawei
#
#====================================================================
#BIBLIOTECAS
import sys
import paramiko
import pickle
import re
import warnings
import os
from zabbix_api import ZabbixAPI
import time
from datetime import datetime
import errno
from socket import error as socket_error
import logging
today = datetime.now()
day = today.day
month = today.month
year = today.year
hora = today.hour
min = today.minute
seg = today.second
#====================================================================
#ARGUMENTOS PARA ACESSO EQUIPAMENTO
username = 'jmnetbkp'
password = '189K0R*f1Td9'


#ZABBIX
addressz = "http://181.215.211.17"
usernamez = 'jmnetbkp'
passwordz = 'CVw65wi*r01g'

#SERVIDOR-FTP
userftp = 'bkp-socitel'

#====================================================================
#Funcoes

def Mikrotik():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('export')
    result = stdout.readlines()
    return result

def Huawei():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('screen-length 0 temporary \n display current-configuration \n')
    result = stdout.readlines()
    return result

def Olt_Huawei():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('enable \n scroll \n  \n display current-configuration \n')
    result = stdout.readlines()
    return result

def Nokia():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('environment no more \n admin display-config \n')
    result = stdout.readlines()
    return result

def Olt_Nokia():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('info configure flat \n')
    result = stdout.readlines()
    return result

def Sw_Datacom():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('show running-config \n shilf+!')
    result = stdout.readlines()
    return result

def Olt_zte():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('terminal length 0 \n show running-config \n   \n   \n   \n   \n')
    result = stdout.readlines()
    return result

def Olt_fiberhome():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('show startup-config \n ')
    result = stdout.readlines()
    return result

def Juniper():
    ssh = paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command('show configuration | no-more \n ')
    result = stdout.readlines()
    return result


#====================================================================
#Codigo Main
#====================================================================

try:
    zapi = ZabbixAPI(server=addressz); zapi.login(usernamez, passwordz)
    id_grupo = zapi.hostgroup.get({"search":{"name":"BACKUPS"}, "output":["groupid","name"] })
    nomes_grupo = zapi.host.get({"groupids":id_grupo[0]['groupid'], "output":["host","hostid"] })
    for y in nomes_grupo:
            ips_host = zapi.hostinterface.get({"hostids":y['hostid'], "output":["ip"]})
            for x in ips_host:
                try:
                    PATH = x['ip']
                    if not os.path.exists('/home/'+userftp+'/'+PATH+''):
                        os.makedirs('/home/'+userftp+'/'+PATH+'')
                    #logging.getLogger("paramiko").setLevel(logging.DEBUG)
                    #paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
                    ssh = paramiko.SSHClient();
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=x['ip'], username=username, password=password, port=22, look_for_keys=False)
                    stdin, stdout, stderr = ssh.exec_command ('system resource print \n screen-length 0 temporary \n display version \n \n enable \n scroll \n \n \n display version \n \n \n show version \n show software-mngt version etsi \n show platform chassis 1 \n show system-group \n show version | no-more \n')
                    resultado = stdout.readlines(); resultstring = " ".join(resultado)
                    try:
                        i = 1
                        while i <= 8:
                            #MIKROTIK
                            if i == 1:
                                verifica = re.search(r'MikroTik', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if verifica[0] == 'MikroTik':
                                    result = Mikrotik()
                                    break
                            #ROUTER E SW HUAWEI
                            if i == 2:
                                verifica = re.search(r'HUAWEI', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if verifica[0] == 'HUAWEI':
                                    result = Huawei()
                                    break
                            #OLT HUAWEI
                            if i == 3:
                                verifica = re.search(r'MA[0-9][azA-Z0-9_]+', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if re.match('MA[0-9][azA-Z0-9_]+',verifica[0]):
                                    result = Olt_Huawei()
                                    break
                            #ROUTER E SW NOKIA
                            if i == 4:
                                verifica = re.search(r'Nokia', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if verifica[0] == 'Nokia':
                                    result = Nokia()
                                    break
                            #OLT NOKIA
                            if i == 5:
                                verifica = re.search(r'isam-release', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if verifica[0] == 'isam-release':
                                    result = Olt_Nokia()
                                    break
                            #SW DATACOM
                            if i == 6:
                                verifica = re.search(r'DM[0-9]+', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if re.match('DM[0-9]+',verifica[0]):
                                    result = Sw_Datacom()
                                    break                
                            #OLT ZTE
                            if i == 7:
                                verifica = re.search(r'ZTE', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if verifica[0] == 'ZTE':
                                    result = Olt_zte()
                                    break
                            #OLT FIBERHOME
                            if i == 8:
                                verifica = re.search(r'FIBERHOME', resultstring)
                                if verifica is None:
                                    i = i+1; ssh.close()
                                    continue
                                if verifica[0] == 'FIBERHOME':
                                    result = Olt_fiberhome()
                                    break                                                                   
                            i = i+1
                    except:
                        print("Falha na identificacao do Host = " +PATH+'')
                    file = open('/home/'+userftp+'/'+PATH+'/'+PATH+'_DIA_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'.txt','w')
                    file.writelines(result)
                    file.close(); ssh.close()
                    sz = os.path.getsize(r'/home/'+userftp+'/'+PATH+'/'+PATH+'_DIA_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(hora)+'_'+str(min)+'.txt')
                    if sz > 1000:
                        print ("Sucesso no Backup do Host = " +PATH+'')
                    else:
                        print ("Falha ao gravar arquivo do Host = " +PATH+'')
                except paramiko.AuthenticationException:
                    print ("Falha na autenticacao do Host = " +PATH+'')
                except socket_error as socket_err:
                    print ("Falha no acesso do Host = " +PATH+'')
except:
    print ("FALHA CODIGO INTEIRO")
