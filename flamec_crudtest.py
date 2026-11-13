from decimal import Decimal
from getpass import getpass
from itertools import combinations

import mysql.connector as m

from flamec_crud import FlamebackCaterData

checks_run = 0
checks_passed = 0
failed_checks = []

def check(label, actual, expected, show_result=False):
	"""Compare results and record passed or failed checks"""
	global checks_run, checks_passed
	checks_run += 1

	if isinstance(actual, list) and isinstance(expected, list):
		passed = sorted(actual) == sorted(expected)
	else:
		passed = actual == expected

	if not passed:
		failed_checks.append(label)
		print(
			f"FAIL: {label}\n"
			f"Expected: {expected}\n"
			f"Actual: {actual}"
		)
		return False

	checks_passed += 1

	if show_result:
		print(f"PASS: {label}: {actual}")
	else:
		print(f"PASS: {label}")

	return True

def test_reads(name, read, expected_count, primary_key, filters):
	"""Check default reads, projections, and filter combinations."""
	rows = read()
	check(f"{name} default row count", len(rows), expected_count)

	expected_ids = [(row[0],) for row in rows]

	for columns in (primary_key, (primary_key,), [primary_key]):
		check(f"{name} columns={columns!r}", read(columns=columns), expected_ids)

	for size in range(1, len(filters) + 1):
		for group in combinations(filters, size):
			arguments = {}
			expected = rows

			for argument, position in group:
				value = rows[0][position]
				arguments[argument] = value
				expected = [row for row in expected if row[position] == value]

			check(f"{name} filters={arguments}", read(**arguments), expected)
			check(f"{name} selected columns with filters={arguments}", read(columns=(primary_key,), **arguments), [(row[0],) for row in expected])

	primary_argument = filters[0][0]
	check(f"{name} missing primary key", read(**{primary_argument: -1}), [])

def test_changes(name, save, read, delete, id_argument, initial, updated):
	"""Verify a temp record through its lifecycle"""
	original_rows = read()
	result = save(**initial)
	record_id = result["id"]
	lookup = {id_argument: record_id}

	try:
		check(f"{name} INSERT row count", result["affected_rows"], 1)
		check(f"{name} after INSERT", read(**lookup), [(record_id,) + tuple(initial.values())], show_result=True)
		result = save(**updated, **lookup)
		check(f"{name} UPDATE result", result, {"id": record_id, "affected_rows": 1})
		check(f"{name} after UPDATE", read(**lookup), [(record_id,) + tuple(updated.values())], show_result=True)
	finally:
		deleted_rows = delete(record_id)

	check(f"{name} DELETED row count", deleted_rows, 1)
	check(f"{name} after DELETE", read(**lookup), [], show_result=True)
	check(f"{name} original data preserved", read(), original_rows)

