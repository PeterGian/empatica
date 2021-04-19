# Empatica Challenge n°2
This repository contains all files needed to deploy 2 lambda functions on AWS leveraging on this **IaC tools**:
- Ansible 
- Serverless.

**Used programming language**:
- Python 3

### Ansible
The `empatica_taks_manager.yml` playbook contained in /ansible/playbook can be used in order to deliver all needed files and initialize the virtual environment used in the serverless deployment phase 

### Serverless
The 3 important files are:
- `app.py` contains the definition of 2 Python's Flask functions
- `serveless.yml` contains all the steps needed in order to programmatically create the AWS services
- `requirements.txt` a list of packages needed in the virtual environment we create, that has to be deployed on AWS

## How the application works

### Function 1: [POST] add_task
#### In a nutshell
Users can call this function in order to add new tasks to the tasks table via API
#### Choices
- I decided to store all new tasks in an **AWS DynamoDB** since this kind of NoSQL DB is powerful and easy to use.
- I assigned a **unique ID** to each task, this would make it a lot easier to implement new functionalities like "modify" or "delete" (not required in this challenge)

#### Requirements
- This funcion can be called only using the **secretkey** created at deployment time by AWS function (basic authentication)
- The payload of the call should be a json in this form '{"task":"<task_value"}'

_e.g.: curl -u secretkey -H "Content-Type: application/json" -X POST https://xxxxxxx.execute-api.eu-central-1.amazonaws.com/prod/add_task -d '{"task": "buy milk"}'_

### Function 2: [GET] task_list
#### In a nutshell
Users can call this function in order to display all tasks present in the tasks table via API
#### Choices
I simply decided to scan the whole tasks table and return items using a loop in order to overcome 1MB limit for scan

#### Requirements
Nothing in particular.

_e.g.: curl -H "Content-Type: application/json" -X GET https://xxxxxxxxx.execute-api.eu-central-1.amazonaws.com/prod/task_list'_

## AWS Services involved:
- Lambda Functions:
   - empatica-task-manager-prod-tasksList
   - empatica-task-manager-prod-app
   - empatica-task-manager-prod-basicAuthenticator
   - empatica-task-manager-prod-addTasks

- Api Gateway:
  - /add_task [POST] with basic authentication
  - /task_list [GET]

- Elastic Service:
  - empatica-elasticsearch

## NOTES
The only thing that I wasn't able to create programmatically is shipping the logs from CloudWatch to the Elasticsearch cluster that I created within the serverless deployment.
I did it manually from the AWS console.
