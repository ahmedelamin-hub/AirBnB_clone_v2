-- Use the root user to run this script.
-- Ensure that the user has sufficient privileges to create databases and manage users.

-- Create the database if it does not already exist.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user with specified credentials if it does not exist.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant the user all privileges on the new database.
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Ensure the user has only SELECT privilege on the performance_schema database.
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Make changes take effect immediately
FLUSH PRIVILEGES;
