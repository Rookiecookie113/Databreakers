# Flameback Catering System (Project Group 12)

**Authors:** Hurrsh Misttry, Tetsuya Bassler, Allen Dickey  
CS 340, Project Step 3 (Draft)

## Description

The Flameback Catering System is a Python application that allows users to work with the company database without having to write or interact with SQL directly. All database queries are handled in one file (`flamec_crud.py`), while the rest of the application uses its methods to access and manage the data.

The purpose of this project is to replace the company's current process of keeping track of information using paper records and spreadsheets. By moving everything into a database with an application to manage it, the goal is to make organizing and accessing company information easier and more efficient.

The database keeps track of suppliers, inventory items, recipes, recipe ingredients, menu items, customers, orders, and order details.

## Project Files

| File | Description |
|------|-------------|
| `DDL for project step 2.sql` | Creates the database tables and adds the sample data. |
| `flamec_crud.py` | Contains the `FlamebackCaterData` class and handles all SQL queries. |
| `flamec_crudtest.py` | Runs tests for each data layer method and displays the results. |
| `flamec_dml.sql` | Contains a reference list of the SQL queries used in the data layer. It uses `:variable` placeholders, so it is not meant to be run directly. |
| `CLI_OUT.txt` | Contains the saved output from a test run. |

## Installation and Dependencies

Before running the application, make sure you have the following installed:

- **Python 3**
- **MySQL or MariaDB** running locally
- **mysql-connector-python**

You can install the MySQL connector using pip:

```bash
pip install mysql-connector-python
```

## How to Run the Application

Follow these steps to set up the database and run the tests.

1. **Create the database.**

   Log into MySQL and run the following commands:

   ```sql
   CREATE DATABASE flamebackcater_db;
   USE flamebackcater_db;
   ```

2. **Create the tables and load the sample data.**

   From the MySQL prompt, run the following command from the project folder:

   ```sql
   SOURCE DDL for project step 2.sql;
   ```

3. **Update your database credentials.**

   Open `flamec_crudtest.py` and find the `mysql.connector.connect(...)` section. Update the `host`, `user`, and `password` values to match your local MySQL setup.

4. **Run the test script.**

   Open a terminal in the project folder and run:

   ```bash
   python flamec_crudtest.py
   ```

**Important:** The test script makes changes to the database by inserting, updating, and deleting records. If you want to get the same results each time you run it, reload the DDL file from step 2 before running the tests again.

## Expected Output

The first 8 lines of output show the contents of each database table. They appear in the following order: Suppliers, InventoryItems, RecipeIngredients, Recipes, MenuItems, OrderDetails, Orders, and Customers.

```text
[(1, 'Valley Poultry', '541-737-1000'), (2, 'Benton Produce', '541-737-8787'), (3, 'Cascade Foods', '541-737-4331')]
[(1, 1, 'Chicken Fillet', 12, Decimal('5.50')), (2, 2, 'Potatoes', 25, Decimal('1.25')), (3, 2, 'Onions', 45, Decimal('0.75'))]
[(1, 1, 1, 2), (2, 2, 2, 1), (3, 3, 3, 4), (4, 1, 2, 1), (5, 1, 3, 1), (6, 3, 1, 2)]
[(1, 'Ultimate Stuffed Baked Potato'), (2, 'French Fry'), (3, 'Chicken Curry')]
[(1, 1, Decimal('4.50'), 1), (2, 2, Decimal('2.75'), 1), (3, 3, Decimal('6.99'), 1)]
[(1, 1, 1, 2, Decimal('9.00')), (2, 2, 2, 1, Decimal('2.75')), (3, 3, 3, 3, Decimal('20.97')), (4, 1, 2, 2, Decimal('5.50')), (5, 3, 1, 1, Decimal('4.50'))]
[(1, 1, datetime.datetime(2025, 10, 23, 0, 0)), (2, 2, datetime.datetime(2025, 11, 2, 0, 0)), (3, 1, datetime.datetime(2025, 12, 5, 0, 0))]
[(1, 'Alfonso Guachelle'), (2, 'Hardy McSnikerson'), (3, 'Joann Takarini')]
```

The next 6 lines show the results of the insert, update, and delete tests. Each line displays the number of rows affected by the operation.

```text
None    <- add_recipe_ingredient(2, 5, 5)
1       <- update_recipe_ingredient(4, 10)
1       <- delete_recipe_ingredient(4)
1       <- add_order_detail(1, 2, 3, 4)
1       <- update_order_detail(1, 2)
1       <- delete_order_detail(1)
```

The first test returns `None` because ingredient 5 does not exist in the InventoryItems table. Since the database uses a foreign key constraint, it prevents the insert from going through.

The other tests return `1`, which means that one row was successfully affected by the operation.

## Citation

This README was drafted with help from Claude (Anthropic, claude.ai) on November 4, 2026. Claude produced an initial draft based on our project files and test output, which we then reviewed and rewrote.

**Prompt:** "I need help with a readme for our repo," along with our project files and draft README.
