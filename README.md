# automatiza-backups
Código desenvolvido em python para automatizar backups de equipamentos de redes.

O código utiliza python3 com a biblioteca paramikto e apiZabbix para obter listas de hosts. Com estas listar o mesmo identifica o fabricante e acessa individualmente cada equipamento para realizar a ação de backups necessária.

OBRIGATORIO:

  Ter usuario ssh no Zabbix e nos equipamentos

Dependencias para todas o código:

		apt update

		apt-get install python3

		apt install python3-pip

		pip3 install --upgrade pip

		pip3 --version

		pip3 install paramiko
    
		pip3 install zabbix-api

		pip3 install PyJWT
