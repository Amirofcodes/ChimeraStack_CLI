-- Create developer user
CREATE USER IF NOT EXISTS 'developer'@'%' IDENTIFIED BY 'devpassword';
GRANT ALL PRIVILEGES ON exampledb.* TO 'developer'@'%';
FLUSH PRIVILEGES;

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
