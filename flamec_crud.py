import mysql.connector as m

class FlamebackCaterData:
	"""Provide controlled access to the Flameback Catering DB"""
	def __init__(self, host, user, password, database):
		self._connection = m.connect(
			host=host,
			user=user,
			password=password,
			database=database
		)
		try:
			self._cursor = self._connection.cursor()
		except m.Error:
			self._connection.close()
			raise

	def close(self):
		"""Release the DB cursor and connection"""
		try:
			self._cursor.close()
		finally:
			self._connection.close()

	def _fetch_all(self, sql, parameters=()):
		"""Execute a SELECT query and return its rows"""
		self._cursor.execute(sql, parameters)
		return self._cursor.fetchall()
	
	def _select(self, table, columns=None, **filters):
		"""Build a SELECT using application defined tables and filters"""
		if columns is None:
			selected_columns = "*"
		else:
			if isinstance(columns, str):
				columns = (columns,)
			if not isinstance(columns, (tuple, list)) or not columns:
				raise ValueError("Columns must be a nonempty tuple or list")
			for column in columns:
				if not isinstance(column, str) or not column.isidentifier():
					raise ValueError(f"Invalid column name: {column}")
			selected_columns = ", ".join(f"{column}" for column in columns)

		sql = f"SELECT {selected_columns} FROM {table}"
		conditions = []
		parameters = []

		for column, value in filters.items():
			if value is not None:
				conditions.append(f"{column} = %s")
				parameters.append(value)
		if conditions:
			sql += " WHERE " + " AND ".join(conditions)
		return self._fetch_all(sql + ";", tuple(parameters))

	def _call_procedure(self, procedure, parameters=()):
		"""Execute a stored procedure and return its parameters"""
		try:
			result = self._cursor.callproc(procedure, parameters)
			self._connection.commit()
			return result
		except m.Error:
			self._connection.rollback()
			raise

	def _save(self, procedure, parameters, record_id=None):
		"""Return the ID and row count from a save procedure"""
		result = self._call_procedure(procedure, parameters + (record_id, 0))
		return {
			"id": result[-2],
			"affected_rows": result[-1]
		}
	
	def _delete(self, procedure, record_id):
		"""Delete one record using an application defined primary key"""
		if record_id is None:
			raise ValueError("A record ID is required for deletion")
		result = self._call_procedure(procedure, (record_id, 0))
		return result[-1]

	def reset_database(self):
		"""Restore the database schema and sample data"""
		self._call_procedure("sp_reset_database")

# Read ops for all tables
	def get_suppliers(self, supplier_id=None, columns=None, is_active=None):
		return self._select(
			"Suppliers",
			columns,
			supplier_id=supplier_id,
			is_active=is_active
		)

	def get_inventory_items(self, ingredient_id=None, supplier_id=None, columns=None):
		return self._select(
			"InventoryItems",
			columns,
			ingredient_id=ingredient_id,
			supplier_id=supplier_id
		)

	def get_recipes(self, recipe_id=None, columns=None):
		return self._select(
			"Recipes",
			columns,
			recipe_id=recipe_id
		)

	def get_recipe_ingredients(self, recipe_ingredients_id=None, recipe_id=None, ingredient_id=None, columns=None):
		return self._select(
			"RecipeIngredients",
			columns,
			recipe_ingredients_id=recipe_ingredients_id,
			recipe_id=recipe_id,
			ingredient_id=ingredient_id
		)

	def get_menu_items(self, menu_id=None, recipe_id=None, availability=None, columns=None):
		return self._select(
			"MenuItems",
			columns,
			menu_id=menu_id,
			recipe_id=recipe_id,
			availability=availability
		)

	def get_customers(self, customer_id=None, columns=None):
		return self._select(
			"Customers",
			columns,
			customer_id=customer_id
		)

	def get_orders(self, order_id=None, customer_id=None, columns=None):
		return self._select(
			"Orders",
			columns,
			order_id=order_id,
			customer_id=customer_id
		)

	def get_order_details(self, order_details_id=None, order_id=None, menu_id=None, columns=None):
		return self._select(
			"OrderDetails",
			columns,
			order_details_id=order_details_id,
			order_id=order_id,
			menu_id=menu_id
		)

# create, update, and delete operations
	def set_supplier_active(self, supplier_id, is_active):
		"""Archive or restore a supplier in the Suppliers table"""
		if supplier_id is None:
			raise ValueError("A supplier id is required")
		if not isinstance(is_active, bool):
			raise ValueError("Active status must be True or False")

		result = self._call_procedure(
			"sp_set_supplier_active",
			(supplier_id, int(is_active), 0)
		)

		return result[-1]

	def delete_supplier(self, supplier_id):
		"""Delete an archived supplier if no inventory items reference it"""
		if supplier_id is None:
			raise ValueError("A supplier id is required for deletion")
		
		return self._delete("sp_delete_supplier", supplier_id)

	def save_recipe_ingredients(self, recipe_id, ingredient_id, quantity, recipe_ingredients_id=None):
		"""Insert or update one recipe-ingredient relationship"""
		return self._save(
			"sp_save_recipe_ingredients",
			(recipe_id, ingredient_id, quantity),
			record_id=recipe_ingredients_id
		)

	def save_order_details(self, order_id, menu_id, quantity, total_cost, order_details_id=None):
		"""Insert or update one order line"""
		return self._save(
			"sp_save_order_details",
			(order_id, menu_id, quantity, total_cost),
			record_id=order_details_id
		)

	def delete_recipe_ingredients(self, recipe_ingredients_id):
		"""Delete one recipe-ingredient relationship"""
		return self._delete(
			"sp_delete_recipe_ingredients",
			recipe_ingredients_id
		)

	def delete_order_details(self, order_details_id):
		"""Delete one order line"""
		return self._delete(
			"sp_delete_order_details",
			order_details_id
		)
