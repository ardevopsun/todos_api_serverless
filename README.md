# Serverless Todo API (AWS Lambda + API Gateway + DynamoDB)

This is a fully serverless Todo API built using AWS Lambda, API Gateway, and DynamoDB. It provides CRUD operations for managing todo items.

## Features

- RESTful API with the following endpoints:
  - `GET /todos` – List all todos
  - `GET /todos/{id}` – Get a todo by ID
  - `POST /todos` – Create a new todo
  - `PUT /todos/{id}` – Update an existing todo
  - `DELETE /todos/{id}` – Delete a todo

- Serverless architecture using:
  - AWS Lambda (Python 3.12)
  - Amazon DynamoDB
  - API Gateway (REST API)
  - IAM Roles for secure access

---

## Technologies Used

- AWS Lambda
- Amazon DynamoDB
- AWS API Gateway
- Python (boto3)
- Postman (for testing)

---

## Setup Instructions

### 1. Create DynamoDB Table

- Table Name: `TodoTable`
- Partition Key: `id` (String)

### 2. Create Lambda Function

- Function Name: `TodoApiHandler`
- Runtime: Python 3.12
- Set the following environment variable: `TODOS_TABLE=TodoTable`

Paste the Lambda code from [lambda_function.py](lambda_function.py) into the inline editor or upload a ZIP.

### 3. Add IAM Permissions

- Attach the policy to your Lambda role.
- Now you’re on the IAM Lambda function role page.
- Click the Add permissions button.
- Choose Attach policies.
- Search for: AmazonDynamoDBFullAccess (easiest for development)
- save.

### 4. Setup API Gateway

#Create a REST API

**Add resources:**

  - /todos
  - /todos/{id}

**Add methods:**

  - GET /todos
  - POST /todos
  - GET /todos/{id}
  - PUT /todos/{id}
  - DELETE /todos/{id}

Integrate each method with the Lambda function using Lambda Proxy integration

#### Example Request Payloads

**POST /todos**

    {
      "task": "Learn AWS Lambda",
      "status": "pending"
    }

**PUT /todos/{id}**

    {
      "task": "Learn AWS Lambda deeply",
      "status": "completed"
    }

### Testing with Postman

| Method | URL    (Invoke URL)                                                | Description       |
| ------ | ------------------------------------------------------------------ | ----------------- |
| GET    | https://<api-id>.execute-api.<region>.amazonaws.com/dev/todos      | List all todos    |
| GET    | https://<api-id>.execute-api.<region>.amazonaws.com/dev/todos/{id} | Get a todo by ID  |
| POST   | https://<api-id>.execute-api.<region>.amazonaws.com/dev/todos      | Create a new todo |
| PUT    | https://<api-id>.execute-api.<region>.amazonaws.com/dev/todos/{id} | Update a todo     |
| DELETE | https://<api-id>.execute-api.<region>.amazonaws.com/dev/todos/{id} | Delete a todo     |

**Set Header:**

 - Content-Type: application/json.
 - Replace {id} with the id from the POST response.
 - Body → raw → JSON:
 
        {
        "task": "Finish Lambda-DynamoDB integration - updated",
        "status": "done"
         }

  #### Happy Devops

Arun (ardevopsun)  
Built using AWS Free Tier and tested on Postman.

