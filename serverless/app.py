import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key

#import flask and needed dependecies

from flask import Flask, jsonify, request
app = Flask(__name__)

#create db's related variables
tasks_table=os.environ['TASKS_TABLE']
client = boto3.client('dynamodb')
db = boto3.resource('dynamodb')


#First function: return list of tasks present in the DynamoDB's task_list table
@app.route("/task_list")
def get_tasks():
    #scan the whole tasks table and return items using a loop in order to overcam 1MB limit for scan
    table = db.Table(tasks_table)
    response = table.scan()
    result = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        result.extend(response['Items'])
    
    return jsonify(result)
    
#Second function: add a "task" and a "unique ID" to the DynamoDB's task_list table 
@app.route("/add_task", methods=["POST"])
def create_task():

    task = request.json.get('task')
    uid = str(uuid.uuid4())
    #Check if the task is correctly passed to the function
    if not task:
        return jsonify({'error': 'Please provide a valid task'}), 400
    
    #add taskID and task to the table
    resp = client.put_item(
        TableName=tasks_table,
        Item={
            'taskID': {'S': uid },
            'task': {'S': task }
        }
    )

    return jsonify({
        uid: task
    })

