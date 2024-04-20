-- Use the root user to run this script.
-- Make sure that the root user has sufficient privileges to create databases and manage users.

-- Create the test database if it does not already exist.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the user with specified credentials if it does not exist.
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant the user all privileges on the test database.
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Ensure the user has only SELECT privilege on the performance_schema database.
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Refresh the privileges to ensure all changes take effect immediately.
FLUSH PRIVILEGES;
