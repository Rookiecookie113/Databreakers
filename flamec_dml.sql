-- :name placeholders represent values supplied by the application

--Query retrieves all data from the Suppliers table
SELECT * FROM Suppliers;

--Query that retrieves all data from the InventoryItems table
SELECT * FROM InventoryItems;

--Gets all data from the RecipeIngredients intersection table
SELECT * FROM RecipeIngredients;

--Gets all data from the Recipes table
SELECT * FROM Recipes;

--Gets all data from the MenuItems table
SELECT * FROM MenuItems;

--Gets all data from the OrderDetails intersection table
SELECT * FROM OrderDetails;

--Gets all data from the Orders table
SELECT * FROM Orders;

--Gets all data from the Customers table
SELECT * FROM Customers;

-- Filter rows by pk
SELECT * FROM Suppliers
WHERE supplier_id = :supplier_id;

-- Select specific columns
SELECT supplier_name, supplier_phone
FROM Suppliers;

-- Select specific columns and filter rows
SELECT ingredient_name, quantity_on_hand
FROM InventoryItems
WHERE supplier_id = :supplier_id;

-- Combine multiple filters
SELECT * FROM RecipeIngredients
WHERE recipe_id = :recipe_id
AND ingredient_id = :ingredient_id;

-- Filer availablity, including False
SELECT * FROM MenuItems
WHERE availability = :availability;

-- Insert a new ingredient for a recipe into the RecipeIngredients intersection table
INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity_needed)
VALUES (:recipe_id, :ingredient_id, :quantity_needed);

-- Update an ingredient for a recipe into the RecipeIngredients intersection table
UPDATE RecipeIngredients
SET recipe_id = :recipe_id,
	ingredient_id = :ingredient_id,
	quantity_needed = :quantity_needed
WHERE recipe_ingredients_id = :recipe_ingredients_id;

-- DELETE an ingredient from a recipe in the RecipeIngredients intersection table
DELETE FROM RecipeIngredients
WHERE recipe_ingredients_id = :recipe_ingredients_id;

-- Insert a new order detail into the OrderDetails intersection table
INSERT INTO OrderDetails (order_id, menu_id, quantity_ordered, total_cost)
VALUES (:order_id, :menu_id, :quantity_ordered, :total_cost);

-- Update an order detail into the OrderDetails intersection table
UPDATE OrderDetails
SET order_id = :order_id,
	menu_id = :menu_id,
	quantity_ordered = :quantity_ordered,
	total_cost = :total_cost
WHERE order_details_id = :order_details_id;

-- Delete an order detail from the OrderDetails intersection table
DELETE FROM OrderDetails
WHERE order_details_id = :order_details_id;