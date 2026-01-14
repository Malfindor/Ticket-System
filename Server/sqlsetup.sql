-- Create the database
CREATE DATABASE IF NOT EXISTS `ticket-system`;

-- Use the database
USE `ticket-system`;

-- Create application user
CREATE USER IF NOT EXISTS 'tickets'@'localhost'
IDENTIFIED BY 'password';

-- Grant privileges on the ticket-system database
GRANT ALL PRIVILEGES ON `ticket-system`.* TO 'tickets'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;

-- Create Employees table
CREATE TABLE Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create Tickets table
CREATE TABLE Tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignee INT NULL,
    dueDate DATE,
    notes TEXT,

    CONSTRAINT fk_tickets_assignee
        FOREIGN KEY (assignee)
        REFERENCES Employees(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Optional: index for faster lookups by assignee
CREATE INDEX idx_tickets_assignee ON Tickets(assignee);
