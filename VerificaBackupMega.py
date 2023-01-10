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
#CRIADO 10/01/2023
#====================================================================
#BIBLIOTECAS UTILIZADAS
import sys
import paramiko
import pickle
import itertools
from datetime import datetime
import re
today = datetime.now()
day = today.day
month = today.month
year = today.year
hora = today.hour
min = today.minute
seg = today.second
#====================================================================
#ARQGUMENTOS
#SERVIDOR FTP
address = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

#DATA
now = datetime.now()
month = now.strftime("%m"); year = now.strftime("%Y"); day = now.strftime("%d")
DATA = year+'-'+month+'-'+day
#====================================================================
#ACESSO
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=address, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('rclone lsf  --format "tsp" mega:backup')
    stdin.close()
    diretorio = stdout.readlines()
    if not diretorio:
       resultadofinal = '0'
    else:
        for linasdiretorio in diretorio:
            resultadodir = linasdiretorio.replace('\n','')
            verificatamanho = resultadodir.split(' ')
            if verificatamanho[0] == DATA:
                resultadofinal = '1'
            else:
                resultadofinal = '0'
    print(resultadofinal)
except:
    print('2')
