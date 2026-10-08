# ==========================================
# E-COMMERCE INVENTORY & ORDER SYSTEM
# ==========================================


# ---------- USER CLASS ----------
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# ---------- CUSTOMER CLASS ----------
class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.cart = {}


# ---------- ADMIN CLASS ----------
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)


# ---------- PRODUCT CLASS ----------
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


# ---------- ORDER CLASS ----------
class Order:
    def __init__(self, customer, items, total):
        self.customer = customer
        self.items = items
        self.total = total


# ==========================================
# DATA
# ==========================================

customers = []
products = []
orders = []


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def find_customer(username):
    for customer in customers:
        if customer.username == username:
            return customer

    return None


def find_product(product_id):
    for product in products:
        if product.product_id == product_id:
            return product

    return None


# ==========================================
# REGISTER
# ==========================================

def register():
    print("\n--- CUSTOMER REGISTRATION ---")

    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check for duplicate username
    if find_customer(username):
        print("Username already exists!")
        return

    customer = Customer(username, password)
    customers.append(customer)

    print("Registration successful!")


# ==========================================
# LOGIN
# ==========================================

def login():
    print("\n--- CUSTOMER LOGIN ---")

    username = input("Enter username: ")
    password = input("Enter password: ")

    customer = find_customer(username)

    if customer and customer.password == password:
        print("Login successful!")
        print("Welcome", customer.username)

        customer_menu(customer)

    else:
        print("Invalid username or password!")


# ==========================================
# DISPLAY PRODUCTS
# ==========================================

def display_products():
    print("\n--- PRODUCTS ---")

    if len(products) == 0:
        print("No products available.")
        return

    for product in products:
        print(
            f"ID: {product.product_id} | "
            f"Name: {product.name} | "
            f"Price: ₦{product.price} | "
            f"Stock: {product.stock}"
        )


# ==========================================
# ADD PRODUCT
# ==========================================

def add_product():
    print("\n--- ADD PRODUCT ---")

    product_id = int(input("Enter product ID: "))

    # Prevent duplicate product ID
    if find_product(product_id):
        print("Product ID already exists!")
        return

    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))

    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return

    product = Product(product_id, name, price, stock)
    products.append(product)

    print("Product added successfully!")


# ==========================================
# UPDATE PRODUCT
# ==========================================

def update_product():
    print("\n--- UPDATE PRODUCT ---")

    product_id = int(input("Enter product ID: "))

    product = find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Current name:", product.name)
    print("Current price:", product.price)
    print("Current stock:", product.stock)

    product.name = input("Enter new name: ")
    product.price = float(input("Enter new price: "))
    product.stock = int(input("Enter new stock: "))

    if product.price < 0 or product.stock < 0:
        print("Price and stock cannot be negative.")
        return

    print("Product updated successfully!")


# ==========================================
# DELETE PRODUCT
# ==========================================

def delete_product():
    print("\n--- DELETE PRODUCT ---")

    product_id = int(input("Enter product ID: "))

    product = find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    products.remove(product)

    print("Product deleted successfully!")


# ==========================================
# ADD TO CART
# ==========================================

def add_to_cart(customer):
    display_products()

    try:
        product_id = int(input("\nEnter product ID: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Please enter numbers only.")
        return

    product = find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if product.stock == 0:
        print("This product is out of stock.")
        return

    # Check if requested quantity is available
    current_quantity = customer.cart.get(product_id, 0)

    if current_quantity + quantity > product.stock:
        print("Not enough stock available.")
        return

    # Add product to cart
    customer.cart[product_id] = current_quantity + quantity

    print("Product added to cart!")


# ==========================================
# VIEW CART
# ==========================================

def view_cart(customer):
    print("\n--- YOUR CART ---")

    if len(customer.cart) == 0:
        print("Your cart is empty.")
        return

    total = 0

    for product_id, quantity in customer.cart.items():

        product = find_product(product_id)

        if product:
            cost = product.price * quantity
            total += cost

            print(
                f"{product.name} | "
                f"Quantity: {quantity} | "
                f"Price: ₦{product.price} | "
                f"Cost: ₦{cost}"
            )

    print("-------------------------")
    print("Total: ₦", total)


# ==========================================
# PLACE ORDER
# ==========================================

def place_order(customer):
    print("\n--- PLACE ORDER ---")

    if len(customer.cart) == 0:
        print("Your cart is empty.")
        return

    total = 0

    # Check stock first
    for product_id, quantity in customer.cart.items():

        product = find_product(product_id)

        if product is None:
            print("A product in your cart no longer exists.")
            return

        if quantity > product.stock:
            print(f"Not enough stock for {product.name}.")
            return

        total += product.price * quantity

    # Reduce stock
    for product_id, quantity in customer.cart.items():

        product = find_product(product_id)

        product.stock -= quantity

    # Create order
    order = Order(customer, customer.cart.copy(), total)

    orders.append(order)

    # Empty cart
    customer.cart.clear()

    print("Order placed successfully!")
    print("Total amount: ₦", total)


# ==========================================
# CUSTOMER MENU
# ==========================================

def customer_menu(customer):

    while True:

        print("\n========== CUSTOMER MENU ==========")
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. View Cart")
        print("4. Place Order")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            display_products()

        elif choice == "2":
            add_to_cart(customer)

        elif choice == "3":
            view_cart(customer)

        elif choice == "4":
            place_order(customer)

        elif choice == "5":
            print("Logged out.")
            break

        else:
            print("Invalid option.")


# ==========================================
# ADMIN MENU
# ==========================================

def admin_menu():

    while True:

        print("\n========== ADMIN MENU ==========")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            display_products()

        elif choice == "3":
            update_product()

        elif choice == "4":
            delete_product()

        elif choice == "5":
            print("Admin logged out.")
            break

        else:
            print("Invalid option.")


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    # Create default admin
    admin = Admin("admin", "1234")

    # Add some products
    products.append(Product(1, "Laptop", 500000, 5))
    products.append(Product(2, "Phone", 250000, 10))
    products.append(Product(3, "Headphones", 25000, 15))

    while True:

        print("\n================================")
        print("     MINI E-COMMERCE SYSTEM")
        print("================================")

        print("1. Register")
        print("2. Customer Login")
        print("3. Admin Login")
        print("4. View Products")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register()

        elif choice == "2":
            login()

        elif choice == "3":

            username = input("Enter admin username: ")
            password = input("Enter admin password: ")

            if username == admin.username and password == admin.password:
                print("Admin login successful!")
                admin_menu()

            else:
                print("Invalid admin username or password!")

        elif choice == "4":
            display_products()

        elif choice == "5":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid option.")


# Start program
main()