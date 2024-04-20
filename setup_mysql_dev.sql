-- setup_mysql_dev.sql
-- Run this script with the MySQL root or another privileged user

-- Creating the database if it does not already exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creating the user if it does not already exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Granting privileges on the hbnb_dev_db database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Revoking all privileges on other databases
REVOKE ALL PRIVILEGES ON *.* FROM 'hbnb_dev'@'localhost';
GRANT USAGE ON *.* TO 'hbnb_dev'@'localhost';

-- Granting SELECT privilege on the performance_schema database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Applying the changes
FLUSH PRIVILEGES;

-- Display commands to check the setup, to be run after script execution
-- You can run these commands to ensure everything is set up correctly:
-- echo "SHOW DATABASES;" | mysql -uhbnb_dev -p | grep hbnb_dev_db
-- echo "SHOW GRANTS FOR 'hbnb_dev'@'localhost';" | mysql -uroot -p
