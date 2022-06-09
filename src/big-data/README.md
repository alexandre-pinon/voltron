# Big Data

This documentation presents all the documentation about the project's Big Data part

## Introduction

We choose to go for a AWS Cloud DataBase architecture. To explain this choice, we can talk about:
- maintainability
- scalability
- access to the data
- access on pre-made data dashboards
- support
- documentation

### Used Services

This project is based on well-known AWS services:

- API Gateway
- DynamoDB
- Kinesis Data Stream
- Lambda Functions
- S3 (Simple Storage Service)
- SQS (Simple Queue Service)

## Project Source Code

### Testing and POC

In a way to check all the tools that we use on the Big Data part we've mocked all the Big Data in the `poc/` directory.

So, you'll have to get all the package needed on your Python Environment. We recommend a >=3.6 Python Development Environment.

```shell
pip install -r poc/requirements.txt
```

You can now test the different components using this command:

```shell
pytest poc/*.py 
```
