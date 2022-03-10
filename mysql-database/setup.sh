#!/bin/bash
ROOT_PASS="toor"
mysql -u root --password=$ROOT_PASS --execute "CREATE DATABASE res_database;"
mysql -u root --password=$ROOT_PASS res_database < ./schema.ddl
mysql -u root --password=$ROOT_PASS --execute "CREATE USER 'resdb'@'%' IDENTIFIED BY 'password';"
mysql -u root --password=$ROOT_PASS --execute "GRANT ALL PRIVILEGES ON res_database.* TO 'resdb'@'%';"
#mysql -u root --password=$ROOT_PASS --execute "UPDATE mysql.user SET host='%' WHERE user='resdb';"
