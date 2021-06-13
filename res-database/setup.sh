#!/bin/bash
ROOT_PASS="newpassword"
mysql -u root -p --execute "ALTER USER 'root'@'localhost' IDENTIFIED BY '$ROOT_PASS';"
mysql -u root --password=$ROOT_PASS --execute "CREATE DATABASE res_database;"
mysql -u root --password=$ROOT_PASS news_database < ./schema.ddl