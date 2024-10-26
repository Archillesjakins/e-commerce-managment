
# E-Commerce Order Management System

This is a simple e-commerce application built with Flask and SQLAlchemy for managing customers, products, and orders. The system includes customer registration, product and order management, order history viewing, and order status updating.

## Table of Contents
- [Setup](#setup)
- [Database Configuration](#database-configuration)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Using the Application](#using-the-application)

---

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/ecommerce-app.git
   cd ecommerce-app
   ```

2. **Install the required packages**:
   Ensure you have Python 3 and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the project root with your database credentials:
   ```
   username=your_mysql_username
   password=your_mysql_password
   ```

### Database Configuration

1. **Set up the MySQL Database**:
   - Ensure you have a MySQL database named `ecommerce`.
   - Configure your `.env` file with the correct credentials.
  
2. **Initialize the Database**:
   In the project directory, run:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Features

- **Customer Management**: Register new customers with basic information.
- **Product Management**: Products with stock, price, and other details.
- **Order Management**: Place new orders for customers, with items and quantities.
- **Order History**: View the order history of each customer.
- **Order Status Update**: Change the status of an order (e.g., pending, shipped, delivered, canceled).

### API Endpoints

1. **Homepage**  
   **Endpoint**: `GET /`  
   **Description**: Displays the application homepage with forms to interact with the API.

2. **Register Customer**  
   **Endpoint**: `POST /register_customer`  
   **Description**: Registers a new customer.  
   **Request JSON**:
   ```json
   {
     "name": "Customer Name",
     "email": "email@example.com",
     "phone_number": "1234567890"
   }
   ```

3. **Place Order**  
   **Endpoint**: `POST /place_order`  
   **Description**: Places an order for a customer with multiple items.  
   **Request JSON**:
   ```json
   {
     "customer_id": 1,
     "items": [
       {
         "product_id": 101,
         "quantity": 2
       },
       {
         "product_id": 102,
         "quantity": 5
       }
     ]
   }
   ```

4. **Order History**  
   **Endpoint**: `GET /order_history/<customer_id>`  
   **Description**: Streams the order history for a customer.

5. **Update Order Status**  
   **Endpoint**: `PATCH /update_order_status`  
   **Description**: Updates the status of a specific order.  
   **Request JSON**:
   ```json
   {
     "order_id": 1,
     "status": "shipped"
   }
   ```

### Using the Application

1. **Start the Flask Application**:
   ```bash
   python app.py
   ```
   The application will run on `http://localhost:5000`.

2. **Access the Homepage**:
   Open a web browser and navigate to `http://localhost:5000` to view the main page with forms for registration, order placement, and status updating.

3. **Register a Customer**:
   - Fill in the name, email, and phone number in the "Register Customer" form.
   - Submit to register a new customer.

4. **Place an Order**:
   - Enter the customer ID, then specify multiple product IDs and quantities.
   - Submit to place the order.

5. **View Order History**:
   - Visit `/order_history/<customer_id>` in the browser (replace `<customer_id>` with an actual ID) to view past orders.

6. **Update Order Status**:
   - Enter an order ID and select the new status in the "Update Order Status" form.
   - Submit to update the order's status.

### Additional Notes

- **Decorator for Stock Validation**: `validate_stock` decorator verifies if there’s sufficient stock before placing an order.
- **Lambda for Discounts**: Orders with more than 10 items receive a 10% discount using a lambda function.
- **Generator for Order History**: Streams order history with a generator function to efficiently handle large datasets.
