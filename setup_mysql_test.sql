-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the user if it doesn't already exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant the user all privileges on the hbnb_test_db database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Revoke all privileges from all databases to clean up any previously granted privileges
REVOKE ALL PRIVILEGES ON *.* FROM 'hbnb_test'@'localhost';
GRANT USAGE ON *.* TO 'hbnb_test'@'localhost';  -- This grants the right to connect without any database privileges

-- Grant SELECT privilege on the performance_schema database
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply the new privileges
FLUSH PRIVILEGES;

-- Commands for verification (to be run after executing the script):
-- echo "SHOW DATABASES;" | mysql -uhbnb_test -p | grep hbnb_test_db
-- echo "SHOW GRANTS FOR 'hbnb_test'@'localhost';" | mysql -uroot -p
