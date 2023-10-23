-- prepares a MySQL server for the project
-- creates a new user and a new database
CREATE DATABASE IF NOT EXISTS cbase_dev_db;
CREATE USER IF NOT EXISTS 'cbase_dev'@'localhost' IDENTIFIED BY 'cbase_dev_pwd';
GRANT ALL PRIVILEGES ON cbase_dev_db.* TO 'cbase_dev'@'localhost';
FLUSH PRIVILEGES;
