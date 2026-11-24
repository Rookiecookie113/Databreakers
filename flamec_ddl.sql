-- Flameback Catering - Inventory Management System
-- CS 340 Project Step 4, Group 12
-- Hurrsh Misttry, Tetsuya Bassler, Allen Dickey

DROP PROCEDURE IF EXISTS sp_reset_database;

DELIMITER $$

CREATE PROCEDURE sp_reset_database()
BEGIN
	DROP TABLE IF EXISTS OrderDetails;
	DROP TABLE IF EXISTS Orders;
	DROP TABLE IF EXISTS Customers;
	DROP TABLE IF EXISTS MenuItems;
	DROP TABLE IF EXISTS RecipeIngredients;
	DROP TABLE IF EXISTS Recipes;
	DROP TABLE IF EXISTS InventoryItems;
	DROP TABLE IF EXISTS Suppliers;

-- =========================================================
-- TABLE DEFINITIONS
-- =========================================================

-- Suppliers: vendors that provide ingredients

CREATE TABLE Suppliers (
	supplier_id INT(11) NOT NULL AUTO_INCREMENT,
	supplier_name VARCHAR(50) NOT NULL,
	supplier_phone VARCHAR(20) NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (supplier_id)
);

-- InventoryItems: ingredients and their current stock levels.
-- Each inventory item belongs to exactly one supplier.

CREATE TABLE InventoryItems (
	ingredient_id INT(11) NOT NULL AUTO_INCREMENT,
	supplier_id INT(11) NOT NULL,
	ingredient_name VARCHAR(50) NOT NULL,
	quantity_on_hand INT(11) NOT NULL,
	price_per_unit DECIMAL(10,2) NOT NULL,
	PRIMARY KEY (ingredient_id),

	CONSTRAINT fk_inventory_supplier
		FOREIGN KEY (supplier_id)
		REFERENCES Suppliers (supplier_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	CONSTRAINT chk_inventory_quantity
		CHECK (quantity_on_hand >= 0),
	
	CONSTRAINT chk_inventory_price
		CHECK (price_per_unit >= 0)
);

-- Recipes: recipes used to prepare menu items.

CREATE TABLE Recipes (
	recipe_id INT(11) NOT NULL AUTO_INCREMENT,
	recipe_name VARCHAR(50) NOT NULL,
	PRIMARY KEY (recipe_id)
);

-- RecipeIngredients: connects recipes to inventory items
-- and records the quantity of each ingredient required.
CREATE TABLE RecipeIngredients (
	recipe_ingredients_id INT(11) NOT NULL AUTO_INCREMENT,
	recipe_id INT(11) NOT NULL,
	ingredient_id INT(11) NOT NULL,
	quantity_needed INT(11) NOT NULL,
	PRIMARY KEY (recipe_ingredients_id),

	CONSTRAINT uq_recipeingredients_recipe_ingredient
		UNIQUE (recipe_id, ingredient_id),

	CONSTRAINT fk_recipeingredients_recipe
		FOREIGN KEY (recipe_id)
		REFERENCES Recipes (recipe_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fk_recipeingredients_ingredient
		FOREIGN KEY (ingredient_id)
		REFERENCES InventoryItems (ingredient_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	CONSTRAINT chk_recipeingredients_quantity
		CHECK (quantity_needed > 0)
);

-- MenuItems: items offered for sale, their current prices,
-- and whether they are currently available.

CREATE TABLE MenuItems (
	menu_id INT(11) NOT NULL AUTO_INCREMENT,
	recipe_id INT(11) NOT NULL,
	price DECIMAL(10,2) NOT NULL,
	availability BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (menu_id),

	CONSTRAINT fk_menu_recipe
		FOREIGN KEY (recipe_id)
		REFERENCES Recipes (recipe_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	CONSTRAINT chk_menu_price
		CHECK (price >= 0)
);

-- Customers: customers who can place catering orders.

CREATE TABLE Customers (
	customer_id INT(11) NOT NULL AUTO_INCREMENT,
	customer_name VARCHAR(50) NOT NULL,
	PRIMARY KEY (customer_id)
);

-- Orders: records each order's customer and date.

CREATE TABLE Orders (
	order_id INT(11) NOT NULL AUTO_INCREMENT,
	customer_id INT(11) NOT NULL,
	order_date DATE NOT NULL,
	PRIMARY KEY (order_id),

	CONSTRAINT fk_orders_customer
		FOREIGN KEY (customer_id)
		REFERENCES Customers (customer_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);

-- OrderDetails: connects orders to the menu items purchased.
-- total_cost stores the line total at the time of purchase,
-- preserving it if the current menu price changes later.

CREATE TABLE OrderDetails (
	order_details_id INT(11) NOT NULL AUTO_INCREMENT,
	order_id INT(11) NOT NULL,
	menu_id INT(11) NOT NULL,
	quantity_ordered INT NOT NULL,
	total_cost DECIMAL(10,2) NOT NULL,
	PRIMARY KEY (order_details_id),

	CONSTRAINT fk_orderdetails_order
		FOREIGN KEY (order_id)
		REFERENCES Orders (order_id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fk_orderdetails_menu
		FOREIGN KEY (menu_id)
		REFERENCES MenuItems (menu_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	CONSTRAINT chk_orderdetails_quantity
		CHECK (quantity_ordered > 0),

	CONSTRAINT chk_orderdetails_cost
		CHECK (total_cost >= 0)
);

-- =========================================================
-- SAMPLE DATA
-- =========================================================
START TRANSACTION;

-- Suppliers
-- Supplier 2 supplies multiple ingredients.
-- Supplier 3 has no inventory items assigned yet.
INSERT INTO Suppliers (supplier_id, supplier_name, supplier_phone, is_active)
VALUES
	(1, 'Valley Poultry', '541-737-1000', TRUE),
	(2, 'Benton Produce', '541-737-8787', TRUE),
	(3, 'Cascade Foods', '541-737-4331', FALSE);

-- InventoryItems
INSERT INTO InventoryItems (ingredient_id, supplier_id, ingredient_name, quantity_on_hand, price_per_unit)
VALUES
	(1, (SELECT supplier_id FROM Suppliers WHERE supplier_name = 'Valley Poultry'), 'Chicken Fillet', 12, 5.50),
	(2, (SELECT supplier_id FROM Suppliers WHERE supplier_name = 'Benton Produce'), 'Potatoes', 25, 1.25),
	(3, (SELECT supplier_id FROM Suppliers WHERE supplier_name = 'Benton Produce'), 'Onions', 45, 0.75);

-- Recipes
INSERT INTO Recipes (recipe_id, recipe_name)
VALUES
	(1, 'Ultimate Stuffed Baked Potato'),
	(2, 'French Fry'),
	(3, 'Chicken Curry');

-- RecipeIngredients
-- Each recipe can use multiple ingredients.
-- Ingredients can be shared by multiple recipes.
INSERT INTO RecipeIngredients (recipe_ingredients_id, recipe_id, ingredient_id, quantity_needed)
VALUES
	(1, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'Ultimate Stuffed Baked Potato'),
		(SELECT ingredient_id FROM InventoryItems WHERE ingredient_name = 'Chicken Fillet'), 2),
	(2, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'French Fry'),
		(SELECT ingredient_id FROM InventoryItems WHERE ingredient_name = 'Potatoes'), 1),
	(3, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'Chicken Curry'),
		(SELECT ingredient_id FROM InventoryItems WHERE ingredient_name = 'Onions'), 4),
	(4, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'Ultimate Stuffed Baked Potato'),
		(SELECT ingredient_id FROM InventoryItems WHERE ingredient_name = 'Potatoes'), 1),
	(5, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'Ultimate Stuffed Baked Potato'),
		(SELECT ingredient_id FROM InventoryItems WHERE ingredient_name = 'Onions'), 1);

-- MenuItems
INSERT INTO MenuItems (menu_id, recipe_id, price, availability)
VALUES
	(1, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'Ultimate Stuffed Baked Potato'), 4.50, TRUE),
	(2, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'French Fry'), 2.75, TRUE),
	(3, (SELECT recipe_id FROM Recipes WHERE recipe_name = 'Chicken Curry'), 6.99, TRUE);

