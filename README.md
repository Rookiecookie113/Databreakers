# Flameback Catering System (Project Group 12)

**Authors:** Hurrsh Misttry, Tetsuya Bassler, Allen Dickey
CS 340, Project Step 4 (Draft)

## Description

The Flameback Catering System is a Python application that allows users to work with the company database without having to write or interact with SQL directly. All database access is handled through `flamec_crud.py`, which uses SELECT queries and stored procedures to access and manage the data.

The purpose of this project is to replace the company's current process of keeping track of information using paper records and spreadsheets. By moving everything into a database with an application to manage it, the goal is to make organizing and accessing company information easier and more efficient.

The database keeps track of suppliers, inventory items, recipes, recipe ingredients, menu items, customers, orders, and order details.

## Project Files

| File                   | Description                                                                                                                                                            |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `flamec_ddl.sql`     | Defines the RESET procedure, creates the database tables, and adds the sample data.                                                                                                                  |
| `flamec_plsql.sql`  | Defines the stored procedures for create, update, and delete operations. |
| `flamec_crud.py`     | Contains the `FlamebackCaterData` class and handles database reads, relationship changes, and supplier archiving and deletion.                                       |
| `flamec_crudtest.py` | Tests the data layer, displays the database before and after testing, and reports passed and failed checks.                                                            |
| `flamec_dml.sql`     | Contains reference queries used by the application and stored procedures. It uses `:variable` placeholders and it is not meant to be run directly. |
| `CLI_OUT.txt`        | Contains the saved output from a test run.                                                                                                                             |

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
   SOURCE flamec_plsql.sql;
   ```
3. **Run the test script.**

   Open a terminal in the project folder and run:

   ```bash
   python flamec_crudtest.py
   ```

   Enter your MySQL username and password when prompted. Pressing Enter without a username defaults to `root`.

**Important:** Run the test script only against the test database. It calls the RESET procedure to drop and recreate the project tables and load the sample data. You do not need to reload the DDL file between test runs.

## Expected Output

The script displays the contents of all eight tables under `DATABASE BEFORE TESTS`, followed by PASS or FAIL messages for each check. These checks cover reads, selected columns, filters, insert/update/delete ops, and supplier archiving, restoration, and deletion.

The RESET test inserts a temporary record and deletes a sample record before calling RESET. It checks that the temporary record is gone and all eight tables match the starting data. After testing, the script displays the tables again under `DATABASE AFTER TESTS` and compares their contents with the starting data.

A successful run ends with:
```text
PASS: Suppliers restored after all tests
PASS: InventoryItems restored after all tests
PASS: Recipes restored after all tests
PASS: RecipeIngredients restored after all tests
PASS: MenuItems restored after all tests
PASS: Customers restored after all tests
PASS: Orders restored after all tests
PASS: OrderDetails restored after all tests

TEST RESULTS
161/161 checks passed
0/161 checks failed

ALL TESTS PASSED
```

The complete saved output is available in `CLI_OUT.txt`. The saved run was tested against a separate local MySQL 8.0 test instance.

If a check fails, the script will display its expected and actual results. The final summary lists the failed checks and shows how many checks passed or failed. Unexpected errors are reported separately and mark the run as incomplete. For an incomplete run, the counts include only checks that were executed.

## Supplier Status and Delete Rules

Suppliers use an `is_active` field so they can be archived without deleting their inventory items. Archived suppliers remain visible in general supplier reads and can be restored later.

The data layer uses `set_supplier_active(supplier_id, False)` to archive a supplier and `set_supplier_active(supplier_id, True)` to restore one. Active suppliers can be selected with `get_suppliers(is_active=True)`.

Permanent supplier deletion requires the supplier to be archived. The database also blocks deletion while inventory items reference that supplier.

Other foreign keys prevent deleting ingredients used by recipes, recipes used by menu items, customers with orders, and menu items referenced by order details. Deleting an otherwise unreferenced recipe removes its recipe-ingredient links. Deleting an order removes its order details.

## Planned Step 5 Enhancement

We plan to add JOIN queries to make the application output easier to read without looking up foreign key IDs separately.

Essential tasks:

- Add a recipe ingredient report with recipe names, ingredient names, and quantities.
- Add an order detail report with customer names, order dates, recipe names, quantities, and costs.
- Add tests for both reports and update the DML reference file.

Optional tasks:

- Add a low-stock inventory report.
- Add total sales grouped by customer.

## Citation

GeeksforGeeks. (2021, April 10). Composite Key in SQL. https://www.geeksforgeeks.org/sql/composite-key-in-sql/ Accessed 7 Oct 2026.

Anthropic. (2026). Claude (Opus 5.5) [Large language model]. https://claude.ai/ Accessed 23 Nov 2026. How we used Claude: We used Claude to help us understand the assignment requirements, to produce an initial README draft that we reviewed and rewrote (Nov 4, 2026), and to review our project files against TA feedback and point out errors and inconsistencies (Nov 23, 2026).

**Prompt:** "I need help with a readme for our repo," along with our project files and draft README.
