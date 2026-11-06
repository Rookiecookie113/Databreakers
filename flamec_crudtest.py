from decimal import Decimal
from getpass import getpass
from itertools import combinations

from flamec_crud import FlamebackCaterData

def check(label, actual, expected):
	"""Compare results and stop immediately if a check fails"""
	if isinstance(actual, list) and isinstance(expected, list):
		passed = sorted(actual) == sorted(expected)
	else:
		passed = actual == expected

	if not passed:
		raise RuntimeError(
			f"FAIL: {label}\n"
			f"Expected: {expected}\n"
			f"Actual: {actual}"
		)

	print(f"PASS: {label}: {actual}")

def test_reads(name, read, expected_count, primary_key, filters):
	"""Check default reads, projections, and filter combinations."""
	rows = read()
	check(f"{name} default row count", len(rows), expected_count)
	print(rows)

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

	primary_arguement = filters[0][0]
	check(f"{name} missing primary key", read(**{primary_arguement: -1}), [])

def test_changes(name, save, read, delete, id_arguement, initial, updated):
	"""Verify a temp record through its lifecycle"""
	original_rows = read()
	result = save(**initial)
	record_id = result["id"]
	lookup = {id_arguement: record_id}

	try:
		check(f"{name} INSERT row count", result["affected_rows"], 1)
		check(f"{name} after INSERT", read(**lookup), [(record_id,) + tuple(initial.values())])
		result = save(**updated, **lookup)
		check(f"{name} UPDATE result", result, {"id": record_id, "affected_rows": 1})
		check(f"{name} after UPDATE", read(**lookup), [(record_id,) + tuple(updated.values())])
	finally:
		deleted_rows = delete(record_id)

	check(f"{name} DELETED row count", deleted_rows, 1)
	check(f"{name} after DELETE", read(**lookup), [])
	check(f"{name} original data preserved", read(), original_rows)

def main():
	db = FlamebackCaterData(
		host="localhost",
		user=input("MySQL user [root]: ").strip() or "root",
		password=getpass("MySQL pwd: "),
		database="flamebackcater_test"
	)

	try:
		read_cases = [
			("Suppliers", db.get_suppliers, 3, "supplier_id", [("supplier_id", 0)]),
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
		print("\nALL TESTS PASSED\n")
	finally:
		db.close()

if __name__ == "__main__":
	main()
