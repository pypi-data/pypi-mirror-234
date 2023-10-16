from typing import List, Union

import boto3
from boto3.dynamodb.conditions import Key
from pydantic import TypeAdapter

from rastless.db.models import ColorMap, LayerModel, LayerStepModel, PermissionModel


class Database:
    def __init__(self, table_name, resource=None):
        if not resource:
            resource = boto3.resource('dynamodb')

        self.table_name = table_name
        self.resource = resource
        self.table = self.resource.Table(table_name)

    def scan_table(self, pk_startswith, sk_startswith=None):
        filter_expression = Key("pk").begins_with(pk_startswith)
        if sk_startswith:
            filter_expression &= Key("sk").begins_with(sk_startswith)

        scan_kwargs = {
            "FilterExpression": filter_expression
        }

        items_list = []

        done = False
        start_key = None

        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.table.scan(**scan_kwargs)
            if items := response.get("Items"):
                items_list.extend(items)
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return items_list

    def query(self, query_params: dict) -> List:
        response = self.table.query(**query_params)
        items = response.get("Items", [])

        while 'LastEvaluatedKey' in response:
            response = self.table.query(ExclusiveStartKey=response['LastEvaluatedKey'], **query_params)
            items.extend(response['Items'])

        return items

    def get_item(self, pk, sk, gsi=None):
        response = self.table.get_item(Key={
            "pk": pk,
            "sk": sk
        })
        return response.get("Item")

    def list_layers(self):
        query_parameters = {
            "KeyConditionExpression": Key('pk').eq("layer")
        }
        return self.query(query_parameters)

    def add_permissions(self, permissions: List[PermissionModel]):
        with self.table.batch_writer() as writer:
            for permission in permissions:
                writer.put_item(
                    Item=permission.model_dump(by_alias=True)
                )

    def get_permission(self, permission, layer_id):
        return self.get_item(f"permission#{permission}", f"layer#{layer_id}")

    def get_layers_for_permission(self, permission):
        query_parameters = {
            "KeyConditionExpression": Key('pk').eq(f"permission#{permission}") & Key('sk').begins_with("layer")
        }
        return self.query(query_parameters)

    def get_permission_for_layer_id(self, layer_id):
        query_parameters = {
            "IndexName": "gsi1",
            "KeyConditionExpression": Key('sk').eq(f"layer#{layer_id}") & Key('pk').begins_with("permission")
        }
        return self.query(query_parameters)

    def add_layer(self, layer: LayerModel):
        self.table.put_item(
            Item=layer.model_dump(by_alias=True, exclude_none=True)
        )

    def get_layer(self, pk, sk) -> Union[LayerModel, None]:
        if item := self.get_item(pk, sk):
            return LayerModel.model_validate(item)

        return None

    def get_layers(self, layer_ids: set):
        response = self.resource.batch_get_item(
            RequestItems={
                self.table_name: {
                    "Keys": [{"pk": "layer", "sk": f"layer#{layer_id}"} for layer_id in layer_ids]
                }
            }
        )

        return response["Responses"][self.table_name]

    def delete_layer(self, layer_id: str):
        query_parameters = {
            "IndexName": "gsi1",
            "KeyConditionExpression": Key('sk').eq(f"layer#{layer_id}")
        }
        items = self.query(query_parameters)

        with self.table.batch_writer() as writer:
            for item in items:
                writer.delete_item(
                    Key={"sk": item["sk"], "pk": item["pk"]}
                )

    def delete_permission(self, permission: str):
        query_parameters = {
            "KeyConditionExpression": Key('pk').eq(f"permission#{permission}")
        }
        items = self.query(query_parameters)

        with self.table.batch_writer() as writer:
            for item in items:
                writer.delete_item(
                    Key={"pk": item["pk"], "sk": item["sk"]}
                )

    def delete_layer_from_layer_permission(self, permissions: List[PermissionModel]):
        with self.table.batch_writer() as writer:
            for permission in permissions:
                writer.delete_item(
                    Key={"pk": f"permission#{permission.permission}", "sk": f"layer#{permission.layer_id}"}
                )

    def get_layer_step(self, step: str, layer_id: str) -> Union[LayerStepModel, None]:
        response = self.table.get_item(Key={"pk": f"step#{step}", "sk": f"layer#{layer_id}"})
        if item := response.get("Item"):
            return LayerStepModel.model_validate(item)

        return None

    def delete_layer_step(self, step: str, layer_id: str):
        self.table.delete_item(
            Key={"pk": f"step#{step}", "sk": f"layer#{layer_id}"}
        )

    def get_layer_steps(self, layer_id: str) -> List[LayerStepModel]:
        query_params = {
            "IndexName": "gsi1",
            "KeyConditionExpression": Key("sk").eq(f"layer#{layer_id}") & Key("pk").begins_with("step")
        }
        items = self.query(query_params)
        adapter = TypeAdapter(List[LayerStepModel])
        return adapter.validate_python(items)

    def add_layer_step(self, layer_step: LayerStepModel):
        self.table.put_item(Item=layer_step.model_dump(by_alias=True))

    def add_color_map(self, color_map: ColorMap):
        self.table.put_item(
            Item=color_map.model_dump(by_alias=True)
        )

    def get_color_map(self, name: str) -> ColorMap:
        if item := self.get_item(pk="cm", sk=f"cm#{name}"):
            return ColorMap.model_validate(item)

    def get_color_maps(self):
        query_parameters = {
            "KeyConditionExpression": Key("pk").eq("cm"),
            "ProjectionExpression": "#name, description",
            "ExpressionAttributeNames": {'#name': 'name'}
        }
        return self.query(query_parameters)

    def delete_color_map(self, name: str):
        self.table.delete_item(
            Key={"pk": "cm", "sk": f"cm#{name}"}
        )
