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

--Insert a new ingredient for a recipe into the RecipeIngredients intersection table
INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity_needed)
VALUES (:recipe_id, :ingredient_id, :quantity_needed);

-- Update the quantity of an ingredient for a recipe in the RecipeIngredients intersection table
UPDATE RecipeIngredients SET quantity_needed = :quantity_needed WHERE recipe_ingredients_id = :recipe_ingredients_id;

-- DELETE an ingredient from a recipe in the RecipeIngredients intersection table
DELETE FROM RecipeIngredients WHERE recipe_ingredients_id = :recipe_ingredients_id;

-- Insert a new order detail into the OrderDetails intersection table
INSERT INTO OrderDetails (order_id, menu_id, quantity_ordered, total_cost)
VALUES (:order_id, :menu_id, :quantity_ordered, :total_cost);

-- Update the quantity_ordered and total cost for an order detail in the OrderDetails table
UPDATE OrderDetails SET quantity_ordered = :quantity_ordered, total_cost = :total_cost WHERE order_details_id = :order_details_id;

-- Delete an order detail from the OrderDetails intersection table
DELETE FROM OrderDetails WHERE order_details_id = :order_details_id;