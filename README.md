# Restaurant Ordering System

A full-stack restaurant management system built with FastAPI, DynamoDB, and React. This system helps restaurants manage their menu and orders through an intuitive web interface.

## Features

- **Menu Management**: Add, edit, and remove menu items with prices and categories
- **Order Processing**: Create and track customer orders
- **Dashboard**: View key metrics including revenue, popular items, and recent orders
- **Real-time Updates**: Instant updates for orders and menu changes
- **Discount Support**: Apply percentage-based discounts to orders

## Tech Stack

**Backend:**
- FastAPI
- DynamoDB
- Python 3.11+
- Boto3

**Frontend:**
- React
- TypeScript
- Tailwind CSS
- Vite

## Getting Started

### Prerequisites

1. Python 3.11 or higher
2. Node.js 16 or higher
3. AWS account with configured credentials
4. Git

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd restaurant-api
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up AWS credentials:
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your preferred region (e.g., us-east-1)
```

5. Initialize the database:
```bash
./manage_db.sh setup
```

6. Start the API server:
```bash
uvicorn api.app:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Build the frontend:
```bash
npm run build
```

4. Start the development server:
```bash
npm run dev
```

## Project Structure

```
restaurant-api/
├── api/
│   ├── controllers/    # API route handlers
│   ├── models/         # Data models
│   ├── repositories/   # Database interaction
│   └── schemas/        # Request/response schemas
├── frontend/
│   └── src/
│       ├── components/ # React components
│       ├── hooks/      # Custom hooks
│       ├── pages/      # Page components
│       ├── services/   # API client services
│       └── types/      # TypeScript types
└── scripts/            # Database management scripts
```

## API Endpoints

### Menu Items

- `GET /menu/` - List all menu items
- `GET /menu/{item_id}` - Get a specific menu item
- `POST /menu/` - Create a new menu item
- `PUT /menu/{item_id}` - Update a menu item
- `PATCH /menu/{item_id}` - Partially update a menu item
- `DELETE /menu/{item_id}` - Delete a menu item

### Orders

- `GET /orders/` - List all orders
- `GET /orders/{order_id}` - Get a specific order
- `POST /orders/` - Create a new order
- `PUT /orders/{order_id}` - Update an order
- `PATCH /orders/{order_id}` - Partially update an order
- `DELETE /orders/{order_id}` - Delete an order


## Cleanup

To remove all DynamoDB tables and data:
```bash
./manage_db.sh teardown
```