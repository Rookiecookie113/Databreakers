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
| `flamec_ddl.sql` | Creates the database tables and adds the sample data. |
| `flamec_crud.py` | Contains the `FlamebackCaterData` class and handles all SQL queries. |
| `flamec_crudtest.py` | Runs tests for each data layer method and displays the results. |
| `flamec_dml.sql` | Contains a reference list of the SQL queries used in the data layer. It uses `:variable` placeholders, so it is not meant to be run directly. |
| `CLI_OUT.txt` | Contains the saved output from a test run. |
| `CLI_OUT_VERBOSE.txt` | Contains the saved verbose output from a test run. |

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
   CREATE DATABASE IF NOT EXISTS flamebackcater_test;
   USE flamebackcater_test;
   ```

2. **Create the tables and load the sample data.**

   From the MySQL prompt, run the following command from the project folder:

   ```sql
   SOURCE flamec_ddl.sql;
   ```

3. **Run the test script.**

   Open a terminal in the project folder and run:

   ```bash
   python flamec_crudtest.py
   ```
   or
   ```bash
   python flamec_crudtest.py -v
   ```

   The script will ask for your MySQL username (press Enter to use `root`) and your MySQL password. The password is hidden as you type. Adding `-v` runs it in verbose mode, which prints the actual result next to every PASS line.

**Note:** The test script inserts, updates, and deletes a temporary row in each intersection table, then deletes it and checks that the original data is unchanged. You do not need to reload the DDL between runs. The READ tests expect the exact sample data from `flamec_ddl.sql`, so if you have changed the data yourself, reload the DDL from step 2 before running the tests.

## Expected Output

The examples below are short excerpts from a test run. The full output from a run right after loading the DDL is saved in `CLI_OUT.txt`, and the verbose output is saved in `CLI_OUT_VERBOSE.txt`.

The first line starts with the username prompt, `MySQL user [root]:`. The password prompt does not appear in the saved output.

If a check fails, the script stops right away and shows a `FAIL` message with the expected and actual values.

### READ tests

The script tests the READ methods for all eight tables in this order: Suppliers, InventoryItems, Recipes, RecipeIngredients, MenuItems, Customers, Orders, and OrderDetails. For each table, it checks the default row count and prints the table's rows, then tests selecting specific columns, each supported filter and combination of filters, and a primary key that does not exist. Here is the Suppliers section:

```text
MySQL user [root]: PASS: Suppliers default row count
[(1, 'Valley Poultry', '541-737-1000'), (2, 'Benton Produce', '541-737-8787'), (3, 'Cascade Foods', '541-737-4331')]
PASS: Suppliers columns='supplier_id'
PASS: Suppliers columns=('supplier_id',)
PASS: Suppliers columns=['supplier_id']
PASS: Suppliers filters={'supplier_id': 1}
PASS: Suppliers selected columns with filters={'supplier_id': 1}
PASS: Suppliers missing primary key
```

Tables with more than one filter show every combination. For example, Orders:

```text
PASS: Orders filters={'order_id': 1}
PASS: Orders selected columns with filters={'order_id': 1}
PASS: Orders filters={'customer_id': 1}
PASS: Orders selected columns with filters={'customer_id': 1}
PASS: Orders filters={'order_id': 1, 'customer_id': 1}
PASS: Orders selected columns with filters={'order_id': 1, 'customer_id': 1}
PASS: Orders missing primary key
```

After the eight tables, two more READ checks run: one makes sure filtering by `availability=False` works (it returns no rows, since every menu item is available), and one selects Suppliers by column names other than the ID.

```text
PASS: MenuItems availability=False
PASS: Suppliers named columns
```

### CREATE, UPDATE, and DELETE tests

After the READ tests, the script tests inserting, updating, and deleting a temporary row in each intersection table (RecipeIngredients and OrderDetails). After each change, it reads the row back to confirm the change worked. At the end, it checks that the original sample data is still unchanged.

```text
PASS: RecipeIngredients INSERT row count
PASS: RecipeIngredients after INSERT: [(7, 2, 1, 5)]
PASS: RecipeIngredients UPDATE result
PASS: RecipeIngredients after UPDATE: [(7, 2, 1, 10)]
PASS: RecipeIngredients DELETED row count
PASS: RecipeIngredients after DELETE: []
PASS: RecipeIngredients original data preserved
PASS: OrderDetails INSERT row count
PASS: OrderDetails after INSERT: [(6, 3, 2, 3, Decimal('8.25'))]
PASS: OrderDetails UPDATE result
PASS: OrderDetails after UPDATE: [(6, 3, 2, 2, Decimal('5.50'))]
PASS: OrderDetails DELETED row count
PASS: OrderDetails after DELETE: []
PASS: OrderDetails original data preserved

ALL TESTS PASSED
```

The temporary rows get their IDs from AUTO_INCREMENT. Right after loading the DDL, they are 7 and 6 as shown above. Each later run without reloading the DDL adds 1 to both IDs (8 and 7, then 9 and 8, and so on). Everything else stays the same.
## Citation

This README was drafted with help from Claude (Anthropic, claude.ai) on November 4, 2026. Claude produced an initial draft based on our project files and test output, which we then reviewed and rewrote.

**Prompt:** "I need help with a readme for our repo," along with our project files and draft README.