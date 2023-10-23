-- prepares a MySQL server for the project
-- creates a new user and a new database
CREATE DATABASE IF NOT EXISTS cbase_test_db;
CREATE USER IF NOT EXISTS 'cbase_test'@'localhost' IDENTIFIED BY 'cbase_test_pwd';
GRANT ALL PRIVILEGES ON cbase_test_db.* TO 'cbase_test'@'localhost';
FLUSH PRIVILEGES;
