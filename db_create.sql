CREATE DATABASE integrity_checker;
USE integrity_checker;
CREATE TABLE file_hashes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(255) NOT NULL,
    hash_value VARCHAR(64) NOT NULL
);


-- Grant all privileges on the integrity_checker database to the root user
GRANT ALL PRIVILEGES ON integrity_checker.* TO 'root'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Verify the grants
SHOW GRANTS FOR 'root'@'localhost';

select * from file_hashes;

ALTER TABLE file_hashes ADD COLUMN scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

truncate file_hashes;


SELECT User, Host FROM mysql.user;