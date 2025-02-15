# Test task for Keymakr

#### To run the project, use the following commands:
Creating a docker image:
```
make build
```
Run docker image:
```
make run
```
Stopping docker image:
```
make stop
```

### Task 1: Working with APIs and Multithreading
Run script:
```
make fetch-api
```
- Sqlalchemy and Alembic are used to connect to sqlite.
- Asynchronous requests to API using the aiohttp library.
- Errors are processed when working with API.
- Logging and writing to a file are implemented.

### Task 2: File Processing and XML/JSON Conversion
Run script:
```
make convert
make convert input=<path> output=<path>
```
- The script parses an XML file, writes data in JSON format and saves it in a new directory.
- Data validation before writing to a new file is implemented.
- The command can be run without arguments, default paths:
```
input -> file_processing/input_data.xml
output -> file_processing/output_data.json
```

### Task 3: CLI Tool for Log Analysis
Run script:
```
make analyze
```
- The script analyzes the log file from the project root.
- The average weight of the response is calculated.
- The most common client and server errors are found.
- The top 5 IPs to which requests are sent are determined.
- Logs are output to the terminal and written to a .txt file.

### Task 4: Task Manager with any lite db (sqlite/…)
Run script:
```
make add-task title=<title> description=<description> due_date=<DD-MM-YYYY>
make update-task status=<status> [task_id=<id> | title=<title>]
make delete-task [task_id=<id> | title=<title>]
make list
```
- **Create a new task with the passed arguments:** title, description, completion date (all arguments are required).
- **Update the task status:** pending, in_progress, completed. An additional argument is required: task ID or title.
- **Delete a task: an additional argument is required:** task ID or title.
- **Output a list of tasks:** the list is sorted by completion date.
