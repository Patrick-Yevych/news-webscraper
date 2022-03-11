CREATE DATABASE res_database;
CREATE USER 'resdb'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON res_database.* TO 'resdb'@'%';
UPDATE mysql.user SET host='%' WHERE user='resdb';