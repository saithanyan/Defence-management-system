CREATE DATABASE defense_db;

USE defense_db;

CREATE TABLE assets (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL
);

-- Insert sample data
INSERT INTO assets VALUES ('a001', 'Tank', 'Military Vehicle', 'Operational');
INSERT INTO assets VALUES ('a002', 'Helicopter', 'Aerial Vehicle', 'Under Maintenance');
INSERT INTO assets VALUES ('a003', 'Fighter Jet', 'Aircraft', 'Operational');

-- Select all records
SELECT * FROM assets;
