# Order Flow Backend

A comprehensive Flask-based backend API for an order management system, featuring user authentication, menu management, shopping cart functionality, order processing, and M-Pesa payment integration.

##  Features

- **User Authentication & Authorization**
  - JWT-based authentication
  - User registration and login
  - Role-based access control
  - Admin user seeding

- **Menu Management**
  - CRUD operations for menu items
  - Category-based organization
  - Price and availability management

- **Shopping Cart**
  - Add/remove items from cart
  - Quantity management
  - Cart persistence per user

- **Order Management**
  - Complete order lifecycle
  - Order status tracking
  - Customer information management

- **Payment Integration**
  - M-Pesa payment processing
  - Secure payment handling
  - Transaction status tracking

##  Tech Stack

- **Backend Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Password Hashing**: Flask-Bcrypt
- **CORS**: Flask-CORS
- **Payment**: M-Pesa API integration
- **Environment Management**: python-dotenv
- **Dependency Management**: Pipenv

##  Prerequisites

- Python 3.8+
- pipenv
- SQLite3

##  Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abdirahmanwsh-cmd/phase-4-project-order-flow-backend.git
   cd phase-4-project-order-flow-backend
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Activate virtual environment**
   ```bash
   pipenv shell
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   FLASK_APP=order-flow-backend/main.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   ```

##  Running the Application

1. **Start the development server**
   ```bash
   pipenv run python order-flow-backend/main.py
   ```

2. **The API will be available at**: `http://127.0.0.1:5555`

##  API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get user profile

### Menu Management
- `GET /api/menu` - Get all menu items
- `POST /api/menu` - Create menu item (Admin only)
- `GET /api/menu/<id>` - Get specific menu item
- `PUT /api/menu/<id>` - Update menu item (Admin only)
- `DELETE /api/menu/<id>` - Delete menu item (Admin only)

### Cart Management
- `GET /api/cart` - Get user's cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/<item_id>` - Update cart item quantity
- `DELETE /api/cart/<item_id>` - Remove item from cart
- `DELETE /api/cart` - Clear entire cart

### Order Management
- `GET /api/orders` - Get user's orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get specific order
- `PUT /api/orders/<id>/status` - Update order status (Admin only)

### Payment
- `POST /api/payments/mpesa/stkpush` - Initiate M-Pesa payment
- `POST /api/payments/mpesa/callback` - M-Pesa payment callback

## 🗄️ Database Schema

### Users
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- role_id (Foreign Key)

### Roles
- id (Primary Key)
- name

### Menu Items
- id (Primary Key)
- name
- description
- price
- category
- available (Boolean)

### Cart Items
- id (Primary Key)
- user_id (Foreign Key)
- menu_item_id (Foreign Key)
- quantity

### Orders
- id (Primary Key)
- customer_name
- phone
- email
- address
- city
- total
- status
- user_id (Foreign Key)
- created_at

### Order Items
- id (Primary Key)
- order_id (Foreign Key)
- menu_item_id (Foreign Key)
- quantity
- price

##  Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

##  Payment Integration

The system integrates with M-Pesa for payment processing:

1. **STK Push**: Initiates payment request to customer's phone
2. **Callback**: Handles payment confirmation from M-Pesa
3. **Status Tracking**: Monitors payment status

##  Testing the API

### Example: Create an Order
```bash
curl -X POST http://127.0.0.1:5555/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "customer_name": "John Doe",
    "phone": "0712345678",
    "email": "john@example.com",
    "address": "123 Main St",
    "city": "Nairobi",
    "total": 2400,
    "items": [
      {"menu_item_id": 1, "quantity": 2, "price": 1200}
    ]
  }'
```

### Example: Register a User
```bash
curl -X POST http://127.0.0.1:5555/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

##  Project Structure

```
order-flow-backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── menu_item.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── routes/              # API route handlers
│   │   ├── auth_routes.py
│   │   ├── menu_routes.py
│   │   ├── cart_routes.py
│   │   ├── order_routes.py
│   │   └── payment_routes.py
│   ├── services/            # Business logic services
│   │   ├── mpesa_service.py
│   │   └── seed_admin.py
│   └── utils/               # Utility functions
│       ├── auth_helpers.py
│       └── order_status.py
├── instance/                # Database files
├── config.py               # Configuration settings
└── main.py                # Application entry point
```

##  Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- CORS configuration for frontend integration
- Input validation and sanitization
- Role-based access control

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the LICENSE file for details.
# live link
https://phase-4-project-order-flow-backend.onrender.com/api/docs

##  Support

For questions or support, please open an issue on GitHub or contact the development team.

---


