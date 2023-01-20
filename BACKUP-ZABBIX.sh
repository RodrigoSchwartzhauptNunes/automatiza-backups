#!/bin/bash
#Ajustes por
#Junior Moraes
#www.juniormoraes.net.br
#Atualizado 14/10/22 By: Rodrigo S Nunes
#Script original:
#https://github.com/itnihao/zabbix-book/blob/master/03-chapter/Zabbix_MySQLdump_per_table.sh
#
#chmod 700 ${PATH}/Zabbix_MySQLdump_per_table_v2.sh
#crontab -e (0 3 * * * ${PATH}/Zabbix_MySQLdump_per_table_v2.sh)
red='\e[0;31m' #
RED='\e[1;31m' 
green='\e[0;32m' #  
GREEN='\e[1;32m' 
blue='\e[0;34m' #
BLUE='\e[1;34m' 
purple='\e[0;35m' #
PURPLE='\e[1;35m' 
NC='\e[0m' #
source .bashrc
source /etc/profile
ftp=1
########DADOS PARA ALTERAR#######
#DADOS ROOT DO SRV FTP
ROOTUSER=root
ROOTSENHA="XXXXXXXXX"
#DADOS LOGIN E USER FTP
USER=XXXXX
SENHA="XXXXXXXXXXXX"
IP="XXXXXXXXXXXX"
PORTA=21
FTPPATH="127.0.0.1"
MySQL_USER=XXXXXXXXXX
MySQL_PASSWORD=XXXXXXXXX
MySQL_HOST=localhost
MySQL_PORT=3306
########DADOS PARA ALTERAR#######

MySQL_DUMP_PATH=/mysql_backup
MYSQL_BIN_PATH=/usr/bin/mysql
MYSQL_DUMP_BIN_PATH=/usr/bin/mysqldump
MySQL_DATABASE_NAME=zabbix
DATE=$(date '+%d_%m_%Y')

########INICIO DO CODIGO########

MySQLDUMP () {
    [ -d ${MySQL_DUMP_PATH} ] || mkdir ${MySQL_DUMP_PATH}
    cd ${MySQL_DUMP_PATH}
    [ -d logs    ] || mkdir logs
    [ -d ${DATE} ] || mkdir ${DATE}
    cd ${DATE}
    TABLE_NAME_ALL=$(${MYSQL_BIN_PATH} -u${MySQL_USER} -p${MySQL_PASSWORD}  -h${MySQL_HOST} ${MySQL_DATABASE_NAME} -e \
    "show tables"|egrep -v "(Tables_in_zabbix|history*|trends*|acknowledges|alerts|auditlog|events|service_alarms)")
    for TABLE_NAME in ${TABLE_NAME_ALL}
    do
        ${MYSQL_DUMP_BIN_PATH} --opt -u${MySQL_USER} -p${MySQL_PASSWORD} -P${MySQL_PORT} -h${MySQL_HOST} \
        ${MySQL_DATABASE_NAME} ${TABLE_NAME} >${TABLE_NAME}.sql
        sleep 0.01
    done

    [ "$?" == 0 ] && echo "${DATE}: Backup zabbix realizado com sucesso"     >> ${MySQL_DUMP_PATH}/logs/ZabbixMysqlDump.log
    [ "$?" != 0 ] && echo "${DATE}: Backup zabbix sem sucesso" >> ${MySQL_DUMP_PATH}/logs/ZabbixMysqlDump.log
    cd ${MySQL_DUMP_PATH}/
    mkdir ${DATE}/etc && mkdir ${DATE}/usr-lib
    cp -R /etc/zabbix ${DATE}/etc
    cp -R /usr/lib/zabbix ${DATE}/usr-lib
    tar czf ${FTPPATH}_${DATE}.tar.gz ${DATE}
    echo "${DATE}: Backup comprimido com sucesso" >> ${MySQL_DUMP_PATH}/logs/ZabbixMysqlDump.log
    rm -rf ${DATE}
    echo "${DATE}: Arquivos temporarios removidos com sucesso" >> ${MySQL_DUMP_PATH}/logs/ZabbixMysqlDump.log
    cd ${MySQL_DUMP_PATH}/
    [ "$?" == 0 ] && rm -rf $(date +%Y-%m-%d --date='5 days ago')
    ######################################
    ######ENVIO DO BACKUP POR FTP ########
    ######################################
    if [ $ftp == 1 ]; then
    ARQUIVO="${FTPPATH}_${DATE}.tar.gz"
    echo Conectando no FTP remoto ................
    ftp -pivn $IP $PORTA << fim
    user $USER $SENHA
    cd $FTPPATH
    put $ARQUIVO
    close
    bye
    EOF
fim
   sleep 10
   ARQUIVO="${FTPPATH}_${DATE}.tar.gz"
   sshpass -p $ROOTSENHA ssh $IP -l $ROOTUSER -o StrictHostKeyChecking=no "chgrp root /home/$USER/$FTPPATH/$ARQUIVO && chown -R root /home/$USER/$FTPPATH/$ARQUIVO"

fi
    exit 0
}

MySQLImport () {
    cd ${MySQL_DUMP_PATH}
    DATE=$(ls  ${MySQL_DUMP_PATH} |egrep "\b^[0-9]+_[0-9]+_[0-9]+$\b")
    echo -e "${green}${DATE}"
    echo -e "${blue}SInforme a data que voce deseja importar:${NC}"
    read SELECT_DATE
    if [ -d "${SELECT_DATE}" ];then
        echo -e "voce selecionou ${green}${SELECT_DATE}${NC}, deseja continuar? ${red}(yes|y|Y)${NC}, ou qualquer tecla para sair"
        read Input
        [[ 'yes|y|Y' =~ "${Input}" ]]
        status="$?"
        if [ "${status}" == "0"  ];then
            echo "importando SQL....... Aguarde......."
        else
            exit 1
        fi
        cd ${SELECT_DATE}
        for PER_TABEL_SQL in $(ls *.sql)
        do
           ${MYSQL_BIN_PATH} -u${MySQL_USER} -p${MySQL_PASSWORD}  -h${MySQL_HOST} ${MySQL_DATABASE_NAME} < ${PER_TABEL_SQL}
           echo -e "importando ${PER_TABEL_SQL} ${PURPLE}........................${NC}"
        done 
        echo "importacao do SQL realizada com sucesso, verifique o Zabbix Database"
        cp -R usr-lib/zabbix/* /var/lib/zabbix/
        cp -R etc/zabbix/* /etc/zabbix/
        echo "importacao dos arquivos de configuracao realizada com sucesso, reinicie o Zabbix"
    else 
        echo "O diretorio ${SELECT_DATE} nao existe" 
    fi
}

case "$1" in
MySQLDUMP|mysqldump)
    MySQLDUMP
    ;;
MySQLImport|mysqlimport)
    MySQLImport
    ;;
*)
    echo "Uso: $0 {(MySQLDUMP|mysqldump) (MySQLImport|mysqlimport)}"
    ;;
esac


