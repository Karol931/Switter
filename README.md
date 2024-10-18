# Switter
The web application built with Django, resembling Twitter, leverages chat GPT API to share only positive posts. Users can engage with a stream of positive messages, promoting a more cheerful and supportive online environment.

# Set Up

## 1. Setting Up PostgreSQL Database

### Step 1: Install PostgreSQL

Ensure PostgreSQL is installed on your local machine.

- **On macOS** (using Homebrew):
  ```bash
  brew install postgresql
  ```
- **On Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ```
- **On Windows**: Download the installer from the official PostgreSQL website, and follow the installation instructions.

### Step 2: Start PostgreSQL Service

- **On macOS/Linux**:
  ```bash
  sudo service postgresql start
  ```
- **On Windows**: Open "pgAdmin" or use `pg_ctl` commands to start the PostgreSQL service.

### Step 3: Access the PostgreSQL Command Line

Once the service is running, access the PostgreSQL shell:
  ```bash
  psql postgres
  ```

### Step 4: Access the PostgreSQL Command Line

In the PostgreSQL shell, create a new database:
  ```sql
  CREATE DATABASE Switter;
  ```

### Step 5: Create a User
 
  ```sql
  CREATE USER your_username WITH PASSWORD 'your_password';
  GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
  ```

### Step 6: Connect to Your Database

You can connect to your newly created database using:
  ```bash
  psql -d your_database_name -U your_username
  ```
## 2. Getting Your OpenAI API Key

To interact with OpenAI models, you will need an API key. Follow these steps to obtain one.

### Step 1: Create an OpenAI Account

Go to the [OpenAI website](https://beta.openai.com/signup) and create an account.

### Step 2: Generate API Key

Once logged in:
  1. Navigate to the [API Keys](https://platform.openai.com/api-keys) page.
  2. Click on Create **new secret key**.
  3. Copy the API key.

## 3. Django Application Setup

### 1. Prerequisites

Before starting, ensure you have the following installed:
- **Python 3**: [Download Python](https://www.python.org/downloads/)
- **pip**: The Python package manager, typically included with Python installations.

### 2. Setup Steps

#### Step 1: Clone the Repository

First, clone the project repository to your local machine using `git`.
  ```bash
  git clone https://github.com/Karol931/Switter.git
  cd your-repository-directory
  ```

#### Step 2: Install Required Libraries

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

For security, environment-specific variables (e.g., secret keys, API keys) should be stored in a .env file.

  1. Create a `.env` file in the `/Switter/switter/switter` directoty:
  2. Add necessary variables such as `SECRET_KEY`, `DATABASE_VARIABLES`, `OPENAI_API_KEY`
     ```bash
     OPENAI_API_KEY=your_openai_api_key
     SECRET_KEY=your_django_secret_key
     NAME=your_database_name
     USER=your_database_username
     PASSWORD=database_password
     HOST=your_database_host
     PORT=your_database_port
     ```
     
#### Step 4: Set Up the Database

Apply database migrations to create the necessary tables.

```bash
python manage.py migrate
```

#### Step 5: Run the Development Server

Finally, run the Django development server:

```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/` to view the application.


