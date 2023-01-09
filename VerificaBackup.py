#!/usr/bin/env python3
#====================================================================
#By Rodrigo S Nunes
#====================================================================
#LEGENDA
#CODIGO 0 = BAKCUP INEXISTENTE OU INCONSISTENTE
#CODIGO 1 = BACKUP OK
#CODIGO 2 = FALHA AO ACESSAR SERVIDOR FTP
#====================================================================
#LOG
#ALTERADO DIA 27/10/22
#====================================================================
#BIBLIOTECAS UTILIZADAS
import sys
import paramiko
import pickle
from datetime import datetime
#====================================================================
#ARQGUMENTOS
#
#SERVIDOR FTP
address = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
#HOST A SER CONFERIDO
iphost = sys.argv[4]
#DATA DE CONFERENCIA
DATA = sys.argv[5]
#FILTRO
FILTRO = """awk '{ print $9 ": " $5 }'"""
#====================================================================
#ACESSO
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=address, username=username, password=password)
#    PATH = iphost
    stdin, stdout, stderr = ssh.exec_command('find /home/'+username+'/'+iphost+' -type f -size +1k -mtime -'+DATA+' -exec ls -l {} \; | '+FILTRO+' ')
    stdin.close()
    diretorio = stdout.readlines()
#    print (diretorio)
    if not diretorio:
       resultadofinal = '0'
    else:
        for linasdiretorio in diretorio:
            resultadodir = linasdiretorio.replace('\n','')
            verificatamanho = resultadodir.split(' ')
#            print (verificatamanho[0])
            if verificatamanho[1] > '1000':
                resultadofinal = '1'
            else:
                resultadofinal = '0'
    print(resultadofinal)
except:
    print('2')

