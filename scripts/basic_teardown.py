#!/usr/bin/env python3
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

class BasicAWSCleanup:
    def __init__(self, region=os.getenv('AWS_DEFAULT_REGION')):
        self.region = region
        self.dynamodb = boto3.client('dynamodb', region_name=region)

    def delete_dynamodb_tables(self):
        """Delete DynamoDB tables created for the restaurant API"""
        tables = ['menu_items', 'orders']

        for table_name in tables:
            try:
                print(f"Deleting table {table_name}...")
                self.dynamodb.delete_table(TableName=table_name)

                # Wait for table deletion
                waiter = self.dynamodb.get_waiter('table_not_exists')
                waiter.wait(TableName=table_name)
                print(f"Table {table_name} deleted successfully")

            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    print(f"Table {table_name} does not exist")
                else:
                    print(f"Error deleting table {table_name}: {str(e)}")

    def cleanup_all(self):
        """Run cleanup"""
        print("Starting AWS DynamoDB cleanup...")
        self.delete_dynamodb_tables()
        print("\nCleanup complete!")
        print("All DynamoDB tables have been removed.")


if __name__ == '__main__':
    cleanup = BasicAWSCleanup()

    # Ask for confirmation before proceeding
    confirm = input(
        "This will delete all DynamoDB tables created for the restaurant API project. Are you sure? (y/N): ")
    if confirm.lower() == 'y':
        cleanup.cleanup_all()
    else:
        print("Cleanup cancelled.")