# Voltron

## Introduction

This repository is an answer to the HealthTech Voltron Epitech Project.

The team is composed by 11 members divided by specialities like this:

- Artificial Intelligence: Bastien, Alex, Alex
- Big Data: Cattelain, Lohan
- Cloud: Louis, Théo
- IOT: Mathias, Vincent
- MSI: Guillaume
- Virtual Reality: Nicolas, Benjamin
- Security: Thomas

## Global Architecure


```text
.
├── README.md
├── doc                             -> Folder containing Project Documentation
│   └── big-data                    -> Folder containing Big Data Documentation
│       ├── architecture            -> Folder containing Big Data Architecture Documentation
│       │   └── architecture.drawio -> Graphic presenting Big Data AWS Architecture
│       └── budget                  -> Folder containing Big Data Budget Documentation
│           ├── bigdata.pdf         -> File presenting Big Data Budget calculation 
│           └── budgetisation.pdf   -> File presenting Big Data AWS calculator budget
└── src                             -> Folder containing Project source code
    └── big-data                    -> Folder containing Big Data source code
        └── poc                     -> Folder containing Big Data POC resources code
            ├── dynamodb.py         -> File presenting DynamoDB tools
            ├── kinesis.py          -> File presenting Kinesis tools
            ├── requirements.txt    -> File containing Python packages needed for the POC
            ├── s3.py               -> File presenting S3 tools
            └── sqs.py              -> File presenting SQS tools
```

## Documentation

### Big Data

This documentation presents all the documentation about the project's Big Data part 

#### Introduction

We choose to go for a AWS Cloud DataBase architecture. To explain this choice, we can talk about:
- maintainability 
- scalability 
- access to the data
- access on pre-made data dashboards
- support
- documentation

#### Used Services

This project is based on well-known AWS services:

- SQS (Simple Queue Service)