-- Customers
-- Joann Takarini has not placed any orders yet.
INSERT INTO Customers (customer_id, customer_name)
VALUES
	(1, 'Alfonso Guachelle'),
	(2, 'Hardy McSnikerson'),
	(3, 'Joann Takarini');

-- Orders
-- Alfonso Guachelle has placed two orders.
INSERT INTO Orders (order_id, customer_id, order_date)
VALUES
	(1, (SELECT customer_id FROM Customers WHERE customer_name = 'Alfonso Guachelle'), '2025-10-23'),
	(2, (SELECT customer_id FROM Customers WHERE customer_name = 'Hardy McSnikerson'), '2025-11-02'),
	(3, (SELECT customer_id FROM Customers WHERE customer_name = 'Alfonso Guachelle'), '2025-12-05');

-- OrderDetails
-- Orders 1 and 3 contain multiple menu items.
-- Menu items 1 and 2 each appear in multiple orders.
-- total_cost records each line's price at purchase time.
INSERT INTO OrderDetails (order_details_id, order_id, menu_id, quantity_ordered, total_cost)
VALUES
	(1, (SELECT o.order_id FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id
			WHERE c.customer_name = 'Alfonso Guachelle' AND o.order_date = '2025-10-23'),
		(SELECT m.menu_id FROM MenuItems m JOIN Recipes r ON m.recipe_id = r.recipe_id
			WHERE r.recipe_name = 'Ultimate Stuffed Baked Potato'), 2, 9.00),
	(2, (SELECT o.order_id FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id
			WHERE c.customer_name = 'Hardy McSnikerson' AND o.order_date = '2025-11-02'),
		(SELECT m.menu_id FROM MenuItems m JOIN Recipes r ON m.recipe_id = r.recipe_id
			WHERE r.recipe_name = 'French Fry'), 1, 2.75),
	(3, (SELECT o.order_id FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id
			WHERE c.customer_name = 'Alfonso Guachelle' AND o.order_date = '2025-12-05'),
		(SELECT m.menu_id FROM MenuItems m JOIN Recipes r ON m.recipe_id = r.recipe_id
			WHERE r.recipe_name = 'Chicken Curry'), 3, 20.97),
	(4, (SELECT o.order_id FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id
			WHERE c.customer_name = 'Alfonso Guachelle' AND o.order_date = '2025-10-23'),
		(SELECT m.menu_id FROM MenuItems m JOIN Recipes r ON m.recipe_id = r.recipe_id
			WHERE r.recipe_name = 'French Fry'), 2, 5.50),
	(5, (SELECT o.order_id FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id
			WHERE c.customer_name = 'Alfonso Guachelle' AND o.order_date = '2025-12-05'),
		(SELECT m.menu_id FROM MenuItems m JOIN Recipes r ON m.recipe_id = r.recipe_id
			WHERE r.recipe_name = 'Ultimate Stuffed Baked Potato'), 1, 4.50);

-- closing
COMMIT;

END $$

DELIMITER ;

CALL sp_reset_database();