def test_supplier_changes(db):
	"""Check supplier archiving, restoring, and deletion"""
	original_suppliers = db.get_suppliers()
	original_inventory = db.get_inventory_items()
	original_recipes = db.get_recipes()
	original_links = db.get_recipe_ingredients()
	supplier_id = ingredient_id = recipe_id = link_id = None

	try:
		# Create a temp supplier and inventory item
		result = db._save(
			"Suppliers",
			"supplier_id",
			{
				"supplier_name": "Test Supplier",
				"supplier_phone": "541-555-0100"
			}
		)
		supplier_id = result["id"]
		check(
			"Suppliers default active status",
			db.get_suppliers(
				supplier_id=supplier_id,
				columns="is_active"),
			[(True,)]
			)
		check(
			"Suppliers active DELETE blocked",
			db.delete_supplier(supplier_id),
			0
		)
		
		result = db._save(
			"InventoryItems",
			"ingredient_id",
			{
				"supplier_id": supplier_id,
				"ingredient_name": "Test Ingredient",
				"quantity_on_hand": 5,
				"price_per_unit": Decimal("1.25")
			}
		)
		ingredient_id = result["id"]
		inventory_rows = db.get_inventory_items()

		check(
			"Suppliers ARCHIVE row count",
			db.set_supplier_active(
				supplier_id,
				False
			),
			1
		)
		check(
			"Suppliers archived active selection",
			db.get_suppliers(
				supplier_id=supplier_id,
				is_active=True
			),
			[]
		)
		check(
			"Suppliers archived status selection",
			db.get_suppliers(
				supplier_id=supplier_id,
				is_active=False,
				columns="supplier_id"
			),
			[(supplier_id,)]
		)

		# Check RESTRICT before adding any recipe references
		delete_blocked = False

		try:
			db.delete_supplier(supplier_id)
		except m.IntegrityError:
			delete_blocked = True

		check(
			"Suppliers referenced DELETE blocked",
			delete_blocked,
			True
		)

		check(
			"Suppliers inventory preserved after blocked DELETE",
			db.get_inventory_items(),
			inventory_rows
		)
		check(
			"Suppliers retained after blocked DELETE",
			db.get_suppliers(
				supplier_id=supplier_id,
				columns="supplier_id"
			),
			[(supplier_id,)]
		)

		# Connect th temp ingredient to a temp recipe
		result = db._save(
			"Recipes",
			"recipe_id",
			{"recipe_name": "Test Recipe"}
		)
		recipe_id = result["id"]
		result = db.save_recipe_ingredient(recipe_id, ingredient_id, 2)
		link_id = result["id"]
		recipe_rows = db.get_recipes()
		link_rows = db.get_recipe_ingredients()

		check(
			"Suppliers RESTORE row count",
			db.set_supplier_active(supplier_id, True),
			1
		)
		check(
			"Suppliers restored active selection",
			db.get_suppliers(
				supplier_id=supplier_id,
				is_active=True,
				columns="supplier_id"
			),
			[(supplier_id,)]
		)
		check(
			"Suppliers ARCHIVE with recipe references",
			db.set_supplier_active(
				supplier_id,
				False
			),
			1
		)
		check(
			"Suppliers inventory preserved after ARCHIVE",
			db.get_inventory_items(),
			inventory_rows
		)
		check(
			"Suppliers recipes preserved after ARCHIVE",
			db.get_recipes(),
			recipe_rows
		)
		check(
			"Suppliers recipe ingredients preserved after ARCHIVE",
			db.get_recipe_ingredients(),
			link_rows
		)

		# Remove temp references before permanently deleting the supplier
		db.delete_recipe_ingredients(link_id)
		link_id = None
		db._delete("InventoryItems", "ingredient_id", ingredient_id)
		ingredient_id = None
		db._delete("Recipes", "recipe_id", recipe_id)
		recipe_id = None
		check(
			"Suppliers archived DELETE row count",
			db.delete_supplier(supplier_id),
			1
		)
		check(
			"Suppliers after DELETE",
			db.get_suppliers(supplier_id=supplier_id),
			[],
			show_result=True
		)
		supplier_id = None

	finally:
		# Clean up temp records even if a check fails
		if link_id is not None:
			db.delete_recipe_ingredients(link_id)
		if ingredient_id is not None:
			db._delete("InventoryItems", "ingredient_id", ingredient_id)
		if recipe_id is not None:
			db._delete("Recipes", "recipe_id", recipe_id)
		if supplier_id is not None:
			db.set_supplier_active(supplier_id, False)
			db.delete_supplier(supplier_id)

	check("Suppliers original data preserved", db.get_suppliers(), original_suppliers)
	check("InventoryItems original data preserved", db.get_inventory_items(), original_inventory)
	check("Recipes original data preserved", db.get_recipes(), original_recipes)
	check("RecipeIngredients original data preserved", db.get_recipe_ingredients(), original_links)

def show_database(db, title):
	"""Display each table and return its current rows"""
	tables = [
		("Suppliers", db.get_suppliers),
		("InventoryItems", db.get_inventory_items),
		("Recipes", db.get_recipes),
		("RecipeIngredients", db.get_recipe_ingredients),
		("MenuItems", db.get_menu_items),
		("Customers", db.get_customers),
		("Orders", db.get_orders),
		("OrderDetails", db.get_order_details)
	]

	contents = {}
	print(f"\n{title}")

	for name, read in tables:
		rows = sorted(read(), key=lambda row: row[0])
		contents[name] = rows
		print(f"\n{name}:")

		if rows:
			for row in rows:
				print(row)
		else:
			print("(empty)")
	
	return contents

