# Minimalist recipe manager using Django

## Installation
Create a Python3 virtual environment, and activate it:
```sh
python3 -m venv <env_name>
source <env_name>/bin/activate
```

Then, install dependencies:
```sh
pip3 install -r requirements.txt
```

Setup a sqlite database:
```sh
$ cd src
$ python3 manage.py makemigrations recipemanager
$ python3 manage.py migrate
```

### Running the server
After completing the installation, just run the application:
```sh
$ python3 manage.py runserver
```

### Usage
Access the recipe manager at `http://127.0.0.1:8000/manager/`
