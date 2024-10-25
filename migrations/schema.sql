-- Create the database
CREATE DATABASE ecommerce;

-- Switch to the newly created database
USE ecommerce;

-- Create the Customers table
CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each customer
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,          -- Ensure no duplicate emails
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Orders table with a foreign key referencing Customers
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique order ID
    customer_id INT,                               -- ID of the customer who placed the order
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date when the order was placed
    total_amount DECIMAL(10, 2) NOT NULL,          -- Total price of the order
    status ENUM('pending', 'shipped', 'delivered', 'canceled') DEFAULT 'pending',
    
    -- Foreign key constraint to maintain integrity
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

-- Create a table to hold order items
CREATE TABLE OrderItems (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique order item ID
    order_id INT,                                  -- ID of the order
    product_name VARCHAR(255) NOT NULL,            -- Product name
    quantity INT NOT NULL,                         -- Quantity of the product
    unit_price DECIMAL(10, 2) NOT NULL,            -- Price per unit of the product
    total_price DECIMAL(10, 2) AS (quantity * unit_price) STORED, -- Calculated total price

    -- Foreign key constraint
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);
