# Multi-Tenant E-Commerce Platform

A Django-based multi-tenant e-commerce backend where multiple vendors (tenants) can host their stores on a shared platform. Each vendor manages their own products, orders, and customers independently while sharing the same backend infrastructure.

## Features

- Multi-tenant architecture with data isolation
- Role-based access control (Store Owner, Staff, Customer)
- JWT authentication with tenant and role information
- RESTful API for product and order management
- Tenant-specific data access

## Setup Steps

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository** (if using git) or navigate to the project directory

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**:
   ```bash
   python multitenant_ecommerce/manage.py migrate
   ```

6. **Create a superuser** (optional, for admin access):
   ```bash
   python multitenant_ecommerce/manage.py createsuperuser
   ```

### Running the Server

```bash
python multitenant_ecommerce/manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and obtain JWT tokens
- `POST /api/token/refresh/` - Refresh JWT tokens

### Tenant Management
- `GET /api/tenants/` - List all tenants
- `POST /api/tenants/` - Create a new tenant
- `GET /api/tenants/{id}/` - Get a specific tenant
- `PUT /api/tenants/{id}/` - Update a tenant
- `PATCH /api/tenants/{id}/` - Partially update a tenant
- `DELETE /api/tenants/{id}/` - Delete a tenant

### Product Management
- `GET /api/store/products/` - List products (tenant-specific)
- `POST /api/store/products/` - Create a new product (Staff/Owner only)
- `GET /api/store/products/{id}/` - Get a specific product
- `PUT /api/store/products/{id}/` - Update a product (Staff/Owner only)
- `PATCH /api/store/products/{id}/` - Partially update a product (Staff/Owner only)
- `DELETE /api/store/products/{id}/` - Delete a product (Staff/Owner only)

### Order Management
- `GET /api/store/orders/` - List orders (tenant-specific)
- `POST /api/store/orders/` - Create a new order (Customer only)
- `GET /api/store/orders/{id}/` - Get a specific order
- `PUT /api/store/orders/{id}/` - Update an order (Staff/Owner only)
- `PATCH /api/store/orders/{id}/` - Partially update an order (Staff/Owner only)
- `DELETE /api/store/orders/{id}/` - Delete an order (Staff/Owner only)

## Implementation Details

### Multi-Tenancy

Multi-tenancy is implemented by:
1. **Tenant Model**: Each vendor is represented by a Tenant model with unique store information
2. **Data Isolation**: All models (Product, Order, User) have a foreign key relationship to the Tenant model
3. **View-Level Filtering**: Views automatically filter data based on the authenticated user's tenant
4. **Database Separation**: Each tenant's data is isolated in the same database through foreign key relationships

### Role-Based Access Control

Role-based access is implemented through:
1. **User Roles**: Each user has a role (Owner, Staff, or Customer)
2. **Method-Level Permissions**: Permissions are checked directly in view methods for clarity
3. **Role Restrictions**:
   - **Store Owner**: Can manage all data (products, orders, users)
   - **Staff**: Can manage only products and orders
   - **Customer**: Can view products and place orders
4. **Tenant Context**: All operations are automatically scoped to the user's tenant

### Authentication

Authentication uses JWT tokens with:
1. **Simple JWT**: Django REST Framework Simple JWT for token management
2. **Custom Claims**: Tokens include user role and tenant information
3. **Automatic Tenant Assignment**: Users are automatically associated with their tenant during operations

## Technology Stack

- **Django**: Web framework
- **Django REST Framework**: API development
- **Simple JWT**: Authentication
- **SQLite**: Database (default, can be changed to PostgreSQL)
- **Python Decouple**: Environment variable management

## Security Notes

- Secret key is stored in `.env` file and excluded from version control
- All API endpoints require authentication (except registration/login)
- Role-based access control prevents unauthorized operations
- Tenant isolation ensures data privacy between vendors
