import os
from datetime import datetime

import boto3
from decimal import Decimal, ROUND_DOWN
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

class BasicAWSSetup:
    def __init__(self, region=os.getenv('AWS_DEFAULT_REGION')):
        self.region = region
        self.dynamodb = boto3.client('dynamodb', region_name=region)

    def create_dynamodb_tables(self):
        """Create DynamoDB tables for the restaurant API"""
        tables = {
            'menu_items': {
                'AttributeDefinitions': [
                    {'AttributeName': 'item_id', 'AttributeType': 'S'}
                ],
                'KeySchema': [
                    {'AttributeName': 'item_id', 'KeyType': 'HASH'}
                ]
            },
            'orders': {
                'AttributeDefinitions': [
                    {'AttributeName': 'order_id', 'AttributeType': 'S'}
                ],
                'KeySchema': [
                    {'AttributeName': 'order_id', 'KeyType': 'HASH'}
                ]
            }
        }

        for table_name, table_config in tables.items():
            try:
                print(f"Creating table {table_name}...")
                self.dynamodb.create_table(
                    TableName=table_name,
                    AttributeDefinitions=table_config['AttributeDefinitions'],
                    KeySchema=table_config['KeySchema'],
                    BillingMode='PAY_PER_REQUEST'  # More cost-effective for development
                )
                # Wait for table creation
                waiter = self.dynamodb.get_waiter('table_exists')
                waiter.wait(TableName=table_name)
                print(f"Table {table_name} created successfully")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceInUseException':
                    print(f"Table {table_name} already exists")
                else:
                    print(f"Error creating table {table_name}: {str(e)}")

    def populate_sample_data(self):
        """Add sample data to DynamoDB tables"""
        # Sample menu items with Decimal for numeric values
        menu_items = [
            {
                'item_id': 'item1',
                'name': 'Margherita Pizza',
                'price': Decimal('12.99'),
                'description': 'Classic tomato and mozzarella pizza',
                'category': 'Pizza'
            },
            {
                'item_id': 'item2',
                'name': 'Spaghetti Carbonara',
                'price': Decimal('14.99'),
                'description': 'Creamy pasta with pancetta',
                'category': 'Pasta'
            },
            {
                'item_id': 'item3',
                'name': 'Caesar Salad',
                'price': Decimal('8.99'),
                'description': 'Fresh romaine lettuce with Caesar dressing',
                'category': 'Salad'
            }
        ]

        orders = [
        {
                'order_id': 'id1',
                'order_number': '000001',
                'items': [
                    {'item':
                        {
                            'item_id': 'item2',
                            'name': 'Spaghetti Carbonara',
                            'price': Decimal('14.99'),
                            'description': 'Creamy pasta with pancetta',
                            'category': 'Pasta'
                        },
                        'quantity': 1
                    },
                    {
                        'item':
                            {
                                'item_id': 'item3',
                                'name': 'Caesar Salad',
                                'price': Decimal('8.99'),
                                'description': 'Fresh romaine lettuce with Caesar dressing',
                                'category': 'Salad'
                            },
                        'quantity': 1
                    }
                ],
                'subtotal': Decimal('23.98'),
                'total': Decimal('23.98'),
                'discount_pct': Decimal('0.00'),
                'order_date': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            },
            {
                'order_id': 'id2',
                'order_number': '000002',
                'items': [
                    {
                        'item':
                            {
                                'item_id': 'item1',
                                'name': 'Margherita Pizza',
                                'price': Decimal('12.99'),
                                'description': 'Classic tomato and mozzarella pizza',
                                'category': 'Pizza'
                            },
                        'quantity': 1,
                    }],
                'subtotal': Decimal('12.99'),
                'discount_pct': Decimal('0.25'),
                'total': Decimal('9.7425').quantize(Decimal('0.01'), rounding=ROUND_DOWN),
                'order_date': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            },
        ]

        menu_table = boto3.resource('dynamodb').Table('menu_items')
        for item in menu_items:
            try:
                menu_table.put_item(Item=item)
                print(f"Added menu item: {item['name']}")
            except ClientError as e:
                print(f"Error adding item {item['name']}: {str(e)}")

        order_table = boto3.resource('dynamodb').Table('orders')
        for order in orders:
            try:
                order_table.put_item(Item=order)
                print(f"Added order: {order['order_number']}")
            except ClientError as e:
                print(f"Error adding order {order['order_number']}: {str(e)}")

    def setup_all(self):
        """Run all setup steps"""
        print("Starting AWS DynamoDB setup...")
        print("\nStep 1: Creating DynamoDB tables...")
        self.create_dynamodb_tables()
        print("\ndebug: scan tables")
        print(boto3.resource('dynamodb').Table('menu_items').scan())
        print(boto3.resource('dynamodb').Table('orders').scan())
        print("\n\nStep 2: Adding sample data...")
        self.populate_sample_data()
        print("\ndebug: scan tables")
        print(boto3.resource('dynamodb').Table('menu_items').scan())
        print(boto3.resource('dynamodb').Table('orders').scan())
        print("\n\nSetup complete!")


if __name__ == '__main__':
    setup = BasicAWSSetup()
    setup.setup_all()