## ⚙️ Installation

### Step 1: Install the virtual environment by running the following command.

```bash
python3 -m pip install --user virtualenv
```

### Step 2: Clone a GitHub Repository

```bash
git clone "https://github.com/patrykbrzozowski/image_api.git"
```

### Step 3: Change the directory to the recent clone repository in which the project is kept

```bash
cd image_api
```

### Step 4: Create a virtual environment

```bash
python -m venv env
```

### Step 5: Activate the virtual environment 

```bash
env\Scripts\activate
```

### Step 6: Install the requirements

```bash
pip install -r requirements.txt
```

### Step 7: Create migration

```bash
python manage.py makemigrations
```

### Step 8: Apply migration

```bash
python manage.py migrate
```

### Step 9: Load data from a json file into the database

```bash
python manage.py loaddata data.json
```

### Step 10: Create admin user

```bash
python manage.py createsuperuser
```

### Run

Run the Django server by running the below command

```bash
python manage.py runserver
```
