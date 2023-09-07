# I-Rent-You

I-Rent-You is a property rental platform that efficiently connects tenants and lessors.

## Project Description

This project aims to provide an online platform for users to register their properties and find available properties for rent. The project is built using the Django framework of Python and uses a multi-layered application structure for easy management and scalability.

## Features

- User registration as lessors and tenants.
- Property registration with details such as property type, rental period, location, size, rental price, etc.
- Viewing of available properties for rent by tenants.
- Rental payment management

## More info 

For additional details about the project, see our [Wiki](https://[github.com/sgalle16/TU_REPO/wiki](https://github.com/sgalle16/I-Rent-You/wiki))


## Installation and Usage

### 1. Clone this repository:
```bash
https://github.com/sgalle16/I-Rent-You.git
```
  
### 2. Create a virtual environment and install dependencies:
```bash
cd I-Rent-You
```

```bash
python -m venv venv
```
```bash
source venv/bin/activate 
```
On Unix systems, on Windows it would be "venv\Scripts\activate"  

## Required Libraries

Before running the program, make sure you have the following libraries installed:

You can install these libraries using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure the database:
```bash
python manage.py migrate
```

### 4. Start the development server:
```bash
python manage.py runserver
```

### 5. Open your web browser and visit:
  http://localhost:8000/ to access the platform.


