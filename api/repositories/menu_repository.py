import os

import boto3
import uuid
from botocore.exceptions import ClientError
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

class MenuRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('menu_items')

    async def create_item(self, item_data: dict) -> dict:
        item_data['item_id'] = str(uuid.uuid4())
        try:
            self.table.put_item(Item=item_data)
            return item_data
        except ClientError as e:
            print(f"Error creating item: {e.response['Error']['Message']}")
            raise

    async def get_all(self) -> list:
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error getting items: {e.response['Error']['Message']}")
            raise

    async def get_by_id(self, item_id: str) -> Optional[dict]:
        try:
            response = self.table.get_item(Key={'item_id': item_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting item: {e.response['Error']['Message']}")
            raise

    async def update_item(self, item_id: str, item_data: dict) -> dict:
        # Remove None values from item_data
        update_data = {k: v for k, v in item_data.items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid update data provided")

        # Build update expression
        update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in update_data)
        expression_attribute_names = {f"#{k}": k for k in update_data}
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}

        try:
            response = self.table.update_item(
                Key={'item_id': item_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes', {})
        except ClientError as e:
            print(f"Error updating item: {e.response['Error']['Message']}")
            raise

    async def patch_item(self, item_id: str, item_data: dict) -> dict:
        # Similar to update but only modifies specified fields
        return await self.update_item(item_id, item_data)

    async def delete_item(self, item_id: str) -> bool:
        try:
            self.table.delete_item(Key={'item_id': item_id})
            return True
        except ClientError as e:
            print(f"Error deleting item: {e.response['Error']['Message']}")
            raise