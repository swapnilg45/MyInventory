# MyInventory

A web-based inventory management system built with Flask.

## Features

- Add and update products
- Track product movements between locations
- View inventory levels by location
- Generate reports of product movements

## Installation

### Local Setup

1. Clone the repository:

   git clone https://github.com/swapnilg45/MyInventory.git
   cd MyInventory

2. Create a virtual environment:
   python -m venv venv
   .\venv\Scripts\activate   # On Windows

3.Install the dependencies:
  pip install -r requirements.txt

4.Initialize the database:
  flask db init
  flask db migrate
  flask db upgrade

5.Run the application:
 flask run





