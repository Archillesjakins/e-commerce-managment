const apiUrl = 'http://127.0.0.1:5000';  // Base URL of the Flask app

// Register Customer
document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone_number = document.getElementById("phone_number").value;

    const response = await fetch(`${apiUrl}/register_customer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, phone_number })
    });

    const result = await response.json();
    document.getElementById("registerResult").innerText = result.message || result.error;
});

// Place Order
document.getElementById("orderForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const customer_id = document.getElementById("customer_id").value;
    const items = [...document.querySelectorAll('.order-item')].map(item => ({
        product_id: item.querySelector('.product_id').value,
        quantity: item.querySelector('.quantity').value
    }));

    const response = await fetch(`${apiUrl}/place_order`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ customer_id, items })
    });

    const result = await response.json();
    document.getElementById("orderResult").innerText = result.message || result.error;
});

// Add another item to the order form
function addOrderItem() {
    const orderItems = document.getElementById("orderItems");
    const newItem = document.createElement("div");
    newItem.classList.add("order-item");
    newItem.innerHTML = `
        <label for="product_id">Product ID:</label>
        <input type="number" class="product_id" required>
        <label for="quantity">Quantity:</label>
        <input type="number" class="quantity" min="1" required>
    `;
    orderItems.appendChild(newItem);
}

// Update Order Status
document.getElementById("updateStatusForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const order_id = document.getElementById("order_id").value;
    const status = document.getElementById("status").value;

    const response = await fetch(`${apiUrl}/update_order_status`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ order_id, status })
    });

    const result = await response.json();
    document.getElementById("statusResult").innerText = result.message || result.error;
});
