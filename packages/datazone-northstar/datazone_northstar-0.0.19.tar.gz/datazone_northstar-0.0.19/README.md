Datazone Northstar Client Library 👋

## Installation
You can install package via pip
````shell
pip install datazone-northstar
````

## Configuration & Login
Run the following command in your terminal
````shell
datazone auth configure
````
When prompted, enter the following information:
````shell
Host [app.datazone.co]: <DATAZONE_ADDRESS>
Username: <USERNAME>
Password: <PASSWORD>
Repeat for confirmation: <PASSWORD_CONFIRM>
````
Then you can run following command to login
````shell
datazone auth login
````
It will keep your tokens until refresh token expired. (Default 30min). Then you can re-run and login again.

## Create first repository
````shell
datazone repository create hello-world
cd hello-world
````

It creates a new folder in your current directory. Thıs folder has two file initially. `config.yaml` and `first_pipeline.py`.
After you modify your script you can deploy project via following command. (It takes about one minute).

```shell
datazone repository deploy
```

After the deployment is complete, you can check your repository status via following command.

```shell
datazone repository summary
```

If repository has deployed, you can run your first execution with following command.
````shell
datazone execution run <pipeline_id>
````

## Commands
Also you can check all command with help sub command. `datazone auth --help` or `datazone repository summary --help`
```shell
# Auth
datazone auth configure
datazone auth login

# Repository
datazone repository list
datazone repository create
datazone repository deploy
datazone repository summary <file_name>
datazone repository clone <repository_id>
datazone repository pull

# Dataset
datazone dataset list
datazone dataset show <dataset_id> [<branch_name>] [<size>] [<transaction_id>]
datazone dataset transactions <dataset_id>

# View
datazone dataset view create
datazone dataset view list <dataset_id>
datazone dataset view delete <view_id>

# Source
datazone source create
datazone source list
datazone source update <source_id>
datazone source delete <source_id>

# Extract
datazone extract create
datazone extract list
datazone extract update <extract_id>
datazone extract delete <extract_id>
datazone extract execute <extract_id>

# Schedule
datazone schedule create
datazone schedule list
datazone schedule delete <source_id>

# Execution
datazone execution run [--extract-id] [--pipeline-id] [<execution_type>] [<transform_selection>]
datazone execution list [--extract-id] [--pipeline-id]
datazone execution log <execution_id>

# Pipeline
datazone pipeline create

# Common
datazone version
datazone info
```
