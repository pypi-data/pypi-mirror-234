import abc
from functools import reduce
from typing import Any, Optional

import boto3
from boto3.dynamodb.conditions import And, Attr

ITEMS_LIMIT = 1000


class AbstractDynamoDB(abc.ABC):
    def __init__(self, table: str):
        db = boto3.resource("dynamodb")
        self.table_name = table
        self.table = db.Table(self.table_name)

    def put_item(self, *, data: dict[str, Any]) -> None:
        self.table.put_item(Item=data)

    def get_item(self, *, key: dict[str, Any]) -> Optional[Any]:
        filters = reduce(And, ([Attr(k).contains(v) for k, v in key.items()]))
        query = dict(
            FilterExpression=filters
        )
        query = {k: v for k, v in query.items() if v is not None}
        response = self.table.scan(**query, Limit=ITEMS_LIMIT)
        item: list = response.get("Items", None)
        return item[0] if len(item) > 0 else None

    def get_all_items(self, **kwargs) -> Optional[Any]:
        filters = reduce(
            And, ([Attr(k).contains(v) for k, v in kwargs.items()])
        )
        query = dict(FilterExpression=filters)
        query = {k: v for k, v in query.items() if v is not None}
        response = self.table.scan(**query, Limit=ITEMS_LIMIT)
        items: list = response.get("Items", None)
        return items