def main():
	# Wasn't prompting for username during testing
	print("MySQL user [root]:", flush=True)
	username = input().strip() or "root"

	db = FlamebackCaterData(
		host="localhost",
		user=username,
		password=getpass("MySQL pwd: "),
		database="flamebackcater_test"
	)

	original_data = None
	errors = []

	try:
		original_data = show_database(db, "DATABASE BEFORE TESTS")

		read_cases = [
			("Suppliers", db.get_suppliers, 3, "supplier_id", [("supplier_id", 0), ("is_active", 3)]),
			("InventoryItems", db.get_inventory_items, 3, "ingredient_id", [("ingredient_id", 0), ("supplier_id", 1)]),
			("Recipes", db.get_recipes, 3, "recipe_id", [("recipe_id", 0)]),
			("RecipeIngredients", db.get_recipe_ingredients, 6, "recipe_ingredients_id", [("recipe_ingredient_id", 0), ("recipe_id", 1), ("ingredient_id", 2)]),
			("MenuItems", db.get_menu_items, 3, "menu_id", [("menu_id", 0), ("recipe_id", 1), ("availability", 3)]),
			("Customers", db.get_customers, 3, "customer_id", [("customer_id", 0)]),
			("Orders", db.get_orders, 3, "order_id", [("order_id", 0), ("customer_id", 1)]),
			("OrderDetails", db.get_order_details, 5, "order_details_id", [("order_detail_id", 0), ("order_id", 1), ("menu_id", 2)])
		]

		for case in read_cases:
			test_reads(*case)

		check(
			"MenuItems availability=False",
			db.get_menu_items(availability=False),
			[]
		)
		check(
			"Suppliers named columns",
			db.get_suppliers(
				columns=("supplier_name", "supplier_phone")
			),
			[(row[1], row[2]) for row in db.get_suppliers()]
		)

		test_changes(
			"RecipeIngredients",
			db.save_recipe_ingredient,
			db.get_recipe_ingredients,
			db.delete_recipe_ingredients,
			"recipe_ingredient_id",
			{
				"recipe_id": 2,
				"ingredient_id": 1,
				"quantity": 5
			},
			{
				"recipe_id": 2,
				"ingredient_id": 1,
				"quantity": 10
			}
		)
		test_changes(
			"OrderDetails",
			db.save_order_details,
			db.get_order_details,
			db.delete_order_detail,
			"order_detail_id", 
			{
				"order_id": 3,
				"menu_id": 2,
				"quantity": 3,
				"total_cost": Decimal("8.25")
			},
			{
				"order_id": 3,
				"menu_id": 2,
				"quantity": 2,
				"total_cost": Decimal("5.50")
			}
		)
		test_supplier_changes(db)
	except Exception as e:
		errors.append(f"Test run: {type(e).__name__}: {e}")
	finally:
		try:
			if original_data is not None:
				final_data = show_database(db, "DATABASE AFTER TESTS")

				for name in original_data:
					check(
						f"{name} restored after all tests",
						final_data[name],
						original_data[name]
					)
		except Exception as e:
			errors.append(
				f"Final database comparison: "
				f"{type(e).__name__}: {e}"
			)
		finally:
			try:
				db.close()
			except Exception as e:
				errors.append(
					f"Closing database: {type(e).__name__}: {e}"
				)

	print("\nTEST RESULTS")
	print(f"{checks_passed}/{checks_run} checks passed")
	print(f"{len(failed_checks)}/{checks_run} checks failed")

	if failed_checks:
		print("\nFailed checks:")
		for label in failed_checks:
			print(f"- {label}")
	if errors:
		print("\nErrors:")
		for e in errors:
			print(f"- {e}")
		print("\nTEST RUN INCOMPLETE - counts include only executed checks")
	elif failed_checks:
		print("\nTESTS FAILED")
	else:
		print("\nALL TESTS PASSED")

	if failed_checks or errors:
		raise SystemExit(1)

if __name__ == "__main__":
	main()
