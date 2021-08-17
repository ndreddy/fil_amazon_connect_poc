## Description of the app files

```text
- requirements.txt: Tracks the dependencies of your application 
- config.py: This configures your application. .
- main.py: This is the entry point to your application, 
- services:  This contains services that interacts with the backend and implements business logic.
- test: Contains tests for the API, which are written with library pytest-asyncio. The file conftest.py contains global fixtures that are automatically evaluated before running any of the tests.
```

## Environment Setting

```text
 App expects the following environment variables from AWS Amazon Connect that are defined in config.py
    instance_id = 'ba24bb27-e8be-415f-9f82-8de74eb8ce78'
    queue_id = '1a7164b5-3846-4a7d-a328-71437aa75f57'
   
```

## Running the app

```
virtualenv -p python3 venv
source venv/bin/activate
```

Next, run

```
pip install -r requirements.txt
```

to get the dependencies.

Finally run the app with

```
app.main:app 
```

## Running tests

To run the test suite, simply pip install it and run from the root directory like so

```commandline
pip install pytest-asyncio
pytest
```

