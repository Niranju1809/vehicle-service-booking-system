CREATE DATABASE service;
USE service;
CREATE TABLE booking(
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    contact_number VARCHAR(11) NOT NULL,
    vehicle_model VARCHAR(100),
    registration_number VARCHAR(30) UNIQUE,
    service_type VARCHAR(50),
    service_date DATE,
    assigned_mechanic VARCHAR(100),
    service_status VARCHAR(30)
);
SELECT * FROM booking;