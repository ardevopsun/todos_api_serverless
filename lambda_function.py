import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TODOS_TABLE'])

def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']
    
    if method == 'GET' and path == '/todos':
        return get_all_todos()
    
    elif method == 'POST' and path == '/todos':
        return create_todo(json.loads(event.get('body', '{}')))
    
    elif method == 'PUT' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return update_todo(todo_id, json.loads(event.get('body', '{}')))
    
    elif method == 'DELETE' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return delete_todo(todo_id)
    
    elif method == 'GET' and path.startswith('/todos/'):
        todo_id = path.split('/')[-1]
        return get_todo_by_id(todo_id)
    
    else:
        return response(400, {"message": "Unsupported method or path"})

def get_all_todos():
    try:
        result = table.scan()
        return response(200, result.get('Items', []))
    except Exception as e:
        return response(500, {"message": "Server error", "error": str(e)})

def get_todo_by_id(todo_id):
    try:
        result = table.get_item(Key={'id': todo_id})
        if 'Item' in result:
            return response(200, result['Item'])
        else:
            return response(404, {'message': 'Todo not found'})
    except Exception as e:
        return response(500, {"message": "Server error", "error": str(e)})

def create_todo(body):
    try:
        todo_id = str(uuid.uuid4())
        item = {
            'id': todo_id,
            'task': body.get('task', ''),
            'status': body.get('status', 'pending')
        }
        table.put_item(Item=item)
        return response(201, item)
    except Exception as e:
        return response(500, {"message": "Server error", "error": str(e)})

def update_todo(todo_id, body):
    try:
        task = body.get('task', '')
        status = body.get('status', 'pending')
        result = table.update_item(
            Key={'id': todo_id},
            UpdateExpression="SET task = :taskVal, #st = :statusVal",
            ExpressionAttributeValues={
                ':taskVal': task,
                ':statusVal': status
            },
            ExpressionAttributeNames={
                '#st': 'status'
            },
            ReturnValues="UPDATED_NEW"
        )
        return response(200, result.get('Attributes', {}))
    except Exception as e:
        return response(500, {"message": "Server error", "error": str(e)})

def delete_todo(todo_id):
    try:
        table.delete_item(Key={'id': todo_id})
        return response(204, {})
    except Exception as e:
        return response(500, {"message": "Server error", "error": str(e)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
